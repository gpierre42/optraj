/*
CARRE NICOLAS
OPTRAJ
*/

(function() {

	// Si on est pas connecté, on supprime tous les liens sauf celui de l'accueil et de login
	if (sessionStorage.alreadyco != 100 || sessionStorage.isco == 0){
	
		sessionStorage.isco = 0;
		sessionStorage.lvladminreq = 0;
		document.getElementById('choix11').parentNode.removeChild(document.getElementById('choix11'));
		document.getElementById('choix3').parentNode.removeChild(document.getElementById('choix3'));
		document.getElementById('choix4').parentNode.removeChild(document.getElementById('choix4'));
		document.getElementById('choix5').parentNode.removeChild(document.getElementById('choix5'));
		document.getElementById('choix6').parentNode.removeChild(document.getElementById('choix6'));
		document.getElementById('choix18').parentNode.removeChild(document.getElementById('choix18'));
		document.getElementById('choix20').parentNode.removeChild(document.getElementById('choix20'));
	
	}
	// Si on est déjà connecté, on supprime le lien vers login et on cache le lien vers la gestion
	// de l'administration si on a pas les droits necéssaires.
	if (sessionStorage.isco == 1){

		document.getElementById('choix15').parentNode.removeChild(document.getElementById('choix15'));
		if (sessionStorage.lvladminreq != 3){
			document.getElementById('choix18').parentNode.removeChild(document.getElementById('choix18'));
		}
		// On met en place les variables de session et on affiche nom et prénom du connecté.
	    var name = document.getElementById('menuname');
		var div = document.createElement('li');
		var logname = sessionStorage.logname;
		var logfirstname = sessionStorage.logfirstname;
		div.setAttribute('class' , 'logname');
		div.appendChild(document.createTextNode(logfirstname + " " + logname));
		name.appendChild(div);

		}
})();

