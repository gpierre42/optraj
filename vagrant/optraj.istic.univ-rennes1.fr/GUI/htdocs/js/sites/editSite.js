//Jérémy vigneron

var currSite = {};
var clickedOnMap = false;
(function() {    
    $('#colorPicker').hide();

    //on récupère les chantiers afin de construire la liste déroulante
    var site = JSON.parse(localStorage.site);
    var dataSite = new FormData();
    dataSite.append('data', 'num='+site.num);
    request("templates/proxy.php?url=http://localhost:5000/site/byid/", followUp, dataSite);
    $('#colorPicker').attr('data-color',site.color);
})();

//cache le corps de la page pour afficher une grande carte
function expandMap(){
    var buttonReduce = "<div id='cReduce'>" +
                            "<button type='button' class='btn btn-primary' " +
                            "data-container='body' data-placement='right' " +
                            "onclick='reduceMap();'>Réduire la carte</button>" +
                        "</div>";
    $(".panel-heading .row").append(buttonReduce);
    var bigMapDiv = "<table id='tabShuttle'>" +
                        "<thead class='thead'>" +
                            "<tr id='tabShuttle_head_0'>" +              
                            "</tr>" +
                            "<tr id='tabShuttle_head_1' class='months'>" +
                            "</tr>" +
                            "<tr id='tabShuttle_head_2' class='weekNumber'></tr>" +
                        "</thead>" +
                    "</table>" +
                    "<div id='bigMapDiv' style='background-color:#f5f5f5;'>"+
                        "<div id='bigMap' style='width:100%;height:"+$(window).height()+"px;position:relative;'></div>"+
                    "</div>";
    $("#panel1").fadeOut(600);
    $(".panel-heading").after(bigMapDiv);
    
    $("#expandMap").hide();
    $('#bigMapDiv').hide();

    var now = new Date();
    initHeader(now, 17, "tabShuttle", false, changeWeek);
    selectOne("tabShuttle", now.getWeekNumber());
	$('#bigMapDiv').show(600, function(){
		loadBigMap();
	});
}

//cache la grande carte et réaffiche le corps de page standard
function reduceMap(){
    charCountPickup = 1;
    charCountShuttle = 1;
    $("#modPickup").remove();
    $("#cReduce").remove();
    $('#tabShuttle').remove();
    $("#expandMap").show();
    $("#bigMapDiv").hide(600, function(){
        $(this).remove();
	});
    $("#panel1").fadeIn(200, function(){
        $(this).show();
    });
}

function followUp(xhr) {
    var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
        //On créer les variables en rapport au chantier que l'on édite
        var site = JSON.parse(resp["data"]);
        
        currSite.numSite=site.numSite;
        currSite.name = site.name;
        currSite.phases = site.phases;
        currSite.latitude = site.position.latitude;
        currSite.longitude = site.position.longitude;
        currSite.address = site.position.address;
        currSite.siteMaster = site.siteMaster;
        currSite.siteManager = site.siteManager;
        currSite.num = site.num;
        currSite.color = site.color;
        currSite.dateInit = site.dateInitD+"/"+site.dateInitM+"/"+site.dateInitY;
        currSite.dateI = new Date(site.dateInitY, site.dateInitM-1, site.dateInitD);
        currSite.dateEnd = site.dateEndD+"/"+site.dateEndM+"/"+site.dateEndY;
        currSite.dateE = new Date(site.dateEndY, site.dateEndM-1, site.dateEndD);

        loadForm();
    }
}

/**
affiche le formulaire avec les informations liées à un chantier
*/
function loadForm(){
    // Récupération de toutes les infos d'un chantier
    var numSite = currSite.numSite;
    var name = currSite.name;
    var dateInit = currSite.dateInit;	
    var dateEnd = currSite.dateEnd;
    var siteMaster = currSite.siteMaster;
    var siteManager = currSite.siteManager;
    var address = currSite.address;
    var color = currSite.color;

    //remplissage du formulaire avec les valeurs récupérées
    var numS = document.getElementById('numSite');
    numS.innerHTML = numSite;
    numS.addEventListener('click', function(e) {modifInput(e.target);}, false);

    var ad = document.getElementById('address');
    ad.innerHTML = address;
    ad.addEventListener('click', function(e) {modifInput(e.target);}, false);

    var n = document.getElementById('name');
    n.innerHTML = name;
    n.addEventListener('click', function(e) {modifInput(e.target);}, false);

    var dI = document.getElementById('dateInit');
    dI.innerHTML = dateInit;
    dI.addEventListener('click', function(e) {modifInput(e.target);}, false);

    var dE = document.getElementById('dateEnd');
    dE.innerHTML = dateEnd;
    dE.addEventListener('click', function(e) {modifInput(e.target);}, false);

    var siteMast = document.getElementById('siteMaster');
    siteMast.innerHTML = siteMaster;
    siteMast.addEventListener('click', function(e) {modifInput(e.target);}, false);
    
    var siteMana = document.getElementById('siteManager');
    siteMana.innerHTML = siteManager;
    siteMana.addEventListener('click', function(e) {modifInput(e.target);}, false);

    var colorTD = document.getElementById('colorPick');
    colorTD.value=color.slice(1,7).toUpperCase();
    colorTD.style.backgroundColor=color;
    colorTD.addEventListener('click', function(e) {modifInput(e.target);}, false);

    // On cache les boutons de modif, suppression et verification
    $('.validation').hide();
    drawMap("map");
}
function found(address){
    console.log(address);
    $('#cAddress').addClass('disabled');
    $('#address').val(address);
    clickedOnMap = true;

}
function notFound(lat,long){
    $('#cAddress').addClass('disabled');
    $('#address').val("");
    console.log("cette position n'a pas d'adresse mais on enregistre");
    clickedOnMap = true;
}

function allowClick(funcFound, funcFail) {
    google.maps.event.addListener(map, 'click', function(event) {
        var latitude = event.latLng.lat();
        var longitude = event.latLng.lng();
        var point = new google.maps.LatLng(latitude,longitude);
        //efface le marqueur s'il existe
        if (!currSite.marker) {
            currSite.marker = new google.maps.Marker({
                position: point,
                map: map
            });
            
        } else {
            currSite.marker.setPosition(point);
        }
        getAddress(latitude, longitude, funcFound, funcFail);
    });
}

/**
 * Fonction qui permet d'afficher le formulaire de modification d'un chantier lorsque l'on clique sur un champs
 */
function modifInput(el){

    // test qui permet de determiner si les inputs sont déja affiché
    if (document.getElementsByClassName('form') != null && (sessionStorage.lvladminreq == 1 || sessionStorage.lvladminreq == 3)){
        allowClick(found,notFound);

        // On récupere les elements du formulaire
        children = document.getElementsByClassName('form');
        // Et on les parcourt en créant pour chaque enfant, un input avec la valeur associée
        while (children.length){
            var input = document.createElement('input');
            if(children[0].id != "color" && children[0].id != "dateInit" && children[0].id != "dateEnd"){
                input.className = 'form-control';
                input.name = children[0].id;
                input.id = children[0].id;
                input.required = true;
                input.value = children[0].innerHTML;
                children[0].parentNode.appendChild(input);
                
                 // Si l'enfant est l'élement que l'on a cliqué, on lui donne le focus
                if (el === children[0]){
                    children[0].parentNode.lastChild.focus();
                    children[0].parentNode.lastChild.select();
                }
                children[0].parentNode.removeChild(children[0]);

            }
            else if(children[0].id == "color"){
                $('#colorPick').hide();
                $('#colorPicker').show();

                 // Si l'enfant est l'élement que l'on a cliqué, on lui donne le focus
                if (el === children[0]){
                    children[0].parentNode.lastChild.focus();
                    children[0].parentNode.lastChild.select();
                }
                children[0].parentNode.removeChild(children[0]);
            }
            else if(children[0].id == "dateInit"){

                $('#dateInit').replaceWith('<div class="input-group date" id="datetimepickerD"><input class="form-control" name="dateInit" required data-format="DD/MM/YYYY" placeholder="jj/mm/aaaa" value="'+children[0].innerHTML+'" /><span class="input-group-addon"><span class="fa fa-calendar"></span></span></div>');
                $(function () {
                    $('#datetimepickerD').datetimepicker({
                        language: 'fr',
                        pickTime: false
                    });
                });

            }
            else{

                $('#dateEnd').replaceWith('<div class="input-group date" id="datetimepickerF"><input class="form-control" name="dateEnd" required data-format="DD/MM/YYYY" placeholder="jj/mm/aaaa" value="'+children[0].innerHTML+'" /><span class="input-group-addon"><span class="fa fa-calendar"></span></span></div>');
                $(function () {
                    $('#datetimepickerF').datetimepicker({
                        language: 'fr',
                        pickTime: false
                    });
                });

            }
            
           

        }
        $('#address').keyup(function () { clickedOnMap = false;
                                          $('#cAddress').removeClass('disabled');
                                        }); 
        $('#cAddress').removeClass('disabled');
        $('#cValid').removeClass('disabled');
		$('#cSuppr').removeClass('disabled');
    }
}

/**
appellée lors de l'appui sur "valider"
*/
function editSite(){
    if(clickedOnMap){
        followUpEdition(currSite.marker.position.lat(),currSite.marker.position.lng());
    }else{
        var address = $('#form input[name="address"]').val();
        codeAddress(address, followUpEdition, addressFail);
    }
    
}

/**
appelée lors de l'appui sur "supprimer"
*/
function deleteSite(){
    var idToDelete = currSite.num;
    var data = new FormData();
    data.append('data', 'num='+idToDelete);
    $("#supprModal").modal('hide');
    setTimeout(function(){request("templates/proxy.php?url=http://localhost:5000/site/delete/", editionOk, data)},50);
}

/**
appelée une fois la résolution d'adresse terminée
*/
function followUpEdition(latitude, longitude){
    // Id du chantier que l'on souhaite modifier pour la requete
    var name = $('#form input[name="name"]').val();
    var dateInit = $('#form input[name="dateInit"]').val();
    var dateEnd = $('#form input[name="dateEnd"]').val();
    var numSite = $('#form input[name="numSite"]').val();
    var siteMaster = $('#form input[name="siteMaster"]').val();
    var siteManager = $('#form input[name="siteManager"]').val();
    var address = $('#form input[name="address"]').val();
    var firstWeek = parseInt(document.getElementById('tabWeek_head_2').firstChild.innerHTML, 10);
    var metiers = document.getElementsByClassName('metier');
    var phases = currSite.phases;
    var numNewPhase = -1;
    var numNewNeed = 0;
    var needs;
    var need;
    // On parcours les différentes lignes du tableau
    for (var m = 1; m < metiers.length; m++){
        needs = metiers[m].parentNode.childNodes;
        // Puis toutes les cases de chaques lignes
        for (var i = 1; i < 18; i++){
            var year = new Date().getFullYear();
            if (i + firstWeek === year52_53(new Date())){
                year++;
            }
            // Si la case a une valeur, on doit l'envoyer
            if (needs[i].innerHTML){
                // On peut seulement créer 17 nouvelles phases, donc on initialise a un nombre plus petit pour
                // ne pas etre en conflit avec les possible valeurs des nouvelles phases déjà créées
                var idPhase = -10000;
                // On cherche ensuite la phase modifiée
                if (phases[year] && phases[year][parseInt(i+firstWeek-1, 10)]){
                    idPhase = [year, parseInt(i+firstWeek-1, 10)];
                }
                for (var y in phases){
                    for (var temp = numNewPhase; temp > 0; temp++){
                        if (phases[y][temp]["numWeek"] == parseInt(i+firstWeek-1, 10) && y == year){
                            idPhase = [y, temp];
                        }
                    }
                }
                // Si idPhase est a -10000, c'est qu'il faut créer une nouvelle phase
                if (idPhase == -10000){
                    idPhase = [year, numNewPhase];
                    if (!phases[idPhase[0]]){
                        phases[idPhase[0]] = {};
                    }
                    phases[idPhase[0]][idPhase[1]] = {'numWeek': parseInt(i+firstWeek-1, 10), 'numYear': year, 'needs': {}};
                    numNewPhase--;
                }
                // On parcours maintenant toutes les qualif pour cette phase courante
                var qualification = document.getElementsByClassName("qualif"+metiers[m].id);
                for (var n = 0; n < qualification.length; n++){
                    // On regarde si on a une valeur dans la case
                    if (qualification[n].childNodes[i].lastChild.value){
                        var idNeed = -1;
                        // On cherche le need modifié
                        for (var ne in phases[idPhase[0]][idPhase[1]]['needs']){
                            if (phases[idPhase[0]][idPhase[1]]['needs'][ne]['craft']['num'] == metiers[m].id &&
                                phases[idPhase[0]][idPhase[1]]['needs'][ne]['qualification']['name'] == qualification[n].childNodes[0].innerHTML){
                                idNeed = ne;
                            }
                        }
                        // Si idNeed est à -1, c'est qu'il faut créer un nouveau need
                        if (idNeed == -1){
                            idNeed = idNeed - numNewNeed;
                            numNewNeed++;
                            need = {'need': parseInt(qualification[n].childNodes[i].lastChild.value, 10),
                                    'craft': {'num':metiers[m].id},
                                    'qualification': {'name':qualification[n].childNodes[0].innerHTML}};
                            phases[idPhase[0]][idPhase[1]]['needs'][idNeed] = need;
                        // Sinon on met a jour la valeur
                        } else {
                            phases[idPhase[0]][idPhase[1]]['needs'][idNeed]['need'] = parseInt(qualification[n].childNodes[i].lastChild.value, 10);
                        }
                    }
                }
            }
        }
    }
    console.log(phases);
    if(numSite==""){
			$('#formNum').removeClass('has-success');
			$('#formNum').addClass('has-error');
			$('#cValid').attr("data-content","Le champ \'Numéro\' n'est pas rempli");
			$('#cValid').popover('show');
			setTimeout(function(){$('#cValid').popover('destroy');},2000);
            return;
	}
	else if(name == ""){
			$('#formNum').removeClass('has-error');
			$('#formNum').addClass('has-success');
			$('#formNom').removeClass('has-success');
			$('#formNom').addClass('has-error');
			$('#cValid').attr("data-content","Le champ \'Nom\' n'est pas rempli");
			$('#cValid').popover('show');
			setTimeout(function(){$('#cValid').popover('destroy');},2000);
            return;
	}
	else if(!checkDate(dateInit)){
			$('#formNum').removeClass('has-error');
			$('#formNum').addClass('has-success');
			$('#formNom').removeClass('has-error');
			$('#formNom').addClass('has-success');
			$('#formDateD').removeClass('has-success');
			$('#formDateD').addClass('has-error');
			$('#cValid').attr("data-content","Le champ \'Date de début\' n'est pas valide");
			$('#cValid').popover('show');
			setTimeout(function(){$('#cValid').popover('destroy');},2000);
			return;
	}
	else if(!checkDate(dateEnd)){
			$('#formNum').removeClass('has-error');
			$('#formNum').addClass('has-success');
			$('#formNom').removeClass('has-error');
			$('#formNom').addClass('has-success');
			$('#formDateD').removeClass('has-error');
			$('#formDateD').addClass('has-success');
			$('#formDateF').removeClass('has-success');
			$('#formDateF').addClass('has-error');
			$('#cValid').attr("data-content","Le champ \'Date de fin\' n'est pas valide");
			$('#cValid').popover('show');
			setTimeout(function(){$('#cValid').popover('destroy');},2000);
			return;
	}
	else if(siteMaster==""){
			$('#formNum').removeClass('has-error');
			$('#formNum').addClass('has-success');
			$('#formNom').removeClass('has-error');
			$('#formNom').addClass('has-success');
			$('#formDateD').removeClass('has-error');
			$('#formDateD').addClass('has-success');
			$('#formDateF').removeClass('has-error');
			$('#formDateF').addClass('has-success');
			$('#formChefC').removeClass('has-success');
			$('#formChefC').addClass('has-error');
			$('#cValid').attr("data-content","Le champ \'Chef de Chantier\' n'est pas rempli");
			$('#cValid').popover('show');
			setTimeout(function(){$('#cValid').popover('destroy');},2000);
			return;
	}else if(siteManager==""){
			$('#formNum').removeClass('has-error');
			$('#formNum').addClass('has-success');
			$('#formNom').removeClass('has-error');
			$('#formNom').addClass('has-success');
			$('#formDateD').removeClass('has-error');
			$('#formDateD').addClass('has-success');
			$('#formDateF').removeClass('has-error');
			$('#formDateF').addClass('has-success');
			$('#formChefC').removeClass('has-error');
			$('#formChefC').addClass('has-success');
			$('#formCondT').removeClass('has-success');
			$('#formCondT').addClass('has-error');
			$('#cValid').attr("data-content","Le champ \'Conducteur de travaux\' n'est pas rempli");
			$('#cValid').popover('show');
			setTimeout(function(){$('#cValid').popover('destroy');},2000);
			return;
	}


    var s = 'name='+name+
            '^num='+currSite.num+
            '^numSite='+numSite+
            '^siteMaster='+siteMaster+
            '^siteManager='+siteManager+
            '^dateInit='+dateInit+
            '^dateEnd='+dateEnd+
            '^latitude='+latitude+
            '^longitude='+longitude+
            '^address='+address+
            '^phases='+JSON.stringify(phases)+
            '^color='+document.getElementById('colorPicker').value;

    var data = new FormData();
    data.append('data', s);
    
    $('#formNum').removeClass('has-error');
	$('#formNum').addClass('has-success');
	$('#formNom').removeClass('has-error');
	$('#formNom').addClass('has-success');
	$('#formDateD').removeClass('has-error');
	$('#formDateD').addClass('has-success');
	$('#formDateF').removeClass('has-error');
	$('#formDateF').addClass('has-success');
	$('#formChefC').removeClass('has-error');
	$('#formChefC').addClass('has-success');
    $('#formCondT').removeClass('has-error');
	$('#formCondT').addClass('has-success');
	
	request("templates/proxy.php?url=http://localhost:5000/site/update/", editionOk, data);
}

/**
appelée une fois l'édition terminée
*/
function editionOk(xhr){
    var resp = JSON.parse(xhr.responseText);
    localStorage.clear();
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
        reportSuccess(resp["message"], null, "index.php?choix=12");
    }
}


/**
appellée lors de l'appui sur "valider adresse"
*/
function checkAddress(){
    var address = $('#form input[name="address"]').val();
    codeAddress(address, addressOK, addressFail);
}

function addressOK(latitude, longitude){
    document.getElementById("address").style.backgroundColor = 'rgb(117,254,98)';
	document.getElementById("address").style.color="black";
    showPosition(latitude, longitude);
}

/**
appelé si la résolution d'adresse à échouée
*/
function addressFail(address){
	$('#cAddress').attr("data-content", address ? "L'adresse semble incorrecte : "+address : "Champ \'adresse\' vide");
	$('#cAddress').popover('show');
	setTimeout(function(){$('#cAddress').popover('destroy');},2000);
	setTimeout(function(){$('#cValid').popover('destroy');},2000);
	document.getElementById("address").style.backgroundColor = 'rgb(254,50,50)';
	document.getElementById("address").style.color="white";
}
