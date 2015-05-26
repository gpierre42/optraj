# coding=utf8

class Need(object):
    '''
    Classe Need définissant un besoin
    
    Attributs publics :
    - num : l'identifiant unique du besoin (int)
    - numPhase : l'identifiant de la phase liée (int)
    - craft : le métier requis (Craft.Craft)
    - qualification : la qualification demandée (Qualification.Qualification)
    - need : le nombre d'ouvriers demandé (int)
    '''

    def __init__(self, num=-1, numPhase=-1, craft=None, qualification=None, need=-1):
        '''
        Constructeur d'un Need
        
        Args:
            num : l'identifiant unique du besoin (int)
            numPhase : l'identifiant de la phase liée (int)
            craft : le métier requis (Craft.Craft)
            qualification : la qualification demandée (Qualification.Qualification)
            need : le nombre d'ouvriers demandé (int)
        '''
        self._num = num
        self._numPhase = numPhase
        self._craft = craft
        self._qualification = qualification
        self._need = need

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
    def numPhase(self):
        return self._numPhase

    @numPhase.setter
    def numPhase(self, value):
        self._numPhase = value

    @property
    def craft(self):
        return self._craft

    @craft.setter
    def craft(self, value):
        self._craft = value

    @property
    def need(self):
        return self._need

    @need.setter
    def need(self, value):
        self._need = value

    @property
    def qualification(self):
        return self._qualification

    @qualification.setter
    def qualification(self, value):
        self._qualification = value

    '''
    ================ Méthodes publiques ================
    '''

    def __str__(self):
        '''
        retourne le besoin sous une forme lisible pour l'humain.

        Returns:
            le besoin sous forme de string
            
        Examples:
            >>> "Besoin de 2 Macon N3P1"
        '''
        return "Besoin de {} {} {}\n".format(self.need, self.craft.name, self.qualification.name)

    def serial(self):
        '''
        serialise un besoin pour pouvoir la transmettre facilement

        Returns:
            un dict contenant le besoin serialisé
            
        Examples:
            >>> {'num': 50, '__class__': 'Need', 'need': 2, 'craft': {'num': 2, '__class__': 'Craft', 'name': u'Macon'}, 'qualification': {'num': 5, '__class__': 'Qualification', 'name': u'N3P1'}, 'phase': 30}
        '''
        return {"__class__": "Need",
                "num": self.num,
                "phase": self.numPhase,
                "craft": self.craft.serial(),
                "qualification": self.qualification.serial(),
                "need": self.need
                }

if __name__ == '__main__':
    """
    from interfacebdd.NeedDAO import NeedDAO as dao
    from interfacebdd.Connexion import Connexion
    elem = dao()
    co = Connexion().connect()
    allelems = elem.getAll(co, False, [])
    x = allelems.pop()
    print x.serial()
    print x
    pass
    """
    
