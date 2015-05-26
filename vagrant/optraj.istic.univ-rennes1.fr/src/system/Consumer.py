# coding=utf8

class Consumer(object):
    '''
    Classe Consumer définissant un utilisateur
    
    attributs publics :
    - num : identifiant unique (int)
    - login  : le login de l'utilisateur(str)
    - pwd : mot de passe de l'utilisateur (str)
    - lvl : le groupe auquel appartient l'utilisateur (int)
    - firstname : le prénom (str)
    - name : le nom (str)
    '''

    def __init__(self, num = -1 , lvl=0, login="", pwd="", firstname="", name=""):
        '''
        Constructeur d'un utilisateur
        
        Args:
            num : l'identifiant (int)
            login : le login de l'utilisateur (str)
            pwd : mot de passe de l'utilisateur (str)
            lvl : le groupe auquel appartient l'utilisateur (int)
            firstname : le prénom (str)
            name : le nom (str)
        '''
        self._num = num
        self._login = login
        self._pwd = pwd
        self._lvl = lvl
        self._firstname = firstname
        self._name = name        
        

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
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def pwd(self):
        return self._pwd

    @pwd.setter
    def pwd(self, value):
        self._pwd = value

    @property
    def lvl(self):
        return self._lvl

    @lvl.setter
    def lvl(self, value):
        self._lvl = value

    @property
    def firstname(self):
        return self._firstname

    @firstname.setter
    def firstname(self, value):
        self._firstname = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    '''
    ================ Méthodes publiques ================
    '''

    def __str__(self):
        '''
        Retourne l'utilisateur sous une forme lisible pour l'humain.

        Returns:
            l'utilisateur sous forme de string
        
        Examples:
            >>> "Utilisateur gdupain s'applant Gérard Dupain qui a les droits d'acces 2 de num 4 . "
        '''
        return "Utilisateur {} s'applant {} {} qui a les droits d'acces {} de num {} . \n".format(self.login, self.firstname, self.name, self.lvl, self.num)

    def serial(self):
        '''
        Sérialise un utilisateur pour pouvoir le transmettre facilement

        Returns:
            un dict contenant l'utilisateur sérialisé
            
        Examples:
            >>> {'name': u'Dupain', 'firstname': u'G\xe9rard', '__class__': 'Consumer', 'pwd': u'21232f297a57a5a743894a0e4a801fc3', 'num': 4, 'lvl': 2, 'login': u'gdupain'}
        '''
        return {"__class__": "Consumer",
                "num": self.num,
                "login": self.login,
                "pwd": self.pwd,
                "lvl": self.lvl,
                "firstname": self.firstname,
                "name": self.name
                
                }

if __name__ == '__main__':
    """
    from interfacebdd.ConsumerDAO import ConsumerDAO as dao
    from interfacebdd.Connexion import Connexion
    elem = dao()
    co = Connexion().connect()
    allelems = elem.getAll(co, False, [])
    x = allelems.pop()
    print x.serial()
    print x
    pass
    """
