# coding=utf8

from Position import Position
from datetime import date

class Worker(object):
    '''
    Classe worker définissant un ouvrier
    
    Attributs :
    - num : son numentifiant unique (int)
    - name : le name de famille (str)
    - firstName : le prénom (str)
    - birthdate : la date de naissance de l'ouvrier (datetime)
    - licence : liste des permis du worker (str)
    - position : la position de son domicile (Position.Position)
    - métier : le métier  (Craft.Craft)
    - qualification : La qualification (Qualification.Qualification)
    '''

    def __init__(self, num=-1, name=None, firstName=None, birthdate=None, licence=None, position=None, craft=None, qualification=None):
        '''
        Constructeur d'un ouvrier
        
        Args:
            num : son numentifiant unique (int)
            name : le name de famille (str)
            firstName : le prénom (str)
            birthdate : la date de naissance de l'ouvrier (datetime)
            licence : liste des permis du worker (str)
            position : la position de son domicile (Position.Position)
            métier : le métier  (Craft.Craft)
            qualification : La qualification (Qualification.Qualification)
        '''
        self._num = num
        self._name = name
        self._firstName = firstName
        self._birthdate = birthdate
        self._licence = licence
        self._position = position
        self._craft = craft
        self._qualification = qualification


    '''
    ========================= Setters/accesseurs ==============================
    '''
    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, value):
        self._num = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def firstName(self):
        return self._firstName

    @firstName.setter
    def firstName(self, value):
        self._firstName = value

    @property
    def birthdate(self):
        return self._birthdate

    @birthdate.setter
    def birthdate(self, value):
        self._birthdate = value
        
    @property
    def licence(self):
        return self._licence

    @licence.setter
    def licence(self, value):
        self._licence = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def craft(self):
        return self._craft

    @craft.setter
    def craft(self, value):
        self._craft = value

    @property
    def qualification(self):
        return self._qualification

    @qualification.setter
    def qualification(self, value):
        self._qualification = value

    '''
    ========================= Méthodes publiques ===================
    '''

    def __str__(self):
        '''
        Renvois un worker sous une forme lisible pour l'humain

        Returns:
            le Worker sous forme de string
        
        Examples:
            >>> "worker THIERRY MORLIER habitant en [-1.84162, 47.9264], LE LANGAGE  35580 GUIGNEN étant [1, Chef de Chantier] de qualification [1, ETAM] avec comme permis :  . (num 54)"
        '''
        return "worker {} {} habitant en {} étant {} de qualification {} avec comme permis : {}. (num {})".format(self.firstName, self.name, self.position, self.craft, self.qualification, self.licence, self.num)

    def serial(self):
        '''
        serialise une affectation pour pouvoir la transmettre facilement

        Returns:
            un dict contenant l'affectation serialisé
            
        Examples:
            >>> {'num': 54, 'licence': u' ', 'name': u'MORLIER', 'firstName': u'THIERRY', 'birthdateY': '1974', '__class__': 'Worker', 'birthdateM': '05', 'craft': {'num': 1, '__class__': 'Craft', 'name': u'Chef de Chantier'}, 'qualification': {'num': 1, '__class__': 'Qualification', 'name': u'ETAM'}, 'position': {'latitude': 47.9264, '__class__': 'Position', 'longitude': -1.84162, 'address': u'LE LANGAGE  35580 GUIGNEN'}, 'birthdateD': '09'}
        '''

        try:
            sposition = self.position.serial()
        except:
            sposition = ""

        try:
            scraft = self.craft.serial()
        except:
            scraft = ""
            
        try:
            squalif = self.qualification.serial()
        except:
            squalif = ""
        return {"__class__": "Worker",
                "num": self.num,
                "name": self.name,
                "firstName": self.firstName,
                "birthdateY": self.birthdate.strftime('%Y') if self.birthdate != None else "None",
                "birthdateM": self.birthdate.strftime('%m') if self.birthdate != None else "None",
                "birthdateD": self.birthdate.strftime('%d') if self.birthdate != None else "None",
                "licence": self.licence,
                "position": sposition,
                "craft": scraft,
                "qualification": squalif}

if __name__ == '__main__':
    from interfacebdd.WorkerDAO import WorkerDAO as dao
    from interfacebdd.Connexion import Connexion
    elem = dao()
    co = Connexion().connect()
    allelems = elem.getAll(co, False, [])
    x = allelems.pop()
    print x.serial()
    print x
    pass
