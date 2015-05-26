/**
 * Module de gestion des cases du tableau des affectations
 * Permet de modifier à la fois les cases utilisateurs (éléments HTML) ainsi que
 * de tenir à jour les listes de modifications à valider en BDD
 */


var assignmentsToDelete = [];
var assignmentsToAdd = [];
var unavailabilitiesToDelete = [];
var unavailabilitiesToAdd = [];


/*
 ██████╗ ███████╗███████╗████████╗██╗ ██████╗ ███╗   ██╗
██╔════╝ ██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
██║  ███╗█████╗  ███████╗   ██║   ██║██║   ██║██╔██╗ ██║
██║   ██║██╔══╝  ╚════██║   ██║   ██║██║   ██║██║╚██╗██║
╚██████╔╝███████╗███████║   ██║   ██║╚██████╔╝██║ ╚████║
 ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                        
██╗     ██╗███████╗████████╗███████╗███████╗            
██║     ██║██╔════╝╚══██╔══╝██╔════╝██╔════╝            
██║     ██║███████╗   ██║   █████╗  ███████╗            
██║     ██║╚════██║   ██║   ██╔══╝  ╚════██║            
███████╗██║███████║   ██║   ███████╗███████║            
╚══════╝╚═╝╚══════╝   ╚═╝   ╚══════╝╚══════╝            
 */


/**
 * Ajoute une entrée dans la liste des assignments à entrer en BDD
 * @param {int} numWorker numéro du worker
 * @param {int} numYear   année
 * @param {int} numWeek   semaine
 * @param {int} idSite    identifiant du site
 */
function InsertInAssignmentsToAdd (numWorker, numYear, numWeek, idSite) {
	if(numWorker == null ||numWeek == null || numYear == null || idSite == null){
		console.log("erreur element a insérer dans assignmentsToAdd incomplet : ", numWorker, numYear, numWeek, idSite);
	}
	else{
		assignmentsToAdd.push({"numWorker":numWorker,
								"numYear":numYear,
								"numWeek":numWeek,
								"idSite":idSite});
	}
}

/**
 * Ajoute une entrée dans la liste des assignments à retirer de la BDD
 * @param {int} numWorker numéro de l'ouvrier
 * @param {int} numYear   année
 * @param {int} numWeek   semaine
 */
function InsertInAssignmentsToDelete (numWorker, numYear, numWeek, idSite) {
	if(numWorker == null ||numWeek == null || numYear == null || idSite == null){
		console.log("erreur element a insérer dans assignmentsToDelete incomplet : ", numWorker, numYear, numWeek, idSite);
	}
	else{
		assignmentsToDelete.push({"numWorker":numWorker,
								"numYear":numYear,
								"numWeek":numWeek,
								"idSite":idSite});
	}
}

/**
 * Ajoute une entrée dans la liste des indisponibilité à entrer en BDD
 * @param {int} numWorker numéro de l'ouvrier
 * @param {int} numYear   année
 * @param {int} numWeek   semaine
 * @param {text} text      le motif de l'indisponibilité
 */
function InsertInUnavailabilitiesToAdd (numWorker, numYear, numWeek, text) {
	if(numWorker == null ||numWeek == null || numYear == null || text == null){
		console.log("erreur element a insérer dans unavailabilitiesToAdd incomplet : ", numWorker, numYear, numWeek, text);
	}
	else{
		unavailabilitiesToAdd.push({"numWorker":numWorker,
								"numYear":numYear,
								"numWeek":numWeek,
								"type":text});
	}
}

/**
 * Ajoute une entrée dans la liste des indisponibilités à retirer de la BDD
 * @param {int} numWorker numéro de l'ouvrier
 * @param {int} numYear   année
 * @param {int} numWeek   semaine
 */
function InsertInUnavailabilitiesToDelete (numWorker, numYear, numWeek, text) {
	if(numWorker == null ||numWeek == null || numYear == null || text == null){
		console.log("erreur element a insérer dans unavailabilitiesToDelete incomplet : ", numWorker, numYear, numWeek, text);
	}
	else{
		unavailabilitiesToDelete.push({"numWorker":numWorker,
								"numYear":numYear,
								"numWeek":numWeek,
								"type":text});
	}
}

/**
 * Retire une entrée de la liste des assignments à aouter en BDD
 * @param {int} numWorker numéro de l'ouvrier
 * @param {int} numYear   année
 * @param {int} numWeek   semaine
 */
function RemoveFromAssignmentToAdd (numWorker, numYear, numWeek) {
	for(var iterator in assignmentsToAdd){
		if(assignmentsToAdd[iterator].numWorker == numWorker &&
			assignmentsToAdd[iterator].numYear == numYear &&
			assignmentsToAdd[iterator].numWeek == numWeek){
			assignmentsToAdd.splice(iterator, 1);
		}
	}
}

/**
 * retire une entrée de la liste des indisponibilités à ajouter en BDD
 * @param {int} numWorker numéro de l'ouvrier
 * @param {int} numYear   année
 * @param {int} numWeek   semaine
 */
function RemoveFromUnavailabilitiesToAdd (numWorker, numYear, numWeek) {
	for(var iterator in unavailabilitiesToAdd){
		if(unavailabilitiesToAdd[iterator].numWorker == numWorker &&
			unavailabilitiesToAdd[iterator].numYear == numYear &&
			unavailabilitiesToAdd[iterator].numWeek == numWeek){
			unavailabilitiesToAdd.splice(iterator, 1);
		}
	}
}

/*
 ██████╗ ███████╗███████╗████████╗██╗ ██████╗ ███╗   ██╗
██╔════╝ ██╔════╝██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║
██║  ███╗█████╗  ███████╗   ██║   ██║██║   ██║██╔██╗ ██║
██║   ██║██╔══╝  ╚════██║   ██║   ██║██║   ██║██║╚██╗██║
╚██████╔╝███████╗███████║   ██║   ██║╚██████╔╝██║ ╚████║
 ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                        
 ██████╗ █████╗ ███████╗███████╗███████╗                
██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝                
██║     ███████║███████╗█████╗  ███████╗                
██║     ██╔══██║╚════██║██╔══╝  ╚════██║                
╚██████╗██║  ██║███████║███████╗███████║                
 ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝                
 */

/**
 * Initialise une case du tableau avec des info récupérée de la BDD
 * @param  {[type]} numWorker [description]
 * @param  {[type]} numWeek   [description]
 * @param  {[type]} id        [description]
 * @param  {[type]} text      [description]
 * @return {[type]}           [description]
 */
function initCase(numWorker, numWeek, id, text){
	var td = $('tr[data-numworker="' + numWorker + '"] td[data-numweek="' + numWeek + '"]');
	switch(id){
		case -1:
			break;
		case 0:
			td.attr("class", "unavailability");
			td.html(text);
			break;
		default:
			var currSite = sitesById[id];//récupération du site courant
			td.attr("class", "assigned");
			setColor(td, currSite.color);
			setContent(td, currSite.numSite);
			td.attr("data-idsite", currSite.num);
			td.attr("data-numsite", currSite.numSite);
			break;
	}
}

// Fonction qui mets à jour le tableau avec une proposition de l'algo
function setProposal(workerNum,idWeek,idSite, year)
{	
	var currSite = sitesById[idSite];

	// style CSS pour une proposition d'affectation
	var styles = {"background" : currSite.color, "cursor" : 'pointer'};
	
	// déclaration d'une occurence de proposition d'affectation (il s'agit ici d'un dictionnaire -> pour le flask)
	var line = {"numWorker" : workerNum , "numWeek" : idWeek, "idSite" : idSite, "numYear" : year};
    //console.log(sitesById)

    var tdSelected = $('[data-numworker="'+ workerNum+ '"] td[data-numweek="' + idWeek + '"]');
    // Si la case est vide
    if(tdSelected.hasClass("empty"))
    {
    	// On ajoute dans le tableau des affectations crées la proposition actuelle
    	assignmentsToAdd.push(line);
    	
    	tdSelected.removeClass("empty");
    	tdSelected.addClass('proposal');
		tdSelected.attr('data-idsite', idSite);
		tdSelected.attr('data-numsite', currSite.numSite);
    	//tdSelected.html(currSite.numSite.substring(0,5)+"<br/>"+currSite.numSite.substring(5,9));
    	tdSelected.html(currSite.numSite);
   		tdSelected.css(styles);
   		setColor(tdSelected, currSite.color);
   	}
   	else{
   		//reportError("proposition de l'algo sur une case non vide")
   	}
}

/**
 * Change une case a partir d'un nouvel identifiant et d'un texte
 * @param {} tdToChange var JQuery d'un td du tableau
 * @param {int} newId     -1 pour aucun, 0 pour une indisponibilité, >0 pour une affectation (id d'un chantier)
 * @param {string} text      le motif d'indispo 
 */
function setCase (tdToChange, newId, text) {
	newId = parseInt(newId);
	console.log("setcase", tdToChange[0], newId, text);
	var elem = {};
	elem.numWorker = tdToChange.parent().attr('data-numworker');
	elem.numYear = tdToChange.attr('data-numyear');
	elem.numWeek = tdToChange.attr('data-numweek');
	elem.oldId = tdToChange.attr('data-idsite');
	elem.oldText = tdToChange.text();
	//on change une case qui a déjà été modifiée
	if(tdToChange.hasClass('modified')){
		//on change une affectation déjà modifée
		if(tdToChange.hasClass('assigned')){
			switch(newId){
				case -1://passage en empty
					RemoveFromAssignmentToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek);
					resetCaseTo(tdToChange, "empty modified");
					break;
				case 0://passage en indisponible
					RemoveFromAssignmentToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek);
					InsertInUnavailabilitiesToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek,
						text);
					resetCaseTo(tdToChange, "unavailability modified");
					break;
				default://choix d'un chantier
					//le chantier ne change pas
					if (newId == $(tdToChange).attr("data-idsite")) {
						return;//rien a faire
					}
					//on change de chantier
					else{
						RemoveFromAssignmentToAdd(elem.numWorker,
							elem.numYear,
							elem.numWeek);
						InsertInAssignmentsToAdd(elem.numWorker,
							elem.numYear,
							elem.numWeek,
							newId);
						resetCaseTo(tdToChange, "assigned modified");
					}
					break;
			}
		}
		//on change une indisponibilité déjà modifée
		else if(tdToChange.hasClass('unavailability')){
			switch(newId){
				case -1://passage en empty
					RemoveFromUnavailabilitiesToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek);
					resetCaseTo(tdToChange, "empty modified");
					break;
				case 0://passage en indisponible
					RemoveFromUnavailabilitiesToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek);
					InsertInUnavailabilitiesToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek,
						text);
					resetCaseTo(tdToChange, "unavailability modified");
					break;
				default://choix d'un chantier
					RemoveFromUnavailabilitiesToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek);
					InsertInAssignmentsToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek,
						newId);
					resetCaseTo(tdToChange, "assigned modified");
					break;
			}
		}
		//on change une case vide
		else if(tdToChange.hasClass('empty')){
			switch(newId){
				case -1://passage en empty
					return;
				case 0://passage en indisponible
					InsertInUnavailabilitiesToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek,
						text);
					resetCaseTo(tdToChange, "unavailability modified");
					break;
				default://choix d'un chantier
					InsertInAssignmentsToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek,
						newId);
					resetCaseTo(tdToChange, "assigned modified");
					break;
			}
		}
	}
	//on change une case qui n'a pas été modifiée
	else{
		//on change une affectation présente en base
		if(tdToChange.hasClass('assigned')){
			switch(newId){
				case -1://passage en empty
					InsertInAssignmentsToDelete(elem.numWorker,
						elem.numYear,
						elem.numWeek,
						elem.oldId);
					resetCaseTo(tdToChange, "empty modified");
					break;
				case 0://passage en indisponible
					InsertInAssignmentsToDelete(elem.numWorker,
						elem.numYear,
						elem.numWeek,
						elem.oldId);
					InsertInUnavailabilitiesToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek,
						text);
					resetCaseTo(tdToChange, "unavailability modified");
					break;
				default://choix d'un chantier
					//le chantier ne change pas
					if (newId == $(tdToChange).attr("data-idsite")) {
						return;//rien a faire
					}
					//on change de chantier
					else{
						//TODO test
						InsertInAssignmentsToDelete(elem.numWorker,
							elem.numYear,
							elem.numWeek,
							elem.oldId);
						InsertInAssignmentsToAdd(elem.numWorker,
							elem.numYear,
							elem.numWeek,
							newId);
						resetCaseTo(tdToChange, "assigned modified");
					}
					break;
			}
		}
		//on change une proposition de l'algo
		else if(tdToChange.hasClass('proposal')){
			switch(newId){
				case -1://passage en empty
					RemoveFromAssignmentToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek);
					resetCaseTo(tdToChange, "empty modified");
					break;
				case 0://passage en indisponible
					RemoveFromAssignmentToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek);
					InsertInUnavailabilitiesToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek,
						text);
					resetCaseTo(tdToChange, "unavailability modified");
					break;
				default://choix d'un chantier ou validation de la proposition
					if (newId != $(tdToChange).attr("data-idsite")) {
						//modification de liste à faire uniquement si ce n'est pas le meme chantier
						RemoveFromAssignmentToAdd(elem.numWorker,
							elem.numYear,
							elem.numWeek);
						InsertInAssignmentsToAdd(elem.numWorker,
							elem.numYear,
							elem.numWeek,
							newId);
					}
					resetCaseTo(tdToChange, "assigned modified");
					break;
			}
		}
		//on change une indisponibilité présente en base
		else if(tdToChange.hasClass('unavailability')){
			switch(newId){
				case -1://passage en empty
					InsertInUnavailabilitiesToDelete(elem.numWorker,
							elem.numYear,
							elem.numWeek,
							elem.oldText);
					resetCaseTo(tdToChange, "empty modified");
					break;
				case 0://passage en indisponible
					if(elem.oldText === text){
						return;
					}
					else{
						InsertInUnavailabilitiesToDelete(elem.numWorker,
							elem.numYear,
							elem.numWeek,
							elem.oldText);
						InsertInUnavailabilitiesToAdd(elem.numWorker,
							elem.numYear,
							elem.numWeek,
							text);
						resetCaseTo(tdToChange, "unavailability modified");
					}
					break;
				default://choix d'un chantier
					InsertInUnavailabilitiesToDelete(elem.numWorker,
							elem.numYear,
							elem.numWeek,
							elem.oldText);
					InsertInAssignmentsToAdd(elem.numWorker,
							elem.numYear,
							elem.numWeek,
							newId);
					resetCaseTo(tdToChange, "assigned modified");
					break;
			}
		}
		//on change une case vide et non modifée auparavant
		else if(tdToChange.hasClass('empty')){
			switch(newId){
				case -1://passage en empty
					return;
				case 0://passage en indisponible
					InsertInUnavailabilitiesToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek,
						text);
					resetCaseTo(tdToChange, "unavailability modified");
					break;
				default://choix d'un chantier
					InsertInAssignmentsToAdd(elem.numWorker,
						elem.numYear,
						elem.numWeek,
						newId);
					resetCaseTo(tdToChange, "assigned modified");
					break;
			}
		}
	}
	//changement du contenu de la case
	tdToChange.attr("data-idsite", newId);
	switch(newId){
		case -1:
			tdToChange.html("");
			tdToChange.attr('bgcolor', '#FFFFFF');
			break;
		case 0:
			tdToChange.html(text);
			tdToChange.attr('bgcolor', '#BBBBBB');
			break;
		default:
		console.log(newId);
			var currSite = sitesById[newId];//récupération du site courant
			setColor(tdToChange, currSite.color);
			//remplissage du nom du chantier
			setContent(tdToChange, currSite.numSite);

			break;
	}

	//désactivation du bouton de lancement de calculs
	$('#launchButton').addClass('disabled');
	$('#criterias').hide();

	console.log("assignmentsToDelete", assignmentsToDelete);
	console.log("assignmentsToAdd", assignmentsToAdd);
	console.log("unavailabilitiesToDelete", unavailabilitiesToDelete);
	console.log("unavailabilitiesToAdd", unavailabilitiesToAdd);
}

function setColor (td, color) {
	var R = parseInt(color.substring(1,3), 16);
	var G = parseInt(color.substring(3,5), 16);
	var B = parseInt(color.substring(5,7), 16);
	luma = 0.375*R + 0.5*G + 0.125*B;

	td.attr('style', 'background:' + color);
	td.attr('bgcolor', color);
	if(luma<110){
		$(td).css('color', 'white');
	}
	else{
		$(td).css('color', 'black');
	}
}

function setContent(td, content){
	if(isNaN(parseInt(content.substring(0,5)))){
		td.html(content);
	}
	else{
		td.html(content.substring(0,5)+"<br/>"+content.substring(5,9));
	}
}

/**
 * retire tous les attributs et mises en forme d'une case
 * 
 * @param  {[type]} tdToChange [description]
 * @return {[type]}            [description]
 */
function cleanCase (tdToClean) {
	tdToClean.removeAttr("style");
	tdToClean.removeAttr("data-original-title");
	tdToClean.removeAttr("title");
	tdToClean.removeAttr("data-idsite");
	tdToClean.removeAttr("data-numsite");
	tdToClean.removeClass("assigned");
	tdToClean.removeClass("proposal");
	tdToClean.removeClass("modified");
	tdToClean.removeClass("unavailability");
	tdToClean.removeClass("empty");
	tdToClean.empty();
}

/**
 * efface les mises en forme d'une case et redéfini ses classes
 * @param  {} tdToReset (JQuery) td à modifier
 * @param  {string} classes   chaine contenant les classes
 */
function resetCaseTo (tdToReset, classes) {
	cleanCase(tdToReset);
	tdToReset.attr("class", classes);
}
