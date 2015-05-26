# coding=utf8

from AbstractDAO import AbstractDAO
from NaturalJoin import NaturalJoin, INNER_JOIN
from string import Template
from system.Assignment import Assignment
from system.Unavailability import Unavailability
from WorkerDAO import WorkerDAO
from PhaseDAO import PhaseDAO
from PositionDAO import PositionDAO
from CraftDAO import CraftDAO
from QualificationDAO import QualificationDAO
from system.Worker import Worker
from system.Position import Position
from system.Phase import Phase
from QualificationDAO import QualificationDAO
from CraftDAO import CraftDAO
from Connexion import Connexion
from copy import deepcopy

import operator
import pymysql

class UnavailabilityDAO(AbstractDAO):
    '''
    Classe UnavailabilityDAO :
    Hérite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"NUM_WEEK": "numWeek",
                    "NUM_YEAR" : "numYear",
                    "TYPE" : "type",
                    "ID_WORKER" : "idWorker"}
    
    MAPPING_FIL = {"numWeek":"NUM_WEEK",
                    "numYear":"NUM_YEAR",
                    "type":"TYPE",
                    "idWorker":"ID_WORKER"}


    def __init__(self):
        super(UnavailabilityDAO, self).__init__(tableName="UNAVAILABILITY",
                                            mappingCols=self.MAPPING_COLS,
                                            mappingFil=self.MAPPING_FIL)

    def _createElement(self):
        '''
        Créée un objet de type Unavailability
        '''
        return Unavailability()

    '''
    ========================= Méthodes publiques ===================
    '''
if __name__ == '__main__':
    try:
        conn = Connexion().connect()
        unDAO = UnavailabilityDAO()
        x = Unavailability(1, 1, 2014, "toto")
        id = unDAO.insert(conn, x)
        if True:
            print unDAO.delete(conn,
                        ('idWorker', 1),
                        ('numWeek', 1),
                        ("numYear", 2014))
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur de connexion lors de la création du véhicule"}
    finally:
        #Connexion().disconnect(conn)
        print "3"
