/*(function() {
	initMap();
})();*/

var map;
var marker;

function initMap() {    
    // Déclaration des options de la map
    console.log("ok");
	var optionsMap = {
		center : new google.maps.LatLng(48.1134750,-1.6757080),
		zoom : 12
	};
    //Ici, nous chargeons la map dans l'élément html ayant pour id "map"
	map = new google.maps.Map(document.getElementById("map"), optionsMap);
	if(marker != undefined){marker.setMap(null);}
}

function showPosition(latitude, longitude) {
	var point = new google.maps.LatLng(latitude,longitude);
	//efface le marqueur s'il existe
	if(marker != undefined){marker.setMap(null);}

	var bound = new google.maps.LatLngBounds(); 
	bound.extend(point);
	bound.extend(new google.maps.LatLng(48.1134750,-1.6757080));
	// var optionsMap = {
	// 	center : new google.maps.LatLng(48.1134750,-1.6757080),
	// 	zoom : 12
	// };
 //         Ici, nous chargeons la map dans l'élément html ayant pour id "map" 
	// map = new google.maps.Map(document.getElementById("map"), optionsMap);
	map.fitBounds(bound);
	
	//affiche le nouveau marqueur
	marker = new google.maps.Marker({
        position: point,
        map: map
    });
}

function allowClick(funcFound, funcFail) {
    google.maps.event.addListener(map, 'click', function(event) {
        var latitude = event.latLng.lat();
        var longitude = event.latLng.lng();
        var point = new google.maps.LatLng(latitude,longitude);
        //efface le marqueur s'il existe
        if (!marker) {
            marker = new google.maps.Marker({
                position: point,
                map: map
            });
            
        } else {
            marker.setPosition(point);
        }
        getAddress(latitude, longitude, funcFound, funcFail)
    });
}

function getMarker() {
    return marker;
}
function route(positions) {
    var origin = positions[0]; 
    var destination = positions[1]; 
    var panel;
    
    var optionsMap = {
        center : new google.maps.LatLng(48.1134750,-1.6757080),
        zoom : 12
    };
    /* Ici, nous chargeons la map dans l'élément html ayant pour id "map" */
    map = new google.maps.Map(document.getElementById("map"), optionsMap);
    var direction = new google.maps.DirectionsRenderer({
        map   : map,
        panel : panel
    });
    
    var request = {
        origin      : origin,
        destination : destination,
        travelMode  : google.maps.DirectionsTravelMode.DRIVING // Type de transport
    }
    var directionsService = new google.maps.DirectionsService(); // Service de calcul d'itinéraire
    directionsService.route(request, function(response, status){ // Envoie de la requête pour calculer le parcours
        if(status == google.maps.DirectionsStatus.OK){
            direction.setDirections(response); // Trace l'itinéraire sur la carte et les différentes étapes du parcours
        }
        else
        {
            reportError("Error : "+status);
        }
    });
}


	