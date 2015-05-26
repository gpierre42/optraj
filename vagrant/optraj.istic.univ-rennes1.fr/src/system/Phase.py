# coding=utf8

class Phase(object):
    '''
    Classe Phase définissant une période d'une semaine pour un chantier
    
    Attributs publics:
    - num : identifiant unique d'une phase (int)
    - numSite : identifiant du chantier associé a la phase (int)
    - numWeek : le numéro de la semaine de la phase (int)
    - numYear : l'année de la phase (int)
    - needs : les besoins en ouvriers pour la phase. (list(Need.Need))
    '''

    def __init__(self, num=-1, numSite=-1, numWeek=-1, numYear=-1, needs=[], nbWorkers=0, totalWorkers=0):
        '''
        Constructeur d'une Phase
        
        Args:
            num : identifiant unique d'une phase (int)
            numSite : identifiant du chantier associé a la phase (int)
            numWeek : le numéro de la semaine de la phase (int)
            numYear : l'année de la phase (int)
            needs : les besoins en ouvriers pour la phase. (list(Need.Need))
        '''
        self._num = num
        self._numSite = numSite
        self._numWeek = numWeek
        self._numYear = numYear

        self._nbWorkers = nbWorkers
        self._needs = needs
        self._totalWorkers = totalWorkers

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
    def numWeek(self):
        return self._numWeek

    @numWeek.setter
    def numWeek(self, value):
        self._numWeek = value

    @property
    def numYear(self):
        return self._numYear

    @numYear.setter
    def numYear(self, value):
        self._numYear = value

    @property
    def needs(self):
        return self._needs

    @needs.setter
    def needs(self, value):
        self._needs = value

    @property
    def nbWorkers(self):
        return self._nbWorkers

    @nbWorkers.setter
    def nbWorkers(self, value):
        self._nbWorkers = value

    @property
    def totalWorkers(self):
        return self._totalWorkers

    @totalWorkers.setter
    def totalWorkers(self, value):
        self._totalWorkers = value

    '''
    ================ Méthodes publiques ================
    '''

    def __str__(self):
        '''
        retourne la Phase sous une forme lisible pour l'humain.

        Returns:
            la Phase sous forme de string
            
        Examples:
            >>> "Phase d'id 5, Semaine n°13 de l'année 2014"
            >>> "Besoin de 1 Grutier N3P2"
            >>> "Besoin de 3 Macon N4P1"
            >>> "Besoin de 2 Coffreur N2"
        '''
        s = ""
        for n in self.needs:
            s += str(n)
        return "Phase d'id {}, Semaine n°{} de l'année {} \n".format(self.num, self.numWeek, self.numYear) + s

    def serial(self):
        '''
        Sérialise une phase pour pouvoir la transmettre facilement

        Returns:
            un dict contenant la phase serialisé
            
        Examples:
            >>> {'needs': {8: {'num': 8, '__class__': 'Need', 'need': 3, 'craft': {'num': 2, '__class__': 'Craft', 'name': u'Macon'}, 'qualification': {'num': 3, '__class__': 'Qualification', 'name': u'N4P1'}, 'phase': 5}, 9: {'num': 9, '__class__': 'Need', 'need': 1, 'craft': {'num': 12, '__class__': 'Craft', 'name': u'Grutier'}, 'qualification': {'num': 4, '__class__': 'Qualification', 'name': u'N3P2'}, 'phase': 5}, 54: {'num': 54, '__class__': 'Need', 'need': 2, 'craft': {'num': 6, '__class__': 'Craft', 'name': u'Coffreur'}, 'qualification': {'num': 6, '__class__': 'Qualification', 'name': u'N2'}, 'phase': 5}}, 'num': 5, 'numYear': 2014, 'numWeek': 13, 'totalWorkers': 0, 'nbWorkers': 0, '__class__': 'Phase', 'numSite': 5}
        '''
        return {"__class__": "Phase",
                "num": self.num,
                "numSite": self.numSite,
                "numWeek": self.numWeek,
                "numYear": self.numYear,
                "needs": {i.num:i.serial() for i in self.needs},
                "nbWorkers": self.nbWorkers,
                "totalWorkers":self.totalWorkers

                }

    def compareTime(self, phaseToCompare):
        '''
        Compare 2 phases en se basant sur la période qu'elles désignent (la semaine)

        Args:
            phaseToCompare (Phase) : la phase à laquelle on se compare

        Return:
            -1 si self précède phaseToCompare
            0 si les deux phases se déroulent en même temps (la même semaine)
            1 si self suit phaseToCompare
        '''
        if(self._numYear < phaseToCompare._numYear or
           self._numYear == phaseToCompare._numYear and self._numWeek < phaseToCompare._numWeek):
            return -1
        elif (self._numYear == phaseToCompare._numYear and self._numWeek == phaseToCompare._numWeek):
            return 0
        else:
            return 1

if __name__ == '__main__':
    """
    from interfacebdd.PhaseDAO import PhaseDAO as dao
    from interfacebdd.Connexion import Connexion
    elem = dao()
    co = Connexion().connect()
    allelems = elem.getAll(co, False, [])
    x = allelems.pop()
    print x.serial()
    print x
    pass
    """
