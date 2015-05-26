/*
CARRE NICOLAS
OPTRAJ
*/

(function() {
	if (sessionStorage.isco == 1) {
		// Si on est connecté, on supprime le lien vers les champs de connexion et on affiche un message
		document.getElementById('idconnect').parentNode.removeChild(document.getElementById('idconnect'));

		var idconnecté = document.getElementById('idconnecté');
		var td = document.createElement("td");
		td.innerHTML = "Vous êtes déjà connecté";
		idconnecté.appendChild(td);
	}

	document.getElementById("title").innerHTML='<h2 class="page-header">Connexion</h2>';

	$('input').keydown(function(e) {
	    if (e.keyCode == 13) {
	        checkPwd();
	    }
	});
})();




function checkPwd (){
	var login = document.getElementById('inputlog').value;
	var pwd = document.getElementById('inputpwd').value;
	var md5pwd = MD5(pwd);
	if (login == "" || pwd == ""){
		reportError("Veuillez remplir tous les champs");
	}
	else{
		var lv = 'login='+login+'^pwd='+md5pwd;
		var data = new FormData();
		data.append("data", lv);
		request("templates/proxy.php?url=http://localhost:5000/user/connect/", followUpPwd, data);
	}
}
	
function followUpPwd (xhr){
	var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"], null, "./index.php");
        return
    }
    else{
        //console.log(xhr.responseText);
		var lvl = JSON.parse(resp["data"]);
		var login = document.getElementById('inputlog').value;	
		sessionStorage.lvladminreq = lvl;
		sessionStorage.isco = 1;
		sessionStorage.alreadyco = 100;
		var lv = 'login='+login
		var data = new FormData();
		data.append("data", lv);
		request("templates/proxy.php?url=http://localhost:5000/user/name/", printName, data);	
    }
}
	
function printName (xhr) {
	var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"], null, "./index.php");
        return
    }
    else{
    	var user = JSON.parse(resp["data"]);
    	console.log(user)
		sessionStorage.logname = user.name;
		sessionStorage.logfirstname = user.firstname;
		reportSuccess("Bienvenue "+user.firstname + " " + user.name + " !", 1000, "./index.php")
    }
}
