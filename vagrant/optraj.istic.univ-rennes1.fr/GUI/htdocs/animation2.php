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
	center : new google.maps.LatLng(48.118892 , -1.439209),
	zoom : 11,
    mapTypeId : google.maps.MapTypeId.ROADMAP
};
/* Ici, nous chargeons la map dans l'élément html ayant pour id "map" */
var map = new google.maps.Map(document.getElementById("map"), optionsMap);
var first = true
google.maps.event.addListener(map, 'tilesloaded', function() {
	setTimeout(function(){
		if(first){
			first = false;
			draw();
		}
	}, 500);
});

var rennes = new google.maps.LatLng(48.113391 , -1.665802);
var vitre = new google.maps.LatLng(48.122559 , -1.215363);
var sites = [rennes, vitre]
var bleus = [new google.maps.LatLng(48.051005 , -1.496887),
            new google.maps.LatLng(48.084042 , -1.617737),
            new google.maps.LatLng(48.093216 , -1.661682),
            new google.maps.LatLng(48.178449 , -1.304626),
            new google.maps.LatLng(48.121643 , -1.459808)];
var oranges = [new google.maps.LatLng(48.219069 , -1.578941),
            new google.maps.LatLng(48.212206 , -1.504097),
            new google.maps.LatLng(48.113535 , -1.399555),
            new google.maps.LatLng(48.136308 , -1.609497),
            new google.maps.LatLng(48.054677 , -1.51474)
            ]
var pickupA = new google.maps.LatLng(48.100826 , -1.464443);
var pickupB = new google.maps.LatLng(48.103434 , -1.414833);
var pickupC = new google.maps.LatLng(48.203332 , -1.525469);
var circles = [];
var directionsService = new google.maps.DirectionsService();
function draw () {
    /******************
    cercles
    *****************/
    for(var x in bleus){
        circles.push(new google.maps.Circle({
                        map: map,
                        center: bleus[x],
                        strokeOpacity: 0.2,
                        radius: 500,    // 10 miles in metres
                        fillColor: '#0000FF',
                        fillOpacity: 1
                    }))
    }
    for(var x in oranges){
        circles.push(new google.maps.Circle({
                        map: map,
                        center: oranges[x],
                        strokeOpacity: 0.2,
                        radius: 500,    // 10 miles in metres
                        fillColor: '#FF8800',
                        fillOpacity: 1
                    }))
    }
    for(var x in circles){
        google.maps.event.addListener(circles[x], 'click', function(){console.log(this)});
    }
    var delay = 800;
    var timeout = delay;
    for (i = 0; i < sites.length; i++) {
        sleep(timeout, drawSite, i);
        timeout+=delay;
    }
    timeout+=delay
    for (i = 0; i < sites.length; i++) {
        sleep(timeout, drawSite2, i);
        timeout+=delay;
    }
    sleepRoute(timeout, bleus[3], vitre);
    timeout+=delay;
    sleep(timeout, function(){
        var icon = "https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + String.fromCharCode(65) + "|00FD00|000000";
        new google.maps.Marker({
            position: pickupA,
            animation: google.maps.Animation.DROP,
            map: map,
            icon: icon
        });
    });

    timeout+=delay;
    sleepRoute(timeout, bleus[4], pickupA);
    timeout+=delay;
    sleepRoute(timeout, bleus[0], pickupA);
    timeout+=delay;
    sleepRoute(timeout, oranges[4], pickupA);
    timeout+=delay;
    sleep(timeout, function(){
        var icon = "https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + String.fromCharCode(66) + "|00FD00|000000";
        new google.maps.Marker({
            position: pickupB,
            animation: google.maps.Animation.DROP,
            map: map,
            icon: icon
        });
    });
    timeout+=delay;
    sleepRoute(timeout, oranges[2], pickupB);
    timeout+=delay;
    //navette
    sleepRoute(timeout, bleus[1], vitre, [{location: pickupA, stopover:true},
                         {location: pickupB, stopover:true}]);
    timeout+=delay;
    sleepRoute(timeout, bleus[2], rennes)
    timeout+=delay;
    sleepRoute(timeout, oranges[3], rennes)
    timeout+=delay;
    sleep(timeout, function(){
        var icon = "https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + String.fromCharCode(67) + "|00FD00|000000";
        new google.maps.Marker({
            position: pickupC,
            animation: google.maps.Animation.DROP,
            map: map,
            icon: icon
        });
    });
    timeout+=delay;
    sleepRoute(timeout, oranges[0], pickupC)
    timeout+=delay;
    sleepRoute(timeout, oranges[1], rennes, [{location: pickupC, stopover:true}]);
}

function drawRoute (origin, destination, waypoints) {
    var renderer, request;
    if(waypoints==null){
        renderer = new google.maps.DirectionsRenderer({
            map: map,
            polylineOptions: {
              strokeColor: '#FF0000',
              strokeOpacity: .6,
              strokeWeight: 4,
            },
            suppressMarkers : true,
            preserveViewport : true
        });
        request = {
            origin      : origin,
            destination : destination,
            travelMode  : google.maps.DirectionsTravelMode.DRIVING
        };
    }
    else{
        renderer = new google.maps.DirectionsRenderer({
            map: map,
            polylineOptions: {
              strokeColor: '#F00000',
              strokeOpacity: .7,
              strokeWeight: 6,
            },
            suppressMarkers : true,
            preserveViewport : true
        });
        request = {
            origin      : origin,
            destination : destination,
            waypoints   : waypoints,
            travelMode  : google.maps.DirectionsTravelMode.DRIVING,
            optimizeWaypoints:true
        };
    }
    directionsService.route(request, function(response, status){ // Envoie de la requête pour calculer le parcours
            if(status == google.maps.DirectionsStatus.OK){
                renderer.setDirections(response); // Trace l'itinéraire sur la carte et les différentes étapes du parcours
                renderer.setMap(map);
            }
        });

}

function drawSite(i){
    /* on récupère nos coordonnées dans le tableau de chantier et on les mets dans le tableau de points */
    if(i==0){
        pos = rennes;
    }
    else{
        pos = vitre;
    }   
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
    var content1 = '<div class="gMapWindowSite">I need :<br />' +
                    '<i class="fa fa-circle" style="color:#0000FF"></i> : 1<br/>' +
                    '<i class="fa fa-circle" style="color:#FF8800"></i> : 3</div';
    var content2 = '<div class="gMapWindowSite">I need :<br />' +
                    '<i class="fa fa-circle" style="color:#0000FF"></i> : 4<br/>' +
                    '<i class="fa fa-circle" style="color:#FF8800"></i> : 2</div';
    var pos;
    if(i==0){
        infoBulle.setContent(content1);
        pos = rennes;    
        marker = new google.maps.Marker({
        map:map,
        position: pos
        }); 
    }
    else{
        infoBulle.setContent(content2);
        pos = vitre;    
        marker = new google.maps.Marker({
        map:map,
        position: pos
        }); 
    }

	infoBulle.open(map, marker);
}

function sleep(millis, callback, i) {
    setTimeout(function()
            { callback(i); }
    , millis);
}
function sleepRoute(millis, origin, destination, waypoints) {
    setTimeout(function()
            { drawRoute(origin, destination, waypoints); }
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