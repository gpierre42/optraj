var clickedOnMap = false;
(function() {
	$("#tabWeek").hide();
	initMap();
	allowClick(found,notFound);
	$('#address').keyup(function () { clickedOnMap = false; 
									  $('#cAddress').removeClass('disabled');
									});
})();

function found(address){
	console.log(address);
	$('#cAddress').addClass('disabled');
	$('#address').val(address);
	clickedOnMap= true;

}
function notFound(lat,long){
	$('#cAddress').addClass('disabled');
	$('#address').val("");
	console.log("cette position n'a pas d'adresse mais on enregistre");
	clickedOnMap = true;
}
function createSite(){
	if(clickedOnMap){
		var marker = getMarker();
		followUpCreation(marker.position.lat(),marker.position.lng());
	}else{
		var address = $('#form input[name="address"]').val();
		codeAddress(address, followUpCreation, addressFail);
	}
	
}

/**
appelée une fois la résolution d'adresse terminée
*/
function followUpCreation(latitude, longitude){
	// Id du chantier que l'on souhaite modifier pour la requete
    var name = $('#form input[name="name"]').val();
    var dateInit = $('#form input[name="dateInit"]').val();
    var dateEnd = $('#form input[name="dateEnd"]').val();
    var numSite = $('#form input[name="numSite"]').val();
    var siteMaster = $('#form input[name="siteMaster"]').val();
    var siteManager = $('#form input[name="siteManager"]').val();
	var address = $('#form input[name="address"]').val();
	var phases = {};
	// on regarde si le tableau des besoins est visible
	if ($("#tabWeek").is(':visible')){
		var firstWeek = parseInt(document.getElementById('tabWeek_head_2').firstChild.innerHTML);
		var metiers = document.getElementsByClassName('metier');
		var numNewNeed = 0;
		var needs;
		var need;
		// On parcours les différentes lignes du tableau
		for (var m = 1; m < metiers.length; m++){
		    needs = metiers[m].parentNode.childNodes;
		    // Puis toutes les cases de chaques lignes
		    for (var i = 1; i < 18; i++){
		        var year = new Date().getFullYear();
		        if (i + firstWeek === 52){
		            year++;
		        }
		        // Si la case a une valeur, on doit l'envoyer
		        if (needs[i].innerHTML){
		        	// On test si la phase n'est pas déjà créée. Si elle ne l'est pas, on le fais.
		            if (phases[parseInt(i+firstWeek-1)] == null){
		            	phases[parseInt(i+firstWeek-1)] = {'numWeek': parseInt(i+firstWeek-1), 'numYear': year, 'needs': {}};
		            }
		            idPhase = parseInt(i+firstWeek-1);
		            // On parcours maintenant toutes les qualif pour cette phase courante
		            var qualification = document.getElementsByClassName("qualif"+metiers[m].id);
		            for (var n = 0; n < qualification.length; n++){
		                // On regarde si on a une valeur dans la case
		                if (qualification[n].childNodes[i].lastChild.value){
		                    var idNeed = -1;
							// On créer un nouveau need
		                    idNeed = idNeed - numNewNeed;
		                    numNewNeed++;
		                    need = {'need': parseInt(qualification[n].childNodes[i].lastChild.value),
		                            'craft': {'num':metiers[m].id},
		                            'qualification': {'name':qualification[n].childNodes[0].innerHTML}};
		                    phases[idPhase]['needs'][idNeed] = need;
		                }
		            }
		        }
		    }
		}
	}
	console.log(phases);
	
	// Tests sur les champs du formulaire
	// si le champ est vide/invalide
	// on met le champ en question en rouge
	// et on affiche un popover
	if(numSite==""){
			$('#formNum').removeClass('has-success');//On enlève la classe qui permet de mettre en vert
			$('#formNum').addClass('has-error');//On ajoute la classe qui permet de mettre en rouge
			$('#cWorker').attr("data-content","Le champ \'Numéro\' n'est pas rempli"); // le contenu du popover
			$('#cWorker').popover('show'); // affiche le popover
			setTimeout(function(){$('#cWorker').popover('destroy')},2000); //enlève le popover au bout de 2s
			return;
	}
	// si on arrive à ce test, c'est que numSite est rempli et name vide
	// on met le champ numsite en vert et name en rouge
	else if(name == ""){
			$('#formNum').removeClass('has-error');
			$('#formNum').addClass('has-success');
			$('#formNom').removeClass('has-success');
			$('#formNom').addClass('has-error');
			$('#cWorker').attr("data-content","Le champ \'Nom\' n'est pas rempli");
			$('#cWorker').popover('show');
			setTimeout(function(){$('#cWorker').popover('destroy')},2000);
			return;
	}
	else if(!checkDate(dateInit)){
			$('#formNum').removeClass('has-error');
			$('#formNum').addClass('has-success');
			$('#formNom').removeClass('has-error');
			$('#formNom').addClass('has-success');
			$('#formDateD').removeClass('has-success');
			$('#formDateD').addClass('has-error');
			$('#cWorker').attr("data-content","Le champ \'Date de début\' n'est pas valide");
			$('#cWorker').popover('show');
			setTimeout(function(){$('#cWorker').popover('destroy')},2000);
			return;
	}
	else if(!checkDate(dateEnd)){
			$('#formNum').removeClass('has-error');
			$('#formNum').addClass('has-success');
			$('#formNom').removeClass('has-error');
			$('#formNom').addClass('has-success');
			$('#formDateD').removeClass('has-error');
			$('#formDateD').addClass('has-success');
			$('#formDateF').removeClass('has-success');
			$('#formDateF').addClass('has-error');
			$('#cWorker').attr("data-content","Le champ \'Date de fin\' n'est pas valide");
			$('#cWorker').popover('show');
			setTimeout(function(){$('#cWorker').popover('destroy')},2000);
			return;
	}
	else if(siteMaster==""){
			$('#formNum').removeClass('has-error');
			$('#formNum').addClass('has-success');
			$('#formNom').removeClass('has-error');
			$('#formNom').addClass('has-success');
			$('#formDateD').removeClass('has-error');
			$('#formDateD').addClass('has-success');
			$('#formDateF').removeClass('has-error');
			$('#formDateF').addClass('has-success');
			$('#formChefC').removeClass('has-success');
			$('#formChefC').addClass('has-error');
			$('#cWorker').attr("data-content","Le champ \'Chef de Chantier\' n'est pas rempli");
			$('#cWorker').popover('show');
			setTimeout(function(){$('#cWorker').popover('destroy')},2000);
			return;
	}else if(siteManager==""){
			$('#formNum').removeClass('has-error');
			$('#formNum').addClass('has-success');
			$('#formNom').removeClass('has-error');
			$('#formNom').addClass('has-success');
			$('#formDateD').removeClass('has-error');
			$('#formDateD').addClass('has-success');
			$('#formDateF').removeClass('has-error');
			$('#formDateF').addClass('has-success');
			$('#formChefC').removeClass('has-error');
			$('#formChefC').addClass('has-success');
			$('#formCondT').removeClass('has-success')
			$('#formCondT').addClass('has-error');
			$('#cWorker').attr("data-content","Le champ \'Conducteur de travaux\' n'est pas rempli");
			$('#cWorker').popover('show');
			setTimeout(function(){$('#cWorker').popover('destroy')},2000);
			return;
	}
	var s = 'numSite='+numSite+
			'^name='+name+
			'^dateInit='+dateInit+
			'^dateEnd='+dateEnd+
			'^address='+address+
			'^latitude='+latitude+
			'^longitude='+longitude+
			'^siteMaster='+siteMaster+
			'^siteManager='+siteManager+
			'^color='+document.getElementById("colorPicker").value+
			'^phases='+JSON.stringify(phases);
	var data = new FormData();
    data.append('data', s);
    console.log(data)
    
    // si tout est bon, on met tout en vert
    $('#formNum').removeClass('has-error');
	$('#formNum').addClass('has-success');
	$('#formNom').removeClass('has-error');
	$('#formNom').addClass('has-success');
	$('#formDateD').removeClass('has-error');
	$('#formDateD').addClass('has-success');
	$('#formDateF').removeClass('has-error');
	$('#formDateF').addClass('has-success');
	$('#formChefC').removeClass('has-error');
	$('#formChefC').addClass('has-success');
    $('#formCondT').removeClass('has-error')
	$('#formCondT').addClass('has-success');
	
	request("templates/proxy.php?url=http://localhost:5000/site/create/", creationDone, data);
}

/**
appelée une fois la création terminée
*/
function creationDone(xhr){
	var resp = JSON.parse(xhr.responseText)
	localStorage.clear();
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return
    }
	else{
		reportSuccess(resp["message"], null, "index.php?choix=12")
	}
}


/**
appellée lors de l'appui sur "valider adresse"
*/
function checkAddress(){
	var address = $('#form input[name="address"]').val();
	codeAddress(address, addressOK, addressFail);
	
	function addressOK(latitude, longitude){
		document.getElementById("address").style.backgroundColor = 'rgb(117,254,98)';
		document.getElementById("address").style.color="black";
		showPosition(latitude, longitude);//inclure minimap.js pour que cela fonctionne
	}
}

/**
appelé si la résolution d'addresse à échouée
*/
function addressFail(address){
	// affichage du popover si l'adresse est vide ou incorrecte
	$('#cAddress').attr("data-content", address ? "L'adresse semble incorrecte : "+address : "Champ \'adresse\' vide");
	$('#cAddress').popover('show');
	setTimeout(function(){$('#cAddress').popover('destroy')},2000);
	setTimeout(function(){$('#cWorkers').popover('destroy')},2000);
	document.getElementById("address").style.backgroundColor = 'rgb(254,50,50)';
	document.getElementById("address").style.color="white";
}

/**
 * Fonction qui affiche le tableau de need lorsque l'on clique sur le bouton
 */
function showMeTab(){
	$('#tabWeek').show();
	$('#addNeedButton').hide();
}
