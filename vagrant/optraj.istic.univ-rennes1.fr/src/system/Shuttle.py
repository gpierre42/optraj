# coding=utf8

from Worker import Worker
from Phase import Phase
from Car import Car

class Shuttle(object):
    '''
    Classe représentant les navettes (un lien entre un véhicule, un conducteur et une phase)
    
    Attributs publics:
    - num : l'identifiant unique (int)
    - driver : le conducteur (Worker.Worker)
    - car : le véhicule (Car.Car)
    - phase : la phase liée (Phase.Phase)
    - pickup : les points de ramassages 
    - passengers : les passagers (ensemble de Passenger)
    '''

    def __init__(self, num=-1, driver=Worker(), car=Car(), phase=Phase(), pickups=[], passengers=[]):
        '''
        Constructeur d'une navette
        
        Args:
            num : l'identifiant unique (int)
            driver : le conducteur (Worker.Worker)
            car : le véhicule (Car.Car)
            phase : la phase liée (Phase.Phase)
            pickups : les points de ramassages (ensemble de Pickup)
            passengers : les passagers (ensemble de Worker)
        '''
        self._num = num
        self._driver = driver
        self._car = car
        self._phase = phase
        self._pickups = pickups
        self._passengers = passengers

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
    def driver(self):
        return self._driver

    @driver.setter
    def driver(self, value):
        self._driver = value

    @property
    def car(self):
        return self._car

    @car.setter
    def car(self, value):
        self._car = value

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        self._phase = value

    @property
    def pickups(self):
        return self._pickups

    @pickups.setter
    def pickups(self, value):
        self._pickups = value
        
    @property
    def passengers(self):
        return self._passengers

    @passengers.setter
    def passengers(self, value):
        self._passengers = value

    def __str__(self):
        '''
        retourne la navette sous une forme lisible pour l'humain.

        Returns:
            la navette sous forme de string
            
        Examples:
            >>> num : 1, id du pilote : 1, id de la voiture : 45, id de la phase : 4
            >>> Liste des points de ramassage :
            >>>     (num: 1) Le point de ramassage 1, et de coordonées : [-1.67869, 48.1075], est associé à la navette 1
        '''
        s = "\nListe des points de ramassage :"
        for pl in self.pickups:
            s += "\n\t\t" + str(pl)
        return "num : {}, id du pilote : {}, id de la voiture : {}, id de la phase : {}".format(self.num, self.driver.num, self.car.num, self.phase.num) + s

    def serial(self):
        '''
        serialise un metier pour pouvoir la transmettre facilement

        Returns:
            un string contenant le metier serialise
            
        Examples:
            >>> {'car': {'plate': u'7797XR35', 'model': u'C15', 'num': 45, '__class__': 'Car', 'nbPlace': 5}, 'driver': {'num': 1, 'licence': u' ', 'name': u'BALARD', 'firstName': u'OLIVIER', 'birthdateY': '1982', '__class__': 'Worker', 'birthdateM': '02', 'craft': {'num': 1, '__class__': 'Craft', 'name': u'Chef de Chantier'}, 'qualification': {'num': 1, '__class__': 'Qualification', 'name': u'ETAM'}, 'position': {'latitude': 48.077, '__class__': 'Position', 'longitude': -1.71586, 'address': u'38 MAIL LEON BLUM  35131 ST JACQUES DE LA LANDE'}, 'birthdateD': '09'}, '__class__': 'Shuttle', 'num': 1, 'pickupLinks': {1: {'pickup': {'position': {'latitude': 48.1075, '__class__': 'Position', 'longitude': -1.67869, 'address': u'Boulevard de la Libert\xe9 35000 RENNES'}, 'num': 1, '__class__': 'Pickup'}, 'num': 1, '__class__': 'PickupLink', 'numShuttle': 1}}, 'phase': {'needs': {56: {'num': 56, '__class__': 'Need', 'need': 2, 'craft': {'num': 6, '__class__': 'Craft', 'name': u'Coffreur'}, 'qualification': {'num': 6, '__class__': 'Qualification', 'name': u'N2'}, 'phase': 4}, 6: {'num': 6, '__class__': 'Need', 'need': 4, 'craft': {'num': 2, '__class__': 'Craft', 'name': u'Macon'}, 'qualification': {'num': 3, '__class__': 'Qualification', 'name': u'N4P1'}, 'phase': 4}, 7: {'num': 7, '__class__': 'Need', 'need': 1, 'craft': {'num': 12, '__class__': 'Craft', 'name': u'Grutier'}, 'qualification': {'num': 4, '__class__': 'Qualification', 'name': u'N3P2'}, 'phase': 4}}, 'num': 4, 'numYear': 2014, 'numWeek': 14, 'totalWorkers': 0, 'nbWorkers': 0, '__class__': 'Phase', 'numSite': 5}}
        '''
        return {"__class__": "Shuttle",
                "num": self.num,
                "driver": self.driver.serial(),
                "car": self.car.serial(),
                "phase": self.phase.serial(),
                "pickups": {i.num:i.serial() for i in self.pickups},
                "passengers": {i.num:i.serial() for i in self.passengers}}

if __name__ == '__main__':
    """
    from interfacebdd.ShuttleDAO import ShuttleDAO as dao
    from interfacebdd.Connexion import Connexion
    elem = dao()
    co = Connexion().connect()
    allelems = elem.getAll(co, False, [])
    x = allelems.pop()
    print x.serial()
    print x
    pass
    """
