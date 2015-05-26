/**
appelée pour la création de la navette
*/
function createShuttle(){
	var plate = $('#form input[name="plate"]').val();
    var model = $('#form input[name="model"]').val();
    var nbPlace = $('#form input[name="nbPlace"]').val();
    
    // Tests sur les champs du formulaire
	// si le champ est vide/invalide
	// on met le champ en question en rouge
	// et on affiche un popover
    if(plate==""){
			$('#formPlate').removeClass('has-success');
			$('#formPlate').addClass('has-error');
			$('#cWorker').attr("data-content","Le champ \'Numéro d'immatriculation\' n'est pas rempli");
			$('#cWorker').popover('show');
			setTimeout(function(){$('#cWorker').popover('destroy')},2000);
			return;
	}
	else if(model == ""){
			$('#formPlate').removeClass('has-error');
			$('#formPlate').addClass('has-success');
			$('#formModel').removeClass('has-success');
			$('#formModel').addClass('has-error');
			$('#cWorker').attr("data-content","Le champ \'Modèle\' n'est pas rempli");
			$('#cWorker').popover('show');
			setTimeout(function(){$('#cWorker').popover('destroy')},2000);
			return;
	}
	else if(nbPlace == 0){
			$('#formPlate').removeClass('has-error');
			$('#formPlate').addClass('has-success');
			$('#formModel').removeClass('has-error');
			$('#formModel').addClass('has-success');
			$('#formNbplaces').removeClass('has-success');
			$('#formNbplaces').addClass('has-error');
			$('#cWorker').attr("data-content","Le champ \'nombre de places\' n'est pas valide");
			$('#cWorker').popover('show');
			setTimeout(function(){$('#cWorker').popover('destroy')},2000);
			return;
	}

    var data = new FormData();
    var s = 'plate='+plate+'^model='+model+'^nbPlace='+nbPlace;
    data.append('data', s);
    
    // si tout est bon, on met tout en vert
    $('#formPlate').removeClass('has-error');
	$('#formPlate').addClass('has-success');
	$('#formModel').removeClass('has-error');
	$('#formModel').addClass('has-success');
	$('#formNbplaces').removeClass('has-error');
	$('#formNbplaces').addClass('has-success');
	
	var req = "templates/proxy.php?url=http://localhost:5000/car/create/";		
	
	request(req, creationOk, data);
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
		reportSuccess(resp["message"], null, "index.php?choix=3")
	}
}