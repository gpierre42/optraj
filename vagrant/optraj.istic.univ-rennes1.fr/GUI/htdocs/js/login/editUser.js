var currAdmin = {};
   
(function() {
    var admin = JSON.parse(localStorage.admin);
    currAdmin.name = admin.name;
    currAdmin.firstname = admin.firstname;
    currAdmin.lvl = admin.lvl;
    currAdmin.pwd = admin.pwd;
    currAdmin.login = admin.login;
	currAdmin.num = admin.num;
    if($("#editUser").length>0){//si on est sur la page d'édition d'utilisateur
        loadForm();
    }
})();

/**
affiche le formulaire avec les informations liées à l'utilisateur
*/
function loadForm(){
    var name = currAdmin.name;
	var firstname = currAdmin.firstname;
	var lvl = currAdmin.lvl;
	//var pwd = currAdmin.pwd;
	var login = currAdmin.login;
    //remplissage du formulaire avec les valeurs récupérées
    var n = document.getElementById('name');
    n.innerHTML = name;
    n.addEventListener('click', function(e) {modifInput(e.target);}, false);

    var f = document.getElementById('firstname');
    f.innerHTML = firstname;
    f.addEventListener('click', function(e) {modifInput(e.target);}, false);
	
	var l = document.getElementById('login');
    l.innerHTML = login;
    l.addEventListener('click', function(e) {modifInput(e.target);}, false);
	
	document.getElementById('lvladmin_select').selectedIndex = lvl;	
	var lv = document.getElementById('lvladmin_select');
    lv.addEventListener('click', function(e) {modifInput(e.target);}, false);
	
    // On cache les boutons de modif, suppression et verification
    $('#btnValidate').addClass('disabled');	
}

/**
 * Fonction qui permet d'afficher le formulaire de modification d'un chantier lorsque l'on clique sur un champs
 */
function modifInput(el){
	//levelreq ()
    // test qui permet de determiner si les inputs sont déja affiché
    if (document.getElementsByClassName('form') != null && (sessionStorage.lvladminreq == 1 || sessionStorage.lvladminreq == 3)){
        // On récupere les elements du formulaire
        children = document.getElementsByClassName('form');
        // Et on les parcourt en créant pour chaque enfant, un input avec la valeru associée
        while (children.length-1){
            var input = document.createElement('input');
            input.type = 'text';
            input.name = children[0].id;
            input.id = children[0].id;
            input.required = true;
            input.value = children[0].innerHTML;
            children[0].parentNode.appendChild(input);
            // Si l'enfant est l'élement qe l'on a cliqué, on lui donne le focus
            if (el === children[0]){
                children[0].parentNode.lastChild.focus();
                children[0].parentNode.lastChild.select();
            }
            children[0].parentNode.removeChild(children[0]);
        }
        $('#btnValidate').removeClass('disabled');  
    }
}

/**
appellée lors de l'appui sur "valider"
*/
function editUser(){
	var idToUpdate = currAdmin.num;
	var name = $('#form input[name="name"]').val();
	var firstname = $('#form input[name="firstname"]').val();
	var login = $('#form input[name="login"]').val();
	//var pwd = $('#form input[name="pwd"]').val();
	var lvl = document.getElementById('lvladmin_select').value;

	//application de mise en forme et message d'erreur si des champs sont incomplets
    if(name=="" || firstname == "" || login == ""){
        if(name==""){
            $('#formLastname').removeClass('has-success');//On enlève la classe qui permet de mettre en vert
            $('#formLastname').addClass('has-error');//On ajoute la classe qui permet de mettre en rouge
        }
        else{
            $('#formLastname').removeClass('has-error');//On enlève la classe qui permet de mettre en vert
            $('#formLastname').addClass('has-success');//On ajoute la classe qui permet de mettre en rouge
        }
        if(firstname==""){
            $('#formFirstname').removeClass('has-success');//On enlève la classe qui permet de mettre en vert
            $('#formFirstname').addClass('has-error');//On ajoute la classe qui permet de mettre en rouge
        }
        else{
            $('#formFirstname').removeClass('has-error');//On enlève la classe qui permet de mettre en vert
            $('#formFirstname').addClass('has-success');//On ajoute la classe qui permet de mettre en rouge
        }
        if(login==""){
            $('#formLogin').removeClass('has-success');//On enlève la classe qui permet de mettre en vert
            $('#formLogin').addClass('has-error');//On ajoute la classe qui permet de mettre en rouge
        }
        else{
            $('#formLogin').removeClass('has-error');//On enlève la classe qui permet de mettre en vert
            $('#formLogin').addClass('has-success');//On ajoute la classe qui permet de mettre en rouge
        }
        reportError("Remplissez tous les champs");
        return;
    }
    else if(lvl==""){
            $('#formLevel').removeClass('has-success');//On enlève la classe qui permet de mettre en vert
            $('#formLevel').addClass('has-error');//On ajoute la classe qui permet de mettre en rouge
            reportError("Choisissez le niveau d'utilisateur"); // le contenu du popover
            return;
    }
    else{
            $('#formLevel').removeClass('has-error');//On enlève la classe qui permet de mettre en vert
            $('#formLevel').addClass('has-success');//On ajoute la classe qui permet de mettre en rouge
    }

	var md5pwd = currAdmin.pwd;
	var s = 'name='+name+'^num='+idToUpdate+'^firstname='+firstname+'^login='+login
	+'^md5pwd='+md5pwd+'^lvl='+lvl;
	var data = new FormData();
	data.append("data", s);
	request("templates/proxy.php?url=http://localhost:5000/user/update/",
        updateDone,
        data);
}

/**
appellée lors de l'appui sur "valider" de la page de modification de mot de passe
*/
function editPassword(){
    
    var idToUpdate = currAdmin.num;
    var name = currAdmin.name;
    var firstname = currAdmin.firstname;
    var login = currAdmin.login;
    var lvl = currAdmin.lvl;
    var num = currAdmin.num;
    
    var newpwd = $('#form input[name="newpwd"]').val();
    var verifpwd = $('#form input[name="newpwdverif"]').val();
    var md5newpwd = MD5(newpwd);
    
    if(newpwd==""){
        reportError("Remplissez tous les champs");
        return;
    }
    else if(newpwd!=verifpwd){
        reportError("Les mots de passe ne correspondent pas")
        return;
    }
    else if(currAdmin.pwd==md5newpwd){
        reportError("Le nouveau mot de passe doit être différent de l'ancien.");
        return;
    }
    
    var s = 'name='+name+'^num='+idToUpdate+'^firstname='+firstname+'^login='+login
    +'^md5pwd='+md5newpwd+'^lvl='+lvl;
    var data = new FormData();
    data.append("data", s);
    request("templates/proxy.php?url=http://localhost:5000/user/update/", updateDone, data);
}

/**
appelée lors de l'appui sur "supprimer"
*/
function deleteUser(){
    $("#supprModal").hide();
    var idToDelete = currAdmin.num;
    var data = new FormData();
    data.append('data', 'num='+idToDelete);
    request("templates/proxy.php?url=http://localhost:5000/user/delete/", 
        updateDone,
        data);
}

/*
Fonction appellée par callback après édition d'un utilisateur
*/
function updateDone(xhr){
    var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        reportSuccess(resp["message"], null, "index.php?choix=18")
    }
}