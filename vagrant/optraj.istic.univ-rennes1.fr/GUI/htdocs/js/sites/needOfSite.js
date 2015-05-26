var metiers = [];
var qualifs = [];
var realCraftQualif = [];

(function() {
	//on récupère les chantiers afin de construire la liste déroulante
    request("templates/proxy.php?url=http://localhost:5000/craft/all/", createTab);
})();

/**
 * Fonction qui créer le tableau des différentes semaine d'un chantier
 */
function createTab(xhr) {
    // récupération de tout les métiers disponible en BDD et ajout de la case "Besoin" en premier ligne
    var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        metiers = JSON.parse(resp["data"]);
        metiers.sort(function(a,b){return a.name>b.name;});
        
        // Création du header
        initHeader(new Date(), 17, 'tabWeek', false, null, null);

        // requete pour récuperer les qualifs
        request("templates/proxy.php?url=http://localhost:5000/qualification/all/", recordQualif);
    }
}

/**
 * Fonction qui enregistre dans la variable globale les qualif présentes en base
 */
 function recordQualif(xhr){
    var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
        qualifs = JSON.parse(resp["data"]);
        qualifs.sort(function(a,b){
                    var a = a.num;
                    var b = b.num;
                    if (a<b) return 1;
                    else if(a>b) return -1;
                    return 0;
                });

        // requete pour récupere le comptage des workers par craft et qualif
        request("templates/proxy.php?url=http://localhost:5000/worker/count/bycraftqualif/", getCount);
    }

 }

function getCount (xhr) {
    var resp = JSON.parse(xhr.responseText);
    var count;
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        count = JSON.parse(resp["data"]);
        createRealCraftQualif(count);
        realCraftQualif.unshift([{"craft" : {'name': "Besoins", 'num': -1}}]);

        // Création de la premiere colonne du tableau (metiers)
        var tab = document.getElementById('tab_Week');
        var tr, td;
        for (var i in realCraftQualif){
            tr = document.createElement('tr');
            td = document.createElement('td');
            td.innerHTML = realCraftQualif[i][0].craft.name;
            td.id = realCraftQualif[i][0].craft.num;
            td.className = "metier";
            tr.appendChild(td);
            tab.appendChild(tr);
            if (i != 0){
                tr.addEventListener('click', function(e) {addLineQualif(e.target.parentNode);}, true);
                tr.className = "redHover greyT";
            }
        }

        // Affichage des phases du chantier courant si on est dans le cas de l'édition d'un chantier
        if('function' == typeof(showNeed)){
            showNeed();
        }
    }
}

function getBackCraft (idCraft) {
    for (var i = 0; i < metiers.length; i++){
        if (metiers[i].num == idCraft){
            return metiers[i];
        }
    }
}

function getBackQualif (idQualif) {
    for (var i = 0; i < qualifs.length; i++){
        if (qualifs[i].num == idQualif){
            return qualifs[i];
        }
    }
}

function createRealCraftQualif (count) {
    for (var i = 0; i < count.length; i++){
        craft = getBackCraft(count[i].numCraft);
        qualif = getBackQualif(count[i].numQualification);
        if (!realCraftQualif[craft.num]){
            realCraftQualif[craft.num] = [{"craft" : craft, "qualif" : qualif}];
        } else {
            realCraftQualif[craft.num].push({"craft" : craft, "qualif" : qualif});
        }
    }
}

/**
 * Cette fonction remplie le tableau avec le nombre de worker demandé dans une phase pour le chantier courant.
 */
function showNeed(){
    if ("function" === typeof(modifInput)){
        document.getElementById("tabWeek").addEventListener('click', function(e) {modifInput(e.target);}, true);
    }
    var phases;
    // Si la variable currSite n'est pas définie c'est que l'on est dans la page de création d'un chantier
    // donc on n'as pas besoin d'afficher les données des phases en base puisqu'il n'y en a pas
	if (typeof(currSite) != 'undefined'){
        phases = currSite.phases;
    } else {
        phases = {};
    }
    var tabPhase = {};
    var dictMonth = {};
    var dictPhase, dictQualif;
    var year = new Date().getFullYear();
    // Premiere étapes, création d'un dico contenant tous les besoins du chantier courant
    for (var y in phases){
        for (var w in phases[y]){
            dictPhase = {};
            temp = phases[y][w];
            var numYear = temp['numYear'];
            var numWeek = temp['numWeek'];
            for (var j in temp['needs']){
                var craft = temp['needs'][j]['craft']['num'];
                var q = temp['needs'][j]['qualification']['num'];
                if (!tabPhase[numYear]){
                    tabPhase[numYear] = {};
                }
                if (!tabPhase[numYear][numWeek]){
                    tabPhase[numYear][numWeek] = {};
                }
                if (!tabPhase[numYear][numWeek][craft]){
                    tabPhase[numYear][numWeek][craft] = {};
                }
                if (!tabPhase[numYear][numWeek][craft][q]){
                    tabPhase[numYear][numWeek][craft][q] = {};
                }
                tabPhase[numYear][numWeek][craft][q] = temp['needs'][j]['need'];
            }
        }
    }

    // Puis on peut commencer a remplir le tableau avec les données recupérées
    var firstWeek = parseInt(document.getElementById('tabWeek_head_2').firstChild.innerHTML, 10);
    var lignes = document.getElementsByClassName('metier');
    var metier, td, input;
    // On parcours toute les lignes du tableaux
    for (var i = 0; i < lignes.length; i++){
        var valueCompute = [];
        metier = parseInt(lignes[i].id, 10);
        // Puis toute les cases d'une lignes
        for (var j = 0; j < 17; j++){
            var year = new Date().getFullYear();
            if (j+firstWeek === year52_53(new Date())){
                year++;
            }
            td = document.createElement('td');
            // Si le chantier n'est pas commencé ou déja terminé, on grise la case
            if (greyCaseBegin(firstWeek+j, year) || greyCaseEnd(firstWeek+j, year)) {
                td.style.background = "#ededed";
            }
            td.className = j;
            td.addEventListener('change', function(e) {computeNeed(parseInt(e.target.className, 10));}, false);
            lignes[i].parentNode.appendChild(td);
        }
        if (metier !== -1) {
            // Ajout des lignes des differentes qualif. Elles sont cachées pour le moment
            for (var k = 0; k < realCraftQualif[metier+1].length; k++){	
                newTr = document.createElement("tr");
                newTr.className = "whiteT qualif qualif"+lignes[i].parentNode.firstChild.id;
                var q = document.createElement("td");
                q.innerHTML = realCraftQualif[metier+1][k].qualif.name;
                newTr.appendChild(q);
                for (var j = 0; j < 17; j++){
                    year = new Date().getFullYear();
                    if (j+firstWeek === year52_53(new Date())){
                        year++;
                    }
                    var td = document.createElement("td");
                    // Si le chantier est commencé, on affiche les input
                    if (!greyCaseBegin(firstWeek+j, year)){
                        var input = document.createElement("input");
                        input.style = "max-width:30px;";
                        input.className = j;
                        // Si le chantier est terminé, on affiche l'input mais on lui met une couleur grise
                        // pour signaler que normalement les chantier est terminé
                        if (greyCaseEnd(firstWeek+j, year)){
                            input.style.background = "#ededed";
                            td.style.background = "#ededed";
                        }
                        try{
                            // On complete les cases avec les bons needs
                            if (tabPhase[year][j+firstWeek][metier][realCraftQualif[metier+1][k].qualif.num]){
                                input.value = tabPhase[year][j+firstWeek][metier][realCraftQualif[metier+1][k].qualif.num];
                                valueCompute.push(j);
                            }
                        } catch (erreur){}
                        input.addEventListener('keydown', function(e) {copyValue(e);}, false);
                        input.addEventListener('change', function(e) {testIfNull(e.target); computeCraft(e.target.parentNode.parentNode, parseInt(e.target.className, 10));}, false);
                        td.appendChild(input);
                    } else {
                        // Sinon on grise les case et on ne met pas les input
                        td.style.background = "#ededed";
                    }
                    newTr.appendChild(td);
                }
                insertAfter(newTr, lignes[i].parentNode);
            }
            for (var l = 0; l < valueCompute.length; l++){
                computeCraft(lignes[i].parentNode, valueCompute[l]);
            }
            $('.qualif').hide();
        }
    }
}

function greyCaseBegin (weekNumber, year) {
    // si currSite est définit, on peut répondre
    if (typeof(currSite) != 'undefined'){
        return ((weekNumber < currSite.dateI.getWeekNumber() && year <= currSite.dateI.getFullYear() &&
            getMonthFromWeekNumber(weekNumber) <= currSite.dateI.getMonth()) || (year < currSite.dateI.getFullYear()));
    } else {
        return false;
    }
}

function greyCaseEnd (weekNumber, year) {
    // si currSite est définit, on peut répondre
    if (typeof(currSite) != 'undefined'){
        return ((weekNumber > currSite.dateE.getWeekNumber() && year >= currSite.dateE.getFullYear() &&
            getMonthFromWeekNumber(weekNumber) >= currSite.dateE.getMonth()) || (year > currSite.dateE.getFullYear()));
    } else {
        return false;
    }
}

/**
 * Fonction permettant d'ajouter les lignes des differentes qualif disponibles pour un craft
 */
 function addLineQualif(tr){
    var idCraft = parseInt(tr.firstChild.id, 10)+1;
    // On cache les lignes qualif si elles sont déjà affichées.
    $(".qualif").hide();
    $('tr').removeClass('redT');
	//$('tr').className += "greyT";
    tr.className += " redT";
    // Sinon, on reaffiche les qualif deja créées
    var tmp = tr;
    for (var i = 0; i < realCraftQualif[idCraft].length; i++){
        $(tmp).next().show();            
        tmp = tmp.nextSibling;
    }
 }

/**
 * Fonction permettant de faire la somme de chaque colonne du tableau pour les afficher dans la lignes 'Besoin'
 */
function computeNeed(week){
    var lignes = document.getElementsByClassName('metier');
    var res = 0;
    // On parcours les lignes du tableaux
    for (var m = 1; m < lignes.length; m++){
        try {
            if (lignes[m].parentNode.childNodes[week+1].innerHTML){
                res = res + parseInt(lignes[m].parentNode.childNodes[week+1].innerHTML, 10);
            }
        } catch(erreur) {}
    }
    lignes[0].parentNode.childNodes[week+1].innerHTML = res;
}

/**
 * Fonction permettant de faire la somme de chaque colonne du tableau pour les afficher dans le craft associé
 */
function computeCraft(target, week){
    // On remonte jusqu'à la ligne d'un craft
    while (target.firstChild.className !== "metier"){
        target = target.previousSibling;
    }
    var metier = parseInt(target.firstChild.id, 10)+1;
    // On parcours les lignes correspondant au qualif du craft
    var res = 0;
    var tmp = target;
    for (var m = 0; m < realCraftQualif[metier].length; m++){
        if (target.nextSibling.childNodes[week+1].lastChild.value){
            res = res + parseInt(target.nextSibling.childNodes[week+1].lastChild.value, 10);
        }
        target = target.nextSibling;
    }
    tmp.childNodes[week+1].innerHTML = res;
    computeNeed(week);
}

function testIfNull (target) {
    if (target.value == ''){
        target.value = 0;
    }
}

/**
 * Fonction qui copie la valeur de l'element el dans la case suivante lors de l'appuie sur la touche tab
 */
function copyValue(el) {
    var event;
    if (window.el)
        event = window.el;
	// --- Netscape and other explorers
    else {
        event =  el;
    }
    if (parseInt(event.keyCode, 10) == 9){
        if (el.target.value == ''){
            el.target.value = 0;
        }
        if (el.target.parentNode.nextSibling){
            el.target.parentNode.nextSibling.lastChild.value = el.target.value;
        }
        computeCraft(el.target.parentNode.nextSibling.parentNode, parseInt(el.target.parentNode.nextSibling.lastChild.className, 10));
        computeCraft(el.target.parentNode.parentNode, parseInt(el.target.parentNode.lastChild.className, 10));
    }
}

function insertAfter(newElement, afterElement) {
    var parent = afterElement.parentNode;
    
    if (parent.lastChild === afterElement) { // Si le dernier élément est le même que l'élément après lequel on veut insérer, il suffit de faire appendChild()
        parent.appendChild(newElement);
    } else { // Dans le cas contraire, on fait un insertBefore() sur l'élément suivant
        parent.insertBefore(newElement, afterElement.nextSibling);
    }
}