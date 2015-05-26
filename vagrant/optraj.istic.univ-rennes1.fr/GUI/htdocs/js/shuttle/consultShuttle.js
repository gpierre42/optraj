var allCar;
var currShuttle = [];

/**
appellée lors du chargement de la page
*/
(function() {
    //on récupère les navettes afin de construire la liste déroulante
    request("templates/proxy.php?url=http://localhost:5000/car/all/", follow); 
})();

function follow(xhr){
    var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
        // récupération de toutes les navettes 
        allCar = JSON.parse(resp["data"]); 
        for (var i in allCar){
			allCar[i].used = false; 
        }
	}

    // On trie les voitures par modèle
    allCar.sort(function(a,b){
        return a["model"].toUpperCase()>b["model"].toUpperCase();
    });

    // récupération du champs recherche pour ajouter le filtrage lors de la saisie d'une navette
    var search = document.getElementById('search');
    search.addEventListener("keyup", function(e) {filter(e.target, allCar, 'tab_Car');}, false);
    search.addEventListener("change", function(e) {filter(e.target, allCar, 'tab_Car');}, false);

    // on récupere les véhicules utilisé entre cette semaine et les quatres prochaines
    var today = new Date();
    var week = today.getWeekNumber();
    var year = today.getFullYear();
    var data = new FormData();
    data.append("data", "week="+week+"^year="+year);
    request("templates/proxy.php?url=http://localhost:5000/car/used/fromweek/", getUsedCar, data);
}

// fonction qui récupere les véhicules utilisés
function getUsedCar(xhr){
    var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
        usedCar = JSON.parse(resp["data"]);
    }
    

    // on marque les véhicules utilisé avec un booléen
    for (var i in usedCar){
        for (var j in allCar){
            if (usedCar[i].num == allCar[j].num){
                allCar[j].used = true;
            }
        }
    }

    // on affiche la liste
    showList(allCar, 'tab_Car');
}

/**
 * fonction qui affiche la liste des navettes passé en paramètre
 */
function showList(car, tabName){
    // on récupere le tableau qui va contenir toutes les navettes
    var table = document.getElementById(tabName);
    var curLetter = "";
    for(var i = 0; i < car.length; i++){
        // on récupere la premiere lettre de la navette pour faire l'affichage alphabetique
        var temp = car[i]["model"].substring(0,1).toUpperCase();
        // si c'est la premiere fois qu'on a une navette qui commence par la lettre temp, on l'ajoute
        if (curLetter !== temp){
            curLetter = temp;         
            var sep = document.createElement("tr");
            var sep1 = document.createElement("td");
            sep1.setAttribute('colspan', '3');
            sep1.className = "separation";
            sep1.innerHTML = curLetter;
            table.appendChild(sep);
            sep.appendChild(sep1);
        }
        // puis on ajoute le nom du véhicule dans la liste
        var tr = document.createElement("tr");
		
        if (car[i].used){
            tr.className = 'navetteLine used'; 
        } else {
            tr.className = 'navetteLine'; 
        }

        var td = document.createElement("td");
        var td1 = document.createElement("td");
        var td2 = document.createElement("td");
        td.innerHTML = car[i]["model"].charAt(0).toUpperCase() + car[i]["model"].substring(1).toLowerCase(); 
        td.className = 'navette';
        td1.innerHTML = car[i]["plate"];
        td1.className = 'navette';
        td2.innerHTML = car[i]["nbPlace"];  
        td2.className = 'navette';
        tr.id = i;
        tr.appendChild(td);
        tr.appendChild(td1);
        tr.appendChild(td2);
        table.appendChild(tr);
        // enfin, on ajoute l'évenement qui permet d'afficher les infos complémentaires lorsque l'on clique sur une navette
        tr.addEventListener("click",
            function(e) {
                setSession(car[e.target.parentNode.id]); window.location.href="index.php?choix=4";
            },
            true);
    } 
}
/**
 * fonction qui met en place les variables de session pour la page de consultation
 */
function setSession(car){
    localStorage.car = JSON.stringify(car);
}

/**
 * fonction qui permet de filtrer les navettes selon ce que l'on tape dans le champs de recherche (e)
 */
function filter(e, car, tabName){
    // On remplace le tableau des navettes par un nouveau tableau vierge
    var table = document.getElementById(tabName);
    var newTab = document.createElement('table');
    newTab.id = tabName;
    newTab.className = "table table-striped table-bordered table-hover";
    table.parentNode.replaceChild(newTab, table);
    // tableau qui contiendra toutes les navettes a afficher (par rapport au filtre)
    filterCar = [];
    for (var i = 0; i < car.length; i++){
        if( e.value==null || e.value==""){
            filterCar.push(car[i]);
        }
        // si le filtre est un sous-chaîne d'un nom d'un ouvrier, on l'ajoute aux ouvriers a afficher
        else{
            var motClef = "";
            if (car[i].used){
                motClef = "utilisée";
            }
            workerText = (car[i]["model"] + " " + car[i]["plate"] + " " + motClef).toLocaleLowerCase();
            var searchStrings = e.value.toLocaleLowerCase().split(" ");
            var allStrFound = true; 
            for(var j = 0; j<searchStrings.length && allStrFound; j++){//on vérifie tous les critères de recherche
                if(workerText.indexOf(searchStrings[j]) == -1){//on trouve la chaine quelque part dans le texte de la ligne
                    allStrFound = false; //un des critère de recherche n'est pas remplit
                }
            }
            if(allStrFound){
                filterCar.push(car[i]);
            }
        }
    }
    // puis on appel la fonction qui construit la liste des navettes
    showList(filterCar, tabName);
    // Changement de focus pour éviter le bug du double click après une recherche
    if (e.id == "search") {
        var temp = document.getElementById("test2");
    } else {
        var temp = document.getElementById("test");
    }
    temp.focus();
    e.focus();
}