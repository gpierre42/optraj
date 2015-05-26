/**
Ce module sert à gérer les messages affichées par le GUI
**/

/***
affiche un message de rapport d'information en bleu
avec une icone représentant le gogo "i"
***/
function reportInfo(message, fadeTime, url){
	if(fadeTime==null){fadeTime=2000;}

	//définition du type de l'alerte
	$("#reportModalAlert").addClass('alert-info');
	$("#reportModalAlert").removeClass('alert-danger');
	$("#reportModalAlert").removeClass('alert-success');
	$("#reportModalAlert").removeClass('alert-warning');

	//définition du message à afficher
	$('#reportModalMessage').html('<i class="fa fa-info"></i> ' + message);

    $("#reportModal").modal('show');
    setTimeout(function(){$("#reportModal").modal('hide');},fadeTime);

    if(url!=null){
		setTimeout(function(){
				document.location.href=url;	
		},fadeTime+100);
    }
	return;
}

/***
affiche un message de rapport de succès en vert
avec une icone de case cochée
***/
function reportSuccess(message, fadeTime, url){
	if(fadeTime==null){fadeTime=2000;}

	//définition du type de l'alerte
	$("#reportModalAlert").addClass('alert-success');
	$("#reportModalAlert").removeClass('alert-info');
	$("#reportModalAlert").removeClass('alert-danger');
	$("#reportModalAlert").removeClass('alert-warning');

	//définition du message à afficher
	$('#reportModalMessage').html('<i class="fa fa-check"></i> ' + message);

    $("#reportModal").modal('show');
    setTimeout(function(){$("#reportModal").modal('hide');},fadeTime);

    if(url!=null){
		setTimeout(function(){
				document.location.href=url;	
		},fadeTime+100);
    }
	return;
}

/***
affiche un message de rapport de warning orange
avec une icone de point d'exclamation
***/
function reportWarning(message, fadeTime, url){
	if(fadeTime==null){fadeTime=2000;}

	//définition du type de l'alerte
	$("#reportModalAlert").addClass('alert-warning');
	$("#reportModalAlert").removeClass('alert-info');
	$("#reportModalAlert").removeClass('alert-success');
	$("#reportModalAlert").removeClass('alert-danger');

	//définition du message à afficher
	$('#reportModalMessage').html('<i class="fa fa-warning"></i> ' + message);

    $("#reportModal").modal('show');
    setTimeout(function(){$("#reportModal").modal('hide');},fadeTime);

    if(url!=null){
		setTimeout(function(){
				document.location.href=url;	
		},fadeTime+100);
    }
	return;
}

/***
affiche un message de rapport d'erreur rouge
avec une icone de sens interdit
***/
function reportError(message, fadeTime, url){
	if(fadeTime==null){fadeTime=2000;}

	//définition du type de l'alerte
	$("#reportModalAlert").addClass('alert-danger');
	$("#reportModalAlert").removeClass('alert-info');
	$("#reportModalAlert").removeClass('alert-success');
	$("#reportModalAlert").removeClass('alert-warning');

	//définition du message à afficher
	$('#reportModalMessage').html('<i class="fa fa-minus-circle"></i> ' + message);

    $("#reportModal").modal('show');
    setTimeout(function(){$("#reportModal").modal('hide');},fadeTime);

    if(url!=null){
		setTimeout(function(){
				document.location.href=url;	
		},fadeTime+100);
    }
	return;
}

function reportCheck (header, body, callback) {
	$("#modalCheckHeader").html(header);
	$("#modalCheckBody").html(body);
	$("#modalCheckButton").on('click', callback);
	$("#modalCheck").modal('show');
}