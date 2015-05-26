function afficheMenu(obj){
			
			var idMenu     = obj.id;
			var idSousMenu = 'sous' + idMenu;
			var sousMenu   = document.getElementById(idSousMenu);
			
			/*****************************************************/
			/**	on cache tous les sous-menus pour n'afficher    **/
			/** que celui dont le menu correspondant est cliqué **/
			/** où 4 correspond au nombre de sous-menus         **/
			/*****************************************************/
			for(var i = 1; i <= 5; i++){
				if(document.getElementById('sousmenu' + i) && document.getElementById('sousmenu' + i) != sousMenu){
					document.getElementById('sousmenu' + i).style.display = "none";
				}
			}
			
			if(sousMenu){
				//alert(sousMenu.style.display);
				if(sousMenu.style.display == "block"){
					sousMenu.style.display = "none";
				}
				else{
					sousMenu.style.display = "block";
				}
			}
			
		}
		
function deco (){
	sessionStorage.isco = 0;
	sessionStorage.lvladminreq = 0;
	reportInfo("À bientôt", 1000, "./index.php");
}
