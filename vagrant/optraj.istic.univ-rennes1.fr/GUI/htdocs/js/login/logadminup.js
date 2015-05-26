/*
CARRE NICOLAS
OPTRAJ
*/

(function() {
	if (sessionStorage.isco == 0 || sessionStorage.lvladminreq != 3) {
		reportError("Vous n'avez pas accès à cette page", null, "./index.php")
	}		
})();