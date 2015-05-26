#coding=utf8

class Qualification(object):
    '''
    Classe symbolisant la qualification d'un ouvrier

    Attrributs publics:
    - num : identifiant unique (int)
    - name : le nom de la qualification (str)
    '''

    def __init__(self, num=-1, name=None):
        '''
        Constructeur d'une qualification
        
        Args:
            num : identifiant unique (int)
            name : le nom de la qualification (str)
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
        retourne la qualification sous une forme lisible pour l'humain.

        Returns:
            la qualification sous forme de string
        
        Examples:
            >>> [2, N4P2]
        '''
        return "[{}, {}]".format(self.num, self.name)
    
    def serial(self):
        '''
        Sérialise une qualification pour pouvoir la transmettre facilement

        Returns:
            un string contenant la qualification sérialisée
            
        Examples:
            >>> {'num': 2, '__class__': 'Qualification', 'name': u'N4P2'}
        '''
        return {"__class__": "Qualification",
                "num": self.num,
                "name": self.name}

if __name__ == '__main__':
    """
    from interfacebdd.QualificationDAO import QualificationDAO as dao
    from interfacebdd.Connexion import Connexion
    elem = dao()
    co = Connexion().connect()
    allelems = elem.getAll(co, False, [])
    x = allelems.pop()
    print x.serial()
    print x
    pass
    """
    