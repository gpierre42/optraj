# coding=utf8

from interfacebdd.AbstractDAO import AbstractDAO
from system.Consumer import Consumer
from interfacebdd.Connexion import Connexion


class ConsumerDAO(AbstractDAO):
    '''
    Classe ConsumerDAO :
    H�rite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num",
                    "LOGIN": "login",
                    "PWD": "pwd",
                    "LVL": "lvl",
                    "FIRSTNAME": "firstname",
                    "NAME": "name"}

    MAPPING_FIL = { "num" : "ID",
                   "login" : "LOGIN",
                    "pwd" : "PWD",
                    "lvl" : "LVL" ,
                    "firstname" : "FIRSTNAME",
                    "name" : "NAME"}

    def __init__(self):
        super(ConsumerDAO, self).__init__(tableName="CONSUMER", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL)

    def _createElement(self):
        '''
        Cr��e un objet de type Consumer
        '''
        return Consumer()

if __name__ == '__main__':
    '''
    test de la classe
    '''
    print  ConsumerDAO().tableName
    conIns = Consumer(lvl=1, login="fdumoulin", pwd="admin", firstname="Dumoulin", name="François")
    "print conIns"
    conn = Connexion().connect()
    res =  ConsumerDAO().insert(conn, conIns)
    "print res"
    '''
    res2 =  ConsumerDAO().getById(conn, 1)
    "print res2"
    
    consFilt = ConsumerDAO().getByFilter(("login", "lgicquel"),("pwd", "admin"))
    print consFilt
    print consFilt.lvl
    consFilt = ConsumerDAO().getByFilter(("login", "lgcquel"),("pwd", "admin"))
    print consFilt
    consFilt = ConsumerDAO().getByFilter(("login", "lgicquel"),("pwd", "admi"))
    print consFilt
    '''
