# coding=utf8
'''
Created on 17 février 2014

@author: Vivien Lelouette
'''
from NaturalJoin import NaturalJoin, INNER_JOIN
from PositionDAO import PositionDAO
from AbstractDAO import AbstractDAO
from system.Pickup import Pickup
from interfacebdd.Connexion import Connexion


class PickupDAO(AbstractDAO):
    '''
    Classe PickupDAO :
    Hérite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num",
                    "ID_SITE": "idSite"}

    MAPPING_FIL = {"num": "ID",
                   "position": "ID_POSITION",
                   "idSite": "ID_SITE"}

    JOIN_POSITION = NaturalJoin(joinType=INNER_JOIN, tableName="POSITION", alias="_position", joinClauses=["e.ID_POSITION = _position.ID"], joinMappingCols=PositionDAO.MAPPING_COLS, joinId="ID_POSITION")

    def __init__(self):
        super(PickupDAO, self).__init__(tableName="PICKUP", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL, joins=[self.JOIN_POSITION])
        self._positionDAO = PositionDAO()
        self._dicoAttr = {"_position": self.positionDAO}

    def _createElement(self):
        '''
        Créée un objet de type Pickup
        '''
        return Pickup()

    '''
    ========================= Setters/accesseurs ==============================
    '''

    @property
    def positionDAO(self):
        return self._positionDAO

    @positionDAO.setter
    def positionDAO(self, value):
        self._positionDAO = value

    @property
    def dicoAttr(self):
        return self._dicoAttr

    @dicoAttr.setter
    def dicoAttr(self, value):
        self._dicoAttr = value

if __name__ == '__main__':
    pDAO = PickupDAO()
    try:
        d = Connexion().connect()
        pu = pDAO.getById(d, False, [], 3)
        print pu
    except:
        Connexion().exception()
    finally:
        Connexion().disconnect(d)
