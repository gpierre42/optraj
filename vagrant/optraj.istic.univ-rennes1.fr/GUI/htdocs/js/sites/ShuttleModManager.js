/**
 * Module de gestion des modifications de navettes d'un chantier
 */

(function() {
	// addShuttle(1, 15, 42, [4,2,5], [new Passenger(-1,0,6,4),
	// 								new Passenger(-1,0,7,4),
	// 								new Passenger(-1,0,8,2)]);
})();


/**
 * Ajoute un point de ramassage
 * @param {float} latitude  la latitude
 * @param {float} longitude la longitude
 * @param {string} address   l'adresse de la géolocalisation
 * @return {int} l'identifiant du pickup créé
 */
function addPickup (latitude, longitude, address) {
	var data = new FormData();
	data.append('data', "latitude="+latitude+"^longitude="+longitude+"^address="+address+"^idSite="+currSite.num);
	request("templates/proxy.php?url=http://localhost:5000/pickup/create/", function(xhr){
		var resp = JSON.parse(xhr.responseText);
		var num;
		if(resp["code"] != 1){
		    reportError(resp["message"]);
		}
		else{
			num = resp["data"];
			pickups[num] = {};
			pickups[num].pickup = new Pickup(num, latitude, longitude, address);
			drawPickup(num); //affiche le marker
		}
	}, data);
}

/**
 * Supprime un point de ramassage
 * @param  {int} idPickup l'identifiant du pickup
 */
function removePickup(idPickup){
	var data = new FormData();
	data.append('data', "idPickup="+idPickup);
	request("templates/proxy.php?url=http://localhost:5000/pickup/delete/", function(xhr){
		var resp = JSON.parse(xhr.responseText);
		var num;
		if(resp["code"] != 1){
			reportError(resp["message"]);
		}
		else{
			erasePickup(idPickup); //enleve le marker
			delete pickups[idPickup];
			
			// on met à jour les navettes touché par ce changement
			for (var i in shuttles){
				// On parcours les passager de la navette pour vérifier qu'il ne vont pas a larret supprimé
				for (var j in shuttles[i].shuttle.passengers){
					if (shuttles[i].shuttle.passengers[j].pickup.num == idPickup){
						shuttles[i].shuttle.passengers[j].pickup.num = null;
					}
				}
				// on supprime le pickup de la navette si il est dedans
				if (shuttles[i].shuttle.pickups[idPickup]){
					delete shuttles[i].shuttle.pickups[idPickup];
				}
				drawShuttle(i, shuttles[i].numID);
			}
		}
	}, data);
}

/**
 * Passe un ouvrier en mode "direct", il se rend au chantier par ses propres moyens
 * si c'était un passager, on édite pour le retirer de la navette
 * ensuite, quel que soit le cas, on fait un trait vers le chantier
 * @param {int} idWorker l'identifiant de l'ouvrier
 */
function setWorkerAsDirect(idWorker){
	var passenger = isPassenger(idWorker);
	if(passenger){//c'est un passager
		var data = new FormData();
		data.append('data',
					'idShuttle='+passenger.idShuttle+'^idWorker='+passenger.worker.num);
		request("templates/proxy.php?url=http://localhost:5000/shuttle/passenger/remove/", function(xhr){
			var resp = JSON.parse(xhr.responseText);
			if(resp["code"] != 1){
			    reportError(resp["message"]);
			    console.error(resp);
			}
			else{//suppression réussie
				//on édite la shuttle locale pour refléter les changements
				listPassengers = shuttles[passenger.idShuttle].shuttle.passengers;
				for(var i in listPassengers){
					if(listPassengers[i].worker.num == passenger.worker.num){
						delete shuttles[passenger.idShuttle].shuttle.passengers[i];
						break;
					}
				}
				//on retrace le lien
				drawDirectLink(idWorker);
			}
		}, data);
	}
	else{
		//on retrace le lien
		drawDirectLink(idWorker);
	}
}

/**
 * Passe un ouvrier en passager d'une navette
 * @param {int} idWorker  l'identifiant de l'ouvrier
 * @param {int} idShuttle l'identifiant de la navette
 * @param {int} idPickup  l'identifiant du point de ramassage s'il en utilise un, ou Null s'il part du départ de navette
 */
function setWorkerAsPassenger(idWorker, idShuttle, idPickup){
	if(idPickup == 0) idPickup = null;
	var passenger = isPassenger(idWorker);
	if(passenger){//c'était un passager
		if(passenger.pickup != null && passenger.pickup.num == idPickup && passenger.idShuttle==idShuttle) return; //pas de changements
		var data = new FormData();
		if(passenger.pickup != null){
			data.append('data',
					'idWorker='+idWorker +
					'^oldIdShuttle='+passenger.idShuttle+'^oldIdPickup='+passenger.pickup.num+
					'^newIdShuttle='+idShuttle+'^newIdPickup='+idPickup);
		}
		else{
			data.append('data',
					'idWorker='+idWorker +
					'^oldIdShuttle='+passenger.idShuttle+'^oldIdPickup='+null+
					'^newIdShuttle='+idShuttle+'^newIdPickup='+idPickup);
		}
		request("templates/proxy.php?url=http://localhost:5000/shuttle/passenger/update/", function(xhr){
			var resp = JSON.parse(xhr.responseText);
			if(resp["code"] != 1){
			    reportError(resp["message"]);
			    console.error(resp);
			}
			else{//edition réussie
				idPassenger = resp["data"];
				//on édite les éléments locaux pour refléter les changements
				var listPassengers = shuttles[idShuttle].shuttle.passengers;
				if(passenger.idShuttle==idShuttle){//on a modifié le pickup
					for(var i in listPassengers){
						if(listPassengers[i].worker.num == passenger.worker.num){
							if(idPickup != null)
								shuttles[idShuttle].shuttle.passengers[i].pickup = pickups[idPickup].pickup;
							else
								delete shuttles[idShuttle].shuttle.passengers[i].pickup;
							break;
						}
					}
				}
				else{//on a changé la navette
					//suppression du passager de sa navette actuelle
					delete shuttles[passenger.idShuttle].shuttle.passengers[idPassenger];
					//ajout du passager dans la navette cible
					shuttles[idShuttle].shuttle.passengers[idPassenger] = new Passenger(idPassenger, idWorker, idShuttle, idPickup);
				}
				//on retrace le lien
				drawLink(idShuttle, shuttles[idShuttle].shuttle.passengers[idPassenger]);
			}
		}, data);
	}
	else{//il était direct au site
		var data = new FormData();

		data.append('data', 'passenger='+JSON.stringify({'idWorker':idWorker,
														'idShuttle':idShuttle,
								         				'idPickup':idPickup}));
		request("templates/proxy.php?url=http://localhost:5000/shuttle/passenger/insert/", function(xhr){
			var resp = JSON.parse(xhr.responseText);
			if(resp["code"] != 1){
			    reportError(resp["message"]);
			    console.error(resp);
			}
			else{
				var idPassenger = resp["data"];
				//edition des listes
				shuttles[idShuttle].shuttle.passengers[idPassenger] = new Passenger(idPassenger, idWorker, idShuttle, idPickup);
				//on retrace le lien
				drawLink(idShuttle, shuttles[idShuttle].shuttle.passengers[idPassenger]);
			}
		}, data);
	}
}


/**
 * Ajoute une navette
 * @param {int} idDriver      l'identifiant du conducteur(un ouvrier)
 * @param {int} idCar         l'identifiant du véhicule
 * @param {[int]} pickupsIds    liste d'identifiant de pickups
 * @param {[Passengers]} passengersIds liste d'identifiants de passagers (des ouvriers)
 */
function addShuttle (idDriver, idCar, idPhase, pickupsIds, passengers) {
	var data = new FormData();
	data.append('data', "idDriver="+idDriver+
						"^idCar="+idCar+
						"^idPhase="+idPhase+
						"^pickupsIds="+JSON.stringify(pickupsIds)+
						"^passengersIds="+JSON.stringify(passengers));
	request("templates/proxy.php?url=http://localhost:5000/shuttle/create/", function(xhr){
		var resp = JSON.parse(xhr.responseText);
		var num;
		if(resp["code"] != 1){
			console.error(resp["data"]);
			reportError(resp["message"]);
		}
		else{
			idNewShuttle = resp["data"];
			data = new FormData();
			data.append('data', "id="+idNewShuttle);

			request("templates/proxy.php?url=http://localhost:5000/shuttle/byid/lazy/", function (xhr, idNewShuttle){
				var resp = JSON.parse(xhr.responseText);
				var shuttle;
				if(resp["code"] != 1){
					reportError(resp["message"]);
				}
				else{
					// maj de la liste des navettes
					shuttle = resp["data"];
					shuttles[idNewShuttle] = {"shuttle": shuttle};
					drawShuttle(idNewShuttle);
				}
			}, data, idNewShuttle);
		}
	}, data);
}

/**
 * Modifie une navette
 * @param  {int} idShuttle     l'identifiant de la navette à modifier
 * @param  {int} idDriver      l'identifiant du conducteur
 * @param  {int} idCar         l'identifiant du véhicule
 * @param  {[int]} pickupsIds    liste d'identifiants de pickups
 * @param  {[int]} passengersIds liste d'identifiants de passagers
 */
function changeShuttle (idShuttle, idDriver, idCar, pickupsIds, passengersIds) {

	// maintenant on envoi l'update de la navette pour le véhicule et les point d'arrêts
	var data = new FormData();
	data.append('data', "idCar="+idCar+
						"^idShuttle="+idShuttle+
						"^idPickups="+JSON.stringify(pickupsIds));
	request("templates/proxy.php?url=http://localhost:5000/shuttle/update/", function(xhr){
		var resp = JSON.parse(xhr.responseText);
		var num;
		if(resp["code"] != 1){
			console.error(resp["data"]);
			reportError(resp["message"]);
		}
		else{
			idNewShuttle = resp["data"];
			data = new FormData();
			data.append('data', "id="+idNewShuttle);

			request("templates/proxy.php?url=http://localhost:5000/shuttle/byid/lazy/", function (xhr, idNewShuttle){
				var resp = JSON.parse(xhr.responseText);
				var shuttle;
				if(resp["code"] != 1){
					reportError(resp["message"]);
				}
				else{
					// maj de la liste des navettes
					shuttle = resp["data"];
					shuttles[idNewShuttle].shuttle = shuttle;

					// on regarde pour chaque passager si il n'est pas déja passager
					for (var i in passengersIds){

						// on regarde si le point d'arret du passager est toujours présent pour la navette
						if (!isInPickups(idNewShuttle, passengersIds[i].idPickup)){
							setWorkerAsPassenger(passengersIds[i].idWorker, idNewShuttle, null);
						} else {
							var bool = false;
							for (var j in shuttles[idNewShuttle].shuttle.passengers){
								if (passengersIds[i].idWorker == shuttles[idNewShuttle].shuttle.passengers[j].worker.num){
									bool = true;
									break;
								}
							}
							// si on a pas le worker dans le passager de la navette, on doit le rajouter
							if (!bool){
								setWorkerAsPassenger(passengersIds[i].idWorker, idNewShuttle, passengersIds[i].idPickup);
							}
						}
					}

					// Maintenant on regarde si les passagers ne sont pas supprimé de la navette
					for (var i in shuttles[idNewShuttle].shuttle.passengers){
						var bool = false;
						for (var j in passengersIds){
							if (passengersIds[j].idWorker == shuttles[idNewShuttle].shuttle.passengers[i].worker.num){
								bool = true;
								break;
							}
						}
						// si l'ouvrier n'est pas dans la liste des nouveaux passager, il faut le supprimer
						if (!bool){
							setWorkerAsDirect(shuttles[idNewShuttle].shuttle.passengers[i].worker.num);
						}
					}
					eraseShuttle(idNewShuttle);
					drawShuttle(idNewShuttle, shuttles[idNewShuttle].numID);
				}
			}, data, idNewShuttle);
		}
	}, data);
}

/**
 * Supprime une navette
 * @param  {int} idShuttle l'identifiant de la navette à supprimer
 */
function removeShuttle (idShuttle) {
	var data = new FormData();
	data.append('data', "id="+idShuttle);
	request("templates/proxy.php?url=http://localhost:5000/shuttle/delete/byid", function(xhr){
		eraseShuttle(idShuttle);
		delete shuttles[idShuttle];
	}, data);
}

/**
 * Fait un échange de conducteur d'une navette entre le conducteur initial et un de ses passagers
 * @param  {int} idShuttle l'identifiant de la navette à modifier
 * @param  {int} idDriverNew  l'identifiant de nouveau conducteur
 */
function swapDriver (idShuttle, idDriverNew) {
	var data = new FormData();
	data.append("data", "idShuttle="+idShuttle+"^idDriverNew="+idDriverNew);
	request("templates/proxy.php?url=http://localhost:5000/shuttle/driver/swap/", function(xhr){
		var resp = JSON.parse(xhr.responseText);
		if(resp["code"] != 1){
		    reportError(resp["message"]);
		}
		else{
			var newShuttle = resp["data"];
			idMarker = shuttles[idShuttle].numID;
			eraseShuttle(idShuttle);
			shuttles[idShuttle] = {"shuttle":newShuttle};
			drawShuttle(idShuttle, idMarker);
		}
	}, data);
}


function Pickup(idPickup, latitude, longitude, address){
	if(idPickup>0) this.num = idPickup;
	else{
		newPickupsIdCount++;
		this.num = -(newPickupsIdCount);
	}
	this.position = new Position(latitude, longitude, address);
}

function Passenger(idPassenger, idWorker, idShuttle, idPickup){
	this.num = idPassenger;
	this.idShuttle = idShuttle;
	this.worker = workers[getWorkerById(idWorker)];
	if (pickups[idPickup]){
		this.pickup = pickups[idPickup].pickup;
	} else {
		this.pickup = null;
	}
}

function Position(latitude, longitude, address){
	this.latitude = latitude;
	this.longitude = longitude;
	this.address = address;
}


