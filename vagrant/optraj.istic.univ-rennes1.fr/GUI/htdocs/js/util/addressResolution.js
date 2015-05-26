var addChanged=false;
var positionFound = false;
var geocoder = new google.maps.Geocoder();
var newLat;
var newLng;

/**
Code une addresse en 2 coordonnées, latitude et longitude
Si le codage est russit on appelle funcFound, sinon funcFail
*/
function codeAddress(addressToTest, funcFound, funcFail) {
	/* Récupération de la valeur de l'adresse saisie */
	//var address = document.getElementById("address").value;
	/* Appel au service de geocodage avec l'adresse en paramètre */
	geocoder.geocode( { 'address': addressToTest}, function(results, status) {
		/* Si l'adresse a pu être géolocalisée */
		if (status == google.maps.GeocoderStatus.OK) {
			/* Récupération de sa latitude et de sa longitude */
			var coords = (results[0].geometry.location);
			funcFound(coords.lat(), coords.lng());//cette fonction est à définir par l'appelant
		}else{
			funcFail(addressToTest);//cette fonction est à définir par l'appelant
		}
	});
}

/**
Cette fonction prend en paramètre des coordonnées et renvoi l'adresse correspondante si trouvée
*/
function getAddress(latitude, longitude, funcFound, funcFail) {
    var latlng = new google.maps.LatLng(latitude,longitude);
    geocoder.geocode({ 'latLng': latlng }, function (results, status) {
        if (status !== google.maps.GeocoderStatus.OK) {
            funcFail(latitude, longitude);
        }
        // This is checking to see if the Geoeode Status is OK before proceeding
        if (status == google.maps.GeocoderStatus.OK) {
			//alert(results[0].formatted_address);
            funcFound(results[0].formatted_address);
        }
    });
}
