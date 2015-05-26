/***************************
affiche le tableau des affectation en le remplissant grâces aux
ouvriers et affectations dans la BDD

****************************/

var urlSites = "templates/proxy.php?url=http://localhost:5000/site/all/lazy/";
var urlWorkers = "templates/proxy.php?url=http://localhost:5000/worker/all/";
//var urlAssignments = "templates/proxy.php?url=http://localhost:5000/assignments/all/";
var urlPartAssignments = "templates/proxy.php?url=http://localhost:5000/assignments/part/";
var urlNeedBySite = "templates/proxy.php?url=http://localhost:5000/need/bysite/byweek";
var urlUnavailability = "templates/proxy.php?url=http://localhost:5000/unavailability/after/";

var sitesById = {}; //table associative contenant les chantier (les clés sont les id chantier). La position ainsi que les phases ne sont PAS définies



var workers;

var sortOrder = {"column" : "workerName", //la colonne sur laquelle le tri s'applique
				"order" : true};//l'ordre (si vrai ordre alpha normal, sinon inversé)

var timeLimits = {};//les numéros de semaine/année de début et fin du tableau

// élément qui stockera la case cliqué dans le tableau de l'opti 
var starter = {};

// élément qui stockera la dernière case sélectionnée
var iteratorSelected = {};

// Fonctions lancées lors du chargement du script
//lance la première requete et initialise les animations des différents types de cellules
// Fonctions lancées lors du cargement du script
(function() {
	// On ajoute un spinner à la div status (l'icone de chargement)
	$("#status").append("<i style='margin:20px;' class='fa fa-spinner fa-spin fa-lg'></i>");
	

	//génère le header de la table
	initHeader(new Date(), 17);

	request(urlSites, function(xhr){
		    var resp = JSON.parse(xhr.responseText);
		    if(resp["code"] != 1){
		        reportError(resp["message"]);
		        return;
		    }
		    else{
			    //on récupère les info sur les chantiers
				resp = JSON.parse(resp["data"]);
				//transformation de l'array en associative array
				for(var i = 0; i<resp.length; i++){
					sitesById[resp[i].num] = resp[i];
				}
				request(urlWorkers, showTable);//une fois les info sur les chantiers récupérée on peut afficher correctement la table
		    }
			});
})();

function followUpNeed(xhr){
	var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
    	showNeed(JSON.parse(resp["data"]));
    }
}


/*********************************************
 ██████╗ ███████╗███╗   ██╗███████╗███╗   ██╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
██╔════╝ ██╔════╝████╗  ██║██╔════╝████╗  ██║██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
██║  ███╗█████╗  ██╔██╗ ██║█████╗  ██╔██╗ ██║███████║   ██║   ██║██║   ██║██╔██╗ ██║
██║   ██║██╔══╝  ██║╚██╗██║██╔══╝  ██║╚██╗██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
╚██████╔╝███████╗██║ ╚████║███████╗██║ ╚████║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
 ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                                    
██████╗ ███████╗    ██╗      █████╗     ████████╗ █████╗ ██████╗ ██╗     ███████╗   
██╔══██╗██╔════╝    ██║     ██╔══██╗    ╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔════╝   
██║  ██║█████╗      ██║     ███████║       ██║   ███████║██████╔╝██║     █████╗     
██║  ██║██╔══╝      ██║     ██╔══██║       ██║   ██╔══██║██╔══██╗██║     ██╔══╝     
██████╔╝███████╗    ███████╗██║  ██║       ██║   ██║  ██║██████╔╝███████╗███████╗   
╚═════╝ ╚══════╝    ╚══════╝╚═╝  ╚═╝       ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝ 
*********************************************/

//génère le header de la table dynamiquement
//startingDate : la date de début d'affichage
//numberOfWeeksToShow : le nombre de semaines à afficher (4 mois en général));
function initHeader(startingDate, numberOfWeeksToShow){
	var currWeekNumber = startingDate.getWeekNumber();//le numéro ISO de la semaine actuelle
	var yearNumber = startingDate.getFullYear();

	timeLimits["startWeek"] = currWeekNumber;
	timeLimits["startYear"] = yearNumber;

	// Récupération du nombre de semaines de l'année de la date actuelle (52 ou 53)
	var totalWeek = year52_53(startingDate);

	//génération de l'année	
	var textYear = "";
	var colspan = 0;
	if((currWeekNumber + 16) > totalWeek){//l'affichage est a cheval sur 2 années
		colspan = (totalWeek - currWeekNumber) + 1;
		textYear += '<th class="annee" colspan="' + colspan + '">' + yearNumber + '</th>';
		textYear += '<th class="annee" colspan="' + (numberOfWeeksToShow - colspan) + '">' + (yearNumber + 1) + '</th>';
		timeLimits["endYear"] = timeLimits["startYear"] + 1;
	}
	else{//on a qu'une seule année pour tout le tableau
		textYear += '<th class="annee" colspan="17">' + yearNumber + '</th>';
		timeLimits["endYear"] = timeLimits["startYear"];
	}
	$('#tab_site_head_0').append(textYear);
	//fin de génération de l'année
	
	//génération des semaines et des mois
	var textWeek = "";
	var textMonth = "";
	colspan = 0;
	var numLastWeek=currWeekNumber, lastMonth=startingDate.getMonth(), numYear=yearNumber;
	for(var i=currWeekNumber; i< currWeekNumber + numberOfWeeksToShow; i++){

		colspan++;//le mois contient une semaine de plus
		if(numLastWeek>/*52*/totalWeek){
			numLastWeek = 1;
			numYear++;
		}
		//textWeek += '<th class="weekNumber">' + numLastWeek + '</th>';
		textWeek += '<th class="weekNumber" data-numweek="'+numLastWeek+'" data-numyear="'+ numYear+'" >' + numLastWeek + '</th>';
		if(getMonthFromWeekNumber((numLastWeek+1) % (totalWeek +1)) != lastMonth || i == currWeekNumber + numberOfWeeksToShow -1){//nouvau mois ou dernier mois à afficher
			textMonth += '<th class="month" colspan="' + colspan + '">' + getMonthName(lastMonth) + '</th>';
			lastMonth = (lastMonth + 1) % 12;
			colspan = 0;
		}
		numLastWeek++;
	}
	timeLimits["endWeek"] = numLastWeek;
	$('.weekNumber').append(textWeek);
	$('.months').append(textMonth);
	//fin de génération des semaines/mois

	//spécification des largeurs des cases semaines
	var wtab = $("#tab_site").width();
	var wtaken = $($(".workerInfo")[0]).width() + $($(".workerInfo")[1]).width() + $($(".workerInfo")[2]).width();
	var w = ((wtab-wtaken)/17)/wtab*100 + "%";
	$(".weekNumber").css("width", w);
}

// fonction qui génère/affiche le tableau qui contiendra les affectations
function showTable(xhr){
	//récupération et triage des ouvriers par nom
	var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
		workers = JSON.parse(resp["data"]);
	}
	workers.sort(function(a,b){
		var comp = (a.name).localeCompare(b.name);
		if(comp===0){
			return (a.firstName).localeCompare(b.firstName);
		}
		else return comp;
	});

	//remplir le tableau avec les ouvriers
	completeTable();

	//searching things
	var search = document.getElementById('search');
	search.addEventListener("keyup", function(e) {filterTable(e.target.value);}, false);
	search.addEventListener("change", function(e) {filterTable(e.target.value);}, false);
	
	// On enlève le spinner de la div status
	// Et on ajoute des boutons dans la barre de status
	var statusDiv = $("#status");
	statusDiv.empty();
	statusDiv.append("<br/>");
	if(sessionStorage.lvladminreq == 1 || sessionStorage.lvladminreq == 3){
		statusDiv.append("	<div id='removable'>\
								<input id='launchButton' onClick='launchOpti();' class='buttonstatus btn btn-info' type='button' value='Lancer les calculs'>\
								<div id='criterias'>\
								</br>\
								<p>Critères de l'algorithme :</p>\
								<input id='slider' class='form-control' onChange='changeSlide(0)' type='range' name='critere' min='0' max='10'>\
								<div class='btn-group-sm'>\
								  <button type='button' onClick='changeSlide(1)' class='btn btn-default'><small id='distance'>Distance: 50%</small></button>\
								  <button type='button' onClick='changeSlide(-1)' class='btn btn-default'><small id='constance'>Constance: 50%</small></button>\
								</div>\
								<!--<div class='input-group'>\
									<span id='valMu' class='input-group-addon'>50</span>\
									<input id='sliderMu' class='form-control' type='range' name='critere' min='10' max='100'>\
								</div>\
								<div class='input-group'>\
									<span id='valLambda' class='input-group-addon'>50</span>\
									<input id='sliderLambda' class='form-control' type='range' name='critere' min='10' max='100'>\
								</div>\
								<div class='input-group'>\
									<span id='valNgen' class='input-group-addon'>10</span>\
									<input id='sliderNgen' class='form-control' type='range' value='10' name='critere' min='5' max='25'>\
								</div>-->\
								</div>\
								</div>");
		statusDiv.append("<br/>");
		statusDiv.append("<input id='validateAllButton' onclick='validate();' class='buttonstatus btn btn-success' type='button' value='Valider les choix'>");
		statusDiv.append("<br/>");
		statusDiv.append("<br/>");
		statusDiv.append("<a	name='anchor' href='#' onClick='return tabletoExcel(this);' download='Affectation_.xls'>" + 
			"<input id='excelButton' type='button' class='buttonstatus btn btn-info' value='Exporter en xls'></a>");
		}
	// $('#sliderMu').on("change", function (e, result) {
	// 	$('#valMu').html(document.getElementById('sliderMu').value);
 //    });
 //    $('#sliderLambda').on("change", function (e, result) {
	// 	$('#valLambda').html(document.getElementById('sliderLambda').value);
 //    });
 //    $('#sliderNgen').on("change", function (e, result) {
	// 	$('#valNgen').html(document.getElementById('sliderNgen').value);
 //    });

	// On cache ces boutons pour mieux les afficher ensuite
	$('#status').hide();	
}

//Fonction qui modifie la valeur du slider
function changeSlide(i){
	var slide = document.getElementById("slider");
	var max = parseInt(slide.max);
	var value = parseInt(slide.value);
	var temp = (parseInt(slide.value) + i) * 100 / max;
	if (i == 0){
		document.getElementById("distance").innerHTML = "Distance: "+temp+"%";
		document.getElementById("constance").innerHTML = "Constance: "+(100-temp)+"%";
	}
	if (i == 1 && value < max){
		slide.value = parseInt(slide.value) + i;
		document.getElementById("distance").innerHTML = "Distance: "+temp+"%";
		document.getElementById("constance").innerHTML = "Constance: "+(100-temp)+"%";		
	} else if (i == -1 && value > 0){
		slide.value = parseInt(slide.value) + i;
		document.getElementById("distance").innerHTML = "Distance: "+temp+"%";
		document.getElementById("constance").innerHTML = "Constance: "+(100-temp)+"%";	
	}
}


function searchWorkerById(id){

	for (var i =0; i<workers.length;i++){
		if (workers[i].num == id){
			return workers[i];
		}
	}
}

// Initialise le tableau d'affectation (cases vide)
// puis qui remplie les affectations existantes
function completeTable(){
	//création d'une ligne par ouvrier
	var myDate = new Date();
	myWeek = myDate.getWeekNumber();
	
	$('tbody').empty();
	
	for (i = 0; i < workers.length; i++) {
		var name = workers[i].name +" "+ workers[i].firstName;

		//parsage de l'adresse
		var address = getShortAddress(workers[i].position.address);

		var newLine = 
			'<tr data-numworker="'+ workers[i].num +'">'+
			'<td>'+name+'</td>'+
			'<td>'+workers[i].craft.name + '<br/>' + workers[i].qualification.name+'</td>'+
			'<td>'+address+'</td>'+
			 '</tr>';
		$('tbody').append(newLine);

		// on génère les balises td de chaque semaine
		generateTdsIds(workers[i].num, myWeek, myDate.getFullYear());
	}

	$('#tab_site').css('zIndex',-1000);
	//rend le header flottant
	$('#tab_site').floatThead({
		scrollingTop: 0,
		useAbsolutePositioning:false,		// false a l'origine
		zIndex:1
	});

	//remplir le tableau avec les affectations en base
	var data = new FormData();
	data.append('data', 'startWeek='+ timeLimits["startWeek"] +
						 '^startYear='+ timeLimits["startYear"] +
						  '^endWeek='+ timeLimits["endWeek"] +
						   '^endYear='+ timeLimits["endYear"]);
	request(urlPartAssignments, fillTableWithExistingAssignments, data);
	data = new FormData();
	data.append('data', 'numWeek='+ myWeek +
						 '^numYear='+ myDate.getFullYear());
	request(urlUnavailability, fillTableWithExistingUnavailability, data);
}


// fonction permettant de remplir le tableau d'affichage avec les affectations récupérée de la BDD
function fillTableWithExistingAssignments(xhr)
{
	var resp = JSON.parse(xhr.responseText);
	var assignments = [];
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
    	assignments = JSON.parse(resp["data"]);
    }
	localStorage.assignments = JSON.stringify(assignments);

	// Parcours de chaque affectation
	for(i = 0; i < assignments.length; i++)
	{	
		var currSite = sitesById[assignments[i].phase.numSite];

		initCase(assignments[i].worker.num, assignments[i].phase.numWeek, assignments[i].phase.numSite);
	}

	//ajout de l'évènement de popup sur clic
	activatePopups();
	joinCompleteTab();
} // Fin fonction fillTableWithExistingAssignments()

// fonction permettant de remplir le tableau d'affichage avec les congés récupérée de la BDD
function fillTableWithExistingUnavailability(xhr)
{
	var resp = JSON.parse(xhr.responseText);
	var assignments = [];
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
    	unavailability = JSON.parse(resp["data"]);
    }

	localStorage.unavailability = JSON.stringify(unavailability);

	// Parcours de chaque affectation
	for(i = 0; i < unavailability.length; i++)
	{	
		initCase(unavailability[i].idWorker, unavailability[i].numWeek, 0, unavailability[i].type);
	}
	joinCompleteTab();
}

var tcount=0;
function joinCompleteTab () {
	tcount++;
	if(tcount==2){
		$('#status').show('slow');
	}
}

// Fonction qui génère les balise td des semaines de chaque ouvrier avec l'identifiant de la balise
// qui sera définit comme un numéro de semaine (à partir de la date actuelle).
function generateTdsIds(workerNum, myActualWeek, myYear) {
	// Récupération du nombre total de semaines de l'année de la date actuelle (52 ou 53)
	var totalWeek = year52_53(new Date());

	// récupération du sélecteur contenant l'ouvrier (ligne => balise tr)
	var $workerAssignments = $('[data-numworker="' + workerNum + '"]');
	var myWeek = myActualWeek;
	var nbWeek = 17;
	var weekNbToInsert = myWeek;
	
	// Création de l'année suivante pour le cas ou l'on est à cheval sur 2 années
	var nextYear = myYear + 1;
	
	// création des 17 semaines (balises td);
	// si (myWeek + 16 < 53) => si on tiens sur une seule année
	if((myWeek + nbWeek) < (totalWeek + 1)) {
		var weekCounter, td;
		for(weekCounter = 0; weekCounter < nbWeek; weekCounter++) {
			td = $('<td class="' + myYear + ' empty" data-numweek=' + myWeek + ' data-numyear=' + myYear +' data-idsite="-1">&nbsp</td>');
			td.appendTo($workerAssignments);
			myWeek++;
		}
	}
	else{ // Sinon, cela veut dire que l'on doit créer 2 boucles, une pour la fin d'année, et une pour la nouvelle
		var weekCounter_endYear;
		var weekCounter_beginYear;
		// première boucle => fin première année
		for(weekCounter_endYear = myWeek; weekCounter_endYear < (totalWeek + 1); weekCounter_endYear++){
			$('<td class="empty" data-numweek=' + weekCounter_endYear + ' data-numyear=' + myYear + '>&nbsp</td>').appendTo($workerAssignments);
		}
		// deuxième boucle => début première année
		for(weekCounter_beginYear = 1; weekCounter_beginYear <= (nbWeek - ((totalWeek + 1) - myWeek)); weekCounter_beginYear++){
			$('<td class="empty" data-numweek=' + weekCounter_beginYear + ' data-numyear=' + nextYear + '>&nbsp</td>').appendTo($workerAssignments);
		}
	}
} // Fin fonction generateTdsIds()






/*********************************
██╗   ██╗████████╗██╗██╗     
██║   ██║╚══██╔══╝██║██║     
██║   ██║   ██║   ██║██║     
██║   ██║   ██║   ██║██║     
╚██████╔╝   ██║   ██║███████╗
 ╚═════╝    ╚═╝   ╚═╝╚══════╝ 
*********************************/

//transforme une addresse longue (n° + rue + CP + ville) en adresse courte (CP+ville)
function getShortAddress(address){
	//parsage de l'adresse
	var addressSplited = address.split(' ');
	var postalCode = -1;
    for(var j = addressSplited.length -1; j > 0 && postalCode == -1; j--){
        // Si c'est un nombre
        if( !(isNaN(parseInt(addressSplited[j]))) && addressSplited[j].length==5 ){
            postalCode = addressSplited[j];
        }
    }
	var indexStart = workers[i].position.address.lastIndexOf(postalCode);
	var shortAddress = address.slice(indexStart,
									address.length);
	if(indexStart == -1){
		shortAddress = address;
	}

	return shortAddress;
}


//fonction de comparaison entre 2 lignes du tableau, utilisée pour le tri
//row1 et row2 sont les deux éléments <tr> à comparer
//column correspond au nom de colonne que l'on veut trier "workerName" | "workerQualif" | "workerAddress"
//invert : true | false, si vrai inverse l'ordre
//retourne 1 si row1 > row2, -1 si < et 0 si les deux sont égales ou l'inverse si invert vaut true
function compareRows(row1, row2, columnName, invert){
	var columnNumber = -1;
	if(columnName == "workerName"){
		columnNumber=0;
	}
	else if (columnName == "workerQualif"){
		columnNumber=1;
	}
	else if (columnName == "workerAddress"){
		columnNumber=2;
	}
	if(columnNumber != -1){
		var val1 = $($(row1).children()[columnNumber]).text();
		var val2 = $($(row2).children()[columnNumber]).text();
		if(invert) return val2.localeCompare(val1);
		return val1.localeCompare(val2);
	}
	return 0;
}//fin de compareRows


//trie le tableau
//columnName la colonne critère pour le tri
//si le tableau était déjà trié sur cette colone, on inverse l'ordre de tri
function sortTable(columnName){
    if(sortOrder["column"] == columnName){//si on est déjà trié sur cette colonne
    	sortOrder["order"] = !sortOrder["order"];//alors on inverse le tri
    }
    else{
    	sortOrder["column"] = columnName;
    	sortOrder["order"] = true;
    }
    var allRows = $("tbody tr");//toutes les lignes
    allRows.sort(function(a, b){
    	return compareRows(a, b, sortOrder["column"], !sortOrder["order"]);
    });
    $("tbody").empty();
    $("tbody").append(allRows);

    //on réactive les popups
    activatePopups();
}// fin de sortTable

//filtre les lignes du tableau à afficher en fonction d'une chaine de caractère
function filterTable(str){
	$('.selected').popover('destroy');
	$('.selected').removeClass('selected');
	var searchStrings = str.toLocaleLowerCase().split(" ");
	var allRows = $("tbody tr");//toutes les lignes
	for(var rowNumber = 0; rowNumber < allRows.length; rowNumber++){//pour chaque ligne
		if(str == null || str == ""){
			$(allRows[rowNumber]).show();
		}
		else{
			var allStrFound = true; 
			for(var i = 0; i<searchStrings.length && allStrFound; i++){//on vérifie tous les critères de recherche
				if($(allRows[rowNumber]).text().toLocaleLowerCase().indexOf(searchStrings[i]) == -1){//on trouve la chaine quelque part dans le texte de la ligne
					allStrFound = false; //un des critère de recherche n'est pas remplit
				}
			}
			if(allStrFound){
				$(allRows[rowNumber]).show();
			}
			else{
				$(allRows[rowNumber]).hide();
			}
		}
	}
}

/*********************************
██████╗  ██████╗ ██████╗  ██████╗ ██╗   ██╗███████╗██████╗ 
██╔══██╗██╔═══██╗██╔══██╗██╔═══██╗██║   ██║██╔════╝██╔══██╗
██████╔╝██║   ██║██████╔╝██║   ██║██║   ██║█████╗  ██████╔╝
██╔═══╝ ██║   ██║██╔═══╝ ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
██║     ╚██████╔╝██║     ╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
╚═╝      ╚═════╝ ╚═╝      ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝
                                                           
*********************************/
function activatePopups(){
	var interactiveTds = $('tr td.assigned, tr td.empty, tr td.proposal, tr td.modified, tr td.unavailability ');
	var interactiveThs = $('th.weekNumber');

	//destruction des popus encore existantes
	$('.popover').remove();

	$(interactiveTds).on('click', function(event){
		event.stopPropagation();
		if(sessionStorage.lvladminreq == 1 || sessionStorage.lvladminreq == 3){
			$(interactiveTds).popover('destroy');
			showPopUp(this);
			}
	});

	$(interactiveThs).on('click', function(event){
		if(sessionStorage.lvladminreq == 1 || sessionStorage.lvladminreq == 3){
		showPopoverIndicators(this);
		}
	});

	$(document).bind('keydown', function(e){keyDown(e);});
}

function removePopovers () {
	$('.popover').remove();
	$('.tooltip').remove();
}

function showPopoverIndicators(elementClicked){
	//reinit des popovers
	$('.selected').removeClass('selected');
	removePopovers();

	//récupération des infos du nouveau popover
	var numWeek = parseInt($(elementClicked).attr('data-numweek'));
	var numYear = parseInt($(elementClicked).attr('data-numyear'));

	//récupération de l'ensemble des chantiers se déroulant sur la semaine
	var sitesInWeek = [];
	var dateOfCurrWeek = getDateOfISOWeek(numWeek, numYear);
	for (var key in sitesById){
		var currSite = sitesById[key];
         //récupération des dates du chantier
         var dateDeb = new Date();
         dateDeb.setFullYear(currSite.dateInitY, currSite.dateInitM - 1, currSite.dateInitD);
         var dateEnd = new Date();
         dateEnd.setFullYear(currSite.dateEndY, currSite.dateEndM - 1, currSite.dateEndD);
         //si le chantier se déroule dans la semaine cliquée, on l'ajoute à la lsite des chantiers à afficher
         if((dateEnd >= dateOfCurrWeek) && (dateDeb <= dateOfCurrWeek)){
                 sitesInWeek.push(currSite);
         }
	}
	//triage de la liste des chantiers
	sitesInWeek.sort(function(a,b){
		return a.numSite < b.numSite;
	});

	//création de la base du popover
	var contentStr = "<div class='row' style='margin:0;'><div class='col-md-6 col-popup-indic'><ul class='list-group' id='popover-list'>";
	var i = 0;
	for(i; i<sitesInWeek.length/2; i++){
		site = sitesInWeek[i];
		contentStr+="<li class='list-group-item list-site' \
						data-numSite='"+ site.num+"' \
						style='background:" + site.color +"'>" + site.numSite +"</li>";
	}
	contentStr+="</div><div class='col-md-6 col-popup-indic'><ul class='list-group' id='popover-list'>";
	for(i; i<sitesInWeek.length; i++){
		site = sitesInWeek[i];
		contentStr+="<li class='list-group-item list-site' \
						data-numSite='"+ site.num+"' \
						style='background:" + site.color +"'>" + site.numSite +"</li>";
	}
	contentStr+="</ul></div></div>";

	$(elementClicked).popover({
		html:true,
		placement:"bottom",
		title:'<div style="margin-right:10px">Semaine ' + numWeek + '</div>' +
			'<button class="close" onclick="removePopovers();" style="position:absolute; top:0; right:0px;"><i class="fa fa-times"></i></button>',
		content:$(contentStr),
		container:'body',
		trigger:'manual',
		animation:false
	});
	$(elementClicked).popover('show');
	//$('.popover-title').append('<button id="popovercloseid" type="button" class="close">&times;</button>');

	//pour chacun de ces chantiers, récupération de leurs besoins sur la semaine et construction des tooltip
	var data;
	for(var i in sitesInWeek){
		var data = new FormData();
        data.append('data', 'numSite='+ sitesInWeek[i].num +'^numWeek='+ numWeek);
        request(urlNeedBySite, completeNeed , data, sitesInWeek[i].num);
	}
	$('.popover').addClass('popover-indicator');
}

function completeNeed(xhr, numSite){
	var listElem = $('.list-site[data-numsite="'+numSite+'"]');
	var newline = "";
	var resp = JSON.parse(xhr.responseText);
	var needs = [];
	if(resp["code"] != 1){
	    reportError(resp["message"]);
	    return;
	}
	else{
		needs = JSON.parse(resp["data"]);
	}
	var fullfilled = true;
	var tooltipText = "<table class='indicatorsTable'>";
	for (var i = 0; i < needs.length; i++) {
		var totalAjoutLocal = 0;
		//Prise en compte des affectations faites en local
		if (assignmentsToAdd.length){
		    for (var j= 0; j<assignmentsToAdd.length; j++){
				var work = searchWorkerById(assignmentsToAdd[j].numWorker);
				if ((assignmentsToAdd[j].idSite == needs[i].numSite) && (assignmentsToAdd[j].numWeek == needs[i].numWeek)){	
					if ((work.qualification.num == needs[i].qualification.num) && (work.craft.num == needs[i].craft.num)){
						totalAjoutLocal++;
					}
				}
			}
		}
		
		//Prise en compte des suppressions faites en local
		if (assignmentsToDelete.length){
		    for (var j= 0; j<assignmentsToDelete.length; j++){
				var work = searchWorkerById(assignmentsToDelete[j].numWorker);
				if ((assignmentsToDelete[j].idSite == needs[i].numSite) && (assignmentsToDelete[j].numWeek == needs[i].numWeek)){
					if ((work.qualification.num == needs[i].qualification.num) && (work.craft.num == needs[i].craft.num)){
						totalAjoutLocal--;
					}
				}
			}
		}
		
		totalAjoutLocal = totalAjoutLocal + needs[i].totalAff; //mod local + nb d'aff en bdd
		if(totalAjoutLocal < needs[i].need){
			fullfilled = false;
			newLine = '<tr class="unfullfilled">';
		}
		else{
			newLine = '<tr class="fullfilled">';
		}
		newLine+='<td>'+needs[i].craft.name+ " " + '</td>'+
				'<td>'+needs[i].qualification.name+ " " +'</td>'+
				'<td>'+totalAjoutLocal+ "/" +needs[i].need+'</td>'+
				'</tr>';
		tooltipText += newLine;
	}
	tooltipText+="</table>";

	if(needs.length === 0) tooltipText="pas de besoins définis";
	//colorisation des bordures
	if(fullfilled){
		listElem.css("border", "2px solid green");
	}
	else{
		listElem.css("border", "2px solid red");
	}
	//ajout du tooltip sur les éléments de la liste
	listElem.tooltip({
		html:true,
		placement:'left',
		title:tooltipText,
		container:'body'
	});
}


/**
 * Construction et affichage d'une popup liée à une case du tableau
 * @param  {$(td)} elementClicked la case cliquée
 */
function showPopUp(elementClicked){
	$('#tab_site #tab_Workers td.selected').removeClass('selected');
	$(elementClicked).addClass('selected');
	$('.popover').remove();
	//récupération des informations importantes désignant la case
	var popupInfos = {};
	popupInfos["numWorker"] = $(elementClicked).parent().attr('data-numworker');
	popupInfos["nameWorker"] = $('[data-numworker="'+ popupInfos["numWorker"] + '"] td:first').text();
	popupInfos["numWeek"] = $(elementClicked).attr('data-numweek');
	popupInfos["numYear"] = $(elementClicked).attr('data-numyear');
	popupInfos["idSite"] = $(elementClicked).attr('data-idsite');
	popupInfos["numSite"] = $(elementClicked).attr('data-numsite');

    //on récupère la liste des chantiers se déroulant dans cette semaine
	// Récupération de l'ensemble des chantiers se déroulant en meme temps
    var sitesInWeek = [];//la liste des sites de la semaine cliquée
    var dateOfCurrWeek = getDateOfISOWeek(popupInfos["numWeek"], popupInfos["numYear"]);
    var dateOfNextWeek = new Date(dateOfCurrWeek);
    dateOfNextWeek.setDate(dateOfNextWeek.getDate() + 7);
    for(var key in sitesById){
    	var currSite = sitesById[key];
    	//récupération des dates du chantier
    	var dateDeb = new Date();
    	dateDeb.setFullYear(currSite.dateInitY, currSite.dateInitM - 1, currSite.dateInitD);
    	var dateEnd = new Date();
    	dateEnd.setFullYear(currSite.dateEndY, currSite.dateEndM - 1, currSite.dateEndD);

    	//si le chantier se déroule dans la semaine cliquée, on l'ajoute à la lsite des chantiers à afficher
    	if((dateEnd >= dateOfCurrWeek) && (dateDeb <= dateOfNextWeek)){
    		sitesInWeek.push(currSite);
    	}
    }
    //triage de la liste des chantiers
	sitesInWeek.sort(function(a,b){
		return a.numSite < b.numSite;
	});
    //création de la div de la popup
	var content = $("<div></div>");    
    var content2 = $("<div class='row'>Affectation : </div>");
    //construction de la liste déroulante
    var list = $('<select name="fonction" id="select_site">');
	list.append('<option value="-1">Aucune</option>');
	list.append('<option value="0">Indisponible</option>');
	for(var iterator in sitesInWeek){
		list.append('<option value=' + sitesInWeek[iterator].num +
					 ' data-toggle="tooltip" data-animation="false" '+
					 'title="'+sitesInWeek[iterator].name+'">' + sitesInWeek[iterator].numSite + '</option>');
	}
	
    content2.append(list);
    content.append(content2);
    content.append('<form class="form-horizontal" role="form" id="form_popup">'+
    					'<input id="form_unavailability_type" class="row form-control" style="display:none" name="unavailability_type" placeholder="Raison de l\'indisponibilité" autocomplete="off">'+
    					'<button type="submit" class="row btn btn-success btn-block">Valider</button>'+
    				'</form>');

	$(elementClicked).popover({
		html:true,
		placement:"auto",
		title:popupInfos["nameWorker"] + '</br>Semaine ' + popupInfos["numWeek"] +'<button class="close" onclick="removePopovers();" style="position:absolute; top:0; right:0px;"><i class="fa fa-times"></i></button>',
		content:content,
		container:'body',
		trigger:'manual',
		animation:false
	});
	$(elementClicked).popover('toggle');

	//sélèction du bon élément par défaut
	if($(elementClicked).hasClass("empty")){
    	$('#select_site').val(-1);
    }
    else if($(elementClicked).hasClass("unavailability")){
    	$('#select_site').val(0);
    	$('#form_unavailability_type').val($(elementClicked).text());
    }
    else{
    	var temp = $('#select_site option');
    	for(var i=0; i<temp.length; i++){
    		if(temp[i].value==$(elementClicked).attr("data-idsite")){
    			temp[i].selected = true;
    		}
    		else{
    			temp[i].selected = false;
    		}
    	}
    }

	//on montre le formulaire d'indisponibilité si pertinent
	if($("#select_site").val()==0){
	    	$("#form_unavailability_type").show();
	    	$("#form_unavailability_type").attr("required", true);
	    	setTimeout(function() {$("#form_unavailability_type").select();}, 0);
	    	$(elementClicked).popover('show');//rafraichissement du placement du popover
	}
	$("#select_site").on("change", function() {
			if($(this).val()==0){
		    	$("#form_unavailability_type").show();
		    	$("#form_unavailability_type").attr("required", true);
		    	setTimeout(function() {$("#form_unavailability_type").select();}, 0);
		    }
		    else{
		    	$("#form_unavailability_type").hide();
		    	$("#form_unavailability_type").attr("required", false);
		    }
		    $(elementClicked).popover('show');//rafraichissement du placement du popover
		});

	$('#form_popup').submit(function(event){
			event.preventDefault();
			validatePopUp($(elementClicked));
	    	removePopovers();
		});
}// end showPopUp

/**
 * validation d'un choix dans la popup
 * @param  {[type]} elementClicked [description]
 */
function validatePopUp(elementClicked){
	//récupération de l'id chantier qui a étée validée
	var idSiteValidated = $('#select_site option:selected').val();//l'identifiant du site selectionné
	if(idSiteValidated == null){//si rien n'as été selectionné, c'est soit que l'utilisateur a laissé le choix par défaut
		idSiteValidated = $('#select_site option:default').val();//recup num par défaut
	}
	//changements de la case montrée et des listes d'éditions
	setCase(elementClicked, idSiteValidated, $('#form_unavailability_type').val());
	elementClicked.addClass('selected');
}



// Fonction qui permet de mettre à jour la case suivante sur clique du bouton TAB
// après avoir valider une création d'affectation dans l'opti
// Sur clique de ECHAP, la sélection disparait
function keyDown(event) {
	//traitement normal si on a le focus sur le champ de recherche
	if($('input').is(':focus')){
		return;
	}
	
	// on clone l'élément d'origine ciblé
	var $tdSource = $('#tab_site #tab_Workers td.selected');
	var code = parseInt(event.keyCode);

	// si appui sur la touche TAB
	if(code == 9 && $tdSource){
		// on annule l'ancien comportement de la touche TAB pour qu'elle soit exclusive à notre fonction
		event.preventDefault();
		//suppression des popover
		$('tr td.assigned, tr td.empty, tr td.proposal, tr td.modified, tr td.unavailability ').popover("destroy");
		$tdDestination = $tdSource.next('td');
		setCase($tdDestination, $tdSource.attr('data-idsite'), $tdSource.text());
		$tdSource.removeClass('selected');
		$tdDestination.addClass('selected');

	}
	// Si appui sur la touche ECHAP, fermeture des popup
	else if(code == 27){
		event.preventDefault();
		removePopovers();
		//$tdSource.removeClass('selected');
	}
	// Si l'utilisateur appuie sur la touche suppr , effacage de la case
	else if(code == 46 || code == 8){
		event.preventDefault();
		removePopovers();
		// On récupère les infos de ce que l'on va supprimer pour l'enlever de la table AssignTable
		setCase($tdSource, -1, "");
		if(code == 8){//backspace, on déplace la selection a gauche
			$tdDestination = $tdSource.prev('td');
			if($tdDestination.hasClass("assigned") || $tdDestination.hasClass("proposal") || $tdDestination.hasClass("unavailability") || $tdDestination.hasClass("empty")){
				$tdSource.removeClass('selected');
				$tdDestination.addClass('selected');
			}
		}
	}
}


/***************************************
██╗   ██╗ █████╗ ██╗     ██╗██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
██║   ██║██╔══██╗██║     ██║██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
██║   ██║███████║██║     ██║██║  ██║███████║   ██║   ██║██║   ██║██╔██╗ ██║
╚██╗ ██╔╝██╔══██║██║     ██║██║  ██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
 ╚████╔╝ ██║  ██║███████╗██║██████╔╝██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
  ╚═══╝  ╚═╝  ╚═╝╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
***************************************/

function validate () {
	var proposals = $(".proposal");
	if(proposals.length>0){
		$('#validateModal1').modal();
	}
	else if(assignmentsToAdd.length>0 || assignmentsToDelete.length>0 || unavailabilitiesToDelete.length>0 || unavailabilitiesToAdd.length>0){
		$('#validateModal2').modal();
	}
	else {
		reportWarning("Aucune Modification à enregistrer");
	}
}

/**
 * valide uniquement les modifications validées par l'utilisateur
 */
function validateModifs () {
	//suppression des assignments à ajouter proposés par l'algo
	var proposals = $(".proposal");
	for (var i = 0; i < proposals.length; i++) {
		var c = $(proposals[i]);
		var numWorker = parseInt(c.parent().attr('data-numworker'));
		var numYear = c.attr('data-numyear');
		var numWeek = c.attr('data-numweek');
		RemoveFromAssignmentToAdd(numWorker, numYear, numWeek);
	}

	//validation de ce qu'il reste dans le tableau
	validateAll();
}


/* commit l'ensemble des modification validées par l'utilisateur 
les modifications deviennent effectives en base */
function validateAll(){
	$('#validateModal1').hide();
	$('#validateModal2').hide();
	if (assignmentsToAdd.length>0 || assignmentsToDelete.length>0 || unavailabilitiesToDelete.length>0 || unavailabilitiesToAdd.length>0){
		// création d'un tableau qui comprend les sites et les numéros de semaine affectés
		// par les modification de l'utilisateur ou de l'algorithme.
		var assignChanged = [];
		for (var i = 0; i < assignmentsToAdd.length; i++){
			assignChanged.push({"idSite": assignmentsToAdd[i]["idSite"], "numWeek": assignmentsToAdd[i]["numWeek"], "numYear": assignmentsToAdd[i]["numYear"]});
		}
		for (var i = 0; i < assignmentsToDelete.length; i++){
			assignChanged.push({"idSite": assignmentsToDelete[i]["idSite"], "numWeek": assignmentsToDelete[i]["numWeek"], "numYear": assignmentsToDelete[i]["numYear"]});
		}

		localStorage.assignments = JSON.stringify(assignChanged);
		var data = new FormData();

		data.append('data', 'tab='+JSON.stringify(assignmentsToAdd) +'^remove='+JSON.stringify(assignmentsToDelete));
		var  req = "templates/proxy.php?url=http://localhost:5000/assignments/insert/";
		request(req, validate1, data);
	}
	else {
		reportWarning("Aucune Modification à enregistrer");
	}

}

/*
appellée une fois la requete de validation terminée
*/
function validate1(xhr){
	res = JSON.parse(xhr.responseText);
	if(res["code"]!=1){
		reportError(res["message"], null);
	}
	var data = new FormData();
	data.append('data', 'remove='+JSON.stringify(unavailabilitiesToDelete));
	request("templates/proxy.php?url=http://localhost:5000/unavailability/delete/", validate2, data);
}

/*
appellée une fois la requete de validation terminée
*/
function validate2(xhr){
	res = JSON.parse(xhr.responseText);
	if(res["code"]!=1){
		reportError(res["message"], null);
	}
	var data = new FormData();
	data.append('data', 'insert='+JSON.stringify(unavailabilitiesToAdd));
	request("templates/proxy.php?url=http://localhost:5000/unavailability/insert/",	validate3, data);
}

/*
appellée une fois la requete de validation terminée
*/
function validate3(xhr){
	res = JSON.parse(xhr.responseText);
	if(res["code"]==1){
		if (JSON.parse(localStorage.assignments).length > 0){
		    localStorage.indexSite = 0;
			reportSuccess("Modifications validées", null, "index.php?choix=5");
		} else {
			reportSuccess("Modifications validées", null, "index.php?choix=5")
		}
	}
	else{
		reportError(res["message"], null, "index.php?choix=5");
	}	
}

/* exporte la table vers un xls*/
 function tabletoExcel(anchor) {
 	var table =  "tab_site";
 	$('thead tr th').attr('bdcolor', '#888888')
	var headerSite0 = document.getElementById('tab_site_head_0');
 	var headerSite1 = document.getElementById('tab_site_head_1');
 	var headerSite2 = document.getElementById('tab_site_head_2');
 	var headerSite =  '<tr>' + headerSite0.innerHTML + '</tr><tr>' + headerSite1.innerHTML + '</tr><tr>' + headerSite2.innerHTML + '</tr>';

    var uri = 'data:application/vnd.ms-excel;base64,',
    			template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table border="1">{header}{table}</table></body></html>',
    			base64 = function (s) { return window.btoa(unescape(encodeURIComponent(s))); } ,
    			format = function (s, c) { return s.replace(/{(\w+)}/g, function (m, p) { return c[p]; }); };
	    if (!table.nodeType) table = document.getElementById('tab_Workers');
	    var content="";
	    var t = $("#tab_Workers tr");
	    for(var i=0; i<t.length; i++){
	    	if($(t[i]).is(":visible")){
	    		content+='<tr>' + t[i].innerHTML + '</tr>';
	    	}
	    }
	    var ctx = { worksheet: 'Affectation', table: content, header: headerSite};
	    anchor.href = uri + base64(format(template, ctx));

    return true;
}

