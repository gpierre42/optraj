/* 
 * Projet OPTRAJ
 * TIMELINE
 * Vigneron Jérémy
 */


/**Variables globales de la timeline
 */
var chantiers = [];
// Tableau contenant tous les mois de l'année
var months = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
// Tableau contenant tous les chantiers qui ne sont pas visible dans la timeline
var chantiersInvisible = [];
// Tableau contenant tous les chantiers visibles dans la timeline
var chantiersVisible = [];
// Entier représentant le nombre de mois affichés par la timeline
var nbMonth = parseInt(document.getElementById('nbMonth').value);
// valeur max prise par le nombre de mois a afficher
var max = parseInt(document.getElementById('nbMonth').max);
// valeur min prise par le nombre de mois a afficher
var min = parseInt(document.getElementById('nbMonth').min);
// Date correspondant à la date de début de la timeline
var debTime = new Date();
debTime = new Date(debTime.getFullYear(), debTime.getMonth(), debTime.getDate());
/**Cette fonction permet de trier les chantiers dans les deux tableaux visible et invisible.
 * 
 * @returns {refreshChantiers}
 */
function refreshChantiers(){
    // On initialise les tableaux
    chantiersVisible = [];
    chantiersInvisible = [];
    // On calcul le nombre de mois et d'année qui correspondent au nombre de mois affichés
    var nbmtemp = nbMonth % 12;
    var nbytemp = Math.floor(nbMonth / 12);
    // On construit la date de fin de timeline
    var finTime = new Date(debTime.getFullYear() + nbytemp, debTime.getMonth() + nbmtemp);
    
    // On parcours tout notre ensemble de chantier
    for (var i = 0; i < chantiers.length; i++){
        // On construit la date de début et de fin du chantier courant
        var debChant = new Date(parseInt(chantiers[i].dateInitY), parseInt(chantiers[i].dateInitM)-1);
        var endChant = new Date(parseInt(chantiers[i].dateEndY), parseInt(chantiers[i].dateEndM)-1, 30);
        // Si le chantier est en dehors de la timeline, on l'ajoute au chantiers invisibles
        if (endChant < debTime || debChant >= finTime){
            chantiersInvisible.push(chantiers[i]);
        }
        // Sinon, on le met dans la liste de ceux visibles
        else {
            chantiersVisible.push(chantiers[i]);
        }
    }
    chantiersVisible.sort(function(a,b){
        var a = a.numSite;
        var b = b.numSite;
        if (a<b) return 1;
        else if(a>b) return -1;
        return 0;
    });
}

/**Fonction qui retourne le nombre de jour de la date passé en paramètre
 * 
 * @param {type} date
 * @returns {Number}
 */
function getNbJours(date){
    return new Date(date.getFullYear(), date.getMonth()+1, -1).getDate()+1;
} 
 
/**Calcul la différence entre la date d1 et la date d2 en nombre de mois.
 * Le format des dates est d = (Year, month).
 * 
 * @param {type} d1
 * @param {type} d2
 * @returns {Number}
 */
function diffMonth(d1, d2){
    var months = (d1.getFullYear() - d2.getFullYear()) * 12;
    months -= d2.getMonth();
    months += d1.getMonth();
    return months;
}
 
/**C'est la fonction principale de ce code. Elle parcours le tableau des chantiers visibles construit précedement
 * et les met en place dans le code html avec les bonnes classes pour que l'affichage se fasse correctement.
 * 
 * @returns {undefined}
 */
function afficheVisible(){
    // On efface d'abord toutes les lignes du tableaux si il y en a
    var el = document.getElementById('body');
    while (el.firstChild){
        el.removeChild(el.firstChild);
    }

    // On parcours nos chantiers visibles
    for (var i = 0; i < chantiersVisible.length; i++){
        // Variable ou est stockée le chantier en cours de traitement
        var curSite = chantiersVisible[i];
        // On construit la date de début du chantier
        var initSite = new Date(parseInt(curSite.dateInitY), parseInt(curSite.dateInitM)-1);
        // On construit la date de fin du chantier
        var endSite = new Date(parseInt(curSite.dateEndY), parseInt(curSite.dateEndM)-1);
        // On calcul la durée du chantier
        var duree = diffMonth(endSite, initSite) + 1;
        
        // Création des éléments html necéssaires
        var tr = document.createElement('tr');
        var td = document.createElement('td');
        td.className = 'chantier';
        td.style.backgroundColor = curSite.color;
        var text = document.createTextNode(curSite.numSite);
        
        // Si le chantier démarre avant la date de début de timeline, on coupe le début
        if (debTime > initSite){
            td.className += ' cutBegin';
            // On calcule la différence entre le debut de timeline et le début de chantier
            var dif = diffMonth(debTime, initSite);
            // On regarde si le chantier ne déborde pas à droite (durée trop longue)
            if (duree > (nbMonth + dif)){
                // Si c'est le cas, on met cette durée au nombre de mois affichés
                duree = nbMonth;
                td.className += ' cutEnd';
            // Sinon, on soustrait seulement la différence calculée précedement à la durée du chantier
            } else {
                duree -= dif;
            }
            td.colSpan = duree;
        }
        // Sinon, le chantier démarre après le début de la timeline
        else {
            // On calcule la différence entre le debut de chantier et de timeline
            var dif = diffMonth(initSite, debTime);
            if (dif !== 0){
                // On crée l'élément qui sert à décaler le chantier au bon endroit dans la timeline
                var tdDec = document.createElement('td');
                tdDec.className = "decalage";
                tdDec.colSpan = dif;
                tr.appendChild(tdDec);
            }
            // Si la durée du chantier est supérieur au nombre de mois affichés moins la différence calculé avant,
            // le chantier sera coupé sur la fin
            if (duree > nbMonth - dif){
                // Mise à jour de la durée qui devient le nombre de mois affichés moins la différence calculée
                duree = nbMonth - dif;
                td.className += ' cutEnd';
            }
            // On affecte la durée calculé précedement
            td.colSpan = duree;
        }
        
        // On rajoute ces elements dans la page
        td.appendChild(text);
        tr.appendChild(td);
        var element = document.getElementById('body');
        element.appendChild(tr);
        // On leur rajoute les évenements permettant d'afficher et de cacher les infos supplémentaires
        addInfoChantier(td, i);
    }

    // On creer deux lignes en plus pour ne pas avoir des chantiers trop large
    el.appendChild(document.createElement('tr'));
    el.appendChild(document.createElement('tr'));
}

/**Cette fonction nous permet à partir d'un string correspondant à un mois de l'année, de nous retourner 
 * le mois suivant si bool est vrai le mois précedent sinon.
 * Pré-condition: le String passé en paramètre doit être dans la liste des mois.
 * 
 * @param {type} month
 * @param {type} bool
 * @returns {String}
 */
function nextMonth(month, bool){
    if (bool) {
        var res = "Février";
        for (var i = 0; i < months.length; i++){
            if (months[i] === month){
                res = months[(i+1)%12];
            }
        }
    } else {
        var res = "Décembre";
        for (var i = 0; i < months.length; i++){
            if (months[i] === month){
                res = months[(i+11)%12];
            }
        }
    }
    return res;
}

// Fonction qui trouve en fonction de la timeline et d'un booleen bool, l'année suivante à afficher si bool vaut vrai,
// l'année précédente si bool est a faux et la retourne sous forme d'élément HTMl em
function findNextYear(bool){
    if (bool){
        // On récupere la date courante
        var year = (debTime.getFullYear() + Math.floor(nbMonth / 12)) + 1;
    } else {
        var year = debTime.getFullYear();
    }
    // Affection de la nouvelle année dans un noeud texte
    var text = document.createTextNode(year);
    // Création du nouvel element em
    var em = document.createElement('em');
    // On lui remet une classe 'year' et on met l'année dedans
    em.className = 'year';
    em.appendChild(text);
    return em;
}

/**Fonction qui modifie le nombre de mois affichés sur la timeline. Elle prend en paramètre
 * nb correspond au décalage que l'on doit effectuer (-1 on ajoute un mois au début et 1 on en supprime un).
 * force est un booléen qui permet de forcé l'execution meme si on dépasse le nombre de mois maximum et minimum affichable
 *
 * @param {type} nb
 * @returns {undefined}
 */
function changeEndTime(nb, force) {
    // On test d'abord si nb est compris entre les valeurs min et max car sinon on ne peut pas traiter la demande
    var range = document.getElementById('nbMonth');
    // On récupere la ligne du bas du tableau
    var element = document.getElementById('tabFoot');
    // On récupere le texte du dernier mois affiché et on calcule le suivant
    var textMonth = months[(debTime.getMonth() + nbMonth)%12];
    // On augmente le nombre de mois a afficher
    if (nb == 1){
        if (force || (nb + nbMonth <= max)){
            // Création de notre nouvel élement
            var th = document.createElement('th');
            // Avec son texte correspondant
            var text = document.createTextNode(textMonth);
            // On modifie ce texte si c'est le mois de janvier que l'on souhaite afficher pour
            // mettre l'année à la place
            if (textMonth === "Janvier"){
                // Test pour savoir si on est en janvier car l'année a afficher sera l'année courante et non l'année suivante
                if (nbMonth == 0){
                    text = findNextYear(false);
                } else {
                    text = findNextYear(true);
                }
            }
            // On met ce nouveau noeud dans le document
            th.appendChild(text);
            element.appendChild(th);
            // Puis on met a jour le nombre de mois affiché
            nbMonth++;
            // On met a jour l'affichage des chantiers
            refreshChantiers();
            afficheVisible();
        }
    // Sinon, on diminue le nombre de mois à afficher
    } else if (nb == -1) {
        if (force || (nb + nbMonth >= min)){
            // On fait une copie de nbMonth car il va être modifié a chaque tour de boucle
            var nbMonthCopie = nbMonth;
            // On supprime le dernier noeud mois
            var el = element.lastElementChild;
            el.parentNode.removeChild(el);
            // On met a jour nbMonth
            nbMonth--;
            // Et on met a jour les chantiers à afficher
            refreshChantiers();
            afficheVisible();
        }
    }
    // Mise a jour de l'input range pour plus de sécurité mais aussi et surtout pour l'initialisation
    document.getElementById('nbMonth').value = nbMonth;
}

/**Fonction qui modifie la taille du tableau principal de la timeline lorsqu'on modifie la date de début de timeline.
 * nb correspond au décalage que l'on doit effectuer (-1 on ajoute un mois au début et 1 on en supprime un).
 * force est un booléen qui permet de forcé l'execution meme si on dépasse le nombre de mois maximum et minimum affichable
 * 
 * @param {type} nb
 * @param {type} b
 * @returns {undefined}
 */
function changeBeginTime(nb, force){
    // On récupere la ligne du bas du tableau
    var element = document.getElementById('tabFoot');
    // On récupere le texte du premier mois affiché et on calcule le précedent
    var textMonth = nextMonth(element.firstElementChild.textContent, false);
    // Si on viens d'augmenter le nombre de mois a afficher
    if (nb == -1){
        if (force || (nb + nbMonth <= max)){
            // Création de notre nouvel élement
            var th = document.createElement('th');
            // Avec son texte correspondant
            var text = document.createTextNode(textMonth);
            // On modifie ce texte si c'est le mois de janvier que l'on souhaite afficher pour
            // mettre l'année à la place
            if (textMonth === "Janvier"){
                //TODO
                text = findNextYear(false);
            }
            // On met ce nouveau noeud dans le document
            th.appendChild(text);
            element.insertBefore(th, element.firstChild);
            // On met a jour la date de debut de timeline
            debTime.setMonth(debTime.getMonth() - 1);
            debTime.setDate(1);
            // On met a jour nbMonth
            nbMonth++;
            document.getElementById('nbMonth').value = nbMonth;
            // On met a jour l'affichage des chantiers
            refreshChantiers();
            afficheVisible();
        }
    }
    // Sinon, on décrémente le nombre de mois a afficher
    else if (nb == 1) {
        if (force || (nb + nbMonth >= min)){
            // On supprime le dernier noeud mois
            var el = element.firstElementChild;
            el.parentNode.removeChild(el);
            // On met a jour la date de debut de timeline
            debTime.setMonth(debTime.getMonth() + 1);
            debTime.setDate(1);
            // On met a jour nbMonth
            nbMonth--;
            document.getElementById('nbMonth').value = nbMonth;
            // Et on met a jour les chantiers à afficher
            refreshChantiers();
            afficheVisible();
        }
    }
}

/** défini le début de la timeline sur aujourd'hui
*/
function resetStartingDate(){
	var actualDate = new Date(debTime);
	var newDate = new Date(Date.now());
	//alert("act =" + actualDate.getMonth() + "/" + actualDate.getFullYear());
	//alert("tod =" + newDate.getMonth() + "/" + newDate.getFullYear());
	var diff = diffMonth(actualDate, newDate);
	
    if (diff > 0){
        for (var i = 0; i < diff; i++){
           changeBeginTime(-1, true);
           //if(actualDate > newDate){diff = -diff;}
           changeEndTime(-1, true);
        }
    } else {
        for (var i = diff; i < 0; i++){
           changeBeginTime(1, true);
           //if(actualDate > newDate){diff = -diff;}
           changeEndTime(1, true);
        }
    }
}

/**Cette fonction affiche les information détaillées du chantier dans l'aside prévu à cet effet
 * Le paramètre de cette fonction est un élement html de classe chantier.
 * 
 * @param {type} e
 * @returns {undefined}
 */
function infoChantier(i){
    var chantier = chantiersVisible[i];
    var info = document.getElementById('info-timeline');
    var h4 = document.createElement('h4');
    var t = document.createTextNode('Informations du chantier '+chantier.numSite+' :');
    h4.appendChild(t);
    var p = document.createElement('p');
    var br = document.createElement('br');
    var br2 = document.createElement('br');    
    var t1 = document.createTextNode(chantier.name);
    var t2 = document.createTextNode("Début du chantier: "+chantier.dateInitM+"/"+chantier.dateInitY);
    var t3 = document.createTextNode("Fin du chantier: "+chantier.dateEndM+"/"+chantier.dateEndY);
    var t4;
    if(chantier.position.address == "None"){
        t4 = document.createTextNode(chantier.position.latitude + ";" + chantier.position.longitude);
    }  
    else{
        t4 = document.createTextNode(chantier.position.address);
    }
    p.appendChild(t1);
    p.appendChild(br);
    p.appendChild(t2);
    p.appendChild(br2);
    p.appendChild(t3);
    p.appendChild(document.createElement('br'));
    p.appendChild(t4);
    info.appendChild(h4);
    info.appendChild(p);
}

/**Fonction qui supprime les infos supplémentaires du chantier contenu
 * 
 * @returns {undefined}
 */
function cacheInfo(){
    var info = document.getElementById('info-timeline');
    while (info.hasChildNodes()){
        info.removeChild(info.lastChild);
    }
}

/**Fonction qui ajoute les évenements à tous les chantiers visibles pour permettre d'afficher les infos supplémentaires
 * 
 * @returns {addInfoChantier}
 */
function addInfoChantier(elt, i){
    elt.onmouseover = function(){
        infoChantier(i);
    };
    elt.onmouseout = function(){
        cacheInfo();
    }
    elt.onclick = function(){
        localStorage.site = JSON.stringify(chantiersVisible[i]);
        window.location.href="index.php?choix=10";
    }
}

function main(xhr){
    var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return
    }
    else{
        chantiers =  JSON.parse(resp["data"]);
        refreshChantiers();
        afficheVisible();
    }
}

/**
 * Cette fonction est executée a chaque fois qu'on charge la page. Elle permet d'ajouter les évenements
 * sur les élements html et fait une première initialisation des variables globales du programme
 * 
 * @returns {undefined}
 */
(function() {
    request("templates/proxy.php?url=http://localhost:5000/site/all/lazyPosition/", main);
    for (var i = 0; i < 8; i++) {
        changeEndTime(1, false);
    }
    var element = document.getElementById('nbMonth');
    // On ajoute l'évenement à l'input de type range
    element.onchange = function(){
        changeEndTime(parseInt(this.value)-nbMonth);
    };
    // Puis au deux bouttons qui modifie le début de la timeline
    element = document.getElementById('buttonMoins');
    element.onclick = function(){
        changeBeginTime(1, true);
        changeEndTime(1, true);
    };
    element = document.getElementById('buttonPlus');
    element.onclick = function(){
        changeBeginTime(-1, true);
        changeEndTime(-1, true);
    };
    // Ajout de l'évenement sur le bouton 'Ce mois-ci'
    element = document.getElementById('curMonth');
    var date = new Date();
    var month = date.getMonth();
    element.onclick = function(){
    resetStartingDate();
    }; 
})();

jQuery("document").ready(function($){
    //Permet d'avoir comme un input type "number" avec un type "text" pour bootstrap
    $("input[name='number']").TouchSpin({
    });
    
    //rend le header flottant
    $('#table').floatThead({
        scrollingTop: 0,
        useAbsolutePositioning:false
    });

    /*
    var foot = $('#foot');

    var myTop = $("#foot").offset().top;
    var myBottom = myTop + $("#foot").outerHeight();
    var viewportBottom = $(window).height() + $(window).scrollTop();
    var vdist = viewportBottom - myBottom;
    console.log("vdist", vdist);
    console.log("myBottom", myBottom);
    console.log("fenetre", $(window).height())

    $(window).scroll(function () {
        var myTop = $("#foot").offset().top;
        var myBottom = myTop + $("#foot").outerHeight();
        var viewportBottom = $(window).height() + $(window).scrollTop();
        var vdist = viewportBottom - myBottom;
        console.log("vdist", vdist);
        console.log("myBottom", myBottom);
        console.log("fenetre", $(window).height())
        if(vdist<0){            
            $('#foot').css("position","fixed");
            $('#foot').css("bottom","0px");
        }
    });*/
    

});