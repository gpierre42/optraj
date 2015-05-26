# coding=utf8

class Pickup:
    '''
    Classe repérant un point de ramassage de navette

    Attributs publics:
    - num : l'identifiant unique du point de ramassage (int)
    - position : la position (Position.Position)
    - idSite : l'id du site lié au pikcup
    '''

    def __init__(self, position=None, num=-1, idSite=-1):
        '''
        Constructeur d'un point de ramassage
        
        Args:
            num : l'identifiant unique du point de ramassage (int)
            position : la position (Position.Position)
            idSite : l'id du site lié au pickup
        '''
        self._position = position
        self._idSite = idSite
        self._num = num

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
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        
    @property
    def idSite(self):
        return self._idSite

    @idSite.setter
    def idSite(self, value):
        self._idSite = value

    '''
    ================ Méthodes publiques ================
    '''

    def __str__(self):
        '''
        retourne le Pickup sous une forme lisible pour l'humain.

        Returns:
            la Pickup sous forme de string
            
        Examples:
            >>> "Le point de ramassage, de num 4, et de coordonnées : [-2.08394, 47.6507]"
        '''
        return "Le point de ramassage, de num {}, et de coordonnées : [{}, {}] est associé au chantier d'id {}".format(self.num, self.position.longitude, self.position.latitude, self.idSite)

    def serial(self):
        '''
        Sérialise un Pickup pour pouvoir la transmettre facilement

        Returns:
            un dict contenant le Pickup sérialise
            
        Examples:
            >>> {'idSite': 1, 'position': {'latitude': 47.6507, '__class__': 'Position', 'longitude': -2.08394, 'address': u'Redon'}, 'num': 4, '__class__': 'Pickup'}
        '''
        return {"__class__": "Pickup",
                "num": self.num,
                "position": self.position.serial(),
                "idSite": self.idSite}
        
if __name__ == '__main__':
    """
    from interfacebdd.PickupDAO import PickupDAO as dao
    from interfacebdd.Connexion import Connexion
    elem = dao()
    co = Connexion().connect()
    allelems = elem.getAll(co, False, [])
    x = allelems.pop()
    print x.serial()
    print x
    pass
    """
