# coding=utf8

from Position import Position
from Phase import Phase
from datetime import date

class Site(object):
    '''
    Classe Site définissant un chantier
    
    Attributs publics:
    - num : identifiant unique d'un chantier (int)
    - numSite : identifiant d'un chantier d'après Cardinal (int)
    - name : le name du chantier (str)
    - siteMaster : le nom du chef de chantier (str)
    - siteManager : le nom du conducteur de travaux (str)
    - position : la position où est le chantier (Position.Position)
    - dateInit : la date de début du chantier (datetime)
    - dateEnd : la date de fin du chantier (datetime)
    - color : la couleur affecté à un chantier en hexadécimal (string)
    - phases : une liste contenant les phases du chantier (list(Phase.Phase))
    '''

    def __init__(self, num=-1, numSite=None, name=None, siteMaster=None, siteManager=None, position=None, dateInit=None, dateEnd=None, color=None, phases=[]):
        '''
        Constructeur d'un chantier
        
        Args:
            num : identifiant unique d'un chantier (int)
            numSite : identifiant d'un chantier d'après Cardinal (int)
            name : le name du chantier (str)
            siteMaster : le nom du chef de chantier (str)
            siteManager : le nom du conducteur de travaux (str)
            position : la position où est le chantier (Position.Position)
            dateInit : la date de début du chantier (datetime)
            dateEnd : la date de fin du chantier (datetime)
            color : la couleur affecté à un chantier en hexadécimal (string)
            phases : une liste contenant les phases du chantier (list(Phase.Phase))
        '''
        self._num = num
        self._numSite = numSite
        self._name = name
        self._siteMaster = siteMaster
        self._siteManager = siteManager
        self._position = position
        self._dateInit = dateInit
        self._dateEnd = dateEnd
        self._color = color
        self._phases = phases

    '''
    =========== Setteurs/Accesseurs ===============
    '''
    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, value):
        self._num = value

    @property
    def numSite(self):
        return self._numSite

    @numSite.setter
    def numSite(self, value):
        self._numSite = value
        
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        
    @property
    def siteMaster(self):
        return self._siteMaster

    @siteMaster.setter
    def siteMaster(self, value):
        self._siteMaster = value
        
    @property
    def siteManager(self):
        return self._siteManager

    @siteManager.setter
    def siteManager(self, value):
        self._siteManager = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def dateInit(self):
        return self._dateInit

    @dateInit.setter
    def dateInit(self, value):
        self._dateInit = value

    @property
    def dateEnd(self):
        return self._dateEnd

    @dateEnd.setter
    def dateEnd(self, value):
        self._dateEnd = value
        
    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def phases(self):
        return self._phases

    @phases.setter
    def phases(self, value):
        self._phases = value

    '''
    ================ Méthodes publiques ================
    '''

    def __str__(self):
        '''
        retourne le chantier sous une forme lisible pour l'humain.

        Returns:
            le chantier sous forme de string
            
        Examples:
            >>> Site n°13025STGI "Mairie SAINT GILLES" (2013-11-19/2015-05-29) en [-1.82859, 48.1546], 5, rue du Prieuré 35590 ST GILLES.
            >>> Chef de chantier : BODERE Vincent
            >>> Conducteur de travaux : MARCEL FOUILLEE
            >>> Phases du chantier : 
            >>> Phase d'id 10, Semaine n°12 de l'année 2014 
            >>> Besoin de 3 Macon N4P1
            >>> Besoin de 1 Grutier N3P2
            >>> Besoin de 3 Coffreur N2
            >>> ...
        '''
        s = ""
        for p in self.phases:
            s += str(p)
        return "Site n°{} \"{}\" ({}/{}) en {}.\nChef de chantier : {}\nConducteur de travaux : {}\nPhases du chantier : \n".format(self.numSite, self.name, self.dateInit, self.dateEnd, self.position, self.siteMaster, self.siteManager) + s

    def serial(self):
        '''
        serialise un chantier pour pouvoir le transmettre facilement

        Returns:
            un dict contenant le chantier serialisé
        '''
        return {"__class__": "Site",
                "num": self.num,
                "numSite": self.numSite,
                "name": self.name,
                "siteMaster": self.siteMaster,
                "siteManager": self.siteManager,
                "position": self.position.serial(),
                "dateInitY": self.dateInit.strftime('%Y'),
                "dateInitM": self.dateInit.strftime('%m'),
                "dateInitD": self.dateInit.strftime('%d'),
                "dateEndY": self.dateEnd.strftime('%Y'),
                "dateEndM": self.dateEnd.strftime('%m'),
                "dateEndD": self.dateEnd.strftime('%d'),
                "color": self.color,
                "phases": {j.numYear: {i.numWeek:i.serial() for i in self.phases} for j in self.phases}
                }

if __name__ == '__main__':
    
    from interfacebdd.SiteDAO import SiteDAO as dao
    from interfacebdd.Connexion import Connexion
    elem = dao()
    co = Connexion().connect()
    allelems = elem.getAll(co, False, [])
    x = allelems.pop()
    print x.serial()
    print x
    pass
    
