/*********************************************
	INITIALISATION DU HEADER DE LA TABLE
*********************************************/

var timeLimits = {};//les numéros de semaine/année de début et fin du tableau

//génère le header de la table dynamiquement
//startingDate : la date de début d'affichage
//numberOfWeeksToShow : le nombre de semaines à afficher (4 mois en général));
function initHeader(startingDate, numberOfWeeksToShow, id, floatable, eventWeek, eventMonth){
	var currWeekNumber = startingDate.getWeekNumber();//le numéro ISO de la semaine actuelle
	var yearNumber = startingDate.getFullYear();

	timeLimits["startWeek"] = currWeekNumber;
	timeLimits["startYear"] = yearNumber;

	//génération de l'année	
	var textYear = "";
	if((currWeekNumber + 16) > 52){//l'affichage est a cheval sur 2 années
		var colspan = (52 - currWeekNumber) + 1;
		textYear += '<th class="annee" colspan="' + colspan + '">' + yearNumber + '</th>';
		textYear += '<th class="annee" colspan="' + (numberOfWeeksToShow - colspan) + '">' + (yearNumber + 1) + '</th>';
		timeLimits["endYear"] = timeLimits["startYear"] + 1;
	}
	else{//on a qu'une seule année pour tout le tableau
		textYear += '<th class="annee" colspan="17">' + yearNumber + '</th>';
		timeLimits["endYear"] = timeLimits["startYear"];
	}
	$('#'+id+'_head_0').append(textYear);
	//fin de génération de l'année
	
	//génération des semaines et des mois
	var textWeek = "";
	var textMonth = "";
	var numLastWeek=0, colspan = 0, lastMonth=startingDate.getMonth();
	for(var i=currWeekNumber; i< currWeekNumber + numberOfWeeksToShow; i++){
		numLastWeek = i;
		colspan++;//le mois contient une semaine de plus
		if(numLastWeek>52) numLastWeek = (i%53)+1;
		if (i == currWeekNumber){
			textWeek += '<th class="weekNumber selected" style="cursor:pointer">' + numLastWeek + '</th>';

		} else {
			textWeek += '<th class="weekNumber" style="cursor:pointer">' + numLastWeek + '</th>';
		}
		if(getMonthFromWeekNumber((numLastWeek+1) % 53) != lastMonth || i == currWeekNumber + numberOfWeeksToShow -1){//nouvau mois ou dernier mois à afficher
			textMonth += '<th class="month" style="cursor:pointer" colspan="' + colspan + '">' + getMonthName(lastMonth) + '</th>';
			lastMonth = (lastMonth + 1) % 12;
			colspan = 0;
		}
	}
	timeLimits["endWeek"] = numLastWeek;
	$('#'+id+' .weekNumber').append(textWeek);
	$('#'+id+' .months').append(textMonth);
	// ajout des event sur click si la fonction eventWeek est définie
	if (eventWeek != null){
		var weeks = document.getElementById(id).getElementsByClassName("weekNumber");
		for (var i = 0; i < weeks.length; i++){
			weeks[i].onclick = function(event){
									event.stopPropagation();
									if (event.target.classList.contains("weekNumber")){
										eventWeek(event.target.innerHTML);
									}
								};;
		}
	}
	// ajout des event sur click si la fonction eventMonth est définie
	if (eventMonth != null){ 
		var months = document.getElementById(id).getElementsByClassName("month");
		for (var i = 0; i < months.length; i++){
			months[i].onclick = function(event){
									event.stopPropagation();
									if (event.target.className == "month"){
										eventMonth(event.target.innerHTML);
									}
								};;
		}
	}
	//fin de génération des semaines/mois

	//spécification des largeurs des cases semaines
	var wtab = $("#"+id).width();
	var wtaken = $($(".craft")[0]).width();
	var w = ((wtab-wtaken)/17)/wtab*100 + "%"
	$("#"+id+" .weekNumber").css("width", w);

	if (floatable){
		//rend le header flottant
		$('#'+id).floatThead({
			scrollingTop: 0,
			useAbsolutePositioning:false,
			zIndex:1
		});
	}
}

function selectRange(id, min, max){
	$('#'+id+' .range').css("background", "#ededed");
	$('#'+id+' .range').removeClass('range');
	$('#'+id+' .selected').css("background", "#a0cdd5");
	$("#"+id+" .weekNumber").each(function (){
		var value = parseInt($(this).html());
		if (value <= max && value >= min && $(this).attr("class") != "weekNumber selected"){
			$(this).css('background', '#ff6d6d');
			$(this).addClass("range");
		}
	});
}

function selectOne(id, val, bool){
	// si la case n'est pas déjà colorée en rouge, c'est quelle ne fait pas partie du "range". Du coup, on lui remet ca couleur d'origine
	$('#'+id+' .selected').css("background", "#ededed");
	$('#'+id+' .selected').removeClass('selected');
	$("#"+id+" .weekNumber").each(function (){
		var value = parseInt($(this).html());
		if (value == val){
			$(this).css("background", "#a0cdd5");
			$(this).addClass("selected");
		}
	});
}