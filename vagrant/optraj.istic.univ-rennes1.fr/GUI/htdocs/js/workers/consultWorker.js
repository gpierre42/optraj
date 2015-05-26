/*
CHAPEL Guillaume
OPTRAJ
*/
/**
appellée lors du chargement de la page
*/
(function() {
    //on récupère les ouvriers afin de construire la liste déroulante
    request("templates/proxy.php?url=http://localhost:5000/worker/all/lazy/", followUpList);
})();

function followUpList(xhr){
    // récupération de tous les ouvrier
    var resp = JSON.parse(xhr.responseText)
    var workers = [];
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        workers = JSON.parse(resp["data"]);
    }
    // récupération du champs recherche pour ajouter le filtrage lors de la saisie d'un ouvrier
    var search = document.getElementById('search');
    search.addEventListener("keyup", function(e) {filter(e.target.value, workers);}, false);
    search.addEventListener("change", function(e) {filter(e.target.value, workers);}, false);
    if(workers != "undefined"){
            //trie par nom des ouvriers
            workers.sort(function(a,b){
                var a = a.name.toLowerCase();
                var b = b.name.toLowerCase();
                if (a<b) return -1;
                else if(a>b) return 1;
                return 0;
            });
            showList(workers);
    }
    else{
            reportError('Une erreur est survenue lors de la récupération des ouvriers.');
            return;
    }
}

/**
 * fonction qui affiche la liste des ouvriers passé en paramètre
 */
function showList(workers){
    // on récupere le tableau qui va contenir tous les ouvriers
    var table = document.getElementById('tab_site');
    var curLetter = "";
    for(var i = 0; i < workers.length; i++){
        // on récupere la premiere lettre de l'ouvrier pour faire l'affiche alphabetique
        var temp = workers[i].name.substring(0,1).toLowerCase();
        // si c'est la premiere fois qu'on a ouvrier qui commence par la lettre temp, on l'ajoute
        if (curLetter != temp){
            curLetter = temp;         
            var sep = document.createElement("tr");
            var sep1= document.createElement("td");
            sep1.setAttribute('colspan','4');
            sep1.className = "separation";
            sep1.innerHTML = curLetter.toUpperCase();
            // Suppression de la bordure inférieure
/*
            if (table.lastChild){
                table.lastChild.style = 'border-bottom: hidden';
            }
*/
            
            table.appendChild(sep);
            sep.appendChild(sep1);
        }
        // puis on ajoute le nom de l'ouvrier dans la liste
        var tr = document.createElement("tr");
        tr.className= 'rowConsult'
        var td = document.createElement("td");
        var td1 = document.createElement("td");
        var td2 = document.createElement("td");
        var td3 = document.createElement("td");
        td.innerHTML = workers[i].name.charAt(0).toUpperCase() + workers[i].name.substring(1).toLowerCase(); 
        td1.innerHTML = workers[i].firstName.charAt(0).toUpperCase() + workers[i].firstName.substring(1).toLowerCase(); 
        td2.innerHTML = workers[i].craft.name;
        td3.innerHTML = workers[i].qualification.name;
        td.className = 'rowElConsult';
        td.id = i;
        td1.className = 'rowElConsult';
        td1.id=i;
        td2.className = 'rowElConsult';
        td2.id=i;
        td3.className = 'rowElConsult';
        td3.id=i;
        tr.appendChild(td);
        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        table.appendChild(tr);
        // enfin, on ajoute l'évenement qui permet d'afficher les infos complémentaires lorsque l'on clique sur un ouvrier
        tr.addEventListener("click", function(e) {setSession(workers[parseInt(e.target.id)]); window.location.href="index.php?choix=8";}, true);
    }
    // suppression de la derniere bordure inférieure
    //table.lastChild.lastChild.style = 'border-bottom: hidden';
}

/**
 * fontcion qui permet de filtrer les ouvriers selon ce que l'on tape dans le champs de recherche (e)
 */
function filter(e, workers){
    // On remplace le tableau des ouvriers par un nouveau tableau vierge
    var table = document.getElementById('tab_site');
    var newTab = document.createElement('table');
    newTab.id = 'tab_site';
    newTab.className = "table table-bordered"
    table.parentNode.replaceChild(newTab, table);
    // tableau qui contiendra tous les ouvriers a afficher (par rapport au filtre)
    filterWorkers = new Array();
    for (var i = 0; i < workers.length; i++){
        if( e==null || e==""){
            filterWorkers.push(workers[i]);
        }
        // si le filtre est un sous-chaîne d'un nom d'un ouvrier, on l'ajoute aux ouvriers a afficher
        else{
            workerText = (workers[i].name + " " +
                            workers[i].qualification.name + " " +
                            workers[i].craft.name + " " +
                            workers[i].firstName).toLocaleLowerCase();
            var searchStrings = e.toLocaleLowerCase().split(" ");
            var allStrFound = true; 
            for(var j = 0; j<searchStrings.length && allStrFound; j++){//on vérifie tous les critères de recherche
                if(workerText.indexOf(searchStrings[j]) == -1){//on trouve la chaine quelque part dans le texte de la ligne
                    allStrFound = false; //un des critère de recherche n'est pas remplit
                }
            }
            if(allStrFound){
                filterWorkers.push(workers[i]);
            }
        }
    }
    // puis on appel la fonction qui construit la liste des ouvriers
    showList(filterWorkers);
    // Changement de focus pour éviter le bug du double click après une recherche
    document.getElementById('test').focus();
    document.getElementById('search').focus();
}

function setSession(worker){
    localStorage.worker = JSON.stringify(worker);
}