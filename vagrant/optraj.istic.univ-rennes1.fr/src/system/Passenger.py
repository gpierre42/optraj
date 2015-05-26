# coding=utf8

from Worker import Worker
from Shuttle import Shuttle
from Pickup import Pickup

class Passenger(object):
    '''
    Classe représentant les liens passagers/navettes
    
    Attributs publics:
    - num : l'identifiant unique d'un Passenger (int)
    - idShuttle : l'id de la navette ramasseuse 
    - worker : l'ouvrier ramassé (Worker.Worker)
    - pickup : le point de ramassage où se rend le passager

    '''

    def __init__(self, num=-1, idShuttle=-1, worker=Worker(), pickup=Pickup()):
        '''
        Constructeur d'un lien passager/navette
        
        Args:
            num : l'identifiant unique d'un Passenger (int)
            idShuttle : l'id de la navette ramasseuse 
            worker : l'ouvrier ramassé (Worker.Worker)
            pickup : le point de ramassage où se rend le passager
        '''
        self._num = num
        self._idShuttle = idShuttle
        self._worker = worker
        self._pickup = pickup
        
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
    def idShuttle(self):
        return self._idShuttle

    @idShuttle.setter
    def idShuttle(self, value):
        self._idShuttle = value

    @property
    def worker(self):
        return self._worker

    @worker.setter
    def worker(self, value):
        self._worker = value
        
    @property
    def pickup(self):
        return self._pickup

    @pickup.setter
    def pickup(self, value):
        self._pickup = value


    def __str__(self):
        '''
        retourne le Passenger sous une forme lisible pour l'humain.

        Returns:
            le Passenger sous forme de string
            
        Examples:
            >>> "num : 1, L'ouvrier 107 est un passager de la voiture : 1, pour la phase 4"
        '''
        return "num : {}, L'ouvrier {} est un passager pour la navette d'id {} et se rend au point {}".format(self.num, self.worker.num, self.idShuttle, self.pickup)

    def serial(self):
        '''
        Sérialise un Passenger pour pouvoir la transmettre facilement

        Returns:
            un dict contenant le Passenger serialise
            
        Examples:
            >>> {'shuttle': {'car': {'plate': u'7797XR35', 'model': u'C15', 'num': 45, '__class__': 'Car', 'nbPlace': 5}, 'driver': {'num': 1, 'licence': u' ', 'name': u'BALARD', 'firstName': u'OLIVIER', 'birthdateY': '1982', '__class__': 'Worker', 'birthdateM': '02', 'craft': {'num': 1, '__class__': 'Craft', 'name': u'Chef de Chantier'}, 'qualification': {'num': 1, '__class__': 'Qualification', 'name': u'ETAM'}, 'position': {'latitude': 48.077, '__class__': 'Position', 'longitude': -1.71586, 'address': u'38 MAIL LEON BLUM  35131 ST JACQUES DE LA LANDE'}, 'birthdateD': '09'}, '__class__': 'Shuttle', 'num': 1, 'pickupLinks': {1: {'pickup': {'position': {'latitude': 48.1075, '__class__': 'Position', 'longitude': -1.67869, 'address': u'Boulevard de la Libert\xe9 35000 RENNES'}, 'num': 1, '__class__': 'Pickup'}, 'num': 1, '__class__': 'PickupLink', 'numShuttle': 1}}, 'phase': {'needs': {56: {'num': 56, '__class__': 'Need', 'need': 2, 'craft': {'num': 6, '__class__': 'Craft', 'name': u'Coffreur'}, 'qualification': {'num': 6, '__class__': 'Qualification', 'name': u'N2'}, 'phase': 4}, 6: {'num': 6, '__class__': 'Need', 'need': 4, 'craft': {'num': 2, '__class__': 'Craft', 'name': u'Macon'}, 'qualification': {'num': 3, '__class__': 'Qualification', 'name': u'N4P1'}, 'phase': 4}, 7: {'num': 7, '__class__': 'Need', 'need': 1, 'craft': {'num': 12, '__class__': 'Craft', 'name': u'Grutier'}, 'qualification': {'num': 4, '__class__': 'Qualification', 'name': u'N3P2'}, 'phase': 4}}, 'num': 4, 'numYear': 2014, 'numWeek': 14, 'totalWorkers': 0, 'nbWorkers': 0, '__class__': 'Phase', 'numSite': 5}}, 'num': 1, 'worker': {'num': 107, 'licence': u' ', 'name': u'BERTHIER', 'firstName': u'EMMANUEL', 'birthdateY': '1986', '__class__': 'Worker', 'birthdateM': '02', 'craft': {'num': 2, '__class__': 'Craft', 'name': u'Macon'}, 'qualification': {'num': 5, '__class__': 'Qualification', 'name': u'N3P1'}, 'position': {'latitude': 47.6765, '__class__': 'Position', 'longitude': -2.0417, 'address': u'6 LA POSNIERE  35600 SAINTE MARIE DE REDON'}, 'birthdateD': '10'}, '__class__': 'Craft'}
        '''
        return {"__class__": "Passenger",
                "num": self.num,
                "idShuttle": self.idShuttle,
                "worker": self.worker.serial(),
                "pickup": self.pickup.serial()}

if __name__ == '__main__':
    """
    from interfacebdd.PassengerDAO import PassengerDAO as dao
    from interfacebdd.Connexion import Connexion
    elem = dao()
    co = Connexion().connect()
    allelems = elem.getAll(co, False, [])
    x = allelems.pop()
    print x.serial()
    print x
    """
    pass