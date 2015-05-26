var currCar = {};
var currShuttle = {};
var currSite;
   
(function() {
    var car = JSON.parse(localStorage.car);
    currCar.plate = car.plate;
    currCar.model = car.model;
    currCar.nbPlace = car.nbPlace;
    currCar.num = car.num;
    
    var data = new FormData();
    tab = [];
    tab.push(currCar.num);
    data.append('data', 'num='+JSON.stringify(tab));
    var req = "templates/proxy.php?url=http://localhost:5000/shuttle/byCar/";
    request(req, loadShuttle, data);
})();

/**
 * Recupère les infos du conducteur à partir de l'ID de la voiture
 * @param {type} xhr
 */
function loadShuttle(xhr) {
    var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
        currShuttle = JSON.parse(resp["data"]);
        console.log(currShuttle)
    }
    if (currShuttle.length > 0){
        $("#form").append("<table>\
                                <thead>\
                                    <tr class='shuttle'>\
                                        <th class='shuttleInfo' width='150px'>Numéro de semaine</th>\
                                        <th class='shuttleInfo' width='150px'>Chauffeur</th>\
                                    </tr>\
                                </thead>\
                                <tbody name='tabContent' id='tab_Driver'>\
                                </tbody>\
                            </table>");
    } else {
        $("#formDriver").hide();
    }
    currShuttle.sort(function(a,b){
        return a["phase"]["numWeek"]>b["phase"]["numWeek"];
    });
    if(typeof currShuttle[0] != 'undefined') {
        var data = new FormData();
        data.append('data', 'num='+currShuttle[0].phase["numSite"]);
        var req = "templates/proxy.php?url=http://localhost:5000/site/byid/";
        request(req, loadSite, data);
    }
    else {
        loadForm();
    }
}

function loadSite(xhr) {
    var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
        return;
    }
    else{
        currSite = JSON.parse(resp["data"]);
        loadForm();
    }
}

/**
affiche le formulaire avec les informations liées à une navette
*/
function loadForm(){
    // Récupération de toutes les infos d'une navette
    var plate = currCar.plate;
    var model = currCar.model;	
    var nbPlace = currCar.nbPlace;
    
    if(typeof currShuttle[0] != 'undefined') {
        var name = currShuttle[0].driver.name;
        var firstName = currShuttle[0].driver.firstName;
    }
    
    //remplissage du formulaire avec les valeurs récupérées
    var n = document.getElementById('plate');
    n.innerHTML = plate;

    var dI = document.getElementById('model');
    dI.innerHTML = model;

    var dE = document.getElementById('nbPlace');
    dE.innerHTML = nbPlace;
    
    if(typeof currShuttle[0] != 'undefined') {
        var dD = document.getElementById('driver');
        dD.innerHTML = name.toUpperCase()+" "+firstName;
        completeTable();

        // Affichage carte
        var waypoints = new Array();
        var start = new google.maps.LatLng(currShuttle[0].driver.position.latitude, currShuttle[0].driver.position.longitude);
        var arrival = new google.maps.LatLng(currSite.position.latitude, currSite.position.longitude);
        var mapSetup = {
            'center' : start, 
            'zoom' : 7,
            'mapTypeId' : google.maps.MapTypeId.ROADMAP
        };

        map = new google.maps.Map(document.getElementById("map"), mapSetup);

        var direction = new google.maps.DirectionsRenderer({ 
            'map'   : map,
            suppressMarkers : true
        });

        for (p in currShuttle[0].pickupLinks){
            waypoints.push({
                location:new google.maps.LatLng(currShuttle[0].pickupLinks[p].pickup.position.latitude, currShuttle[0].pickupLinks[p].pickup.position.longitude),
                stopover:true
            });
        }

        var requete = {
            origin: start,
            destination: arrival,
            travelMode: google.maps.DirectionsTravelMode.DRIVING,
            waypoints: waypoints,
            optimizeWaypoints: true
        };
        var directionsService = new google.maps.DirectionsService();
        directionsService.route(requete, function(response, status){
            if(status == google.maps.DirectionsStatus.OK){
                direction.setDirections(response);
                var myRoute = response.routes[0];
                //Icon as start position
                console.log(response)
                var markerDriver = new google.maps.Marker({
                  position: myRoute.legs[0].steps[0].start_point, 
                  map: map,
                  icon : "https://chart.googleapis.com/chart?chst=d_map_xpin_icon&chld=pin_star|car-dealer|00FFFF|FF0000"
                });
                console.log(currShuttle[0])
                //icone des points de ramassage
                for(var j in currShuttle[0].pickupLinks){
                    console.log(currShuttle[0].pickupLinks[j])
                    var markerWaypoint = new google.maps.Marker({
                        position: new google.maps.LatLng(currShuttle[0].pickupLinks[j].pickup.position.latitude,
                                                        currShuttle[0].pickupLinks[j].pickup.position.longitude),
                        map: map,
                        icon: "https://chart.googleapis.com/chart?chst=d_map_pin_icon&chld=wc-male|00FFFF"
                    });
                    attachInstructionText(markerWaypoint, currShuttle[0].pickupLinks[j].pickup.position.address);
                }

                //Icon as end position
                var finalLeg =  myRoute.legs[myRoute.legs.length-1];
                var markerSite = new google.maps.Marker({
                  position: finalLeg.steps[finalLeg.steps.length-1].end_point, 
                  map: map,
                  icon: "https://chart.googleapis.com/chart?chst=d_map_pin_icon&chld=repair|ADDE63"
                });
                attachInstructionText(markerDriver, currShuttle[0].driver.name.toUpperCase()+
                    " "+currShuttle[0].driver.firstName+
                    '<br/>'+currShuttle[0].driver.position.address);
                attachInstructionText(markerSite, currSite.numSite + '<br/>' + currSite.position.address);

            }
            else {
                alert("Error: " + status);
            }
        });

    //activation du bouton "supprimer" si droits suffisants
    if(sessionStorage.lvladminreq == 1 || sessionStorage.lvladminreq == 3){
        $("#cSuppr").removeClass("disabled");
    }
}
}

function attachInstructionText(marker, text) {
    google.maps.event.addListener(marker, 'click', function() {
      // Open an info window when the marker is clicked on,
      // containing the text of the step.
      stepDisplay = new google.maps.InfoWindow();
      stepDisplay.setContent(text);
      stepDisplay.open(map, marker);
    });
}

function completeTable() {
    $('#tab_Driver').empty();
    
    for (i = 0; i < currShuttle.length; i++) {
        var name = currShuttle[i].driver.name.toUpperCase()+" "+currShuttle[i].driver.firstName;
	var newText = 
		'<tr data-shuttleNum="'+ currShuttle[i].num +'">'
                +'<td>'+currShuttle[i]["phase"]["numWeek"]+'</td>'
		+'<td>'+name+'</td>'
		+ '</tr>';
	$('#tab_Driver').append(newText);
    }
}
        
        
/**
appelée lors de l'appui sur "supprimer"
*/
function deleteCar(){
    $("#supprModal").hide();
    console.log(currCar);
    var idToDelete = currCar.num;
    var data = new FormData();
    var s = 'num='+idToDelete;
    console.log(s);
    data.append('data', s);
    var req = "templates/proxy.php?url=http://localhost:5000/car/delete/";
    request(req, editionOk, data);
}

/**
appelée une fois la modification terminée avec succès
*/
function editionOk(xhr){
    var res = JSON.parse(xhr.responseText);

    localStorage.clear();
    if(res["code"]==1){
        reportSuccess(res["message"], null, "index.php?choix=3");
    }
    else{
        reportError(res["message"]);
    }   
}