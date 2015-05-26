var map;
var currentDate;
var links = [];
var shuttles = {};
var workers = [];
var drivers = [];
var pickups = {};
var charCountPickup = 1;
var charCountShuttle = 1;
var colors = ["blue", "green", "red", "purple", "brown", "grey"];
var rennes = new google.maps.LatLng(48.1134750,-1.6757080);
var geocoder = new google.maps.Geocoder();
var directionsService = new google.maps.DirectionsService();
var infoWindowP = new google.maps.InfoWindow();
var infoWindowW = new google.maps.InfoWindow();
var infoWindowS = new google.maps.InfoWindow();
var nbPlaceByShuttle = 5;


// ██████╗ ██████╗  █████╗ ██╗    ██╗    ███╗   ███╗ █████╗ ██████╗ 
// ██╔══██╗██╔══██╗██╔══██╗██║    ██║    ████╗ ████║██╔══██╗██╔══██╗
// ██║  ██║██████╔╝███████║██║ █╗ ██║    ██╔████╔██║███████║██████╔╝
// ██║  ██║██╔══██╗██╔══██║██║███╗██║    ██║╚██╔╝██║██╔══██║██╔═══╝ 
// ██████╔╝██║  ██║██║  ██║╚███╔███╔╝    ██║ ╚═╝ ██║██║  ██║██║     
// ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝     ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝    


/**
 * fonction qui permet de dessiner la map dans la div dont l'id est passé en paramètre
 * @param  {String} idDiv le nom de la div où placer la map
 * @return {void}
 */
function drawMap(idDiv) {

    // Déclaration des options de la map
    var optionsMap = {
        center : rennes,
        zoom : 12
    };
    
    //Ici, nous chargeons la map dans l'élément html ayant pour id "map"
    map = new google.maps.Map(document.getElementById(idDiv), optionsMap);
    google.maps.event.addListener(map, 'click', function() {
        infoWindowP.close();
        infoWindowW.close();
        infoWindowS.close();
    });

    showPosition(currSite.latitude, currSite.longitude);
}

/**
 * fonction permettant d'afficher un markeur sur la map au position (lati, longi)
 * @param  {int} lati la latitude du point à afficher
 * @param  {int} longi la longitude du point à afficher
 * @return {void}
 */
function showPosition (lati, longi) {

    currSite.mapPosition = new google.maps.LatLng(lati, longi);

    var bound = new google.maps.LatLngBounds(); 
    bound.extend(currSite.mapPosition);
    bound.extend(rennes);

    //affiche le marqueur du chantier
    currSite.marker = new google.maps.Marker({
        position: currSite.mapPosition,
        map: map
    });

    // recalage de la map
    map.fitBounds(bound);
}

/**
 * fonction permettant de dessiner un pickup sur la map
 * @param  {int} id L'id du pickup à dessiner
 * @return {void}
 */
function drawPickup(id){
    pickups[id].mapPosition = new google.maps.LatLng(pickups[id].pickup.position.latitude, pickups[id].pickup.position.longitude);

    // on construit notre marker avec l'icone qui va bien
    var icon = "https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + String.fromCharCode(64+charCountPickup) + "|00FD00|000000";
    
    // on affecte le marker crée au nouveau pickup
    pickups[id].marker = new google.maps.Marker({
        position: pickups[id].mapPosition,
        map: map,
        icon: icon
    });

    // on ajoute le numID
    pickups[id].numID = charCountPickup;
    
    // On oublie pas d'incrémenter charCountPickup
    charCountPickup += 1;
    
    // on ajoute l'evenement sur click pour le nouveau pickup 
    google.maps.event.addListener(pickups[id].marker, 'click', infoPickup(id));
}

/**
 * fonction permettant de supprimer un pickup de la map
 * @param  {int} id l'id du pickup à supprimer
 * @return {void}
 */
function erasePickup (id) {
    pickups[id].marker.setMap(null);
    infoWindowP.close();
}

/**
 * affiche les tracés et marqueurs liés à une navette
 * @param  {int} idShuttle l'id de la shuttle à afficher
 */
function drawShuttle(idShuttle, idMarker){
    drawDriver(idShuttle, idMarker);
    drawRoute(idShuttle);
    for(var p in shuttles[idShuttle].shuttle.passengers){
        drawLink(idShuttle, shuttles[idShuttle].shuttle.passengers[p]);
    }
}

/**
 * fonction permettant de dessiner le marker du conducteur d'une navette
 * @param  {int} id L'id de la navette à dessiner
 * @return {void}
 */
function drawDriver (id, idMarker) {
    // On récupere l'index dans le tableau workers, du conducteur de la navette
    var indexDriver = getWorkerById(shuttles[id].shuttle.driver.num);
    console.log(indexDriver, shuttles[id]);
    var icon;
    
    // on créer le marker de la navette
    if(idMarker == null || idMarker == undefined){
        icon = "https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + charCountShuttle + "|00ADFD|000000";
        shuttles[id].numID = charCountShuttle;
        charCountShuttle += 1;       
    }
    else{
        icon = "https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + idMarker + "|00ADFD|000000";
        shuttles[id].numID = idMarker;
    }
    
    // on ajoute le marker sur le départ de la navette (conducteur)
    shuttles[id].marker = new google.maps.Marker({
        position: workers[indexDriver].mapPosition,
        map: map,
        icon: icon
    });

    // On ajoute l'evenement sur click qui affiche l'infoWindow
    google.maps.event.addListener(shuttles[id].marker, 'click', infoShuttle(id));

    // et on efface le cercle du worker conducteur
    workers[indexDriver].circle.setMap(null);
    // et le lien si celui-ci existe
    if (workers[indexDriver].link){
        workers[indexDriver].link.setMap(null);
    }
}

/**
 * fonction permettant de tracer le chemin d'un passager vers sa navette
 * @param  {int} idS L'id de la navette concernée
 * @param  {object} passenger Le passenger à dessiner
 * @return {void}
 */
function drawLink (idS, passenger) {
    // On récupere l'index du worker dans le tableau workers
    var indexPassenger = getWorkerById(passenger.worker.num);
    var endPoint;
    // on cache le trait si déjà tracé
    if (workers[indexPassenger].link){
        workers[indexPassenger].link.setMap(null);
    } 
    // on regarde si le pickup du passenger est défini
    if (passenger.pickup && passenger.pickup.num){
        endPoint = pickups[passenger.pickup.num].mapPosition;
    } else {
        endPoint = workers[getWorkerById(shuttles[idS].shuttle.driver.num)].mapPosition;
    }
    workers[indexPassenger].link = new google.maps.Polyline({
        map : map,
        path: [workers[indexPassenger].mapPosition, endPoint],
        geodesic: true,
        strokeColor: "#ff0000",
        strokeOpacity: 0.5,
        strokeWeight: 1
    });
}

/**
 * fonction permettant de tracer le chemin d'un passager vers le chantier
 * @param  {int} idWorker L'id du worker
 * @return {void}
 */
function drawDirectLink (idWorker) {
    // On récupere l'index du worker dans le tableau workers
    var index = getWorkerById(idWorker);
    // on cache le trait si déjà tracé
    eraseLink(idWorker);

    var endPoint = currSite.mapPosition;
    workers[index].link = new google.maps.Polyline({
        map : map,
        path: [workers[index].mapPosition, endPoint],
        geodesic: true,
        strokeColor: "#ff0000",
        strokeOpacity: 0.5,
        strokeWeight: 1
    });
}

/**
 * fonction permettant d'effacer les lien entre les workers et l'endroit ou ils se rendent
 * Particulièrement utile lorsqu'on change les passagers d'une navette
 * @param  {int} workerId id du worker à effacer
 * @return {void}
 */
function eraseLink (workerId) {
    if (workers[getWorkerById(workerId)].link){
        workers[getWorkerById(workerId)].link.setMap(null);
    }
}

/**
 * efface tous les éléments UI d'une navette (marqueur, tracé et liens)
 * @param  {[type]} idS [description]
 * @return {[type]}     [description]
 */
function eraseShuttle (idS) {
    // suppression du marker de la navette
    shuttles[idS].marker.setMap(null);
    //suppression du tracé du trajet
    shuttles[idS].direction.setMap(null);
    //réaffichage du cercle autour du conducteur
    indexDriver = getWorkerById(shuttles[idS].shuttle.driver.num);
    workers[indexDriver].circle.setMap(map);
    //suppression des tracés des passagers
    for(var p in shuttles[idS].shuttle.passengers){
        eraseLink(shuttles[idS].shuttle.passengers[p].worker.num);
    }

}

/**
 * fonction qui dessine le chemin entre un conducteur et la destination d'une navette
 * @param  {int} idS L'id de la navette
 * @return {void}
 */
function drawRoute (idS) {
    // on cache la route si elle est déjà tracée
    if (shuttles[idS].direction){
        shuttles[idS].direction.setMap(null);
    } else {
        // sinon, on l'initialise
        shuttles[idS].direction = new google.maps.DirectionsRenderer({
            map: map,
            polylineOptions: {
              strokeColor: colors[shuttles[idS].numID-1],
              strokeOpacity: 0.4,
              strokeWeight: 4,
            },
            suppressMarkers : true
        });
    }

    // on fixe les point de départ et d'arrivé de la navette
    var origin = getDriverFromShuttle(idS).mapPosition;
    var destination = currSite.mapPosition;

    // on construit maintenant les différents point d'arrêt de la navette
    var wayPoints = [];

    for (var i in shuttles[idS].shuttle.pickups) {
        wayPoints.push({
            location: pickups[shuttles[idS].shuttle.pickups[i].num].mapPosition,
            stopover:true,
        });
    }
    // on construit la requete
    var request = {
        origin      : origin,
        destination : destination,
        waypoints   : wayPoints,
        travelMode  : google.maps.DirectionsTravelMode.DRIVING,
        optimizeWaypoints:true
    };

    directionsService.route(request, function(response, status){ // Envoie de la requête pour calculer le parcours
        if(status == google.maps.DirectionsStatus.OK){
            shuttles[idS].direction.setDirections(response); // Trace l'itinéraire sur la carte et les différentes étapes du parcours
            shuttles[idS].direction.setMap(map);
        }
        else
        {
            reportError("Erreur Google Maps : "+status);
        }
    });
}


//  ██████╗ ███████╗████████╗    ███████╗██████╗  ██████╗ ███╗   ███╗    ██████╗ ██████╗ ██████╗ 
// ██╔════╝ ██╔════╝╚══██╔══╝    ██╔════╝██╔══██╗██╔═══██╗████╗ ████║    ██╔══██╗██╔══██╗██╔══██╗
// ██║  ███╗█████╗     ██║       █████╗  ██████╔╝██║   ██║██╔████╔██║    ██████╔╝██║  ██║██║  ██║
// ██║   ██║██╔══╝     ██║       ██╔══╝  ██╔══██╗██║   ██║██║╚██╔╝██║    ██╔══██╗██║  ██║██║  ██║
// ╚██████╔╝███████╗   ██║       ██║     ██║  ██║╚██████╔╝██║ ╚═╝ ██║    ██████╔╝██████╔╝██████╔╝
//  ╚═════╝ ╚══════╝   ╚═╝       ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝    ╚═════╝ ╚═════╝ ╚═════╝


/**
 * fonction permettant de charger la grande carte permettant d'éditer les navettes
 * @return {void}
 */
function loadBigMap(){
    drawMap("bigMap");

    // création des boutons d'ajout et suppression de pickup
    $("#status").append("<div id='modPickup'>"+
                            "<br/>"+
                            "<button id='addPickup' style='width:150px' type='button' onclick='addPickupEvent()' class='btn btn-success btn-sm'>Ajouter un point d'arrêt</button>"+
                            "</div>");

    // requete pour récupérer les pickups
    var data = new FormData();
    data.append("data", "idSite="+currSite.num);
    request("templates/proxy.php?url=http://localhost:5000/pickup/bySite/", getPickups, data);
}

/**
 * fonction permettant de stocker les pickups associés au chantier courant dans la variable pickups
 * @param  {object} xhr La réponse de la requête flask
 * @return {void}
 */
function getPickups (xhr) {
    var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        var pickupsTemp = JSON.parse(resp["data"]);
        pickupsTemp.sort(function(a,b){return a.num > b.num;});
        for (var i = 0; i < pickupsTemp.length; i++) {
            pickups[pickupsTemp[i].num] = {"pickup": pickupsTemp[i]};
            drawPickup(pickupsTemp[i].num);
        }

        // requete pour récupérer les véhicules
        var now = new Date();
        currentDate = {"week": now.getWeekNumber(), "year": now.getFullYear()};
        requestCars(getCars);
    }
}

function requestCars (callBack) {
    var data = new FormData();
    data.append("data", "idSite="+currSite.num+"^week="+currentDate.week+"^year="+currentDate.year);
    request("templates/proxy.php?url=http://localhost:5000/car/unused/forweek/", callBack, data);
}

/**
 * fonction permettant de stocker les véhicules récupérés grâce à Flask dans la varible cars
 * @param  {object} xhr La réponse de la requête flask
 * @return {void}
 */
function getCars (xhr) {
    var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        cars = JSON.parse(resp["data"]);
        cars.sort(function(a,b){return a.model > b.model;});

        // On récupère maintenant les ouvriers
        requestWorkers(getWorkers);
    }
}

/**
 * fonction permettant de récuperer les workers qui sont en base
 * @param  {function} callBack Fonction appelé lorsque la requete à rendue réponse
 * @return {void}
 */
function requestWorkers (callBack) {
    var data = new FormData();
    data.append('data', 'idSite='+currSite.num+'^week='+currentDate.week+'^year='+currentDate.year);
    request("templates/proxy.php?url=http://localhost:5000/worker/assigned/bysite/byweek/", callBack, data);
}

/**
 * fonction permettant de récupérer les ouvriers affectés sur ce chantier pour la semaine courante
 * @param {object} xhr La réponse de la requête flask
 * @return {void}
 */
function getWorkers (xhr) {
    var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        workers = JSON.parse(resp["data"]);
        if (workers.length > 0){
            workers.sort(function(a, b){return a.firstName > b.firstName;});
            drawWorkers();
        }
    }
}

/**
 * fonction permettant de dessiner les ouvriers sur la map et de leurs attacher les evenements dont ils ont besoin
 * @return {[type]} [description]
 */
function drawWorkers () {
    var positions = new Object();
    for (var i = 0; i < workers.length; i++) {
        // on ajoute la position sur la map de chaque ouvrier
        workers[i].mapPosition = new google.maps.LatLng(workers[i].position.latitude, workers[i].position.longitude);

        // on ajoute la position au tableau si elle n'y est pas déjà
        if (positions[workers[i].mapPosition]){
            workers[i].mapPosition = new google.maps.LatLng(workers[i].position.latitude+0.001, workers[i].position.longitude+0.001);
        } else {
            positions[workers[i].mapPosition] = true;
        }
        // on dessine maintenant l'ouvrier
        workers[i].circle = new google.maps.Circle({
            map: map,
            center: workers[i].mapPosition,
            radius: 200,    // 10 miles in metres
            fillColor: '#AA0000'
        });

        // on ajoute maintenant l'evenement sur click qui permet d'afficher l'infoWindow d'un worker
        google.maps.event.addListener(workers[i].circle, 'click', infoWorker(i));
    }

    requestShuttles(getShuttles, currentDate.week, currentDate.year);
}

/**
 * fonction permettant de récuperer les navettes qui sont en base
 * @param  {function} callBack Fonction appelé lorsque la requete à rendue réponse
 * @return {void}
 */
function requestShuttles (callBack, week, year) {
    // récupération des navettes en base
    var data = new FormData();
    data.append('data', 'idSite='+currSite.num+'^week='+week+'^year='+year);
    request("templates/proxy.php?url=http://localhost:5000/shuttle/bysite/byweek/", callBack, data);
}

/**
 * fonction permettant de récupérer les navettes associées à ce chantier pour la semaine courante
 * @param  {object} xhr La réponse de la requête flask
 * @return {void}
 */
function getShuttles (xhr) {
    var resp = JSON.parse(xhr.responseText);
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        var shuttlesTemp = JSON.parse(resp["data"]);
        shuttles = {};
        for (var i = 0; i < shuttlesTemp.length; i++) {
            shuttles[shuttlesTemp[i].num] = {"shuttle": shuttlesTemp[i]};
            
            // on affiche la navette
            drawShuttle(shuttlesTemp[i].num);
        }
        lookAtPreviousWeek();
    }
}

/**
 * fonction qui envoi la requete pour récuperer les navettes de la semaine précédente
 * @return {void}
 */
function lookAtPreviousWeek () {
    var week = currentDate.week-1;
    var year = currentDate.year;
    if (week == 0){
        week = year52_53(new Date(currentDate.year-1, 1 ,1));
        year = year - 1;
    }
    requestShuttles(getPreviousShuttles, week, year);
}

/**
 * fonction qui récupere les navettes de la semaine précédente et qui
 * test si on peut redessiner cette navette ou non pour la semaine courante
 * @param  {object} xhr La réponse de la requete
 * @return {void}
 */
function getPreviousShuttles (xhr) {
    var resp = JSON.parse(xhr.responseText);
    var previousShuttles;
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        previousShuttles = JSON.parse(resp["data"]);
        for (var i = 0; i < previousShuttles.length; i++) {
            var indexDriver = getWorkerById(previousShuttles[i].driver.num);
            // si le conducteur de la navette est toujours présent cette semaine
            if (indexDriver != -1 && isDriver(previousShuttles[i].driver.num) == -1 && isPassenger(previousShuttles[i].driver.num) == null) {
                requestCarIsUsed(previousShuttles[i]);
            }
        }
        directLessThenFiftheen();
    }
}

/**
 * fonction permettant d'executer la requete qui nous dit si le véhicule de la navette est déjà utilisé
 * @param  {object} shuttle La navette concerné
 * @return {void}
 */
function requestCarIsUsed (shuttle) {
    var data = new FormData();
    var week = shuttle.phase.numWeek + 1;
    var year = shuttle.phase.numYear;
    if (week > year52_53(new Date(year, 1, 1))){
        week = 1;
        year = year + 1;
    }
    data.append("data", "week="+week+"^year="+year+"^idCar="+shuttle.car.num);
    request("templates/proxy.php?url=http://localhost:5000/car/isused/forweek/", getCarResponse, data, shuttle);
}

/**
 * fonction de récupération de la requete nous permettant de savoir si le véhicule d'une navette est utilisé
 * @param  {object} xhr     La réponse de la requete
 * @param  {object} shuttle La navette concernée
 * @return {void}
 */
function getCarResponse (xhr, shuttle) {
    var resp = JSON.parse(xhr.responseText);
    var response;
    if(resp["code"] != 1){
        reportError(resp["message"]);
    }
    else{
        response = JSON.parse(resp["data"]);
        // si la voiture n'est pas utilisée, on peut redessiner la navette
        if (!response){

            var idDriver = shuttle.driver.num;
            var idCar = shuttle.car.num;
            var idPhase = currSite.phases[currentDate.year][currentDate.week].num;
            var idPickups = [];
            var passengers = [];

            for (var i in shuttle.pickups) {
                idPickups.push(shuttle.pickups[i].num);
            }

            for (var j in shuttle.passengers){
                var idW = shuttle.passengers[j].worker.num;
                // on vérifie que les passagers sont toujours présent sur la semain courante
                if (getWorkerById(idW) != -1){
                    // puis que le worker n'est pas conducteur ou passager d'une autre navette
                    if (isPassenger(idW) == null && isDriver(idW) == -1){
                        passengers.push({'idWorker':idW,
                                         'idPickup':findBestLink(workers[getWorkerById(idDriver)].mapPosition,
                                                                workers[getWorkerById(idW)].mapPosition,
                                                                idPickups)});
                    }
                }
            }

            addShuttle(idDriver, idCar, idPhase, idPickups, passengers);
        }
    }
}

/**
 * fonction qui met les ouvriers directement sur le chantier si ceux-ci ne sont ni passagers,
 * ni conducteurs, et qu'ils sont à moins de 15 kilomètre du chantier
 * @return {void}
 */
function directLessThenFiftheen () {
    for (var i=0; i < workers.length; i++){
        var idW = workers[i].num;
        // si l'ouvrier n'est ni conducteur, ni passager d'une navette
        if (isPassenger(idW) == null && isDriver(idW) == -1){
            var distance = getDistance(workers[i].mapPosition, currSite.mapPosition);
            // On vérifie qu'il soit à moins de 15 km du chantier
            if (distance < 15000){
                setWorkerAsDirect(workers[i].num);
            }
        }
    }
}

/**
 * fonction permettant de changer de semaine
 * @param  {object} target La semaine cible sur laquelle on viens de cliquer
 * @return {void}
 */
function changeWeek (target) {
    var weekNumberNow = new Date().getWeekNumber();
    var numYear = new Date().getFullYear();
    var weekTarget = parseInt(target, 10);
    // On teste si le numero de semaine sur lequel on a cliqué est inférieur
    // au numero de semaine courante car si c'est le cas, c'est l'année suivante
    if (weekTarget < weekNumberNow){
        numYear += 1;
    }
    resetSettings();
    currentDate = {"week": weekTarget, "year": numYear};
    selectOne("tabShuttle", weekTarget);
    requestCars(getCars);
}

/**
 * fonction qui réinitialise les différents tableau lors du changement de semain
 * @return {void}
 */
function resetSettings () {
    charCountShuttle = 1;
    for (var i in shuttles){
        shuttles[i].marker.setMap(null);
        shuttles[i].direction.setMap(null);
    }
    for (var j in workers){
        workers[j].circle.setMap(null);
        eraseLink(workers[j].num);
    }
}


// ███████╗██╗   ██╗███████╗███╗   ██╗███████╗███╗   ███╗███████╗███╗   ██╗████████╗███████╗
// ██╔════╝██║   ██║██╔════╝████╗  ██║██╔════╝████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
// █████╗  ██║   ██║█████╗  ██╔██╗ ██║█████╗  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ███████╗
// ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ╚════██║
// ███████╗ ╚████╔╝ ███████╗██║ ╚████║███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ███████║
// ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝


/**
 * fonction permettant de gérer les events pour l'ajout des pickup sur la carte
 */
function addPickupEvent () {

    // on construit notre marker avec l'icone qui va bien
    var icon = "https://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=" + String.fromCharCode(64+charCountPickup) + "|00FD00|000000";
    
    // on affecte le marker crée au nouveau pickup
    var marker = new google.maps.Marker({
        map: map,
        icon: icon
    });

    // On ajoute le listener pour que le marker suive la souris
    var listenerHandler = google.maps.event.addListener(map, 'mousemove', function(e) {
        marker.setPosition(e.latLng);
    });

    // On supprime temporairement l'event sur click sur le bouton pour pouvoir faire une annulation
    var button = $("#addPickup");
    button.attr('onclick', '');
    button.on('click', function() {
        listenerHandler.remove();
        marker.setMap(null);
        $(this).off('click');
        // Remise du texte sur le bouton
        button.html("Ajouter un point d'arrêt'");
        button.attr('class', 'btn btn-success btn-sm');
        button.attr('onclick', 'addPickupEvent()');
    });
    
    button.attr('class', 'btn btn-warning btn-sm');
    // On passe le bouton en "Annuler"
    button.html("Annuler");

    // Et on ajoute le listener qui supprime le listener précédent dès qu'on clique sur le marker
    google.maps.event.addListener(marker, 'click', function(){
        
        // suppression sur le listener précédent
        listenerHandler.remove();
        
        // Remise du texte sur le bouton
        button.off('click');
        button.html("Ajouter un point d'arrêt");
        button.attr('class', 'btn btn-success btn-sm');
        button.attr('onclick', 'addPickupEvent()');

        // requête permettant d'avoir l'adresse correspondant à l'endroit  où on à déposé le marker
        geocoder.geocode({'latLng': marker.getPosition()}, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[1]) {
                    // appelle à la fonction pour répercuter les changement
                    addPickup(marker.getPosition().lat(), marker.getPosition().lng(), results[1].formatted_address);
                    marker.setMap(null);
                } else {
                    console.log('No results found');
                }
            } else {
                console.log('Geocoder failed due to: ' + status);
            }
        });
    });
}

/**
 * fonction qui créer l'infoWindow et l'affiche sur la map pour les pickup
 * @param  {int} id L'id du pickup où l'on doit attacher l'infoWindow
 * @return {void}
 */
function infoPickup (id) {
    return function() {
        // on ferme les autre popUp
        infoWindowW.close();
        infoWindowS.close();
        infoWindowP.setContent("<div class='info'>"+pickups[id].pickup.position.address+ "<br/><p>Supprimer ce pickup ?</p>"+
                                                    "<button type='button' class='btn btn-danger btn-sm' "+
                                                    "style='margin: 0px 10px'"+
                                                    "onclick='removePickup("+id+")'>"+
                                                    "Oui</button>"+
                                                    "<button type='button' class='btn btn-success btn-sm' "+
                                                    "style='margin: 0px 10px'"+
                                                    "onclick='infoWindowP.close();'>"+
                                                    "Non</button></div>");
        infoWindowP.open(map, pickups[id].marker);
    };
}

/**
 * fonction permettant d'afficher l'infoWindow d'un ouvrier
 * @param  {int} index L'index du worker
 * @return {void}
 */
function infoWorker (index) {
    return function() {
        // on ferme les autre popUp
        infoWindowP.close();
        infoWindowS.close();
        // on supprime l'event sur le dom pour recharger toute la popup à la prochaine ouverture
        if (infoWindowW.handler){
            infoWindowW.handler.remove();
        }
        var passenger = isPassenger(workers[index].num);
        var content = "<div class='info infoWorker'><h3>"+capitalize(workers[index].firstName)+" "+capitalize(workers[index].name)+"</h3> \
                        <h4>"+capitalize(workers[index].craft.name)+" "+capitalize(workers[index].qualification.name)+"</h4> \
                        <h4>"+capitalize(workers[index].position.address)+"</h4> \
                            <form>";
        // Si l'ouvrier est passager d'un navette
        if (passenger) {
            content +=  "<input type='radio' name='route' value='0' onclick='disableMultiselect(); setWorkerAsDirect("+workers[index].num+")'> Se rend au chantier</br>\
                        <input id='passengerRadio' type='radio' name='route' value='1' onchange='enableMultiselect()' checked> Passager de la navette :\
                        <select id='selectShuttle' class='multiselect' multiple>";
        // Sinon, il va directement au chantier
        } else {
            content += "<input type='radio' name='route' value='0' onclick='disableMultiselect(); setWorkerAsDirect("+workers[index].num+")' checked> Se rend au chantier</br>\
                        <input id='passengerRadio' type='radio' name='route' value='1' onchange='enableMultiselect()'> Passager de la navette : \
                        <select id='selectShuttle' class='multiselect' multiple disabled>";
        }
        // Ajout de la liste des navettes
        for (var i in shuttles) {
            if (passenger && i == passenger.idShuttle){
                content += "<option value='"+i+"' selected>Navette "+shuttles[i].numID+"</option>";
            } else {
                content += "<option value='"+i+"'>Navette "+shuttles[i].numID+"</option>";
            }
        }
        // fermeture du multiselect
        content +=      "</select>";
        // Puis si l'ouvrier est sur une navette, on affiche les pickups liés
        if (passenger){
            content += "<select id='selectPickup' class='multiselect'>\
                            <option value='0' selected>Aucun point d'arrêt</option>";
            // ajout de la liste des pickups
            for (var j in shuttles[passenger.idShuttle].shuttle.pickups) {
                if (passenger.pickup && passenger.pickup.num == shuttles[passenger.idShuttle].shuttle.pickups[j].num){
                    content += "<option value='"+j+"' selected>Point d'arrêt "+String.fromCharCode(64+pickups[j].numID)+"</option>";
                } else {
                    content += "<option value='"+j+"'>Point d'arrêt "+String.fromCharCode(64+pickups[j].numID)+"</option>";
                }
            }
            content += "</select>";
        } else {
            // sinon on affiche un multiselect avec aucun chois.
            content += "<select id='selectPickup' class='multiselect' disabled>\
                            <option value='0' selected>Aucun point d'arrêt</option>\
                        </select>";
        }
        
        content +=      "</br><input id='driverRadio' type='radio' name='route' value='2' onclick='disableMultiselect()'> Conducteur de la navette : ";

        content += "<select id='selectShuttle2' multiple disabled>\
                        <option value='-1'>Nouvelle navette</option>";
        // Ajout de la navette dont le worker est passager
        var passTemp = isPassenger(workers[index].num);
        if (passTemp){
            content += "<option value='"+passTemp.idShuttle+"'>Navette "+shuttles[passTemp.idShuttle].numID+"</option>";
        }

        content += "</select>";

        content += "</form><div/>";
        
        infoWindowW.setContent(content);

        infoWindowW.handler = google.maps.event.addListener(infoWindowW, 'domready', function() {
            $(document).ready(function() {
                $('#selectShuttle').multiselect({
                    nonSelectedText: "Aucune selection",
                    numberDisplayed: 1,
                    buttonClass: 'btn btn-default btn-sm',
                    maxHeight: 150,
                    onChange: changePassengerOfShuttle(workers[index].num)
                });
                $('#selectPickup').multiselect({
                    nonSelectedText: "Aucune selection",
                    numberDisplayed: 1,
                    maxHeight: 150,
                    buttonClass: 'btn btn-default btn-sm',
                    onChange: changePickupOfPassenger(workers[index].num)
                });
                $('#selectShuttle2').multiselect({
                    nonSelectedText: "Aucune selection",
                    numberDisplayed: 1,
                    buttonClass: 'btn btn-default btn-sm',
                    maxHeight: 150,
                    onChange: changeWorkerAsDriver(workers[index].num)
                });
            });
        });

        infoWindowW.setPosition(workers[index].mapPosition);
        infoWindowW.open(map);
    };
}

/**
 * fonction permettant d'afficher l'infoWindow d'une navette
 * @param  {int} id L'id de la navette
 * @return {void}
 */
function infoShuttle (id) {
    return function() {
        // on ferme les autre popUp
        infoWindowP.close();
        infoWindowW.close();
        // on supprime l'event sur le dom pour recharger toute la popup à la prochaine ouverture
        if (infoWindowS.handler){
            infoWindowS.handler.remove();
        }
        infoWindowS.nbPlace = 0;
        var bool;
        var content =   "<div class='info infoShuttle'>"+
                            "<form class='form-horizontal' role='form'>"+
                                "<div class='form-group'>"+
                                    "<div class='col-sm-8'>"+
                                        "<h3>Navette "+shuttles[id].numID+"</h3>"+
                                    "</div>"+
                                "</div>"+
                                "<div class='form-group'>"+
                                    "<label for='driver' class='col-sm-4 control-label'>Conducteur :</label>"+
                                    "<div class='col-sm-8'>"+
                                        "<p class='form-control-static'>"+capitalize(shuttles[id].shuttle.driver.firstName)+" "+capitalize(shuttles[id].shuttle.driver.name)+"</p>"+
                                    "</div>"+
                                "</div>"+
                                "<div class='form-group'>"+
                                    "<label for='cars' class='col-sm-4 control-label'>Véhicule :</label>"+
                                    "<div class='col-sm-8'>"+
                                        "<select id='selectCars' class='multiselect'>";

        // Ajout de la liste des véhicules
        for (var k = 0; k < cars.length; k++) {
            if (cars[k].num == shuttles[id].shuttle.car.num){
                infoWindowS.nbPlace = cars[k].nbPlace;
                content += "<option value='"+cars[k].num+"' selected>"+
                                capitalize(cars[k].model)+" ("+cars[k].nbPlace+ " places)"
                            "</option>";
            } else {
                content += "<option value='"+cars[k].num+"'>"+
                                capitalize(cars[k].model)+" ("+cars[k].nbPlace+ " places)"
                            "</option>";
            }
        }

        // fermeture du multiselect des véhicules
        content += "</select></div></div>";

        // on continue avec les passagers
        content += "<div class='form-group'>"+
                        "<label for='passengers' class='col-sm-4 control-label'>Passagers :</label>"+
                        "<div class='col-sm-8'>"+
                            "<select id='selectPassengers' class='multiselect' multiple='multiple'>";
                                
        // Ajout de la liste des ouvriers pouvant être passagers
        for (var j = 0; j < workers.length; j++){
            bool = false;
            for (var l in shuttles[id].shuttle.passengers) {
                if (workers[j].num == shuttles[id].shuttle.passengers[l].worker.num){
                    bool = true;
                }
            }
            if (bool){
                content += "<option value='"+workers[j].num+"' selected>"+capitalize(workers[j].firstName)+" "+capitalize(workers[j].name)+"</option>";
            } else {
                content += "<option value='"+workers[j].num+"'>"+capitalize(workers[j].firstName)+" "+capitalize(workers[j].name)+"</option>";
            }
        }

        // fermeture du multiselect des passagers
        content += "</select></div></div>";

        // On continue avec les points d'arrêts
        content += "<div class='form-group'>"+
                        "<label for='pdr' class='col-sm-4 control-label'>Points d'arrêts :</label>"+
                        "<div class='col-sm-8'>"+
                            "<div id='selectPickups' class='btn-group' data-toggle='buttons'>";

        // Ajout de les bouton pour chaque points d'arrêt
        for (var i in pickups) {
            bool = false;
            for (var m in shuttles[id].shuttle.pickups) {
                if (pickups[i].pickup.num == shuttles[id].shuttle.pickups[m].num){
                    bool = true;
                    content +=  "<label value='"+i+"' class='btn btn-default btn-xs active'>"+
                                    "<input type='checkbox'>PR "+String.fromCharCode(64+pickups[i].numID)+
                                "</label>";
                    break;
                }
            } 
            if (!bool) {
                content +=  "<label value='"+i+"' class='btn btn-default btn-xs'>"+
                                "<input type='checkbox'>PR "+String.fromCharCode(64+pickups[i].numID)+
                            "</label>";
            }
        }

        // fermeture des points d'arrêts
        content += "</div></div></div>";

        // On termine avec les boutons de confirmation et d'annulation
        content +=  "<div class='form-group'>"+
                        "<div class='col-sm-offset-2 col-sm-7'>"+
                            "<p>"+
                                "<button type='button' onclick='updateShuttle("+id+");' class='btn btn-default btn-sm'>Valider</button>"+
                                "<button type='button' onclick='infoWindowS.close();' class='btn btn-default btn-sm'>Annuler</button>"+
                                "<button type='button' onclick='infoWindowS.close(); removeShuttle("+id+");' class='btn btn-danger btn-sm'>Supprimer</button>"+                                
                            "</p"+
                        "</div>"+
                    "</div></form>";

        infoWindowS.setContent(content);
        
        infoWindowS.handler = google.maps.event.addListener(infoWindowS, 'domready', function() {
            $(document).ready(function() {
                $('#selectPassengers').multiselect({
                    enableCaseInsensitiveFiltering: true,
                    nonSelectedText: "Aucune selection",
                    filterPlaceholder: 'Rechercher',
                    numberDisplayed: 1,
                    buttonClass: 'btn btn-default btn-sm',
                    maxHeight: 150,
                    onChange: maximumSelect()
                });
                $('#selectCars').multiselect({
                    enableCaseInsensitiveFiltering: true,
                    nonSelectedText: "Aucune selection",
                    filterPlaceholder: 'Rechercher',
                    numberDisplayed: 1,
                    buttonClass: 'btn btn-default btn-sm',
                    maxHeight: 150,
                    onChange: function(option, checked){infoWindowS.nbPlace = cars[getCarById(option[0].value)].nbPlace; $("#selectPassengers").each(maximumSelect());}
                });
                // event sur les elements de la liste de passagers
                $('#selectPassengers + div li a').on('mouseover', function(event){showWorker(event);});
                $('#selectPassengers + div li a').on('mouseout', function(event){resetWorker(event);});
            });
            $("#selectPassengers").each(maximumSelect());
        });

        infoWindowS.open(map, shuttles[id].marker);
    };
}

/**
 * Fonction qui affiche l'infoWindow pour une nouvelle navette
 * @param  {int} idDriver L'id du conducteur de cette nouvelle navette
 * @return {void}
 */
function infoNewShuttle (idDriver) {
    // on ferme les autre popUp
    infoWindowP.close();
    infoWindowW.close();
    // on supprime l'event sur le dom pour recharger toute la popup à la prochaine ouverture
    if (infoWindowS.handler){
        infoWindowS.handler.remove();
    }
    //infoWindowS.nbPlace = 0;
    // var bool;
    var driver = workers[getWorkerById(idDriver)];
    var content =   "<div class='info infoShuttle'>"+
                        "<form class='form-horizontal' role='form'>"+
                            "<div class='form-group'>"+
                                "<div class='col-sm-7'>"+
                                    "<h3>Navette "+charCountShuttle+"</h3>"+
                                "</div>"+
                            "</div>"+
                            "<div class='form-group'>"+
                                "<label for='driver' class='col-sm-5 control-label'>Conducteur :</label>"+
                                "<div class='col-sm-7'>"+
                                    "<p class='form-control-static'>"+driver.firstName+" "+driver.name+"</p>"+
                                "</div>"+
                            "</div>"+
                            "<div class='form-group'>"+
                                "<label for='cars' class='col-sm-5 control-label'>Véhicule :</label>"+
                                "<div class='col-sm-7'>"+
                                    "<select id='selectCars' class='multiselect'>";

    // Ajout de la liste des véhicules
    for (var k = 0; k < cars.length; k++) {
        content += "<option value='"+cars[k].num+"'>"+
                                capitalize(cars[k].model)+" ("+cars[k].nbPlace+ " places)"
                    "</option>";
    }

    // fermeture du multiselect des véhicules
    content += "</select></div></div>";

    // on continue avec les passagers
    content += "<div class='form-group'>"+
                    "<label for='passengers' class='col-sm-5 control-label'>Passagers :</label>"+
                    "<div class='col-sm-7'>"+
                        "<select id='selectPassengers' class='multiselect' multiple='multiple'>";
                            
    // Ajout de la liste des ouvriers pouvant être passagers (les ouvrier libres)
    var freeWorkers = getFreeWorkers(driver);
    
    for (var j = 0; j < freeWorkers.length; j++){
        content += "<option value='"+freeWorkers[j].num+"'>"+capitalize(freeWorkers[j].firstName)+" "+capitalize(freeWorkers[j].name)+"</option>";
    }

    // fermeture du multiselect des passagers
    content += "</select></div></div>";

    // On continue avec les points d'arrêts
    content += "<div class='form-group'>"+
                    "<label for='pdr' class='col-sm-5 control-label'>Points d'arrêts :</label>"+
                    "<div class='col-sm-7'>"+
                        "<div id='selectPickups' class='btn-group' data-toggle='buttons'>";

    // Ajout de les bouton pour chaque points d'arrêt
    for (var i in pickups) {
        content +=  "<label value='"+i+"' class='btn btn-default btn-xs'>"+
                        "<input type='checkbox'>PR "+String.fromCharCode(64+pickups[i].numID)+
                    "</label>";
    }

    // fermeture des points d'arrêts
    content += "</div></div></div>";

    // On termine avec les boutons de confirmation et d'annulation
    content +=  "<div class='form-group'>"+
                    "<div class='col-sm-offset-2 col-sm-10'>"+
                        "<p>"+
                            "<button type='button' onclick='newShuttle("+idDriver+");' class='btn btn-default'>Valider</button>"+
                            "<button type='button' onclick='infoWindowS.close();' class='btn btn-default'>Annuler</button>"+
                        "</p"+
                    "</div>"+
                "</div></form>";

    infoWindowS.setContent(content);
    
    infoWindowS.handler = google.maps.event.addListener(infoWindowS, 'domready', function() {
        $(document).ready(function() {
            $('#selectPassengers').multiselect({
                enableCaseInsensitiveFiltering: true,
                nonSelectedText: "Aucune selection",
                filterPlaceholder: 'Rechercher',
                numberDisplayed: 1,
                buttonClass: 'btn btn-default btn-sm',
                maxHeight: 150,
                onChange: maximumSelect()
            });
            $('#selectCars').multiselect({
                enableCaseInsensitiveFiltering: true,
                nonSelectedText: "Aucune selection",
                filterPlaceholder: 'Rechercher',
                numberDisplayed: 1,
                buttonClass: 'btn btn-default btn-sm',
                maxHeight: 150,
                onChange: function(option, checked){infoWindowS.nbPlace = cars[getCarById(option[0].value)].nbPlace; $("#selectPassengers").each(maximumSelect());}
            });
            // event sur les elements de la liste de passagers
            $('#selectPassengers + div li a').on('mouseover', function(event){showWorker(event);});
            $('#selectPassengers + div li a').on('mouseout', function(event){resetWorker(event);});
        });
        $("#selectPassengers").each(maximumSelect());
    });
    infoWindowS.setPosition(driver.mapPosition);
    infoWindowS.open(map);
}

/**
 * fonction permettant d'activer les multiselect shuttle et pickup
 * @return {void}
 */
function enableMultiselect () {
    $("#selectShuttle").multiselect('enable');
    $("#selectShuttle2").multiselect('disable');
    $("#selectPickup").multiselect('enable');
}

/**
 * fonction permettant de désactiver les multiselect shuttle et pickup
 * @return {void}
 */
function disableMultiselect () {
    $('#selectShuttle option').each(function(element) {
        $('#selectShuttle').multiselect('deselect', $(this).val());
    });
    $("#selectPickup").multiselect('select', 0);
    $("#selectShuttle").multiselect('disable');
    $("#selectPickup").multiselect('disable');
    if (document.getElementById("driverRadio").checked){
        $("#selectShuttle2").multiselect('enable');
    } else {
        $("#selectShuttle2").multiselect('disable');
    }
}

/**
 * fonction permettant de simuler un select r
 * @param  {object} option  L'option sur lequel on à cliqué
 * @param  {bool} checked Booléen qui indique si l'option cliquée est selectionnée
 * @param {String} id L'id du multiselect visé
 * @return {void}
 */
function simulateRadio (option, checked, id) {
    var values = [];
    $("#"+ id + ' option').each(function() {
        if ($(this).val() !== option.val()) {
            values.push($(this).val());
        }
    });
    $("#" + id).multiselect('deselect', values);
}

/**
 * fonction permettant de désactiver les options passager lorsqu'on arrive à la limite de capacité du véhicule
 * @return {void}
 */
function maximumSelect () {
    return function(option, checked) {
        // Récupération des options selectionnées.
        var selectedOptions = $('#selectPassengers option:selected');
         
        if (selectedOptions.length >= infoWindowS.nbPlace-1) {
            // Désactivation de toute les autres options
            var nonSelectedOptions = $('#selectPassengers option').filter(function() {
                return !$(this).is(':selected');
            });
         
            nonSelectedOptions.each(function() {
                var input = $('#selectPassengers + div input[value="' + $(this).val() + '"]');
                input.prop('disabled', true);
                input.parent('li').addClass('disabled');
            });
        } else {
            // Sinon, on ré-active toutes les options.
            $('#selectPassengers option').each(function() {
                var input = $('#selectPassengers + div input[value="' + $(this).val() + '"]');
                input.prop('disabled', false);
                input.parent('li').addClass('disabled');
            });
        }
    };
}

/**
 * fonction qui agrandit le cercle des ouvriers pour mieux les identifier
 * @param  {object} event L'evenement déclencheur
 * @return {void}
 */
function showWorker (event) {
    var  element = event.target;
    if (element.nodeName != 'INPUT'){
        element = element.getElementsByTagName('input')[0];
    }
    workers[getWorkerById(element.value)].circle.setRadius(1000);
}

function resetWorker (event) {
    var  element = event.target;
    if (element.nodeName != 'INPUT'){
        element = element.getElementsByTagName('input')[0];
    }
    workers[getWorkerById(element.value)].circle.setRadius(200);
}


//  ██████╗ █████╗  ██████╗██╗   ██╗██╗     ███████╗
// ██╔════╝██╔══██╗██╔════╝██║   ██║██║     ██╔════╝
// ██║     ███████║██║     ██║   ██║██║     ███████╗
// ██║     ██╔══██║██║     ██║   ██║██║     ╚════██║
// ╚██████╗██║  ██║╚██████╗╚██████╔╝███████╗███████║
//  ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚══════╝
 
/**
 * fonction qui permet de trouver quel est le pickup le plus près d'un ouvrier
 * @param  {object} driverPosition La position du conducteur de la navette
 * @param  {object} workerPosition La position de l'ouvrier
 * @param  {[int]} idPickups      Un tableau avec les id des pickups potentiels
 * @return {int}                L'id du pickup le plus proche ou null si l'ouvrier rejoint le conducteur
 */
function findBestLink (driverPosition, workerPosition, idPickups) {
    var distanceMin =   getDistance(workerPosition, driverPosition);
    var result = null;
    for (var i in idPickups) {
        var position = pickups[idPickups[i]].mapPosition;
        var distanceTemp =  getDistance(workerPosition, position);
        if (distanceTemp < distanceMin){
            distanceMin = distanceTemp;
            result = idPickups[i];
        }
    }
    return result;

}


// ██╗   ██╗████████╗██╗██╗     ███████╗
// ██║   ██║╚══██╔══╝██║██║     ██╔════╝
// ██║   ██║   ██║   ██║██║     ███████╗
// ██║   ██║   ██║   ██║██║     ╚════██║
// ╚██████╔╝   ██║   ██║███████╗███████║
//  ╚═════╝    ╚═╝   ╚═╝╚══════╝╚══════╝


/**
 * fonction permettant de mettre à jour une navette après validation des changements sur la popUp
 * @param  {int} idS L'id de navette à mettre à jour
 * @return {void}
 */
function updateShuttle (idS) {
    // récupération des id des différentes information de la navette
    var idDriver = shuttles[idS].shuttle.driver.num;
    var idCar = $('#selectCars option:selected')[0].value;
    var idPassengers = [];
    var selectedPassengers = $('#selectPassengers option:selected');
    var idPickups = [];
    var selectedPickups = $('#selectPickups .active');
    for (var j = 0; j < selectedPickups.length; j++) {
        idPickups.push(parseInt(selectedPickups[j].getAttribute('value'), 10));
    }
    for (var i = 0; i < selectedPassengers.length; i++) {
        var idW = parseInt(selectedPassengers[i].value, 10);
        idPassengers.push({'idWorker':idW,
                         'idPickup':findBestLink(workers[getWorkerById(idDriver)].mapPosition,
                                                            workers[getWorkerById(idW)].mapPosition,
                                                            idPickups)});
    }
    // on met à jour en base
    changeShuttle(idS, idDriver, idCar, idPickups, idPassengers);
    // on ferme l'infoWindow
    infoWindowS.close();
}

function newShuttle (idDriver) {
    var idCar = $('#selectCars option:selected')[0].value;
    var passengers = [];
    var selectedPassengers = $('#selectPassengers option:selected');
    var idPickups = [];
    var selectedPickups = $('#selectPickups .active');
    var idPhase = currSite.phases[currentDate.year][currentDate.week].num;
    for (var j = 0; j < selectedPickups.length; j++) {
        idPickups.push(parseInt(selectedPickups[j].getAttribute('value'), 10));
    }
    for (var i = 0; i < selectedPassengers.length; i++) {
        var idW = parseInt(selectedPassengers[i].value, 10);
        passengers.push({'idWorker':idW,
                         'idPickup':findBestLink(workers[getWorkerById(idDriver)].mapPosition,
                                                                workers[getWorkerById(idW)].mapPosition,
                                                                idPickups)});
    }
    // on met à jour en base
    addShuttle(idDriver, idCar, idPhase, idPickups, passengers);
    // on ferme l'infoWindow
    infoWindowS.close();
}

/**
 * fonction permettant de changer le trajet d'un ouvrier en l'affectant sur une navette différente.
 * Cette fonction permet également de mettre à jour le multiselect des pickups associés à la navette choisie
 * @param  {int} idW L'id de l'ouvrier à affecter sur la navette
 * @return {void}
 */
function changePassengerOfShuttle (idW) {
    return function(option, checked) {
        simulateRadio(option, checked, "selectShuttle");
        // on récupère l'id de la navette affecté à l'ouvrier
        var idShuttle = $('#selectShuttle option:selected')[0].value;

        // On construit les nouvelles option du multiselect des pickups
        var data = [{label: "Aucun point d'arrêt", value: "0"}];
        // ajout de la liste des pickups
        var idPickups = [];
        for (var j in shuttles[idShuttle].shuttle.pickups) {
            data.push({label: "Point d'arrêt "+String.fromCharCode(64+pickups[j].numID), value: ""+j});
            idPickups.push(j);
        }
        // on trouve le point d'arret le plus proche
        var idPickup = findBestLink(workers[getWorkerById(shuttles[idShuttle].shuttle.driver.num)].mapPosition,
                                    workers[getWorkerById(idW)].mapPosition, idPickups);
        // Le passager est plus proche du conducteur que d'un point d'arret
        if (idPickup == null){
            idPickup = 0;
        }
        $("#selectPickup").multiselect('dataprovider', data);
        $("#selectPickup").multiselect('select', idPickup);

        // puis on met à jour en base
        setWorkerAsPassenger(idW, idShuttle, idPickup);
    };
}

/**
 * fonction permettant de mettre à jour le point d'arrêt d'un passager
 * @param  {int} idW L'id de l'ouvrier à mettre à jour
 * @return {void}
 */
function changePickupOfPassenger (idW) {
    return function(option, checked) {
        // on récupère les id de la navette et du pickup selectionnés
        var idShuttle = $('#selectShuttle option:selected')[0].value;
        var idPickup = $('#selectPickup option:selected')[0].value;

        // puis on met jour en base
        setWorkerAsPassenger(idW, idShuttle, idPickup);
    };
}

/**
 * fonction qui permet de mettre un ouvrier en tant que conducteur sur une navette
 * @param  {int} idW L'id de l'ouvrier à mettre en conducteur
 * @return {void}
 */
function changeWorkerAsDriver (idW) {
    return function(option, checked) {
        simulateRadio(option, checked ,"selectShuttle2");
        var idShuttle = $('#selectShuttle2 option:selected')[0].value;

        // On ferme la popUp du worker
        infoWindowW.close();

        // si la navette choisi existe déjà, on swap les drivers
        if (idShuttle != -1){
            // on swap les drivers car on ne peut choisir que la navette dont le worker est passager
            swapDriver(idShuttle, idW);
        } else {
            infoNewShuttle(idW);
        }
    };
}

/**
 * fonction qui test si un pickup est dans la shuttle d'idShuttle
 * @param  {int}  idShuttle L'id de la navette
 * @param  {int}  idPickup  L'id du pickup à tester
 * @return {Boolean}           Vrai si le pickup est dans la navette, faux sinon
 */
function isInPickups (idShuttle, idPickup) {
    for (var i in shuttles[idShuttle].shuttle.pickups){
        if (idPickup == shuttles[idShuttle].shuttle.pickups[i].num){
            return true;
        }
    }
    return false;
}

/**
 * fonction permettant de retrouver un ouvrier par son id
 * @param  {int} idWorker L'id du worker recherché
 * @return {int} L'index du worker recherché si il existe, -1 sinon
 */
function getWorkerById (idWorker) {
    for (var i = 0; i < workers.length; i++){
        if (workers[i].num == idWorker){
            return i;
        }
    }
    return -1;
}

/**
 * fonction permettant de retrouver un véhicule par son id
 * @param  {int} idCar L'id du véhhicule recherché
 * @return {int} L'index du véhicule recherché si il existe, -1 sinon
 */
function getCarById (idCar) {
    for (var i = 0; i < cars.length; i++) {
        if (cars[i].num == idCar){
            return i;
        }
    }
    return -1;
}

/**
 * fonction permettant de retrouver le ouvrier asssocié à l'id du conducteur d'une navette
 * @param  {int} idShuttle L'id de la navette dont on veut récupérer le conducteur
 * @return {object} Le worker correspondant au conducteur de la navette
 */
function getDriverFromShuttle (idShuttle) {
    return workers[getWorkerById(shuttles[idShuttle].shuttle.driver.num)];
}

/**
 * fonction permettant de déterminer si un ouvrier est passager d'un navette
 * @param  {int}  idW L'id de l'ouvrier
 * @return {object} L'objet passenger si l'ouvrier est passager d'une navette, null sinon
 */
function isPassenger (idW) {
    var passenger = null;
    for (var i in shuttles) {
        for (var j in shuttles[i].shuttle.passengers) {
            if (shuttles[i].shuttle.passengers[j].worker.num == idW){
                passenger = shuttles[i].shuttle.passengers[j];
            }
        }
    }
    return passenger;
}

/**
 * fonction permettant de savoir si un ouvrier est conducteur d'une navette
 * @param  {int}  idW L'id de l'ouvrier
 * @return {int} L'id de la navette si l'ouvrier est conducteur, -1 sinon
 */
function isDriver (idW) {
    idShuttle = -1;
    for (var i in shuttles) {
        if (shuttles[i].shuttle.driver.num == idW){
            idShuttle = i;
        }
    }
    return idShuttle;
}

/**
 * fonction qui retourne les workers qui ne sont pas encore assignés sur une navette
 * @param {Object} driverTemp Le driver de la nouvelle navette créée. On l'enlève donc des ouvriers libres
 * @return {[Object]} Les ouvriers actuellement non assignés sur une navette
 */
function getFreeWorkers (driverTemp) {
    var nonFreeWorkers = [];
    for (var i in shuttles) {
        nonFreeWorkers.push(workers[getWorkerById(shuttles[i].shuttle.driver.num)]);
        for (var j in shuttles[i].shuttle.passengers) {
            nonFreeWorkers.push(workers[getWorkerById(shuttles[i].shuttle.passengers[j].worker.num)]);
        }
    }
    var freeWorkers = [];
    for (var k = 0; k < workers.length; k++) {
        if ((nonFreeWorkers.indexOf(workers[k]) == -1) && (driverTemp.num != workers[k].num)){
            freeWorkers.push(workers[k]);
        }
    }
    return freeWorkers;
}

/**
 * Fonction calculant la distance entre deux point
 * @param  {Object} p1 Le premier point
 * @param  {Object} p2 Le deuxieme point
 * @return {int}    La distance entre les deux points en mètres
 */
function getDistance(p1, p2) {
  var R = 6378137; // Earth’s mean radius in meter
  var dLat = rad(p2.lat() - p1.lat());
  var dLong = rad(p2.lng() - p1.lng());
  var a =   Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(rad(p1.lat())) * Math.cos(rad(p2.lat())) *
            Math.sin(dLong / 2) * Math.sin(dLong / 2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  var d = R * c;
  return d; // returns the distance in meter
}

/**
 * Fonction de passage en radius
 * @param  {int} x valeur a passer en raduis
 * @return {int}   La valeur en raduis
 */
var rad = function(x) {
  return x * Math.PI / 180;
};

/**
 * fonction permettant de mettre la premiere lettre d'un mot en majuscule et le reste en minuscule
 * @param  {String} s La chaîne de caractère à traiter
 * @return {String} La chaîne "capitalizer"
 */
function capitalize (s) {
    return s.charAt(0).toUpperCase() + s.slice(1).toLowerCase();
}