<?php
// Ce proxy peut être utilisé de deux manière différentes. Soit il construit une requete POST, soit une requete GET. Dans tous les cas,
// on envoi une requete GET avec une url ainsi que des arg pour la méthode POST.
// Ainsi, une url pour une méthode GET sur Flask ressemble à ca :
//		templates/proxy.php?url=localhost:5000/<une_url_de_flask_qui_demande_un_get> (exemple pour /site/all : proxy.php?url=localhost:5000/site/all/)
// Sinon, pour un POST, il nous faut plus d'informations :
//		templates/proxy.php?url=localhost:5000/<une_url_de_flask_qui_demande_un_post>&arg=<des_arg_pour_un_post> 
//		(exemple pour /site/byid/ : proxy.php?url=localhost:5000/site/byid&arg=num=2)


// On test d'abord si l'url est existante, sinon, on ne peut rien faire
if (!isset($_GET['url'])) die();
// On test ensuite si les paramètres nécessaire à un POST existent
if (isset($_POST['data'])){
	$args = explode('^', $_POST['data']);
	$data = "";
	$cpt = 0;
	foreach ($args as &$value) {
		$cpt++;
    		$data = $value . '&' . $data;
	}
	$data = substr($data, 0, strlen($data)-1);
	// On récupère l'url que l'on envoi à Flask
	$url = urldecode($_GET['url']);
	$url = 'http://' . str_replace('http://', '', $url);
	// Initialisation de la connexion avec cUrl
	$ch = curl_init();
	// Ajout de l'url à curl
	curl_setopt($ch, CURLOPT_URL, $url);
	// Ajout de la méthode POST
	curl_setopt($ch, CURLOPT_POST, $cpt);
	// Ajout des paramètres que l'on passe en paramètre
	curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	// Execution de la requete
	echo curl_exec($ch);
	// Fermeture de la requete
	curl_close($ch);
// Sinon c'est un GET et on envoi juste l'url
} else {
	$url = urldecode($_GET['url']);
	echo file_get_contents($url);
}
?>

