# coding=utf8
'''
Created on 05 fév 2013

@author: Vivien Lelouette
'''
from AbstractDAO import AbstractDAO
from NaturalJoin import NaturalJoin, INNER_JOIN, LEFT_JOIN, LEFT_OUTER_JOIN
from PickupDAO import PickupDAO
from WorkerDAO import WorkerDAO
from system.Passenger import Passenger
from PositionDAO import PositionDAO
from QualificationDAO import QualificationDAO
from CraftDAO import CraftDAO
import operator


class PassengerDAO(AbstractDAO):
    '''
    Classe PassengerDAO :
    Hérite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num",
                    "ID_SHUTTLE": "idShuttle"}

    MAPPING_FIL = {"num": "ID",
                    "pickup": "ID_PICKUP",
                    "worker": "ID_WORKER",
                    "idShuttle": "ID_SHUTTLE"}

    JOIN_WORKER = NaturalJoin(joinType=INNER_JOIN, tableName="WORKER", alias="_worker", joinClauses=["e.ID_WORKER = _worker.ID"], joinMappingCols=WorkerDAO.MAPPING_COLS, joinId="ID_WORKER")
    JOIN_POSITION_WORKER = NaturalJoin(joinType=INNER_JOIN, tableName="POSITION", alias="_worker_position", joinClauses=["_worker.ID_POSITION = _worker_position.ID"], joinMappingCols=PositionDAO.MAPPING_COLS, joinId="ID_POSITION")
    JOIN_CRAFT_WORKER = NaturalJoin(joinType=INNER_JOIN, tableName="CRAFT", alias="_worker_craft", joinClauses=["_worker.ID_CRAFT = _worker_craft.ID"], joinMappingCols=CraftDAO.MAPPING_COLS, joinId="ID_CRAFT")
    JOIN_QUALIFICATION_WORKER = NaturalJoin(joinType=INNER_JOIN, tableName="QUALIFICATION", alias="_worker_qualification", joinClauses=["_worker.ID_QUALIFICATION = _worker_qualification.ID"], joinMappingCols=QualificationDAO.MAPPING_COLS, joinId="ID_QUALIFICATION")
    JOIN_PICKUP = NaturalJoin(joinType=LEFT_JOIN, tableName="PICKUP", alias="_pickup", joinClauses=["e.ID_PICKUP = _pickup.ID"], joinMappingCols=PickupDAO.MAPPING_COLS, joinId="ID_PICKUP")
    JOIN_POSITION_PICKUP = NaturalJoin(joinType=LEFT_JOIN, tableName="POSITION", alias="_pickup_position", joinClauses=["_pickup.ID_POSITION = _pickup_position.ID"], joinMappingCols=PositionDAO.MAPPING_COLS, joinId="ID_POSITION")


    def __init__(self):
        super(PassengerDAO, self).__init__(tableName="PASSENGER", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL, joins=[self.JOIN_WORKER, self.JOIN_POSITION_WORKER, self.JOIN_CRAFT_WORKER, self.JOIN_QUALIFICATION_WORKER, self.JOIN_PICKUP, self.JOIN_POSITION_PICKUP])
        # Objets DAO utile pour former la jointure
        self._pickupDAO = PickupDAO()
        self._workerDAO = WorkerDAO()
        self._dicoAttr = {"_pickup": self._pickupDAO, "_worker": self._workerDAO}

    def _createElement(self):
        '''
        Créée un objet de type Site
        '''
        return Passenger()
    
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
                if operator.attrgetter(attribut.replace("_", ""))(Obj) != None:
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

    def update(self, co=None, Obj=None):
        '''
        Permet de mettre à jour un objet python dans la base de donnÃ©e.
        
        Args:
            co la Connexion
            Obj l'objet python à insérer
            
        Returns:
            l'id de l'objet mis à jour
        '''
        # Construit une liste des valeurs Ã  modifier dans la base
        listValue = [col + "=" + "\"" + str(operator.attrgetter(attr)(Obj)) + "\"" for (col, attr) in self.mappingCols.items()]
        # Construit les Ã©ventuels appels rÃ©cursifs pour insÃ©rer les objets liÃ©
        for j in ([] if self.joins is None else self.joins):
            attribut = j.alias
            if len(attribut.split("_")) <= 2:
                if operator.attrgetter(attribut.replace("_", ""))(Obj) != None:
                    id_obj = operator.attrgetter(attribut.replace("_", ""))(Obj).num
                    listValue.append(j.joinId + "=" + str(id_obj))
                else:
                    listValue.append(j.joinId + "=NULL")
        # Construit la requÃªte SQL
        # TEMPLATE_UPDATE = Template("UPDATE FROM $table SET $columns=$clauses where e.ID=$clauses")
        request = self.TEMPLATE_UPDATE.substitute(table=self.tableName, value=", ".join(listValue), clauses=Obj.num)
        if self._verboseMode:
            print(request)

        # execution d'une requete
        cursor = co[1]
        
        cursor.execute(request)

        co[0].commit()

        if(Obj.num != None):
            return Obj.num
        # on retournel'id de l'objet mis à jour
        return -1
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
    def workerDAO(self):
        return self._workerDAO

    @workerDAO.setter
    def workerDAO(self, value):
        self._workerDAO = value

    @property
    def dicoAttr(self):
        return self._dicoAttr

    @dicoAttr.setter
    def dicoAttr(self, value):
        self._dicoAttr = value
