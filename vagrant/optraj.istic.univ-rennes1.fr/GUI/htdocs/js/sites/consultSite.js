/**
appellée lors du chargement de la page
*/
(function() {
    //on récupère les chantiers afin de construire la liste déroulante
    request("templates/proxy.php?url=http://localhost:5000/site/all/lazy/", followUpList);
})();

/**
appelé une fois la liste de chantiers récupérée
afin de construire la liste
*/
function followUpList(xhr){
    var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return
    }
    else{
        // récupération de tous les chantiers
        var sites = JSON.parse(resp["data"]);
        // récupération du champs recherche pour ajouter le filtrage lors de la saisie d'un chantier
        var search = document.getElementById('search');
        search.addEventListener("keyup", function(e) {filter(e.target.value, sites);}, false);
        search.addEventListener("change", function(e) {filter(e.target.value, sites);}, false);
        if(sites != "undefined"){
                //trie par numSite de chantier
                sites.sort(function(a,b){
                    var a = a.numSite;
                    var b = b.numSite;
                    if (a<b) return 1;
                    else if(a>b) return -1;
                    return 0;
                });
                showList(sites);
        }
        else{
                reportError('Une erreur est survenue lors de la récupération des chantiers.');
                return;
        }
    }
}

/**
 * fonction qui affiche la liste des sites passé en paramètre
 */
function showList(sites){
    // on récupere le tableau qui va contenir tous les sites
    var table = document.getElementById('tab_site');
    var curLetter = "";
    for(var i = 0; i < sites.length; i++){
        // on récupere la premiere lettre du chantier pour faire l'affiche alphabetique
        var temp = sites[i].numSite.toString().substring(0,2);
        // si c'est la premiere fois qu'on a chantier qui commence par la lettre temp, on l'ajoute
        if (curLetter !== temp){
            curLetter = temp;         
            var sep = document.createElement("tr");
            var sep1= document.createElement("td");
            sep1.setAttribute('colspan','3');
            sep1.className = "separation";
            sep1.innerHTML = "20"+curLetter;
            table.appendChild(sep);
            sep.appendChild(sep1);
        }
        // puis on ajoute le nom du chantier dans la liste
        var tr = document.createElement("tr");
        tr.className  = 'rowConsult';
        var td = document.createElement("td");
        var td1 = document.createElement("td");
        var tdcolor = document.createElement("td");
        td.innerHTML = sites[i].numSite; 
        td.className = 'rowElConsult';
        td.id = i;
        td.setAttribute('width','100px');
        td1.innerHTML = sites[i].name;
        td1.className = 'rowElConsult';
        td1.id = i;
        tdcolor.className ="rowElConsult";
        tdcolor.setAttribute('width', '20px');
        td1.setAttribute('style', 'padding-left:20px');
        tdcolor.setAttribute('bgcolor', sites[i].color);

        tr.appendChild(td);
        tr.appendChild(tdcolor);
        tr.appendChild(td1);
        table.appendChild(tr);
        // enfin, on ajoute l'évenement qui permet d'afficher les infos complémentaires lorsque l'on clique sur un chantier
        tr.addEventListener("click", function(e) {setSession(sites[parseInt(e.target.id)]); window.location.href="index.php?choix=10";}, true);
    }
    /*
    $(document).on('click', 'tr.rowConsult', function(event){
        setSession(sites[parseInt(event.target.id)]);
        window.location.href="index.php?choix=10";
    });*/
}

/**
 * fonction qui met en place les variables de session pour la page de consultation
 */
function setSession(site){
    localStorage.site = JSON.stringify(site);
}

/**
 * fontcion qui permet de filtrer les chantiers selon ce que l'on tape dans le champs de recherche (e)
 */
function filter(e, sites){
    // On remplace le tableau des chantier par un nouveau tableau vierge
    var table = document.getElementById('tab_site');
    var newTab = document.createElement('table');
    newTab.id = 'tab_site';
    newTab.className = "table table-bordered"
    table.parentNode.replaceChild(newTab, table);
    // tableau qui contiendra tous les chantier a afficher (par rapport au filtre)
    filterSites = new Array();
    for (var i = 0; i < sites.length; i++){
        if( e==null || e==""){
            filterSites.push(sites[i]);
        }
        // si le filtre est un sous-chaîne d'un nom d'un ouvrier, on l'ajoute aux ouvriers a afficher
        else{
            workerText = (sites[i].name + " " + sites[i].numSite).toLocaleLowerCase();
            var searchStrings = e.toLocaleLowerCase().split(" ");
            var allStrFound = true; 
            for(var j = 0; j<searchStrings.length && allStrFound; j++){//on vérifie tous les critères de recherche
                if(workerText.indexOf(searchStrings[j]) == -1){//on trouve la chaine quelque part dans le texte de la ligne
                    allStrFound = false; //un des critère de recherche n'est pas remplit
                }
            }
            if(allStrFound){
                filterSites.push(sites[i]);
            }
        }
    }
    // puis on appel la fonction qui construit la liste de chantier
    showList(filterSites);
    // Changement de focus pour éviter le bug du double click après une recherche
    document.getElementById('test').focus();
    document.getElementById('search').focus();
};