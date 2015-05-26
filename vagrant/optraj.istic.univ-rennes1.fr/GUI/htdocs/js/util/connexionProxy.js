/**
 * Cette fonction créer une requette http pour le serveur flask en passant pas le proxy. Pour savoir, ce qu'il faut lui envoyer,
 * je vous suggère d'aller jeter un coup d'oeil au fichier templates/proxy.php. Le format des url y est précisé.
 * Cette fonction prend deux paramètres, le premier est l'url que l'on envoi (n'oublié pas de passer par le proxy)
 * et le second paramètre correspond à la fonction qui est appelée lorsque la donnée à été retournée par Flask.
 * @param {type} url
 * @param {type} funcOk
 * @returns {undefined}
 */
function request(url, func, data, param) {
    var xdr = null;
    // Tout les tests necéssaire au fonctionnement sur tous les navigateurs
    if (window.XDomainRequest) {
        xdr = new XDomainRequest(); 
    } else if (window.XMLHttpRequest) {
        xdr = new XMLHttpRequest(); 
    } else {
        alert("Votre navigateur ne supporte pas l'objet XMLHTTPRequest niveau 2... Veuillez utiliser Firefox ou Google Chrome dans leur derniere versions.");
    }
    // Fonction appelé lorsque la requete est completement terminée
    xdr.onload = function() {
        // On appele la fonction callback lorsque la requete recoit des informations
        if (param != undefined){
            func(xdr, param);
        } else {
            func(xdr);
        }
    };
    // On fais un traitement sur l'url pour envoyé toutes les données a Flask
    var method;
    if (data){
        method = "POST";
    } else {
        method = "GET";
    }
    //console.log(url + " " + method);
    xdr.open(method, url, true);
    xdr.send(data);
}
