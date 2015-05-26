<!DOCTYPE HTML>
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script src="js/bootstrap/jquery-1.10.2.js"></script>
<script type="text/javascript" src="js/fonctionsIndex.js"></script>
<script src="js/bootstrap/bootstrap-formhelpers.min.js"></script>
<!-- Core Scripts - Include with every page -->
<script src="js/bootstrap/bootstrap.min.js"></script>
<script src="js/bootstrap/plugins/metisMenu/jquery.metisMenu.js"></script>
<!-- SB Admin Scripts - Include with every page -->
<script src="js/bootstrap/sb-admin.js"></script>
<script src="js/util/floatingMenu.js"></script>
<script src="bootstrap-touchspin/bootstrap.touchspin.js"></script>
<script src="js/util/automaticReports.js"></script>
<script src="js/util/connexionProxy.js"></script>
<html>
    <head>
        <meta charset="UTF-8" />
        <title>OPTRAJ</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css"  href="css/style.css" />
        <link href='http://fonts.googleapis.com/css?family=Open+Sans+Condensed:700,300|Roboto:300' rel='stylesheet' type='text/css'>
		<!--[if IE]>  
			<script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>  
		<![endif]-->
		<link href="css/bootstrap/bootstrap-formhelpers.min.css" rel="stylesheet">
	    <!-- Core CSS - Include with every page -->
	    <link href="css/bootstrap/bootstrap.min.css" rel="stylesheet">
	    <link href="font-awesome/css/font-awesome.css" rel="stylesheet">
	    <!-- SB Admin CSS - Include with every page -->
	    <link href="css/bootstrap/sb-admin.css" rel="stylesheet">
	    <link href="css/bootstrap/bootstrap-datetimepicker.min.css" rel="stylesheet">
		<link rel="stylesheet" href="css/bootstrap/bootstrap-multiselect.css" type="text/css"/>    
		
		<style type="text/css">
			/* Fix Google Maps canvas
			*
			* Wrap your Google Maps embed in a `.google-map-canvas` to reset Bootstrap's
			* global `box-sizing` changes. You may optionally need to reset the `max-width`
			* on images in case you've applied that anywhere else. (That shouldn't be as
			* necessary with Bootstrap 3 though as that behavior is relegated to the
			* `.img-responsive` class.)
			*/
			
			.google-map-canvas,
			.google-map-canvas * { .box-sizing(content-box); }
			
			/* Optional responsive image override */
			img { max-width: none; }
		</style>
    </head>
    <body>
		<div class="panel panel-default" id="consult">
		    <div class="panel-body" id="map" style="width:100%;height:768px;position:relative;">
		    </div>
		</div>
    </body>
</html>

<script type="text/javascript">


/* Déclaration de l'objet qui définira les limites de la map */ 
var sites = [];

/* Déclaration des options de la map */
var optionsMap = {
	center : new google.maps.LatLng(48.1134750,-1.6757080),
	zoom : 10,
    mapTypeId : google.maps.MapTypeId.ROADMAP
};
/* Ici, nous chargeons la map dans l'élément html ayant pour id "map" */
var map = new google.maps.Map(document.getElementById("map"), optionsMap);
var bounds = new google.maps.LatLngBounds();
bounds.extend(new google.maps.LatLng(48.694586, -1.370544));
bounds.extend(new google.maps.LatLng(47.141161, -1.521606));
map.fitBounds(bounds);
var first = true
google.maps.event.addListener(map, 'tilesloaded', function() {
	setTimeout(function(){
		if(first){
			first = false;
			request("templates/proxy.php?url=http://localhost:5000/worker/all/", getWorkers);
		}
	}, 500);
});

function getWorkers(xhr){
	var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
        workers = []
    }
    else{
        workers =  JSON.parse(resp["data"]);
    }
    var timeout = drawWorkers();
    setTimeout(function(){
    	request("templates/proxy.php?url=http://localhost:5000/site/all/", initMap);
    }, timeout+30);
    
}

function initMap(xhr) {
    var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
        sites = []
    }
    else{
        sites =  JSON.parse(resp["data"]);
    }

    /* Déclaration d'un tableau qui contiendra les latitudes et longitudes de chaque chantier */
    var tabPoints = [];
    var tabContenu = [];
	var marker, i;
 	var timeout = 300;
    for (i = 0; i < sites.length; i++) {
		sleep(timeout, drawSite, i);
		timeout+=200;
    }
    for (i = 0; i < sites.length; i++) {
		sleep(timeout, drawSite2, i);
		timeout+=200;
    }
}

function drawSite(i){
    /* on récupère nos coordonnées dans le tableau de chantier et on les mets dans le tableau de points */
    var pos = new google.maps.LatLng(sites[i].position.latitude, sites[i].position.longitude);    
      marker = new google.maps.Marker({
	    map:map,
	    animation: google.maps.Animation.DROP,
	    position: pos
	  });    
}

function drawSite2 (i) {
		var infoBulle = new google.maps.InfoWindow({
		zIndex:i
	});
	    var currWeek = 26;
    var needs = sites[i].phases[2014][currWeek].needs
    var counts = {}
    for(var x in needs){
    	var c = needs[x].craft.num;
    	if(counts[c]==null){
    		counts[c] = 0;
    	}
    	counts[c] += needs[x].need;
    }
    
    var content = '<div class="gMapWindowSite">I need :<br />';
    for(var x in counts){
    	var color = getColor(x);
    	if(counts[x]>0){
    		content += '<i class="fa fa-circle" style="color:'+color+'"></i> : ' + counts[x] + '<br/>';
    	}
    }
	content+='</div>';
	infoBulle.setContent(content);
	var pos = new google.maps.LatLng(sites[i].position.latitude, sites[i].position.longitude);    
	marker = new google.maps.Marker({
	map:map,
	position: pos
	}); 
	infoBulle.open(map, marker);
}

function sleep(millis, callback, i) {
    setTimeout(function()
            { callback(i); }
    , millis);
}

function drawWorker(i){
	// on ajoute la position sur la map de chaque ouvrier
    workers[i].mapPosition = new google.maps.LatLng(workers[i].position.latitude, workers[i].position.longitude);

    // on dessine maintenant l'ouvrier
    workers[i].circle = new google.maps.Circle({
        map: map,
        center: workers[i].mapPosition,
        strokeOpacity: 0.2,
        radius: 3000,    // 10 miles in metres
        fillColor: getColor(workers[i].craft.num),
        fillOpacity: 1,
        zIndex:i
    });
}

function drawWorkers(){
	var timeout = 10;
	for (var i = 0; i < workers.length; i++) {
		sleep(timeout, drawWorker, i);
		timeout+=30;
    }
    return timeout;
}

function getColor(i){
	i = parseInt(i)
	switch (i){
    	case 1:
    	color = '#973333'
    		break;
    	case 2:
    	color = '#fb6600'
    		break;
    	case 3:
    	color = '#b500a3'
    		break;
    	case 4:
    	color = '#ff90cd'
    		break;
    	case 5:
    	color = '#b07cff'
    		break;
    	case 6:
    	color = '#5800b5'
    		break;
    	case  7:
    	color = '#90d7ff'
    		break;
    	case  8:
    	color = '#009ea1'
    		break;
    	case  9:
    	color = '#7cffa6'
    		break;
    	case  10:
    	color = '#04bf00'
    		break;
    	case  11:
    	color = '#b2ff2c'
    		break;
    	case  12:
    	color = '#fbff18'
    		break;
    	case  13:
    	color = '#d37a00'
    		break;
    	default :
    	color = '#ffbb5e'
    }
    return color;
}

</script>