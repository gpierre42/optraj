# coding=utf8
'''
Created on 05 fév 2013

@author: Vivien Lelouette
'''
from AbstractDAO import AbstractDAO
from NaturalJoin import NaturalJoin, INNER_JOIN
from CarDAO import CarDAO
from PhaseDAO import PhaseDAO
from system.Shuttle import Shuttle
from system.Passenger import Passenger
from WorkerDAO import WorkerDAO
from system.Worker import Worker
from PositionDAO import PositionDAO
from QualificationDAO import QualificationDAO
from CraftDAO import CraftDAO
from system.PickupLink import PickupLink
from PickupLinkDAO import PickupLinkDAO
from PassengerDAO import PassengerDAO
from string import Template
from interfacebdd.Connexion import Connexion
import operator

class ShuttleDAO(AbstractDAO):
    '''
    Classe ShuttleDAO :
    Hérite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num"}

    MAPPING_FIL = {"num": "ID",
                    "driver": "ID_DRIVER",
                    "car": "ID_CAR",
                    "phase": "ID_PHASE"
                    }

    JOIN_DRIVER = NaturalJoin(joinType=INNER_JOIN, tableName="WORKER", alias="_driver", joinClauses=["e.ID_DRIVER = _driver.ID"], joinMappingCols=WorkerDAO.MAPPING_COLS, joinId="ID_DRIVER")
    JOIN_CAR = NaturalJoin(joinType=INNER_JOIN, tableName="CAR", alias="_car", joinClauses=["e.ID_CAR = _car.ID"], joinMappingCols=CarDAO.MAPPING_COLS, joinId="ID_CAR")
    JOIN_PHASE = NaturalJoin(joinType=INNER_JOIN, tableName="PHASE", alias="_phase", joinClauses=["e.ID_PHASE = _phase.ID"], joinMappingCols=PhaseDAO.MAPPING_COLS, joinId="ID_PHASE")
    JOIN_POSITION_DRIVER = NaturalJoin(joinType=INNER_JOIN, tableName="POSITION", alias="_driver_position", joinClauses=["_driver.ID_POSITION = _driver_position.ID"], joinMappingCols=PositionDAO.MAPPING_COLS, joinId="ID_POSITION")
    JOIN_CRAFT_DRIVER = NaturalJoin(joinType=INNER_JOIN, tableName="CRAFT", alias="_driver_craft", joinClauses=["_driver.ID_CRAFT = _driver_craft.ID"], joinMappingCols=CraftDAO.MAPPING_COLS, joinId="ID_CRAFT")
    JOIN_QUALIFICATION_DRIVER = NaturalJoin(joinType=INNER_JOIN, tableName="QUALIFICATION", alias="_driver_qualification", joinClauses=["_driver.ID_QUALIFICATION = _driver_qualification.ID"], joinMappingCols=QualificationDAO.MAPPING_COLS, joinId="ID_QUALIFICATION")

    def __init__(self):
        super(ShuttleDAO, self).__init__(tableName="SHUTTLE", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL, joins=[self.JOIN_DRIVER, self.JOIN_POSITION_DRIVER, self.JOIN_CRAFT_DRIVER, self.JOIN_QUALIFICATION_DRIVER, self.JOIN_CAR, self.JOIN_PHASE])
        # Objets DAO utile pour former la jointure
        self._workerDAO = WorkerDAO()
        self._carDAO = CarDAO()
        self._phaseDAO = PhaseDAO()
        self._dicoAttr = {"_driver": self.workerDAO, "_car": self.carDAO, "_phase": self.phaseDAO}

    def _createElement(self):
        '''
        Créée un objet de type Site
        '''
        return Shuttle()

    def _buildObject(self, co=None, lazzy=False, partLazzy=[], dico={}):
        p = super(ShuttleDAO, self)._buildObject(co, lazzy, partLazzy, dico)
        if(not lazzy):
            p.pickups = [x.pickup for x in PickupLinkDAO().getAllByFilter(co, False, [], ("numShuttle", str(p.num)))]
            p.passengers = [elem for elem in PassengerDAO().getAllByFilter(co, False, [], ("idShuttle", str(p.num)))]
        else :
            pickupLinks = PickupLinkDAO().getAllByFilter(co, True, [], ("numShuttle", str(p.num)))
            for x in pickupLinks:
                p.pickups.append(x.pickup)
            p.passengers = PassengerDAO().getAllByFilter(co, True, [], ("idShuttle", str(p.num)))
        return p

    def insert(self, co=None, Obj=None):
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
        idShuttle = cursor.lastrowid
        
        # insertion des pickuplinks liés
        pdao = PickupLinkDAO()
        for p in  Obj.pickups:
            pl = PickupLink(num=-1, pickup = p, numShuttle = idShuttle)
            #print p.num
            #print idShuttle
            pdao.insert(co, pl)
        
        pdao = PassengerDAO()  
        #insertion des passengers liés
        for p in Obj.passengers:
            p.idShuttle=idShuttle
            pdao.insert(co, p)
        return idShuttle
        
    """
    def update(self, co=None, Obj=None):
        idShuttle = super(ShuttleDAO, self).update(co, Obj)
        p = PickupLinkDAO()
        if idShuttle != -1:
            for pl in Obj.pickupLinks:
                idPickupLink = p.update(co, pl)
                if idPickupLink == -1:
                    pl.numShuttle = idShuttle
                    p.insert(co, pl)
            return idShuttle
        else:
            return -1
    """

    def deleteById(self, co=None, ident=-1):
        p = PickupLinkDAO().getAllByFilter(co, False, [], ("numShuttle", str(ident)))
        for pl in p:
            PickupLinkDAO().deleteById(co, pl.num)
        super(ShuttleDAO, self).deleteById(co, ident)

    '''
    ========================= Setters/accesseurs ==============================
    '''

    @property
    def workerDAO(self):
        return self._workerDAO

    @workerDAO.setter
    def workerDAO(self, value):
        self._workerDAO = value

    @property
    def carDAO(self):
        return self._carDAO

    @carDAO.setter
    def carDAO(self, value):
        self._carDAO = value

    @property
    def phaseDAO(self):
        return self._phaseDAO

    @phaseDAO.setter
    def phaseDAO(self, value):
        self._phaseDAO = value

    @property
    def dicoAttr(self):
        return self._dicoAttr

    @dicoAttr.setter
    def dicoAttr(self, value):
        self._dicoAttr = value

if __name__ == '__main__':
    sDAO = ShuttleDAO()
    try:
        d = Connexion().connect()
        shut = ShuttleDAO().getById(d, False, [], 13)
        for p in shut.passengers:
            print p
        print shut
    except:
        Connexion().exception()
    finally:
        Connexion().disconnect(d)
    
