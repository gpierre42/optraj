
(function() {
    //on récupère les admins afin de construire la liste déroulante
    request("templates/proxy.php?url=http://localhost:5000/user/all/", followUpList);
})();

/**
Construit la liste des utilisateurs
*/
function followUpList(xhr){
    var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return
    }
    // récupération de tous les admin
    var admins = JSON.parse(resp["data"])
    // récupération du champs recherche pour ajouter le filtrage lors de la saisie d'un admin
    var search = document.getElementById('search');
    search.addEventListener("keyup", function(e) {filter(e.target.value, admins);}, false);
    search.addEventListener("change", function(e) {filter(e.target.value, admins);}, false);
    if(admins != "undefined"){
            //trie par nom d'admin
            admins.sort(function(a,b){return a.name.toUpperCase()>b.name.toUpperCase()});
            showList(admins);
    }
    else{
            reportError("Une erreur est survenue lors de la récupération de la liste des utilisateurs.");
            return;
    }
}

/**
 * fonction qui affiche la liste des admins passé en paramètre
 */
function showList(admins){
    // on récupere le tableau qui va contenir tous les admins
    var table = document.getElementById('tab_admin');
    var curLetter = "";
    for(var i = 0; i < admins.length; i++){
        // on récupere la premiere lettre du admin pour faire l'affiche alphabetique
        var temp = admins[i].name.substring(0,1).toUpperCase();
        // si c'est la premiere fois qu'on a admin qui commence par la lettre temp, on l'ajoute
        if (curLetter !== temp){
            curLetter = temp;         
            var sep = document.createElement("tr");
            var sep1= document.createElement("td");
            sep1.setAttribute('colspan','2');
            sep1.className = "separation";
            sep1.innerHTML = curLetter;
            table.appendChild(sep);
            sep.appendChild(sep1);
        }

        // puis on ajoute le nom de l'admin dans la liste
        var lvlstring = lvlToString(admins[i].lvl);
        var tr = document.createElement("tr");
        tr.className  = 'rowConsult';
        var td = document.createElement("td");
        var td2 = document.createElement("td");
        td.innerHTML = admins[i].name.charAt(0).toUpperCase() + admins[i].name.substring(1).toLowerCase() + " " + admins[i].firstname.charAt(0).toUpperCase() + admins[i].firstname.substring(1).toLowerCase(); 
        td.className = 'admin rowElConsult';
        td.id = i;
        td.setAttribute('width','80%');
        td2.innerHTML = lvlstring;
        td2.className = 'rowElConsult';
        td2.id = i;
        tr.appendChild(td);
        tr.appendChild(td2);
        table.appendChild(tr);
		
        // enfin, on ajoute l'évenement qui permet d'afficher les infos complémentaires lorsque l'on clique sur un admin
        td.addEventListener("click", function(e) {setSession(admins[parseInt(e.target.id)]); window.location.href="index.php?choix=19";}, true);
    }
}

/*
établie la correspondance niveau d'administration <-> appellation du niveau
*/
function lvlToString(lvl){
	switch(lvl){
		case 1:
		return "Lecture et écriture";
		break;
		case 2:
		return "Lecture seule";
		break;
		case 3:
		return "Administration";
		break;
		default:
		return "pas normal";
		break;
		}
}

/**
 * fonction qui met en place les variables de session pour la page de consultation
 */
function setSession(admin){
    localStorage.admin = JSON.stringify(admin);
}

/**
 * fonction qui permet de filtrer les admins selon ce que l'on tape dans le champs de recherche (e)
 */
function filter(e, admins){
    // On remplace le tableau des admin par un nouveau tableau vierge
    var table = document.getElementById('tab_admin');
    var newTab = document.createElement('table');
    newTab.id = 'tab_admin';
    newTab.className = "table table-striped table-bordered table-hover";
    table.parentNode.replaceChild(newTab, table);
    // tableau qui contiendra tous les admin a afficher (par rapport au filtre)
    filteradmins = new Array();
    for (var i = 0; i < admins.length; i++){
        // si le filtre est un sous-chaîne d'un nom de admin, on l'ajoute au admin a afficher
        if (admins[i].name.toLowerCase().indexOf(e.toLowerCase()) !== -1 
            || admins[i].firstname.toLowerCase().indexOf(e.toLowerCase()) !== -1){
            filteradmins.push(admins[i]);
        }
    }
    // puis on appel la fonction qui construit la liste de admin
    showList(filteradmins);
    // Changement de focus pour éviter le bug du double click après une recherche
    document.getElementById('test').focus();
    document.getElementById('search').focus();
}