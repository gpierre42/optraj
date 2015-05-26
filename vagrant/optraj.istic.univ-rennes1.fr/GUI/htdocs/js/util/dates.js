
//transforme un numéro de semaine et d'année en date au format ISO
function getDateOfISOWeek(w, y) {
    var simple = new Date(y, 0, 1 + (w - 1) * 7);
    var dow = simple.getDay();
    var ISOweekStart = simple;
    if (dow <= 4)
        ISOweekStart.setDate(simple.getDate() - simple.getDay() + 1);
    else
        ISOweekStart.setDate(simple.getDate() + 8 - simple.getDay());
    return ISOweekStart;
}

//a partir d'une date, renvois la date du lundi de la semaine
function getMonday(d) {
  d = new Date(d);
  var day = d.getDay(),
      diff = d.getDate() - day + (day == 0 ? -6:1); // adjust when day is sunday
  return new Date(d.setDate(diff));
}

//appliqué à une date, renvois le numéro de semaine au format ISO (la semaine 1 est celle qui contient le 4 janvier)
Date.prototype.getWeekNumber = function(){
    var d = new Date(+this);
    d.setHours(0,0,0);
    d.setDate(d.getDate()+4-(d.getDay()||7));
    return Math.ceil((((d-new Date(d.getFullYear(),0,1))/8.64e7)+1)/7);
};

//a partir d'un numéro entre 0 et 11 compris, retourne une chaine de caractère correspondant au mois
function getMonthName(i){
  var months = ["janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"];
  return months[i];
}

//retourne le numéros du mois (de 0 à 11) correspondant à la semaine passée en paramètre
function getMonthFromWeekNumber(i){
  if(1 <= i && i <= 4){
    return 0;
  }
  else if(5 <= i && i <= 8){
    return 1;
  }
  else if(9 <= i && i <= 13){
    return 2;
  }
  else if(14 <= i && i <= 17){
    return 3;
  }
  else if(18 <= i && i <= 22){
    return 4;
  }
  else if(23 <= i && i <= 26){
    return 5;
  }
  else if(27 <= i && i <= 30){
    return 6;
  }
  else if(31 <= i && i <= 35){
    return 7;
  }
  else if(36 <= i && i <= 39){
    return 8;
  }
  else if(40 <= i && i <= 43){
    return 9;
  }
  else if(44 <= i && i <= 48){
    return 10;
  }
  else if(49 <= i && i <= 53){
    return 11;
  }
}

// Retourne le nombre de semaines de la date passée en paramètre (52 ou 53)
function year52_53(dateToCheck){
  // récupération de l'année de la date actuelle passée en paramètre
  var year = dateToCheck.getFullYear();

  // Les années pour lesquelles il y a 53 semaines (Source : Wikipédia)
  var years53 = [2015, 2020, 2026, 2032, 2037, 2043, 2048, 2054, 2060, 2065, 2071, 2076, 2082, 2088, 2093, 2099];

  // Valeur de retour
  var result = 52;

  for(var inc = 0; inc < years53.length; inc++){
    // Si l'année en cours est dans le tableau, alors c'est une année à 53 semaines
    if(years53[inc] == year){
      result = 53;
      break;
    }
    // Si l'année en cours est inférieure à la date traitée dans la boucle, on sort
    else if(years53[inc] > year){
      break;
    }
  }

  return result;
}