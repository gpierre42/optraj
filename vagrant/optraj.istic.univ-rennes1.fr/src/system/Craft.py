# coding=utf8

class Craft(object):
    '''
    Classe représentant le métier d'un ouvrier

    Attributs publics :
    - num : l'identifiant unique du métier (int)
    - name : le nom du metier (str)
    '''

    def __init__(self, num=-1, name=None):
        '''
        Constructeur d'un métier
        
        Args:
            num : l'identifiant unique du métier (int)
            name : le nom du metier (str)
        '''
        self._name = name
        self._num = num

    '''
    ================Setteurs/Accesseurs=====================
    '''
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, value):
        self._num = value

    def __str__(self):
        '''
        retourne le métier sous une forme lisible pour l'humain.

        Returns:
            le métier sous forme de string
            
        Examples:
            >>> [8, Chauffeur]
        '''
        return "[{}, {}]".format(self.num, self.name)

    def serial(self):
        '''
        Sérialise un métier pour pouvoir la transmettre facilement

        Returns:
            un dict contenant le metier sérialise
            
        Examples:
            >>> {'num': 8, '__class__': 'Craft', 'name': u'Chauffeur'}
        '''
        return {"__class__": "Craft",
                "num": self.num,
                "name": self.name}

if __name__ == '__main__':
    """
    from interfacebdd.CraftDAO import CraftDAO as dao
    from interfacebdd.Connexion import Connexion
    elem = dao()
    co = Connexion().connect()
    allelems = elem.getAll(co, False, [])
    x = allelems.pop()
    print x.serial()
    print x
    pass
    """