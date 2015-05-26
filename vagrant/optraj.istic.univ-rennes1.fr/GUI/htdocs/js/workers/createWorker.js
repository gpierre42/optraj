var clickedOnMap = false;

(function() {
		
	initMap();
	allowClick(found,notFound);
	$('#address').keyup(function () { clickedOnMap = false; 
									  $('#cAddress').removeClass('disabled');
									});

	//on récupère les métiers afin de construire la liste déroulante
	request("templates/proxy.php?url=http://localhost:5000/craft/all/", followUpCraft);
	
	//on récupère les qualifications afin de construire la liste déroulante
	request("templates/proxy.php?url=http://localhost:5000/qualification/all/", followUpQualif);
		
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

function createWorker(){
	var address = $('#form input[name="address"]').val();
	codeAddress(address, followUpCreation, addressFail);
}

/**
appellée lors du chargement de la page
*/

/**
appelée une fois la résolution d'adresse terminée
*/
function followUpCreation(latitude, longitude){
	var name = $('#form input[name="name"]').val();
	var firstName = $('#form input[name="firstName"]').val();
	var birthdate = $('#form input[name="birthdate"]').val();
	var address = $('#form input[name="address"]').val();
	var craft = document.getElementById('craft_select').value;
	var qualification = document.getElementById('qualif_select').value;

	// Tests sur les champs du formulaire
	// si le champ est vide/invalide
	// on met le champ en question en rouge
	// et on affiche un popover
	if(name==""){
			$('#formNom').removeClass('has-success');//On enlève la classe qui permet de mettre en vert
			$('#formNom').addClass('has-error');//On ajoute la classe qui permet de mettre en rouge
			$('#cWorker').attr("data-content","Le champ \'Nom\' n'est pas rempli");// le contenu du popover
			$('#cWorker').popover('show');// affiche le popover
			setTimeout(function(){$('#cWorker').popover('destroy')},2000); //enlève le popover au bout de 2s
			return;
	}
	// si on arrive à ce test, c'est que name est rempli et firstName vide
	// on met le champ name en vert et firstName en rouge
	else if(firstName == ""){
			$('#formNom').removeClass('has-error');
			$('#formNom').addClass('has-success');
			$('#formPrenom').removeClass('has-success');
			$('#formPrenom').addClass('has-error');
			$('#cWorker').attr("data-content","Le champ \'Prénom\' n'est pas rempli");
			$('#cWorker').popover('show');
			setTimeout(function(){$('#cWorker').popover('destroy')},2000);
			return;
	}
	else if(!checkDate(birthdate)){
			$('#formNom').removeClass('has-error');
			$('#formNom').addClass('has-success');
			$('#formPrenom').removeClass('has-error');
			$('#formPrenom').addClass('has-success');
			$('#formDateN').removeClass('has-success');
			$('#formDateN').addClass('has-error');
			$('#cWorker').attr("data-content","Le champ \'Date\' n'est pas valide");
			$('#cWorker').popover('show');
			setTimeout(function(){$('#cWorker').popover('destroy')},2000);
			return;
	}else if(craft==""){
			$('#formNom').removeClass('has-error');
			$('#formNom').addClass('has-success');
			$('#formPrenom').removeClass('has-error');
			$('#formPrenom').addClass('has-success');
			$('#formDateN').removeClass('has-error');
			$('#formDateN').addClass('has-success');
			$('#formCraft').removeClass('has-success');
			$('#formCraft').addClass('has-error');
			$('#cWorker').attr("data-content","Veuillez sélectioner un métier");
			$('#cWorker').popover('show');
			setTimeout(function(){$('#cWorker').popover('destroy')},2000);
			return;
	}else if(qualification==""){
			$('#formNom').removeClass('has-error');
			$('#formNom').addClass('has-success');
			$('#formPrenom').removeClass('has-error');
			$('#formPrenom').addClass('has-success');
			$('#formDateN').removeClass('has-error');
			$('#formDateN').addClass('has-success');
			$('#formCraft').removeClass('has-error');
			$('#formCraft').addClass('has-success');
			$('#formQualif').removeClass('has-success')
			$('#formQualif').addClass('has-error');
			$('#cWorker').attr("data-content","Veuillez sélectioner une qualification");
			$('#cWorker').popover('show');
			setTimeout(function(){$('#cWorker').popover('destroy')},2000);
			return;
	}
	var s = 'name='+name+
		'^address='+address+
		'^firstName='+firstName+
		'^birthdate='+birthdate+
		'^latitude='+latitude+
		'^longitude='+longitude+
		'^craft='+craft+
		'^qualification='+qualification;
	var data = new FormData();
	data.append("data", s);
	
	// si tout est bon, on met tout en vert
	$('#formNom').removeClass('has-error');
	$('#formNom').addClass('has-success');
	$('#formPrenom').removeClass('has-error');
	$('#formPrenom').addClass('has-success');
	$('#formDateN').removeClass('has-error');
	$('#formDateN').addClass('has-success');
	$('#formCraft').removeClass('has-error');
	$('#formCraft').addClass('has-success');
	$('#formQualif').removeClass('has-error')
	$('#formQualif').addClass('has-success');
	
	request("templates/proxy.php?url=http://localhost:5000/worker/create/", creationOk, data);
}

function followUpCraft(xhr){
	var resp = JSON.parse(xhr.responseText)
    var crafts = [];
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        crafts = JSON.parse(resp["data"]);
    }
	var list = document.getElementById('craft_select');
	if(crafts != "undefined"){
		//trie par métier
		crafts.sort(function(a,b){return a.name>b.name});
		for(var i = 0; i < crafts.length; i++){
			var option = document.createElement("option");
			option.text = crafts[i].name;
			option.value = crafts[i].num;
			list.appendChild(option);
		}
	}
	else{
		reportError('Une erreur est survenue lors de la récupération des métiers.');
		return;
	}

}

function followUpQualif(xhr){
	var resp = JSON.parse(xhr.responseText)
	var qualifs = [];
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        qualifs = JSON.parse(resp["data"]);
    }
	
	var list = document.getElementById('qualif_select');
	if(qualifs != "undefined"){
		//trie par qualification
		qualifs.sort(function(a,b){return a.name>b.name});
		for(var i = 0; i < qualifs.length; i++){
			var option = document.createElement("option");
			option.text = qualifs[i].name;
			option.value = qualifs[i].num;
			list.appendChild(option);
		}
	}
	else{
		reportError('Une erreur est survenue lors de la récupération des qualifications.');
		return;
	}

}

/**
appelée une fois la création terminée avec succès
*/
function creationOk(xhr){
	var resp = JSON.parse(xhr.responseText)
	localStorage.clear();
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return
    }
	else{
		reportSuccess(resp["message"], null, "index.php?choix=6")
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
