/*
CHAPEL Guillaume
OPTRAJ
*/

/**
appellée lors du chargement de la page
*/
var worker={};
var clickedOnMap = false;
(function() {
    //$('.validation').hide();
    workerJSON = JSON.parse(localStorage.worker);
    var data = new FormData();
    
    data.append('data', 'num='+workerJSON.num);
    request("templates/proxy.php?url=http://localhost:5000/worker/byid/", followWorker, data);
    
   
})();

function followWorker(xhr) {
    var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        //On créer les variables en rapport à l'ouvrier que l'on édite
        var workerJSON = JSON.parse(resp["data"]);
        worker.name = workerJSON.name;
        worker.firstName = workerJSON.firstName;
        worker.position={};
        worker.position.latitude = workerJSON.position.latitude;
        worker.position.longitude = workerJSON.position.longitude;
        worker.position.address = workerJSON.position.address;
        worker.num = workerJSON.num;
        worker.birthdate = workerJSON.birthdateD+"/"+workerJSON.birthdateM+"/"+workerJSON.birthdateY;
        worker.craft = workerJSON.craft;
        worker.qualification = workerJSON.qualification;
        workerJSON = JSON.parse(localStorage.worker);
        var today = new Date();
        var data = new FormData();
        data.append('data', 'num='+workerJSON.num+'^week='+today.getWeekNumber()+'^year='+today.getFullYear());
        request("templates/proxy.php?url=http://localhost:5000/assignment/byworker/", followUp, data);
    }
}

/*
fonction de callBack pour la requete concernant les affectations pour un ouvrier
*/
function followUp(xhr){
    var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return
    }
    else{
        var workerAssign = JSON.parse(resp["data"]);
        workerAssign.sort(function(a,b){
                    var a = a.phase.numWeek;
                    var b = b.phase.numWeek;
                    if (a<b) return -1;
                    else if(a>b) return 1;
                    return 0;
                });
        majIHM(workerAssign);
    }
}


/*
Permet de mettre à jour l'ihm selon l'ouvrier demandé
*/
function majIHM(assign){
    var nom = worker.name;

    $('#name').append(document.createTextNode(nom.charAt(0).toUpperCase() + nom.substring(1).toLowerCase())).click(function(e){modifInput(e.target);});
    var prenom = worker.firstName;
    $('#firstName').append(document.createTextNode(prenom.charAt(0).toUpperCase() + prenom.substring(1).toLowerCase())).click(function(e){modifInput(e.target);});
    $('#birthday').append(document.createTextNode(worker.birthdate)).click(function(e){modifInput(e.target);});
    $('#qualification').append(document.createTextNode(worker.qualification.name)).click(function(e){modifInput(e.target);});
    $('#craft').append(document.createTextNode(worker.craft.name)).click(function(e){modifInput(e.target);});
    $('#licence').append(document.createTextNode(worker.licence)).click(function(e){modifInput(e.target);});
    $('#address').append(document.createTextNode(worker.position.address)).click(function(e){modifInput(e.target);});
    //On affiche la localisation de cet ouvrier
    initMap();
    showPosition(worker.position.latitude, worker.position.longitude);

    
    // On affiche les affectations
    if (assign.length > 0){
        for(var i = 0; i < assign.length; i++){
            $('#affectTable').append('<tr><td>'+assign[i].phase.numWeek+'</td><td>'+assign[i].siteName+'</td>/tr>')
        }
    } else {
        $('#tabWeek').hide();
    }
}
function found(address){
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
function modifInput(el){
    if ($('#cValid').is('.disabled') && (sessionStorage.lvladminreq == 1 || sessionStorage.lvladminreq == 3)){
        request("templates/proxy.php?url=http://localhost:5000/craft/all/", majInputCraft);
        request("templates/proxy.php?url=http://localhost:5000/qualification/all/", majInputQualification);
    }
    allowClick(found,notFound); 
    // test qui permet de determiner si les inputs sont déja affiché
    if (document.getElementsByClassName('form') != null && (sessionStorage.lvladminreq == 1 || sessionStorage.lvladminreq == 3)){
         
        // On récupere les elements du formulaire
        children = document.getElementsByClassName('form');
        // Et on les parcourt en créant pour chaque enfant, un input avec la valeru associée
        while (children.length){
            if(children[0].id != "birthday"){
                var input = document.createElement('input');
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
            else{
                $('#birthday').replaceWith('<div class="input-group date" id="datetimepickerN"><input class="form-control" name="birthday" required data-format="DD/MM/YYYY" placeholder="jj/mm/aaaa" value="'+children[0].innerHTML+'" /><span class="input-group-addon"><span class="fa fa-calendar"></span></span></div>');
                $(function () {
                    $('#datetimepickerN').datetimepicker({
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

function majInputCraft(xhr){
    var resp = JSON.parse(xhr.responseText)
    var craft = [];
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        craft = JSON.parse(resp["data"]);
    }
    craft.sort(function(a,b){
            var a = a.name;
            var b = b.name;
            if (a<b) return -1;
            else if(a>b) return 1;
            return 0;
        });
    currentCraft = $('#craft').html();
    $('#craft').replaceWith('<select class="form-control" id="craftSelect"></select>');
    $.each( craft, function( key, value ) {
        $('#craftSelect').append('<option value="'+value.num+'">'+value.name+'</option>');
    });
    $('[id=craftSelect] option').filter(function() { 
        return ($(this).text() == currentCraft); //To select Blue
    }).prop('selected', true);
}

function majInputQualification(xhr){
    var qualif = []
    var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        qualif = JSON.parse(resp["data"]);
    }
    qualif.sort(function(a,b){
            var a = a.name;
            var b = b.name;
            if (a<b) return -1;
            else if(a>b) return 1;
            return 0;
        });
    // console.log(qualif);
    currentQualif = $('#qualification').html();
    $('#qualification').replaceWith('<select class="form-control" id="qualifSelect"></select>');
    $.each( qualif, function( key, value ) {
        $('#qualifSelect').append('<option value="'+value.num+'">'+value.name+'</option>');
    });
    $('[id=qualifSelect] option').filter(function() { 
        return ($(this).text() == currentQualif ); 
    }).prop('selected', true);

}
/**
appellée lors de l'appui sur "valider"
*/
function editWorker(){
    if(clickedOnMap){
        var marker = getMarker();
        followUpEdition(marker.position.lat(),marker.position.lng());
    }else{
        var address = $('input[id="address"]').val();
        codeAddress(address, followUpEdition, addressFail);
    }
    
}

/**
appelée une fois la résolution d'adresse terminée
*/
function followUpEdition(latitude, longitude){
    console.log("latitude :"+latitude+"    |   longitude :"+longitude);
    var name = $('input[id="name"]').val();
    var firstName = $('input[id="firstName"]').val();
    var birthdate = $('input[name="birthday"]').val();
    var craft = $('select[id="craftSelect"]').val();
    var qualification = $('select[id="qualifSelect"]').val();
    var address = $('input[id="address"]').val();
    var checkedlicence = $('.licence:checkbox:checked').map(function() {
        return this.id;
    }).get();
    checkedlicence=checkedlicence.join(",");
    
    if(name==""){
            $('#formNom').removeClass('has-success');
            $('#formNom').addClass('has-error');
            $('#cValid').attr("data-content","Le champ \'Nom\' n'est pas rempli");
            $('#cValid').popover('show');
            setTimeout(function(){$('#cValid').popover('destroy')},2000);
            return;
    }
    else if(firstName == ""){
            $('#formNom').removeClass('has-error');
            $('#formNom').addClass('has-success');
            $('#formPrenom').removeClass('has-success');
            $('#formPrenom').addClass('has-error');
            $('#cValid').attr("data-content","Le champ \'Prénom\' n'est pas rempli");
            $('#cValid').popover('show');
            setTimeout(function(){$('#cValid').popover('destroy')},2000);
            return;
    }
    
else if(!checkDate(birthdate)){
            $('#formNom').removeClass('has-error');
            $('#formNom').addClass('has-success');
            $('#formPrenom').removeClass('has-error');
            $('#formPrenom').addClass('has-success');
            $('#formDateN').removeClass('has-success');
            $('#formDateN').addClass('has-error');
            $('#cValid').attr("data-content","Le champ \'Date\' n'est pas valide");
            $('#cValid').popover('show');
            setTimeout(function(){$('#cValid').popover('destroy')},2000);
            return;
    }
else if(craft==""){
            $('#formNom').removeClass('has-error');
            $('#formNom').addClass('has-success');
            $('#formPrenom').removeClass('has-error');
            $('#formPrenom').addClass('has-success');
            $('#formDateN').removeClass('has-error');
            $('#formDateN').addClass('has-success');
            $('#formCraft').removeClass('has-success');
            $('#formCraft').addClass('has-error');
            $('#cValid').attr("data-content","Veuillez sélectioner un métier");
            $('#cValid').popover('show');
            setTimeout(function(){$('#cValid').popover('destroy')},2000);
            return;
    }else if(qualification==""){
            $('#formNom').removeClass('has-error');
            $('#formNom').addClass('has-success');
            $('#formPrenom').removeClass('has-error');
            $('#formPrenom').addClass('has-success');
            $('#formDateN').removeClass('has-error');
            $('#formDateN').addClass('has-success');
            $('#formCraft').removeClass('has-error');
            $('#formCraft').addClass('has-success');
            $('#formQualif').removeClass('has-success')
            $('#formQualif').addClass('has-error');
            $('#cValid').attr("data-content","Veuillez sélectioner une qualification");
            $('#cValid').popover('show');
            setTimeout(function(){$('#cValid').popover('destroy')},2000);
            return;
    }
    
    var s = 'num='+worker.num+'^name='+name+'^firstName='+firstName+'^birthdate='+birthdate+'^licence='+checkedlicence+'^latitude='+latitude+'^longitude='+longitude+'^address='+address+'^craft='+craft+'^qualification='+qualification;
    var data = new FormData();
    data.append('data', s);
    
    $('#formNom').removeClass('has-error');
    $('#formNom').addClass('has-success');
    $('#formPrenom').removeClass('has-error');
    $('#formPrenom').addClass('has-success');
    $('#formDateN').removeClass('has-error');
    $('#formDateN').addClass('has-success');
    $('#formCraft').removeClass('has-error');
    $('#formCraft').addClass('has-success');
    $('#formQualif').removeClass('has-error')
    $('#formQualif').addClass('has-success');
    
    request("templates/proxy.php?url=http://localhost:5000/worker/update/", editionOk, data);
}

/**
appellée lors de l'appui sur "valider adresse"
*/
function checkAddress(){
    var address = $('input[id="address"]').val();
    codeAddress(address, addressOK, addressFail);

    function addressOK(latitude, longitude){
            document.getElementById("address").style.backgroundColor = 'rgb(117,254,98)';
            showPosition(latitude, longitude);
    }
}

/**
appelé si la résolution d'adresse à échouée
*/
function addressFail(address){
    reportWarning("L'adresse semble incorrecte : ("+address+")");
    document.getElementById("address").style.backgroundColor = "red";
}

/**
appelée une fois l'édition terminée'
*/
function editionOk(xhr){
    var resp = JSON.parse(xhr.responseText)
    localStorage.clear();
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return
    }
    else{
        reportSuccess(resp["message"], null, "index.php?choix=6")
    }
}


/**
appelée lors de l'appui sur "supprimer"
*/
function deleteWorker(){
    var idToDelete = worker.num;
    var data = new FormData();
    data.append('data', 'num='+idToDelete);
    $("#supprModal").modal('hide');
    setTimeout(function(){request("templates/proxy.php?url=http://localhost:5000/worker/delete/", editionOk, data)},50);
}
