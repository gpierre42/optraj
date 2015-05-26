# coding=utf8
'''
Created on 08 Nov 2013

@author: Vivien Lelouette
'''

from AbstractDAO import AbstractDAO
from system.Worker import Worker
from NaturalJoin import NaturalJoin, INNER_JOIN
from PositionDAO import PositionDAO
from CraftDAO import CraftDAO
from QualificationDAO import QualificationDAO
from system.Craft import Craft
from system.Qualification import Qualification
from system.Position import Position
from string import Template
import operator
from interfacebdd.Connexion import Connexion

class WorkerDAO(AbstractDAO):
    '''
    Classe WorkerDAO :
    Hérite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num",
                    "NAME": "name",
                    "FIRST_NAME": "firstName",
                    "BIRTHDATE": "birthdate",
                    "LICENCE": "licence"}

    MAPPING_FIL = {"num": "ID",
                    "name": "NAME",
                    "firstName": "FIRST_NAME",
                    "birthdate": "BIRTHDATE",
                    "licence": "LICENCE"}

    JOIN_POSITION = NaturalJoin(joinType=INNER_JOIN, tableName="POSITION", alias="_position", joinClauses=["e.ID_POSITION = _position.ID"], joinMappingCols=PositionDAO.MAPPING_COLS, joinId="ID_POSITION")
    JOIN_CRAFT = NaturalJoin(joinType=INNER_JOIN, tableName="CRAFT", alias="_craft", joinClauses=["e.ID_CRAFT = _craft.ID"], joinMappingCols=CraftDAO.MAPPING_COLS, joinId="ID_CRAFT")
    JOIN_QUALIFICATION = NaturalJoin(joinType=INNER_JOIN, tableName="QUALIFICATION", alias="_qualification", joinClauses=["e.ID_QUALIFICATION = _qualification.ID"], joinMappingCols=QualificationDAO.MAPPING_COLS, joinId="ID_QUALIFICATION")

    def __init__(self):
        super(WorkerDAO, self).__init__(tableName="WORKER", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL, joins=[self.JOIN_POSITION, self.JOIN_CRAFT, self.JOIN_QUALIFICATION])
        # Objets DAO utile pour former la jointure
        self._positionDAO = PositionDAO()
        self._craftDAO = CraftDAO()
        self._qualificationDAO = QualificationDAO()
        self._dicoAttr = {"_position": self.positionDAO, "_craft": self.craftDAO, "_qualification": self.qualificationDAO}

    def _createElement(self):
        '''
        Créée un objet de type Worker
        '''
        return Worker()

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
    def craftDAO(self):
        return self._craftDAO

    @craftDAO.setter
    def craftDAO(self, value):
        self._craftDAO = value

    @property
    def qualificationDAO(self):
        return self._qualificationDAO

    @qualificationDAO.setter
    def qualificationDAO(self, value):
        self._qualificationDAO = value

    @property
    def dicoAttr(self):
        return self._dicoAttr

    @dicoAttr.setter
    def dicoAttr(self, value):
        self._dicoAttr = value

    def insert(self, co=None, Worker=None):
        '''
        Permet d'insérer un objet python dans la base de donnée.
        On passe ici un objet Obj en paramètre.
        '''

        # Construit une liste des valeurs à insérer dans la base
        listValue = [col + "=" + "\"" + str(operator.attrgetter(attr)(Worker)) + "\"" for (col, attr) in self.mappingCols.items()]

        # Construit les éventuels appels récursifs pour insérer les objets lié
        for j in ([] if self.joins is None else self.joins):

            attribut = j.alias
            if (str(j.alias) == '_craft'):
                listValue.append(j.joinId + "=" + str(Worker.craft.num))

            else:
                if (str(j.alias) == '_qualification'):
                    listValue.append(j.joinId + "=" + str(Worker.qualification.num))

                else:
                    if len(attribut.split("_")) <= 2:
                        id_obj = self._dicoAttr[j.alias].insert(co, operator.attrgetter(attribut.replace("_", ""))(Worker))
                        listValue.append(j.joinId + "=" + str(id_obj))

        # Construit la requÃªte SQL

        request = self.TEMPLATE_INSERT.substitute(table=self.tableName, value=", ".join(listValue))
        # print(request)

        # Initialisation de la connexion
        db = co[0]

        # declaration d'un objet curseur -> sert à executer des requetes sql sur la base
        cursor = co[1]

        # execution d'une requete
        cursor.execute(request)

        db.commit()

        # on retournel'id de l'objet inséré
        return cursor.lastrowid

    def update(self, co=None, Worker=None):
        '''
        Permet de mettre à jour un objet python dans la base de donnée.
        On passe ici un objet Obj en paramètre.
        '''
        # Construit une liste des valeurs à modifier dans la base
        listValue = [col + "=" + "\"" + str(operator.attrgetter(attr)(Worker)) + "\"" for (col, attr) in self.mappingCols.items()]

        # Construit les éventuels appels récursifs pour insérer les objets lié
        for j in ([] if self.joins is None else self.joins):
                    attribut = j.alias
                    if (str(j.alias) == '_craft'):
                        listValue.append(j.joinId + "=" + str(Worker.craft.num))

                    else:
                        if (str(j.alias) == '_qualification'):
                            listValue.append(j.joinId + "=" + str(Worker.qualification.num))

                        else:
                            if len(attribut.split("_")) <= 2:
                                id_obj = self._dicoAttr[j.alias].update(co, operator.attrgetter(attribut.replace("_", ""))(Worker))
                                listValue.append(j.joinId + "=" + str(id_obj))

        # Construit la requÃªte SQL
        # TEMPLATE_UPDATE = Template("UPDATE FROM $table SET $columns=$clauses where e.ID=$clauses")
        request = self.TEMPLATE_UPDATE.substitute(table=self.tableName, value=", ".join(listValue), clauses=Worker.num)
        # print(request)

        # Initialisation de la connexion
        db = co[0]

        # declaration d'un objet curseur -> sert à executer des requetes sql sur la base
        cursor = co[1]

        # execution d'une requete
        cursor.execute(request)

        db.commit()

        # on retournel'id de l'objet mis à jour
        return Worker.num

    def getAssignedToSite(self, co=None, idSite=-1):
        TEMPLATE_WHERE_NAT = Template("select WORKER_FILTER.ID as _num, WORKER_FILTER.NAME as _name, WORKER_FILTER.FIRST_NAME as _firstName, POSITION.LONGITUDE as _position_longitude, POSITION.LATITUDE as _position_latitude, POSITION.ADDRESS as _position_address from " + \
                                        "(select * from WORKER, " + \
                                                        "(select ID_WORKER from ASSIGNMENT " + \
                                                            "NATURAL JOIN " + \
                                                        "(select * from PHASE where ID_SITE=$idSite) PHASE_FILTER) ID_FILTER " + \
                                                        "where WORKER.ID=ID_FILTER.ID_WORKER) WORKER_FILTER " + \
                                        "NATURAL JOIN POSITION;")
        # Construit la requÃªte SQL
        request = TEMPLATE_WHERE_NAT.substitute(idSite=idSite)
        if self._verboseMode:
            print(request)

        cursor = co[1]

        # execution d'une requete
        cursor.execute(request)

        o = cursor.fetchall()
        if o != None:
            # construit et retourne un Objet du Systeme
            res = set()
            for x in o:
                if self._verboseMode:
                    print(x)
                #print(self._buildPartObject(x).serial())
                res.add(self._buildObject(co, False, [], x))
            return res
        else:
            return None
        
    def getAssignedToSiteOnWeek(self, co=None, idSite=-1, week=-1, year=-1):
        TEMPLATE_WHERE_NAT = Template("select WORKER_FILTER.ID as _num, WORKER_FILTER.NAME as _name, WORKER_FILTER.FIRST_NAME as _firstName, POSITION.LONGITUDE as _position_longitude, POSITION.LATITUDE as _position_latitude, POSITION.ADDRESS as _position_address, CRAFT.NAME as _craft_name, QUALIFICATION.NAME as _qualification_name  from " + \
                                        "(select * from WORKER, " + \
                                                        "(select ID_WORKER from ASSIGNMENT INNER JOIN " + \
                                                                "(select * from PHASE where ID_SITE=$idSite and NUM_WEEK=$week and NUM_YEAR=$year)" + \
                                                                "as PHASE_FILTER on ASSIGNMENT.ID_PHASE=PHASE_FILTER.ID) as ID_FILTER " + \
                                                        "where WORKER.ID=ID_FILTER.ID_WORKER) WORKER_FILTER " + \
                                        "INNER JOIN POSITION on WORKER_FILTER.ID_POSITION=POSITION.ID " + \
                                        "INNER JOIN CRAFT on WORKER_FILTER.ID_CRAFT=CRAFT.ID " + \
                                        "INNER JOIN QUALIFICATION on WORKER_FILTER.ID_QUALIFICATION=QUALIFICATION.ID;")
        # Construit la requÃªte SQL
        request = TEMPLATE_WHERE_NAT.substitute(idSite=idSite, week=week, year=year)
        if self._verboseMode:
            print(request)

        cursor = co[1]

        # execution d'une requete
        cursor.execute(request)

        o = cursor.fetchall()
        if o != None:
            # construit et retourne un Objet du Systeme
            res = set()
            for x in o:
                if self._verboseMode:
                    print(x)
                #print(self._buildPartObject(x).serial())
                res.add(self._buildObject(co, False, [], x))
            return res
        else:
            return None
        
    def getCountCraftQualif(self, co=None):
        request = "SELECT ID_CRAFT as numCraft, ID_QUALIFICATION as numQualification, count(*) as nbWorker from WORKER group by ID_CRAFT, ID_QUALIFICATION;"
        cursor = co[1]

        # execution d'une requete
        cursor.execute(request)
        
        o = cursor.fetchall()
        return o

if __name__ == '__main__':
    '''
    test de la classe
    '''
    Ouv = WorkerDAO()
    Pos = PositionDAO()
    '''
    Pos = PositionDAO()
    for c in Ouv.getAll():
        print (c)
    Pos.getById(7)
    Ouv.deleteById(3)
    Pos.getById(7)
    Ouv.getById(3)
    '''
    posIns = Position(num=5, long=1500, lat=8050)
    # OuvIns = Worker(num=1, name="Robert2", firstName="Charles4", birthdate="1960-05-27", position=posIns)
    try:
        d = Connexion().connect()
        Ouv.getCountCraftQualif(d)
    except:
        Connexion().exception()
    finally:
        pass

    '''

    cra = Craft(3, "COCO")z
    qualif = Qualification(2, "Yiyhiys")
    posIns = Position(num=34, long=1500, lat=8050)
    OuvIns = Worker(num=35, name="Robert2", firstName="Charles4777777", birthdate="1960-05-27", position=posIns, craft=cra, qualification=qualif)
    Ouv.update(OuvIns)

    print(Ouv.getByFilter(("firstName", "Bob"), ("name", "Lebricoleur")))
    '''
