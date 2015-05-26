var currSite = {};
var bigMap;
var dateMin;
var shuttles = [];
var workers = [];
var drivers = [];
var links = [];
var cars = [];
var shuttlesToCreate = [];
var pickups = [];
var colors = ["blue", "green", "red", "purple", "brown", "grey"];
var tabSite = [];
var date;
var toVisit = [];
var nbPlaceByShuttle = 5;
var rennes = new google.maps.LatLng(48.1134750,-1.6757080);
var rad = function(x) {
  return x * Math.PI / 180;
};

(function() {
	// récupération des affectations ajouté et supprimé par l"utilisateur ou l"algo
	assigns = JSON.parse(localStorage.assignments);
	if (assigns.length > 0){
		// initialisation du header pour les différentes semaines
		initHeader(new Date(), 17, "tabShuttle", false, showOtherWeek);
		
		// on tri ces affectations par site puis date
		assigns.sort(function(a, b){
			if (a["idSite"] < b["idSite"]){
				return false;
			} else if (a["idSite"] == b["idSite"]){
				if (a["numYear"] < b["numYear"]){
					return false;
				} else if (a["numYear"] == b["numYear"]){
					if (a["numWeek"] < b["numWeek"]){
						return false;
					} else {
						return true;
					}
				} else {
					return true;
				}
			} else {
				return true;
			}
		});
		// suppression des doublons
		for (var i = 0; i < assigns.length; i++){
			if (tabSite.indexOf(assigns[i]["idSite"]) == -1){
				tabSite.push(assigns[i]["idSite"]);
			}
			if (i + 1 < assigns.length){
				if (assigns[i]["idSite"] == assigns[i+1]["idSite"] && assigns[i]["numWeek"] == assigns[i+1]["numWeek"] && assigns[i]["numYear"] == assigns[i+1]["numYear"]){
					assigns.splice(i+1, 1);
				}
			}
		}

		// initialisation du tableau shuttlesToCreate
		for (var j = 0; j < assigns.length; j++){
			if (!shuttlesToCreate[assigns[j].idSite]){
				shuttlesToCreate[assigns[j].idSite] = [];
			}
			if (!shuttlesToCreate[assigns[j].idSite][assigns[j].numYear]){
				shuttlesToCreate[assigns[j].idSite][assigns[j].numYear] = [];
			}
			if (!shuttlesToCreate[assigns[j].idSite][assigns[j].numYear][assigns[j].numWeek]){
				shuttlesToCreate[assigns[j].idSite][assigns[j].numYear][assigns[j].numWeek] = [];
			}
		}

		// On lance la requete qui va supprimer les navettes à enlever de la base
		var data = new FormData();
		data.append("data", "shuttles="+localStorage.assignments);
		request("templates/proxy.php?url=http://localhost:5000/shuttles/delete/", getPickUps, data);
	} else {
		document.location.href = "index.php?choix=5";
	}

})();

// fonction permettant de récuperer les pickup
function getPickUps(xhr){
	// requete pour aller récuperer les pickup en base
	request("templates/proxy.php?url=http://localhost:5000/pickup/all/", formatPickUp);
}

// fonction permettant de mettre en forme les pickup (latitude et longitude en point par exemple)
function formatPickUp(xhr){
	var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
		pickups = JSON.parse(resp["data"]);

		for (var i = 0; i < pickups.length; i++){
			pickups[i].point = new google.maps.LatLng(pickups[i].position.latitude, pickups[i].position.longitude);
		}

		// On récupere les véhicules pour affecter un véhicule à une navette par la suite
		request("templates/proxy.php?url=http://localhost:5000/car/all/", getCars);	}
}

// fonction qui récupere les véhicules en base
function getCars(xhr){
	var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
		cars = JSON.parse(resp["data"]);

		// on les trie par nombre de place
		cars.sort(function(a, b){if (a["nbPlace"] > b["nbPlace"]){ return true;}});

		// on met un booléen pour dire si la voiture est déja utilisée ou non
		for (var i in cars){
			cars[i].used = false;
		}

		getSiteFromAssign(parseInt(localStorage.indexSite, 10));
	}
}

// Fonction qui permet de récuperer le site correspondant a idSite
function getSiteFromAssign(indexSite){


	// test pour savoir si on est sur le dernier element du tableau, auquel cas il faut
	// changer le texte du bouton.
	if (indexSite == (tabSite.length-1)){
		var button = document.getElementById('next');
		button.innerHTML = "Valider les choix";
		button.onclick = completeShuttles;
		button.setAttribute("data-valid", "valid");
	}
	// On vérifie que le chantier est bien dans le tableau tabSite
	if (tabSite[indexSite]){
		// On récupére le nouveau chantier
		var data = new FormData();
		data.append("data", "num="+tabSite[indexSite]);
		request("templates/proxy.php?url=http://localhost:5000/site/byid/", updateCurrSite, data);
	}
}

// Fonction qui met a jour le site courant et qui appelle les fonctions qui initialise la map et l'input
// de changement de semaine
function updateCurrSite(xhr){
	var resp = JSON.parse(xhr.responseText);
	if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
		currSite = JSON.parse(resp["data"]);

		// Création du point correspondant à la position du site
		currSite.point = new google.maps.LatLng(currSite.position.latitude, currSite.position.longitude);

		// Mise a jour du titre
		document.getElementById("titleH4").innerHTML = currSite.numSite + " : " + currSite.name;

		// on récupere la date de la premiere apparation du site dans le tableau
		date = findWeek(currSite.num);
		dateMin = date;

		// on créer le tableau toVisit qui garde une trace des numéro de semaine visité par l'utilisateur
		computeNbWeek();

		requestShuttlesByWeek();
	}
}

// fonction qui envoie la requete pour récuperer toutes les navettes de la semaine courante
function requestShuttlesByWeek(){
	var data = new FormData();
	data.append("data", "week="+date[0]+"^year="+date[1]);
    request("templates/proxy.php?url=http://localhost:5000/shuttle/byweek/", getShuttlesByWeek, data);
}

// fonction qui récuere les navettes de la semaine courante et les enleve des véhicules dispo
function getShuttlesByWeek(xhr){
	var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
		var shuttleOfWeek = JSON.parse(resp["data"]);

		// on remet les véhicules des navettes précédentes en dispo, sauf celles affetées sur une nouvelle navette
		// ainsi que celles déjà en base.
		for (var i = 0; i < cars.length; i++){
			for (var k = 0; k < shuttleOfWeek.length; k++){
				for (var j in shuttlesToCreate.length){
					if	(shuttleOfWeek[k].car.num == cars[i].num || shuttlesToCreate[j][date[1]][date[0]].idCar == cars[i].num){
						cars[i].used = true;
					} else {
						cars[i].used = false;
					}
				}
			}
		}

		// Puis on initialise la map
		initMap();
	}	
}

// Charge la grande carte pour la construction des navettes et récupère les ouvriers assignés
// au chantier courant et à la date spécifiés en paramètre
function initMap(){

	// coloration du numéro de semaine sélectionné dans le header
    selectOne("tabShuttle", date[0], false);

    // coloration des cases du header que l'on peut consulter
    selectRange("tabShuttle", dateMin[0], date[2]);

    //efface le marqueur s'il existe
    if(currSite.marker != undefined){currSite.marker.setMap(null);}

    var bound = new google.maps.LatLngBounds(); 
    bound.extend(currSite.point);
    bound.extend(rennes);
    var optionsMap = {
        center : rennes,
        zoom : 12
    };
        /* Ici, nous chargeons la map dans l'élément html ayant pour id "map" */
    bigMap = new google.maps.Map(document.getElementById("bigMap"), optionsMap);
    bigMap.fitBounds(bound);
    
    //affiche le nouveau marqueur
    currSite.marker = new google.maps.Marker({
        position: currSite.point,
        map: bigMap
    });

    // enfin on recupere les workers assignés à ce chantier pour la semaine courante
    var data = new FormData();
    data.append('data', 'idSite='+currSite.num+'^week='+date[0]+'^year='+date[1]);
    request("templates/proxy.php?url=http://localhost:5000/worker/assigned/bysite/byweek/", getWorkersDirections, data);
}

// recupere les workers et créer les directions
function getWorkersDirections(xhr){
	var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
		workers = JSON.parse(resp["data"]);

		// On créer les cercles représentants les workers sur la map
		addCircle();
		createDirectionsRen();
	}
}

// Fonction qui affiche les cercles représentant les ouvriers sur la map.
function addCircle(){
    $("#status").append('<div id="distWorkers"></div>');
    var infoBulle = new google.maps.InfoWindow();
	for (i = 0; i < workers.length; i++) {
		posWorker = new google.maps.LatLng(workers[i].position.latitude, workers[i].position.longitude);
		workers[i].mapPosition = posWorker;
		// Add circle overlay and bind to marker
		workers[i].circle = new google.maps.Circle({
			map: bigMap,
			center: posWorker,
			radius: 200,    // 10 miles in metres
			fillColor: '#AA0000',
			title: workers[i].num
		});

		google.maps.event.addListener(workers[i].circle, 'click', infoWorkers(infoBulle, workers[i].num));
	}
}

// Fonction de création de l'infobulle d'un worker
function infoWorkers(infoBulle, j) {
    return function() {
		var worker = getWorkerOrDriver(j);
        infoBulle.setContent(worker.firstName + " " + worker.name + " " + worker.position.address);
        infoBulle.setPosition(worker.mapPosition);
        infoBulle.open(bigMap);
    };
}

// Fonction qui trouve les ouvriers les plus éloignés du chantier courant et les
// affecte en temps que conducteur d'une navette.
function createDirectionsRen(){

	var icons = [];
	var nbShuttle = Math.ceil(workers.length/nbPlaceByShuttle);

    // on valide la semaine visité dans le tableau toVisit si ce n'est pas déjà fait
	if (!toVisit[date[0]]){
		toVisit[date[0]] = true;
	}

	// On verifie que l'utilisateur ne soit pas déja passé sur cette semaine pour ce site
	// car si c'est le cas, les navettes sont a prendre dans le tableau shuttles
	shuttles = findOnShuttles();
	if (shuttles.length > 0){
		var indexWorker;
		for (var i = 0; i < shuttles.length; i++){
			// on retrouve le drivers dans la liste des workers
			for (var j = 0; j < workers.length; j++){
				if (shuttles[i].idDriver == workers[j].num){
					indexWorker = j;
				}
			}

			var positions = [];
			// on ajoute la position du driver
			positions.push(workers[indexWorker].mapPosition);
			// on ajoute le worker au tableau de driver
			drivers.push(workers[indexWorker]);
			// et on l'enleve des workers dispo
			workers.splice(indexWorker, 1);

			// On met la position du site
			positions.push(currSite.point);

			// on retrouve le pickup correspondant si il existe
			if (shuttles[i].pickup) {
				for (var k = 0; k < pickups.length; k++) {
					if (pickups[k].num == shuttles[i].pickup) {
						wayPoint = [{location: pickups[k].point, stopover: true}];
						positions.push(wayPoint);
						shuttles[i].pickupMarker = new google.maps.Marker({
							position: wayPoint[0].location,
							map: bigMap,
							icon: "https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + (i+1) + "|428BCA|000000",
							title: pickups[k].position.address
						});
						break;
					}
				}
			}
			shuttles[i].marker.setMap(bigMap);
			shuttles[i].route.setMap(bigMap);
			// icons[i] = "https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + (i+1) + "|00FD00|000000";
			// shuttles[i].marker = new google.maps.Marker({
			//	position: positions[0],
			//	map: bigMap,
			//	icon: icons[i],
			//	draggable: true
			// });
			$("#status").append('<div id="route'+i+'"></div>');

			// Il ne reste qu'a tracer la navette
			//route(positions, i);
			addLine();
		}
	} else {
		if (workers.length > 0){
			// on cherche les workers les plus eloigné et on trace les routes correspondantes
			findDriver(nbShuttle, true, date[0]);
		}
	}
}

// Fonction qui trace l'itinéraire en fonction des positions données et de la direction calculée précédement
function route(positions, i) {
    // On construit le chemin de l'ouvrier le plus éloigné (chauffeur) vers le chantier si celui-ci n'est pas déja construit
    var direction;
    // TODO a voir si le if else est obligé
    if (shuttles[i].route == null){
		direction = new google.maps.DirectionsRenderer({
			map: bigMap,
			draggable:false,
			polylineOptions: {
				strokeColor: shuttles[i].color,
				strokeOpacity: 0.4,
				strokeWeight: 4
			},
			suppressMarkers : true
		});

	} else {
		direction = shuttles[i].route;
	}

    var origin = positions[0];
    var destination = positions[1];

    var request;
    // Si on a une position pour un pickup
    if (positions[2]){
		request = {
			origin      : origin,
			destination : destination,
			waypoints	: positions[2],
			travelMode  : google.maps.DirectionsTravelMode.DRIVING // Type de transport
		};
	} else {
		request = {	origin:origin,
					destination:destination,
					travelMode:google.maps.DirectionsTravelMode.DRIVING // Type de transport
		};
	}
	var directionsService = new google.maps.DirectionsService(); // Service de calcul d'itinéraire
    directionsService.route(request, function(response, status){ // Envoie de la requête pour calculer le parcours
        if(status == google.maps.DirectionsStatus.OK){
            direction.setDirections(response); // Trace l'itinéraire sur la carte et les différentes étapes du parcours
			waitForDirection(direction, i);
			google.maps.event.addListener(direction, 'directions_changed', function() {
				computeRouteDistance(direction.getDirections(),"#route"+i,"Navette "+(i+1));
			});
        }
        else
        {
            reportError("Error : "+status);
        }
    });

}

// Fonction qui trace une ligne d'un ouvrier vers la navette la plus proche
// ou le chantier si celui-ci est plus proche
function addLine(){

	// Remise a zero de links
	for (var i = 0; i < links.length; i++) {
		links[i].setMap(null);
	}

	// remise à zero du nombre du nombre de passager
	for (var j = 0; j < shuttles.length; j++) {
		shuttles[j].passengers = 1;
	}

	var distTotaleWorkers = 0;

    for (x = 0; x < workers.length; x++) {
		var distanceWS = getDistance(workers[x].mapPosition, currSite.point);
		var distanceWR = [];

		for (i = 0; i < shuttles.length; i++){
			var posPickup;
			var posDriver = shuttles[i].route.getDirections().routes[0].legs[0].start_location;

			workerToDriver = getDistance(workers[x].mapPosition, posDriver);
			// on recupere la distance entre le worker et le pickup de la navette si celui-ci existe
			if (shuttles[i].pickup != null){
				posPickup = getPickupById(shuttles[i].pickup).point;
				workerToPickUp = getDistance(workers[x].mapPosition, posPickup);
			} else {
				// sinon, on le met à la valeur de workerToDriver
				workerToPickUp = workerToDriver;
			}
			// on teste ensuite, quelle distance est la plus faible et on ajoute celle-ci dans distanceWR
			if (workerToPickUp < workerToDriver){
				distanceWR.push({"distance": workerToPickUp, "position": posPickup, "indexShuttle": i, "where": "Pikcup"});
			} else {
				distanceWR.push({"distance": workerToDriver, "position": posDriver, "indexShuttle": i, "where": "Driver"});
			}
		}

		// on rajoute les données pour le chantier
		distanceWR.push({"distance": distanceWS, "position":  currSite.point, "indexShuttle": null, "where": "site"});
		var finaleStart;
		var indexMinWR = distanceWR.length-1;
		var distance = distanceWR[indexMinWR].distance;
		for (i = 0; i < distanceWR.length-1; i++){
			// On vérifie si il y a de la place dans la navette et si la distance est inférieure à la distance mini précedente
			if ((shuttles[distanceWR[i].indexShuttle].passengers < shuttles[distanceWR[i].indexShuttle].nbPlace) &&
				(distanceWR[i].distance < distance)){
				indexMinWR = i;
				distance = distanceWR[i].distance;
			}
		}
		// On vérifie que l'index correspond à une distance par rapport à une étape d'une navette
		// et on incrémente le nombre de passagers de celle-ci
		if (indexMinWR != (distanceWR.length-1)){
			shuttles[indexMinWR].passengers += 1;
		}
		finaleStart = distanceWR[indexMinWR].position;
		distTotaleWorkers += distanceWR[indexMinWR].distance;
		links[x] = new google.maps.Polyline({
			map : bigMap,
			path: [workers[x].mapPosition, finaleStart],
			geodesic: true,
			strokeColor: "#ff0000",
			strokeOpacity: 0.5,
			strokeWeight: 1
		});
	}
    // Affectation des véhicules pour chaques navettes
    affectCar();


	//On affiche les marker designant le depart des navettes et on met les event en place si cela n'est pas deja fais
	for (i = 0; i < shuttles.length; i++){
		if (!shuttles[i].eventListener) {
			var infowindow = new google.maps.InfoWindow();
			google.maps.event.addListener(shuttles[i].marker, 'click', infoShuttles(infowindow, i));
			setEvent(i);
			shuttles[i].eventListener = true;
		}
	}
	$('#distWorkers').empty();
	$('#distWorkers').append('<br>Distances Ouvriers cumulées : ' + (distTotaleWorkers/1000).toFixed(1) + ' km');
}

// fonction permettant de retrouver un pickup a partir de son id
function getPickupById (idPickup) {
	for (var i = 0; i < pickups.length; i++) {
		if (pickups[i].num == idPickup) {
			return pickups[i];
		}
	}
}

// Fonction qui permet de creer l'infoBulle des navettes
function infoShuttles(infowindow, x) {
            return function() {
				var worker = getWorkerOrDriver(shuttles[x].idDriver);
				var pA = "Pas de point d'arrêt défini";
				var pickup;
				var nbPlace = shuttles[x].nbPlace;
				if (shuttles[x].pickup){
					pickup = getPickupById(shuttles[x].pickup);
					pA = pickup.position.address;
				}
				infowindow.setContent(	"Conducteur : "+worker.firstName + " " + worker.name +
										"<br/>Nombre de passagers : "+
																	"<select id='passengers'>"+
																		"<option>1</option>"+
																		"<option>2</option>"+
																		"<option>3</option>"+
																		"<option>4</option>"+
																		"<option>5</option>"+
																		"<option>6</option>"+
																		"<option>7</option>"+
																	"</select>"+
							"<br/>Point d'arrêt : "+pA);
                google.maps.event.addListener(infowindow, 'domready', function() {
					$('#passengers').val(nbPlace);
					var select = document.getElementById("passengers");
					select.addEventListener('change', function(){
						var value = parseInt($('#passengers :selected').text(), 10);
						shuttles[x].nbPlace = value;
						addLine();
					});
				});
                infowindow.open(bigMap, shuttles[x].marker);
            };
        }

// Fonction qui permet de mettre les events sur les navettes pour permettre de modifier ces dernieres
function setEvent(i){
	var inCircle = false;
	var oldPosition;
	google.maps.event.addListener(shuttles[i].marker, 'dragstart', function() {
		for (j = 0; j < workers.length; j++) {
			workers[j].circle.setRadius(500);
		}
		oldPosition = shuttles[i].marker.getPosition();
	});
	google.maps.event.addListener(shuttles[i].marker, 'dragend', function() {
		var positions = [];
		positions.push(shuttles[i].marker.getPosition());
		positions.push(currSite.point);
		var newDriver = 0;
		for (j = 0; j < workers.length; j++) {
			if(workers[j].circle.getBounds().contains(shuttles[i].marker.getPosition())){
				inCircle = true;
				newDriver = workers[j].circle.title;
			}
			workers[j].circle.setRadius(200);
		}
		if(inCircle){
			// Récupération et suppression du driver dans le tableau driver
			var driver = getBackDriver(shuttles[i]["idDriver"]);
			// On le remet dans le tableau workers
			workers.push(driver);
			var wTemp;
			// Et on supprime le nouveau driver pour le remettre en workers
			for (var x = 0; x < workers.length; x++){
				if (workers[x].num == newDriver){
					wTemp = workers[x];
					workers.splice(x, 1);
					break;
				}
			}

			// On rajoute le nouveau conducteur au tableau driver
			drivers.push(wTemp);

			// on cherche maintenant le point d'arrêt le plus adapté
			var distDriverSite = getDistance(currSite.point, wTemp.mapPosition);
			var pickupIndex = findPickUp(wTemp, distDriverSite);
			var wayPoint;
			// on ajoute la pickup dans position et on met a jour le marker
			if(pickupIndex != -1){
				var pickup = pickups[pickupIndex];
				wayPoint = [{location: pickup.point, stopover: true}];
				positions.push(wayPoint);
				if (!shuttles[i].pickupMarker){
					shuttles[i].pickupMarker = new google.maps.Marker({
						position: wayPoint[0].location,
						map: bigMap,
						icon: "https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + (i+1) + "|428BCA|000000",
						title: pickup.position.address
					});
				}
				shuttles[i].pickupMarker.setMap(bigMap);
				shuttles[i].pickupMarker.setPosition(wayPoint[0].location);
				shuttles[i].pickupMarker.setTitle(pickup.position.address);
				shuttles[i]["pickup"] = pickup.num;
			} else {
				shuttles[i].pickup = null;
				if (shuttles[i].pickupMarker){
					shuttles[i].pickupMarker.setMap(null);
				}
			}

			shuttles[i]["idDriver"] = newDriver;
			shuttles[i].route.directions = null;
			route(positions, i);
		}else{
			shuttles[i].marker.setPosition(oldPosition);
		}
		
	});
}

// Fonction qui permet de retrouver les shuttle modifié par l'utilisateur dans shuttlesToCreate
function findOnShuttles(){
	var res = [];
	for (var i = 0; i < shuttlesToCreate[currSite.num][date[1]][date[0]].length; i++) {
		res.push(shuttlesToCreate[currSite.num][date[1]][date[0]][i]);
	}
	return res;
}

// fonction qui test si toute les cases de directionsRen sont remplies
function allDirectionIsComplete(){
	var bool = true;
	for (var i = 0; i < shuttles.length; i++){
		if (shuttles[i].route == null){
			bool = false;
			break;
		}
	}
	return bool;
}

// Fonction d'attente des directionRenderer
function waitForDirection(direction, i){
	if (!allDirectionIsComplete()){
		shuttles[i].route = direction;
		computeRouteDistance(direction.getDirections(), "#route"+i,"Navette "+(i+1));
	}
	if (allDirectionIsComplete()){
		addLine();
	}
}

// Fonction qui fait le total de la distance de toutes les navettes affichées
function computeRouteDistance(result, idDiv, navette) {
	var total = 0;
	var myroute = result.routes[0];
	for (var i = 0; i < myroute.legs.length; i++) {
	total += myroute.legs[i].distance.value;
	}
	total = total / 1000.0;
	$(idDiv).empty();
	$(idDiv).append(navette + ' : ' + total.toFixed(1) + ' km');
}

// Fonction permettant de récupere toute les shuttles créées afin de les insérer en base
function computeShuttles () {
	var res = [];
	for (var i = 0; i < shuttlesToCreate.length; i++) {
		if (shuttlesToCreate[i] != undefined) {
			for (var j = 0; j < shuttlesToCreate[i].length; j++){
				if (shuttlesToCreate[i][j] != undefined) {
					for (var k = 0; k < shuttlesToCreate[i][j].length; k++) {
						if (shuttlesToCreate[i][j][k] != undefined) {
							for (var l = 0; l < shuttlesToCreate[i][j][k].length; l++) {
								res.push({	"idDriver": shuttlesToCreate[i][j][k][l].idDriver,
											"idPhase": shuttlesToCreate[i][j][k][l].phase.num,
											"idCar": shuttlesToCreate[i][j][k][l].idCar,
											"pickup": shuttlesToCreate[i][j][k][l].pickup});
							}
						}
					}
				}
			}
		}
	}
	return res;
}

// Fonction qui permet d'envoyer les navettes créées en base
function validateChoice(){
	var finaleShuttles = computeShuttles();
	var data = new FormData();
	console.log(finaleShuttles);
	s = "shuttles="+JSON.stringify(finaleShuttles);
	data.append('data', s);
	request("templates/proxy.php?url=http://localhost:5000/shuttle/create/several/", creationOk, data);
}

// fonction appelée lorsque la création des shuttles en base est terminée
function creationOk(){
	localStorage.clear();
	reportSuccess("Opération effectuée avec succès !", null, "index.php?choix=5");
}

// Fonction qui met à jour les ouvriers associés au numéro de semaine
// sur lequel on vient de cliquer
function showOtherWeek(target) {

	// On met les shuttles créées la semaine passée dans la tableau shuttlesToCreate si il n'y en a pas déja
	if (shuttlesToCreate[currSite.num][date[1]][date[0]].length > 0){
		shuttlesToCreate[currSite.num][date[1]][date[0]] = [];
	}
	for (var i = 0; i < shuttles.length; i++) {
		shuttlesToCreate[currSite.num][date[1]][date[0]].push(shuttles[i]);
	}

	var weekNumberNow = new Date().getWeekNumber();
    var numYear = new Date().getFullYear();
    var weekTarget = parseInt(target, 10);
    // On teste si le numero de semaine sur lequel on a cliqué est inférieur
    // au numero de semaine courante car si c'est le cas, c'est l'année suivante
    if (weekTarget < weekNumberNow){
		numYear += 1;
    }

	date = [weekTarget, numYear, date[2]];
	
	// Remise a zero des paramètres
	resetSettings();
	// on récupere les navettes de la semaine courante pour les enlever des véhicules dispo
	requestShuttlesByWeek();
}

// Fonction permettant de remettre tout à zero lors d'un changement de chantier
function hardResetSettings(){
	currSite = {};
	dateMin = [];
	date = [];
	workers = [];
	drivers = [];
	shuttles = [];
	toVisit = [];

	$('#status').empty();
}

// Fonction permettant de remettre à zero les élements de la map
function resetSettings(){
	drivers = [];
	workers = [];
	shuttles = [];
	$('#status').empty();
}

// Fonction qui calcule la distance entre p1 et p2
function getDistance(p1, p2) {
  var R = 6378137; // Earth’s mean radius in meter
  var dLat = rad(p2.lat() - p1.lat());
  var dLong = rad(p2.lng() - p1.lng());
  var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(rad(p1.lat())) * Math.cos(rad(p2.lat())) *
    Math.sin(dLong / 2) * Math.sin(dLong / 2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  var d = R * c;
  return d; // returns the distance in meter
}

// Fonction permettant de trouver le numero de semaine et l'année à laquel commence
// le site d'idSite dans le tableau assigns
function findWeek(idSite){
	var min, max, year;
	for (var j = 0; j < assigns.length; j++){
		if (assigns[j]["idSite"] == idSite){
			min = parseInt(assigns[j]["numWeek"], 10);
			year = parseInt(assigns[j]["numYear"], 10);
			var i = j;
			while ((i < assigns.length) && (assigns[i]["idSite"] == idSite)){
				max = parseInt(assigns[i]["numWeek"], 10);
				i++;
			}
			break;
		}
	}
    return [min, year, max];
}

// Fonction qui permet de determiner les semaines que l'on peut modifier et qui construit le tableau toVisit en l'initialisant à false.
function computeNbWeek(){
	var nb;
	if (date[0] <= date[2]){
		nb = date[2] - date[0];
	} else {
		nb = year52_53(new Date()) - date[0] + date[2];
	}
	for (var i = 0; i <= nb; i++){
		toVisit[date[0]+i] = false;
	}
}

// fonction qui complete les navettes absente du tableau shuttles
function completeShuttles(){
	for (var b = 0; b < toVisit.length; b++){
		if (toVisit[b] == false){
			// On determine si on est sur l'année courante ou la suivante
			var year = date[1];
			if (b < dateMin[0]) {
				year += 1;
			}
			date = [b, year];
			// enfin on recupere les workers assignés à ce chantier pour la semaine courante
			var data = new FormData();
			data.append('data', 'idSite='+currSite.num+'^week='+b+'^year='+year);
			request("templates/proxy.php?url=http://localhost:5000/worker/assigned/bysite/byweek/", getWorkers, data, date);
		}
	}
	waitForShuttles();
}

// recupere les workers puis calculs permettant de determiner les conducteurs des navettes
function getWorkers(xhr, date){
    // on valide la semaine visité dans le tableau toVisit si ce n'est pas déjà fait
	toVisit[date[0]] = true;

	var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
		workers = JSON.parse(resp["data"]);
		for (i = 0; i < workers.length; i++) {
			posWorker = new google.maps.LatLng(workers[i].position.latitude, workers[i].position.longitude);
			workers[i].mapPosition = posWorker;
		}

		if (workers.length > 0){
			findDriver(Math.ceil(workers.length/nbPlaceByShuttle), false, date[0]);
		}
	}
}

// Fonction qui permet de trouver le conducteurs des navettes et qui les trace sur la map si le booléen drawRoute est a true.
function findDriver(nbShuttle, drawRoute, week){
	// on construit d'abord des cercles autour des pickups afin de determiner quels points d'arrêts
	// sont les plus rentables
	var potentialDrivers = workers.slice();
	var circlesPickUp = [];
	var icons = [];
	for (var i = 0; i < pickups.length; i++){
		// on ajoute pour chaque pickup sa distance par rapport au site
		pickups[i].distanceFromSite = getDistance(pickups[i].point, currSite.point);
		circlesPickUp.push({	"pickup": pickups[i], "indexInPickups": i, "workers": [],
								"circle":	new google.maps.Circle({
											map: null,
											center: pickups[i].point,
											radius: (pickups[i].distanceFromSite*40)/100,    // 10 miles in metres
							})});

		for (var j = 0; j < potentialDrivers.length; j++){
			if (circlesPickUp[i].circle.getBounds().contains(potentialDrivers[j].mapPosition)){
				circlesPickUp[i].workers.push(potentialDrivers[j]);
				potentialDrivers.splice(j, 1);
			}
		}
	}

	// on trie maintenant ces cercles selon le nombre de workers à l'interieur
	circlesPickUp.sort(function(a,b){return a.workers < b.workers;});
	for (var k = 0; k < circlesPickUp.length; k++) {
		if (circlesPickUp[k].workers > nbPlaceByShuttle) {
			var nb = Math.ceil(circlesPickUp[k].workers/nbPlaceByShuttle);
			for (var l = 0; l < nb; l++) {
				circlesPickUp.splice(k+1, 0, circlesPickUp[k]);
			}
		}
	}

	var distanceWorkerSite, distanceWorkerPickUpSite, line, distFarthestWorker, distOtherWorker, index;

	// on determine maintenant pour les nbShuttle premier cercle, qui est le conducteur
	for (var g = 0; g < nbShuttle; g++){
		var driver, pickup, wayPoint;
		if (circlesPickUp[g].workers.length > 0){
			var maxPotential = 0;
			var indexMaxPotential = 0;
			var maxInCircle = 0;
			var indexMaxInCircle = 0;
			var boolPickUp = false;
			// On s'occupe d'abord des workers qui ne sont en dehors des cercles des pickups
			for (var h = 0; h < potentialDrivers.length; h++){
				// on calcul la distance entre le worker et le site
				distanceWorkerSite = getDistance(potentialDrivers[h].mapPosition, currSite.point);

				// on calcul la distance entre le worker et le site en passant par le pickup
				distanceWorkerPickUpSite = getDistance(potentialDrivers[h].mapPosition, circlesPickUp[g].pickup.point) + 
												getDistance(circlesPickUp[g].pickup.point, currSite.point);

				// si la distance avec le pickup est inférieure à la distance sans + 20% de cette derniere,
				// alors on peut considérer que ce worker est le conducteur de la navette
				if (distanceWorkerPickUpSite < (distanceWorkerSite + (10*distanceWorkerSite/100))){
					// On regarde alors si le max est inférieure à la distance passant par le pickup
					if (maxPotential < distanceWorkerPickUpSite){
						maxPotential = distanceWorkerPickUpSite;
						indexMaxPotential = h;
						boolPickUp = true;
					}
				}
			}

			// On fait la meme chose avec les workers dans le circlesPickUp
			for (var m = 0; m < circlesPickUp[g].workers.length; m++){
				// on calcul la distance entre le worker et le site
				distanceWorkerSite = getDistance(circlesPickUp[g].workers[m].mapPosition, currSite.point);

				// on calcul la distance entre le worker et le site en passant par le pickup
				distanceWorkerPickUpSite = getDistance(circlesPickUp[g].workers[m].mapPosition, circlesPickUp[g].pickup.point) + 
												getDistance(circlesPickUp[g].pickup.point, currSite.point);

				// si la distance avec le pickup est inférieure à la distance sans + 20% de cette derniere,
				// alors on peut considérer que ce worker est le conducteur de la navette
				if (distanceWorkerPickUpSite < (distanceWorkerSite + (10*distanceWorkerSite/100))){
					// On regarde alors si le max est inférieure à la distance passant par le pickup
					if (maxInCircle < distanceWorkerPickUpSite){
						maxInCircle = distanceWorkerPickUpSite;
						indexMaxInCircle = m;
						boolPickUp = true;
					}
				}
			}

			// Si on a trouvé un worker pour passé par le point d'arret, on construit la shuttle en fonction
			if (boolPickUp){
				// Il ne reste plus qu'a choisir le worker ayant la plus grand distance à parcourir

				if (maxInCircle > maxPotential){
					driver = circlesPickUp[g].workers[indexMaxInCircle];
					drivers.push(circlesPickUp[g].workers[indexMaxInCircle]);
				} else {
					driver = potentialDrivers[indexMaxPotential];
					drivers.push(potentialDrivers[indexMaxPotential]);
				}

				pickup = circlesPickUp[g].pickup;
				wayPoint = [{location: pickup.point, stopover: true}];

				// On créer la nouvelle navette pour la mettre en base
				line = {"idDriver" : driver.num, "idCar": null, "phase" : currSite.phases[week],
						"pickup" : pickup.num, "nbPlace" : nbPlaceByShuttle, "color" : colors[g],
						"route" : null, "passengers" : 1, "marker" : null, "eventListener": false};
				shuttles.push(line);

			// Sinon, c'est que le détour par ce pickup est trop couteux
			} else {
				distFarthestWorker = 0;
				distOtherWorker = 0;
				index = 0;

				// On récupere l'ouvrier le plus éloigné du chantier
				for (n = 0; n < workers.length; n++) {
					distanceWorkerSite = getDistance(workers[n].mapPosition, currSite.point);

					if (distanceWorkerSite > distFarthestWorker){
						distFarthestWorker = distanceWorkerSite;
						index = n;
						driver = workers[n];
					}
				}

				// On créer la nouvelle navette pour la mettre en base
				line = {"idDriver" : driver.num, "idCar": null, "phase" : currSite.phases[week],
						"pickup" : null, "nbPlace" : nbPlaceByShuttle, "color" : colors[g],
						"route" : null, "passengers" : 1, "marker" : null, "eventListener": false};
				shuttles.push(line);

				drivers.push(workers[index]);
			}
		} else {
			distFarthestWorker = 0;
			distOtherWorker = 0;
			index = 0;

			// On récupere l'ouvrier le plus éloigné du chantier
			for (o = 0; o < workers.length; o++) {
				distanceWorkerSite = getDistance(workers[o].mapPosition, currSite.point);
				if (distanceWorkerSite > distFarthestWorker){
					distFarthestWorker = distanceWorkerSite;
					index = o;
					driver = workers[o];
				}
			}

			// On créer la nouvelle navette pour la mettre en base
			line = {"idDriver" : driver.num, "idCar": null, "phase" : currSite.phases[week],
					"pickup" : null , "nbPlace" : nbPlaceByShuttle, "color" : colors[g],
					"route" : null, "passengers" : 1, "marker" : null, "eventListener": false};
			shuttles.push(line);

			drivers.push(workers[index]);
		}

		// On supprime le driver des workers pour les navettes suivantes
		for (var p = 0; p < workers.length; p++){
			if (workers[p].num == driver.num){
				workers.splice(p, 1);
				break;
			}
		}

		// on le supprime egalement de potentialDriver pour les prochains tours de boucle
		for (var q = 0; q < potentialDrivers.length; q++){
			if (potentialDrivers[q].num == driver.num){
				potentialDrivers.splice(q, 1);
				break;
			}
		}

		// si le booléen drawRoute est a vrai, on trace la route sur la map
		if (drawRoute){
			var positions = [];
			positions.push(driver.mapPosition);
			positions.push(currSite.point);
			if (pickup){
				positions.push(wayPoint);
				shuttles[g].pickupMarker = new google.maps.Marker({
					position: wayPoint[0].location,
					map: bigMap,
					icon: "https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + (g+1) + "|428BCA|000000",
					title: pickup.position.address
				});
			}
			icons[i] = "https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + (g+1) + "|00FD00|000000";
			shuttles[g].marker = new google.maps.Marker({
				position: driver.mapPosition,
				map: bigMap,
				icon: icons[i],
				draggable: true
			});

			$("#status").append('<div id="route'+g+'"></div>');
			// Il ne reste qu'a tracer la navette
			route(positions, g);
		}
	}
}

// Fonction d'attente des calculs des shuttles qui ne sont pas encore définies
function waitForShuttles(){
	if (toVisitIsComplete()){
		
		// On met toutes les nouvelles navettes de shuttles dans le tableau shuttlesToCreate
		for (var i = 0; i < shuttles.length; i++) {
			shuttlesToCreate[currSite.num][date[1]][date[0]].push(shuttles[i]);
		}
		// Remise a zero de toutes les variables
		hardResetSettings();
		
		// on test si on doit envoyer les résultats en base
		var button = document.getElementById('next');
		if (button.getAttribute("data-valid") == "valid"){
			reportCheck("Validation des choix", 'Êtes-vous sur de vouloir valider vos choix ? <br/>Vous ne pourrez plus revenir sur cette page par la suite', validateChoice);
		} else {
			// sinon, on passe au site suivant
			localStorage.indexSite = parseInt(localStorage.indexSite, 10)+1;
			getSiteFromAssign(parseInt(localStorage.indexSite, 10));
		}
	} else {
		// On attend avec un nouvel appel a waitForShuttles
		setTimeout(function(){waitForShuttles();}, 1000);
	}
}

// fonction qui test si toutes les cases de toVisit sont a true
function toVisitIsComplete(){
	bool = true;
	for (var i in toVisit){
		if (!toVisit[i]){
			bool = false;
		}
	}
	return bool;
}

function getBackDriver(id){
	var res = null;
	for (var i = 0; i < drivers.length; i++){
		if (drivers[i].num == id){
			res = drivers[i];
			drivers.splice(i, 1);
		}
	}
	return res;
}

// fonction qui permet de faire l'affectation des véhicules pour chaque navette
function affectCar() {
	for (var i = 0; i < shuttles.length; i++) {
		// On test si la navette à déjà un véhicule de défini
		if (shuttles[i].idCar != null){
			// On récupere le véhicule correspondant
			var car, indexInCars;
			console.log("new Car");
			for (var j = 0; j < cars.length; j++) {
				if (cars[j].num == shuttles[i].idCar){
					car = cars[j];
					indexInCars = j;
					break;
				}
			}
			// On regarde si le véhicule défini à assez de place pour prendre tous les passagers
			// car sinon on doit en trouver un nouveau
			if (shuttles[i].passengers != car.nbPlace){
				console.log("pas assez de place");
				cars[indexInCars].used = false;
				shuttles[i].idCar = findCar(shuttles[i].passengers);
			}
		} else {
			shuttles[i].idCar = findCar(shuttles[i].passengers);
			console.log(i, shuttles[i], shuttles[i].idCar);
		}
	}
}

// Fonction permettant de trouver un véhicule avec un nombre de passager minimum
// Retourne le num du véhicule trouvé.
function findCar(nbPlace) {
	var res;
	for (var i = 0; i < cars.length; i++) {
		if ((cars[i].nbPlace >= nbPlace) && !(cars[i].used)) {
			cars[i].used = true;
			res = cars[i].num;
			break;
		}
	}
	return res;
}

// fonction permettant de trouver le point d'arrêt le plus sensé
function findPickUp(driver, distDriverSite){
	var index = -1;
	var min = distDriverSite + distDriverSite*20/100;
	var temp;
	for (var i = 0; i < pickups.length; i++){
		temp = getDistance(driver.mapPosition, pickups[i].point) + getDistance(pickups[i].point, currSite.point);
		if (temp < min){
			min = temp;
			index = i;
		}
	}
	return index;
}

function getWorkerOrDriver(idWorker){
	var res = null;
	for (var i = 0; i < workers.length; i++){
		if (workers[i].num == idWorker){
			res = workers[i];
			break;
		}
	}
	if (res == null){
		for (var j = 0; j < drivers.length; j++){
			if (drivers[j].num == idWorker){
				res = drivers[j];
				break;
			}
		}
	}
	return res;
}