/**
appelée une fois la résolution d'adresse terminée
*/
function createAdmin(){
	var name = $('#form input[name="name"]').val();
	var firstname = $('#form input[name="firstname"]').val();
	var login = $('#form input[name="login"]').val();
	var pwd = $('#form input[name="pwd"]').val();
	var lvl = document.getElementById('lvladmin_select').value;

	//application de mise en forme et message d'erreur si des champs sont incomplets
	if(name=="" || firstname == "" || login == "" || pwd == ""){
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
		if(pwd==""){
			$('#formPassword').removeClass('has-success');//On enlève la classe qui permet de mettre en vert
			$('#formPassword').addClass('has-error');//On ajoute la classe qui permet de mettre en rouge
		}
		else{
			$('#formPassword').removeClass('has-error');//On enlève la classe qui permet de mettre en vert
			$('#formPassword').addClass('has-success');//On ajoute la classe qui permet de mettre en rouge
		}
		reportError("Remplissez tous les champs")
		return;
	}
	else if(lvl==""){
		$('#formLevel').removeClass('has-success');//On enlève la classe qui permet de mettre en vert
		$('#formLevel').addClass('has-error');//On ajoute la classe qui permet de mettre en rouge
		reportError("Choisissez le niveau d'utilisateur")
		return;
	}
	else{
		$('#formLevel').removeClass('has-error');//On enlève la classe qui permet de mettre en vert
		$('#formLevel').addClass('has-success');//On ajoute la classe qui permet de mettre en rouge
	}

	var md5pwd = MD5(pwd);
	var s = 'name='+name+'^firstname='+firstname+'^login='+login
	+'^md5pwd='+md5pwd+'^lvl='+lvl;
	var data = new FormData();
	data.append("data", s);
	request("templates/proxy.php?url=http://localhost:5000/user/create/", creationOk, data);
}


/**
appelée une fois la création terminée
*/
function creationOk(xhr){
	var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return
    }
	else{
		reportSuccess(resp["message"], null, "index.php?choix=18")
	}
}
