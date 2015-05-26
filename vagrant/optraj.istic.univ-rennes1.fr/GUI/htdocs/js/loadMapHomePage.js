(function() {
	var sites = [];
	request("templates/proxy.php?url=http://localhost:5000/site/current/", initMap);
})();


function initMap(xhr) {
    var resp = JSON.parse(xhr.responseText)
    if(resp["code"] != 1){
        reportError(resp["message"]);
        sites = []
    }
    else{
        sites =  JSON.parse(resp["data"]);
    }
	    
    /* Déclaration de l'objet qui définira les limites de la map */ 
    var bounds = new google.maps.LatLngBounds();
    
    /* Déclaration des options de la map */
	var optionsMap = {
		center : new google.maps.LatLng(48.1134750,-1.6757080),
		zoom : 10,
        mapTypeId : google.maps.MapTypeId.ROADMAP
	};
    /* Ici, nous chargeons la map dans l'élément html ayant pour id "map" */
	var map = new google.maps.Map(document.getElementById("map"), optionsMap);
	
    /* Déclaration d'un tableau qui contiendra les latitudes et longitudes de chaque chantier */
    var tabPoints = [];
    
    var tabContenu = [];
    
	var infoBulle = new google.maps.InfoWindow();
	var marker, i;
 
    for (i = 0; i < sites.length; i++) {
        /* on récupère nos coordonnées dans le tableau de chantier et on les mets dans le tableau de points */
        tabPoints.push(new google.maps.LatLng(sites[i].position.latitude, sites[i].position.longitude));
        
        tabContenu.push('<div class="gMapWindowSite">'+sites[i].name+'<br />'
						+'<table>'
						+	'<tr>'
						+		'<td>Date deb : </td>'
						+		'<td>'+sites[i].dateInitD+"/"+sites[i].dateInitM+"/"+sites[i].dateInitY+'</td>'
						+	'</tr>'
						+	'<tr>'
						+		'<td>Date fin : </td>'
						+		'<td>'+sites[i].dateEndD+"/"+sites[i].dateEndM+"/"+sites[i].dateEndY+'</td>'
						+	'</tr>'
						+'</table></div>');
        
        /* On étend les limites (bounds) de la map grâce à la méthode extend */
        bounds.extend(tabPoints[i]);
        
        /* Ajout des markers */
        marker = new google.maps.Marker({
            position: tabPoints[i],
            map: map
        });
        
        /* Ajout d'événement sur les markers pour afficher des infoBulles (avec le contenu qui va bien) à chaque click */
        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infoBulle.setContent(tabContenu[i]);
                infoBulle.open(map, marker);
            }
        })(marker, i));
    }
    /* Ici, on ajuste le zoom de la map en fonction des limites  */
    if (sites.length>0)
    {
	    map.fitBounds(bounds);
	    document.getElementById("info").innerHTML = "<h4>"+sites.length+" chantier(s) en cours</h4>";
    }
    else
    {
	    document.getElementById("info").innerHTML = "<h4>ATTENTION : aucun chantier en cours</h4>";
    }
    

}


	