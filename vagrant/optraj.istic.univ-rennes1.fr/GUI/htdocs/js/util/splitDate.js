/* 
 * Projet OPTRAJ
 * Gestion Ouvrier
 * Chapel Guillaume
 */

//Parametre : une chaine du type xx/yy/www  (25/04/2013)
//Return : un tableau avec :
//           - res[0] = le jour
//	     - res[1] = le mois
//	     - res[2] = l'année

function splitDate(date){
	var res = date.split("/");
	return res;
}

function verifDate(j,m,a) {

	var d2=new Date(a,m-1,j);
	j2=d2.getDate();
	m2=d2.getMonth()+1;
	a2=d2.getFullYear();
	if ( (j!=j2)||(m!=m2)||(a!=a2) || (a < 1900) ) {
		return false;
	}
	return true;
}

function checkDate(date){
	var temp = splitDate(date);
	return verifDate(temp[0], temp[1], temp[2]);
}
