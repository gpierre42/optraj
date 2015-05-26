# coding=utf8

class PickupLink:
    '''
    Classe liant un point de ramassage (Pickup.Pickup) à une navette (Shuttle.Shuttle)

    Attributs publics:
    - num : l'identifiant unique de la liaison (int)
    - pickup : le point de ramassage associé (Pickup.Pickup)
    - numShuttle : l'id de la navette associé (int)
    '''

    def __init__(self, num=-1, pickup=None, numShuttle=-1):
        '''
        Constructeur d'un PickupLink
        
        Args:
            num : l'identifiant unique de la liaison (int)
            pickup : le point de ramassage associé (Pickup.Pickup)
            numShuttle : l'id de la navette associé (int)
        '''
        self._num = num
        self._pickup = pickup
        self._numShuttle = numShuttle

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
    def pickup(self):
        return self._pickup

    @pickup.setter
    def picup(self, value):
        self._pickup = value

    @property
    def numShuttle(self):
        return self._numShuttle

    @numShuttle.setter
    def numShuttle(self, value):
        self._numShuttle = value

    '''
    ================ Méthodes publiques ================
    '''

    def __str__(self):
        '''
        retourne le PickupLink sous une forme lisible pour l'humain.

        Returns:
            la PickupLink sous forme de string
            
        Examples:
            >>> "(num: 1) Le point de ramassage 1, et de coordonées : [-1.67869, 48.1075], est associé à la navette 1"
        '''
        return "(num: {}) Le point de ramassage {} associé au chantier d'id {}, et de coordonées : [{}, {}], est associé à la navette {}".format(self.num, self.pickup.num, self.pickup.idSite, self.pickup.position.longitude, self.pickup.position.latitude, self.numShuttle)

    def serial(self):
        '''
        Sérialise un PickupLink pour pouvoir le transmettre facilement

        Returns:
            un dict contenant le PickupLink serialise
            
        Examples:
            >>> {'pickup': {'position': {'latitude': 48.1075, '__class__': 'Position', 'longitude': -1.67869, 'address': u'Boulevard de la Libert\xe9 35000 RENNES'}, 'num': 1, '__class__': 'Pickup'}, 'num': 1, '__class__': 'PickupLink', 'numShuttle': 1}
        '''
        return {"__class__": "PickupLink",
                "num": self.num,
                "pickup": self.pickup.serial(),
                "numShuttle": self.numShuttle}

if __name__ == '__main__':
    """
    from interfacebdd.PickupLinkDAO import PickupLinkDAO as dao
    from interfacebdd.Connexion import Connexion
    elem = dao()
    co = Connexion().connect()
    allelems = elem.getAll(co, False, [])
    x = allelems.pop()
    print x.serial()
    print x
    pass
    """