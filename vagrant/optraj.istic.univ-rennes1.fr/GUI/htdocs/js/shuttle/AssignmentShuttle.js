(function() {
	//on récupère les chantiers afin de construire la liste déroulante
    request("templates/proxy.php?url=http://localhost:5000/craft/all/", createTab);
})();

/**
 * Fonction qui créer le tableau des différentes semaine d'un chantier
 */
function createTab(xhr) {
    // récupération de tout les métiers disponible en BDD et ajout de la case "Besoin" en premier ligne
    var resp = JSON.parse(xhr.responseText)
    var metiers = [];
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        metiers = JSON.parse(resp["data"]);
    }
    metiers.sort(function(a,b){return a.num>b.num})
    metiers.unshift({'name': "Besoins", 'num': -1});
    
    // Création du tableau des différentes semaines d'un chantier
    var firstLine = document.getElementById("firstLine");
    var week = parseInt(document.getElementById("firstWeek").innerHTML)+1;
    for (var i = 0; i < 15; i++){
        th = document.createElement("th");
        th.innerHTML = week;
        firstLine.appendChild(th);
        week++;
    }

    // Création de la premiere colonne du tableau (metiers)
    var tab = document.getElementById('tabWeek');
    var tr, td;
    for (var i = 0; i < metiers.length; i++){
        tr = document.createElement('tr');
        td = document.createElement('td');
        td.innerHTML = metiers[i]['name'];
        td.id = metiers[i]['num'];
        td.className = "metier";
        tr.appendChild(td);
        tab.appendChild(tr);
    }

    // Affichage des phases du chantier courant si on est dans le cas de l'édition d'un chantier
    if('function' == typeof(showNeed)){
			showNeed();
	}
}

/**
 * Cette fonction remplie le tableau avec le nombre de worker demandé dans une phase pour le chantier courant.
 */
function showNeed(){
    // Si la variable currSite n'est pas définie c'est que l'on est dans la page de création d'un chantier
    // donc on n'as pas besoin d'afficher les données des phases en base puisqu'il n'y en a pas
	if (typeof(currSite) != 'undefined'){
    	var phases = currSite.phases;
    } else {
    	phases = {};
    }
    var tabPhase = {};
    var dictPhase = {};
    var dictMonth = {};
    var year = new Date().getFullYear();
    
    // Premiere étapes, création d'un dico contenant tous les besoins du chantier courant
    for (var i in phases) {
        dictPhase = {};
        temp = phases[i];
        for (var j in temp['needs']){
            dictPhase[temp['needs'][j]['craft']['name']] = temp['needs'][j]['need'];
            dictMonth[temp['numWeek']] = dictPhase;
            tabPhase[temp['numYear']] = dictMonth;
        }
    }

    // Puis on peut commencer a remplir le tableau avec les données recupérées
    var firstWeek = parseInt(document.getElementById('firstWeek').innerHTML);
    var lignes = document.getElementsByClassName('metier');
    var metier, td, input;
    var year = new Date().getFullYear();
    // On parcours toute les lignes du tableaux
    for (var i = 0; i < lignes.length; i++){
        metier = lignes[i].innerHTML;
        // Puis toute les cases d'une lignes
        for (var j = 0; j < 16; j++){
            td = document.createElement('td');
            input = document.createElement('input');
            input.type = 'number';
            input.style = "max-width:30px;";
            input.className = j;
            input.addEventListener('keydown', function(e) {copyValue(e);}, false);
            input.addEventListener('change', function(e) {computeNeed(parseInt(e.target.className)), false});
			if (typeof(currSite) != 'undefined'){
            	input.addEventListener('click', function(e) {modifInput(e.target);}, false);
            }
            // Pour les ligne des besoins on a rien a faire pour le moment, on complete seulement les autres
            if (metier !== 'Besoin'){
                if (j+firstWeek === 52){
                    year++;
                }
                try{
                    if (tabPhase[year][j+firstWeek][metier]){
                        input.value = tabPhase[year][j+firstWeek][metier];
                    }
                } catch (erreur){}
                td.appendChild(input);
            }
            lignes[i].parentNode.appendChild(td)
            // Enfin on calcul les needs pour chaque semaine
            if (i === lignes.length-1){
                computeNeed(j);
            }
        }
    }
}

/**
 * Fonction permettant de faire la somme de chaque colonne du tableau pour les afficher dans la lignes 'Besoin'
 */
function computeNeed(week){
    var lignes = document.getElementsByClassName('metier');
    var temp = 0;
    var res = 0;
    // On parcours les lignes du tableaux
    for (var m = 1; m < lignes.length; m++){
        if (lignes[m].parentNode.childNodes[week+1].lastChild.value){
            res = res + parseInt(lignes[m].parentNode.childNodes[week+1].lastChild.value);
        }
    }
    lignes[0].parentNode.childNodes[week+1].innerHTML = res;
}

/**
 * Fonction qui copie la valeur de l'element el dans la case suivante lors de l'appuie sur la touche tab
 */
function copyValue(el) {
    if (window.el)
	var event = window.el;
	// --- Netscape and other explorers
    else {
        var event =  el;
    }
    if (el.target.parentNode.previousSibling.lastChild.value && parseInt(event.keyCode) == 9 && el.target.value == ""){
        el.target.value = el.target.parentNode.previousSibling.lastChild.value;
        el.target.select();
        computeNeed(parseInt(el.target.parentNode.lastChild.className));
    }
}