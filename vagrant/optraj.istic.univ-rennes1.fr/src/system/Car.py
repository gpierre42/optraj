# coding=utf8

class Car(object):
    '''
    Classe représentant les véhicules

    attributs publics:
    - num : l'identifiant unique (int)
    - plate : le numéro de plaque (str)
    - model : le nom de modèle (str)
    - nbPlace : le nombre de places (int)
    '''

    def __init__(self, num=-1, plate="", model="", nbPlace=-1):
        '''
        Constructeur d'un véhicule
        
        Args:
            num : l'identifiant unique (int)
            plate : le numéro de plaque (str)
            model : le nom de modèle défaut (str)
            nbPlace : le nombre de places (int)
        '''
        self._num = num
        self._plate = plate
        self._model = model
        self._nbPlace = nbPlace

    '''
    ================Setteurs/Accesseurs=====================
    '''

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, value):
        self._num = value

    @property
    def plate(self):
        return self._plate

    @plate.setter
    def plate(self, value):
        self._plate = value

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def nbPlace(self):
        return self._nbPlace

    @nbPlace.setter
    def nbPlace(self, value):
        self._nbPlace = value

    def __str__(self):
        '''
        Retourne le véhicule sous une forme lisible pour l'humain.

        Returns:
            le véhicule sous forme de string
        
        Examples:
            >>> "num : 62, immatriculation : AE-444-WB, modèle: C3 II , nombre de places : 2"
        '''
        return "num : {}, immatriculation : {}, modèle: {}, nombre de places : {}".format(self.num, self.plate, self.model, self.nbPlace)

    def serial(self):
        '''
        Sérialise un metier pour pouvoir la transmettre facilement

        Returns:
            un dict contenant le metier serialise
            
        Examples:
            >>> {'plate': u'CF-612-PJ (1320XZ35)', 'model': u'SCUDO ', 'num': 218, '__class__': 'Car', 'nbPlace': 2}
        '''
        return {"__class__": "Car",
                "num": self.num,
                "plate": self.plate,
                "model": self.model,
                "nbPlace": self.nbPlace}
        
if __name__ == '__main__':
    """
    from interfacebdd.CarDAO import CarDAO
    from interfacebdd.Connexion import Connexion
    elem = CarDAO()
    co = Connexion().connect()
    all = elem.getAll(co, False, [])
    x = all.pop()
    print x.serial()
    print x
    pass
    """
