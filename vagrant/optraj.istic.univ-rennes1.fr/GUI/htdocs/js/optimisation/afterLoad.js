var urlDistance = "templates/proxy.php?url=http://localhost:5000/optimisation/distance/";
var urlCompute = "templates/proxy.php?url=http://localhost:5000/optimisation/compute/";
var urlResult = "templates/proxy.php?url=http://localhost:5000/optimisation/result/";
var urlTest = "templates/proxy.php?url=http://localhost:5000/optimisation/testing/";
var urlProgressBar = "templates/proxy.php?url=http://localhost:5000/optimisation/progress/";

// On verifie si un algo est déjà en train de tourner
(function() {
	setTimeout("request(urlProgressBar, resultReady)",2000);
})();

// Fonction qui test si un algo est en cours et qui remplace les boutons par la barre de chargement si c'est le cas
function resultReady(xhr){
	var progress = JSON.parse(xhr.responseText);
	// Si on a un progression, c'est qu'un algo est en route, on affiche donc la barre de chargement
	if (progress["progress"]){
		$("#removable").replaceWith("<div style='margin:10px;' class='well' id='optiIndicators'><i style='margin:10px;' class='fa fa-spinner fa-spin fa-lg'></i></div>");
		$("#optiIndicators").empty();
		$("#optiIndicators").append("<p>Calculs en cours</p>");
	    $("#optiIndicators").append("<div class='progress progress-striped active'><div id='progressBar' class='progress-bar' style='width: 0%;'></div></div>");
	    setProgressBar(xhr);
	}
}

// Lancement de l'optimisation
function launchOpti(){
	var data = new FormData();
	data.append('data', 'critere='+ document.getElementById('slider').value +
						 '^max='+document.getElementById('slider').max);
						// '^mu='+document.getElementById('sliderMu').value+
						// '^lambda='+document.getElementById('sliderLambda').value+
						// '^ngen='+document.getElementById('sliderNgen').value
						//);
	request(urlCompute, optiLaunch, data);
}

// Masquage des boutons permettant de lancer l'opti et attente des resultats
function optiLaunch(xhr){
	var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return
    }
    else{
		var response =  resp["message"];
		$("#removable").replaceWith("<div style='margin:10px;' class='well' id='optiIndicators'><i style='margin:10px;' class='fa fa-spinner fa-spin fa-lg'></i></div>");
		$("#optiIndicators").empty();
		$("#optiIndicators").append("<p>"+response+"</p>");
	    $("#optiIndicators").append("<div class='progress progress-striped active'><div id='progressBar' class='progress-bar' style='width: 0%;'></div></div>");
	    waitResult();
	}
}

// Attente des resultats avec une requete vers Flask toute les 2 secondes
function waitResult(){
	setTimeout("request(urlProgressBar, setProgressBar)",500);
}

//change la valeur de la barre de progression
function setProgressBar(xhr){
	var resp = JSON.parse(xhr.responseText);
	if (resp["progress"] != null){
		// if (parseInt(resp["progress"]) - 1 == parseInt(resp["nbGen"])) {
		if(resp["status"]==true){
			request(urlResult, showResults);
		} else {
			var val = (parseInt(resp["progress"]) * 100) / parseInt(resp["nbGen"]);
			if (val == 100){val = 99;}
			if (val > 100){val = 100;}
			var txt = Math.floor(val)+'%';
			$('#progressBar').css('width',val+"%").text(txt);
			waitResult();
		}
	}
}

//affiche les résultats des calculs de l'algo
function showResults(xhr){
	var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return
    }
	else{
		reportSuccess("Calculs terminés")
	}
	console.log(resp)
	var assignmentsAlgo = JSON.parse(resp["data"]);

	// on récupère les propositions d'algo et on les insère dans le localStorage Javascript
	localStorage.assignmentsAlgo = JSON.stringify(assignmentsAlgo);

	//console.log("showResults => Ensemble des affectation proposés par l'algorithme" + JSON.stringify(assignmentsAlgo));
		
	for(i=0; i < assignmentsAlgo.length; i++) {
		var workerNum = assignmentsAlgo[i].worker.num;
		var idWeek = assignmentsAlgo[i].phase.numWeek;
		var siteNum = assignmentsAlgo[i].phase.numSite;
		var numYear = assignmentsAlgo[i].phase.numYear;		
		
		//console.log("	Dans showResults : worker : " + workerNum + ", semaine : " + idWeek + ", idNum : " + siteNum + ", Année : " + numYear);
		setProposal(workerNum,idWeek,siteNum, numYear);	
	}

	//$('.proposal').css({"border":"3px solid rgba(255,0,0,1)"});
	request(urlDistance, showIndicators);
}

function showIndicators(xhr){
	$("#optiIndicators").empty();
	var resp = JSON.parse(xhr.responseText);
	var distance;
	if(resp["code"] != 1){
	    reportError(resp["message"]);
	}
	else{
		distance = JSON.parse(resp["data"]);
	}
	$("#optiIndicators").append("<p><strong>Calculs terminés</strong>");
	//$("#optiIndicators").append("<p><strong>Calculs terminés</strong></p>Distance cumulée : " + distance + "km");
}
