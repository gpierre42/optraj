/*
CARRE NICOLAS
OPTRAJ
*/

(function() {
	if (sessionStorage.isco == 0) {
		reportError("Vous n'avez pas accès à cette page", null, "./index.php")
		}
})();

function levelreq (){
	if (sessionStorage.lvladminreq == 2) {
		reportError("Vous n'avez pas accès à cette page", null, "./index.php")
	}
}