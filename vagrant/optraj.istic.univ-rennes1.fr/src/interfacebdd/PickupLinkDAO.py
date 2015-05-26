# coding=utf8
'''
Created on 17 février 2014

@author: Vivien Lelouette
'''
from NaturalJoin import NaturalJoin, INNER_JOIN
from PositionDAO import PositionDAO
from AbstractDAO import AbstractDAO
from PickupDAO import PickupDAO
from system.PickupLink import PickupLink
from interfacebdd.Connexion import Connexion
import operator


class PickupLinkDAO(AbstractDAO):
    '''
    Classe PickupLinkDAO :
    Hérite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num",
                    "ID_SHUTTLE": "numShuttle"}

    MAPPING_FIL = {"num": "ID",
                   "pickup": "ID_PICKUP",
                   "numShuttle": "ID_SHUTTLE"}

    JOIN_PICKUP = NaturalJoin(joinType=INNER_JOIN, tableName="PICKUP", alias="_pickup", joinClauses=["e.ID_PICKUP = _pickup.ID"], joinMappingCols=PickupDAO.MAPPING_COLS, joinId="ID_PICKUP")
    JOIN_PICKUP_POSITION = NaturalJoin(joinType=INNER_JOIN, tableName="POSITION", alias="_pickup_position", joinClauses=["_pickup.ID_POSITION = _pickup_position.ID"], joinMappingCols=PositionDAO.MAPPING_COLS, joinId="ID_POSITION")

    def __init__(self):
        super(PickupLinkDAO, self).__init__(tableName="PICKUP_LINK", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL, joins=[self.JOIN_PICKUP, self.JOIN_PICKUP_POSITION])
        self._positionDAO = PositionDAO()
        self._pickupDAO = PickupDAO()
        self._dicoAttr = {"_pickup": self.pickupDAO, "_pickup_position": self.positionDAO}

    def _createElement(self):
        '''
        Créée un objet de type PickupLink
        '''
        return PickupLink()

    def insert(self, co=None, Obj=None):
        '''
        Permet d'insÃ©rer un objet python dans la base de donnÃ©e.
        On passe ici un objet Obj en paramètre.
        '''
        # Construit une liste des valeurs Ã  insÃ©rer dans la base
        listValue = [col + "=" + "\"" + str(operator.attrgetter(attr)(Obj)) + "\""  for (col, attr) in self.mappingCols.items()]
 
        # Construit les Ã©ventuels appels rÃ©cursifs pour insÃ©rer les objets liÃ©
        for j in ([] if self.joins is None else self.joins):
            attribut = j.alias
            if len(attribut.split("_")) <= 2:
                id_obj = operator.attrgetter(attribut.replace("_", ""))(Obj).num
                listValue.append(j.joinId + "=" + str(id_obj))
 
        # Construit la requÃªte SQL
        request = self.TEMPLATE_INSERT.substitute(table=self.tableName, value=", ".join(listValue))
        if self._verboseMode:
            print(request)
 
        cursor = co[1]
        # execution d'une requete
        cursor.execute(request)
 
        co[0].commit()
 
        # on retournel'id de l'objet insÃ©rÃ©
        idPuLink = cursor.lastrowid
        return idPuLink

    '''
    ========================= Setters/accesseurs ==============================
    '''

    @property
    def pickupDAO(self):
        return self._pickupDAO

    @pickupDAO.setter
    def pickupDAO(self, value):
        self._pickupDAO = value

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
    pDAO = PickupLinkDAO()
    pDAO.setVerboseMode(True)
    try:
        d = Connexion().connect()
        pu = pDAO.getById(d, False, [], 26)
        print pu
    except:
        Connexion().exception()
    finally:
        Connexion().disconnect(d)
