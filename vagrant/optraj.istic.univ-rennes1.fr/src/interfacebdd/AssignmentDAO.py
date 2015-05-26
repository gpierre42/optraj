# coding=utf8
'''
Created on 11 Nov 2013

@author: Vivien Lelouette
'''

from AbstractDAO import AbstractDAO
from NaturalJoin import NaturalJoin, INNER_JOIN
from string import Template
from system.Assignment import Assignment
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

class AssignmentDAO(AbstractDAO):
    '''
    Classe AssignmentDAO :
    Hérite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num"}

    MAPPING_FIL = {"num": "ID",
                   "worker": "ID_WORKER",
                   "phase": "ID_PHASE"}

    JOIN_WORKER = NaturalJoin(joinType=INNER_JOIN, tableName="WORKER", alias="_worker", joinClauses=["e.ID_WORKER = _worker.ID"], joinMappingCols=WorkerDAO.MAPPING_COLS, joinId="ID_WORKER")
    JOIN_PHASE = NaturalJoin(joinType=INNER_JOIN, tableName="PHASE", alias="_phase", joinClauses=["e.ID_PHASE = _phase.ID"], joinMappingCols=PhaseDAO.MAPPING_COLS, joinId="ID_PHASE")
    JOIN_POSITION_WORKER = NaturalJoin(joinType=INNER_JOIN, tableName="POSITION", alias="_worker_position", joinClauses=["_worker.ID_POSITION = _worker_position.ID"], joinMappingCols=PositionDAO.MAPPING_COLS, joinId="ID_POSITION")
    JOIN_CRAFT_WORKER = NaturalJoin(joinType=INNER_JOIN, tableName="CRAFT", alias="_worker_craft", joinClauses=["_worker.ID_CRAFT = _worker_craft.ID"], joinMappingCols=CraftDAO.MAPPING_COLS, joinId="ID_CRAFT")
    JOIN_QUALIFICATION_WORKER = NaturalJoin(joinType=INNER_JOIN, tableName="QUALIFICATION", alias="_worker_qualification", joinClauses=["_worker.ID_QUALIFICATION = _worker_qualification.ID"], joinMappingCols=QualificationDAO.MAPPING_COLS, joinId="ID_QUALIFICATION")

    def __init__(self):
        super(AssignmentDAO, self).__init__(tableName="ASSIGNMENT", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL, joins=[self.JOIN_WORKER, self.JOIN_PHASE, self.JOIN_POSITION_WORKER, self.JOIN_CRAFT_WORKER, self.JOIN_QUALIFICATION_WORKER])
        # Objets DAO utile pour former la jointure
        self._workerDAO = WorkerDAO()
        self._phaseDAO = PhaseDAO()
        self._dicoAttr = {"_worker": self.workerDAO, "_phase": self.phaseDAO}

    def _createElement(self):
        '''
        Créée un objet de type Assignment
        '''
        return Assignment()
    
    def insert(self, co=None, Obj=None):
        '''
        Permet d'insÃ©rer un objet python dans la base de donnÃ©e.
        On passe ici un objet Obj en paramètre.
        '''
        idAssign = super(AssignmentDAO, self).update(co, Obj)
        if idAssign == -1:
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
    
            cursor = co[1]
            # execution d'une requete
            cursor.execute(request)

            co[0].commit()
    
            # on retournel'id de l'objet insÃ©rÃ©
            idAssign = cursor.lastrowid
            if idAssign == -1:
                return idAssign
            return idAssign
        else:
            return idAssign
    
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

    '''
    ========================= Méthodes publiques ===================
    '''
    def _buildPartObject(self, dico):
        a = Assignment()
        a.phase.numWeek = dico["_phase_numWeek"]
        a.phase.numYear = dico["_phase_numYear"]
        a.phase.numSite = dico["_phase_numSite"]
        a.worker.num = dico["_worker_num"]
        return a


    @staticmethod
    def getExistingAssignmentsTree(co=None, lazzy=False, partLazzy=[], numYears=range(2000, 2100), numWeeks=range(1, 53)):

        '''
        Récupère les affectations existantes en BDD et les ranges dans un dictionnaire dict(num year, dict(num week, set(ouvrier)))

        On peut voir ca comme un arbre de profondeur 3, le premier niveau représentant les années,
        le second les semaines et le troisième les ouvriers affectés durant cette semaine.

        Il est possible de filtrer le résultat par année ou semaine

        Args:
            numYears::set(int) l'ensemble des années pour lesquelles on filtre (on auras pas d'années dans le résultat qui ne soit pas dans cet ensemble)
            numWeek::set(int) l'ensemble des années pour lesquelles on filtre (on auras pas d'années dans le résultat qui ne soit pas dans cet ensemble)

        Returns
            un dict(num year, dict(num week, set(ouvrier))) contenant la représentation de toutes les phases en BDD
        '''
        assign = AssignmentDAO()
        existingAssignments = dict()  # existingAssignement::dict(nun year, dict(num week, set(ouvrier)))
        for elem in assign.getAll(co, lazzy, partLazzy):
            p = elem.phase
            if p.numYear in numYears and p.numWeek in numWeeks:
                if p.numYear not in existingAssignments:  # initialisation de l'ensemble si la clé est inexistante
                    existingAssignments[p.numYear] = dict()
                if p.numWeek not in existingAssignments[p.numYear]:  # initialisation de l'ensemble si la clé est inexistante
                    existingAssignments[p.numYear][p.numWeek] = set()
                existingAssignments[p.numYear][p.numWeek].add(elem.worker)  # ajout de l'ouvrier dans l'ensemble
        return existingAssignments

    @staticmethod
    def getExistingAssignmentsByPhase(co=None, lazzy=False, partLazzy=[]):
        '''
        Récupère les affectations existantes en BDD et les ranges dans un dictionnaire dict(n°phase, set(ouvrier))

        Returns
            un dict(n°phase, set(ouvrier))
        '''
        assign = AssignmentDAO()
        res = dict()
        for elem in assign.getAll(co, lazzy, partLazzy):
            numP = elem.phase.num
            if numP not in res:
                res[numP] = set()
            res[numP].add(elem.worker)
        return res

    def getPartAssignment(self, co=None, numWeekInit=-1, numYearInit=-1, numWeekEnd=-1, numYearEnd=-1):
        '''
        Prend en parametre un ou plusieurs doublets du type : ("nom", "bob") => WHERE NOM='Bob'
        Permet de rÃ©cupÃ©rer un objet python depuis la base de donnÃ©e en fonction d'un filtre.
        Le type d'objet retournÃ©e varie en fonction de la classe fille qui l'appel.
        '''

        TEMPLATE_WHERE_NAT = Template("select A.ID_WORKER as _worker_num, A.FIRST_NAME as _worker_firstName, A.NAME as _worker_name, A.ADDRESS as _worker_position_address," + \
                                         "E.ID_SITE _phase_site_num, E.NUM_SITE as _phase_site_numSite, E.NUM_WEEK as _phase_numWeek, E.NUM_YEAR as _phase_numYear " + \
                                        "from (select w.ID as ID_WORKER, w.FIRST_NAME, w.NAME, p.ADDRESS " + \
                                                "from WORKER w, POSITION p " + \
                                                "where w.ID_POSITION = p.ID) A, " + \
                                            "(select G.ID_WORKER, D.ID_SITE, D.NUM_SITE, D.NUM_WEEK, D.NUM_YEAR " + \
                                                "from ASSIGNMENT G, (select B.ID_SITE, B.NUM_SITE, C.NUM_WEEK, C.NUM_YEAR, C.ID_PHASE " + \
                                                                    "from (select SITE.ID as ID_SITE, SITE.NUM_SITE " + \
                                                                            "from SITE " + \
                                                                            """where "$dateInit" >= SITE.DATE_INIT and "$dateEnd" <= SITE.DATE_END) B, """ + \
                                                                         "(select PHASE.ID as ID_PHASE, PHASE.NUM_WEEK, PHASE.NUM_YEAR, PHASE.ID_SITE " + \
                                                                             "from PHASE " + \
                                                                             "where $numYearInit <= PHASE.NUM_YEAR and $numYearEnd >= PHASE.NUM_YEAR " + \
                                                                                     "and $numWeekInit <= PHASE.NUM_WEEK and $numWeekEnd >= PHASE.NUM_WEEK) C ) D " + \
                                                "where G.ID_PHASE = D.ID_PHASE) E " + \
                                        "where A.ID_WORKER = E.ID_WORKER")
        
        from isoweek import Week
        d1 = Week(numYearInit, numWeekInit).monday()
        d2 = Week(numYearEnd, numWeekEnd).monday()
        # Construit la requÃªte SQL
        request = TEMPLATE_WHERE_NAT.substitute(dateInit = d1.isoformat(), dateEnd = d2.isoformat(), numYearInit = numYearInit, numYearEnd = numYearEnd, numWeekInit = numWeekInit, numWeekEnd = numWeekEnd)
        if self._verboseMode:
            (request)

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
                res.add(self._buildObject(co, x))
            return res
        else:
            return None
        
    def getPartAssignment2(self, co=None, numWeekInit=-1, numYearInit=-1, numWeekEnd=-1, numYearEnd=-1):
        '''
        effectue une requete afin de récupérer les assignments avec les info suivante : numWorker, idSite, numWeek, numYear
        
        Les affectations retournées sont filtrée suivant les valeurs en paramètre
        '''

        TEMPLATE_WHERE_NAT = Template("select ASSIGNMENT.ID_WORKER as _worker_num, PHASE_FILTRE.ID_SITE as _phase_numSite, PHASE_FILTRE.NUM_WEEK as _phase_numWeek, PHASE_FILTRE.NUM_YEAR as _phase_numYear " + \
                                        "from ASSIGNMENT, (select PHASE.ID as ID_PHASE, PHASE.NUM_WEEK, PHASE.NUM_YEAR, PHASE.ID_SITE " + \
                                                        "from PHASE " + \
                                                        "where ($numYearInit <= PHASE.NUM_YEAR and $numWeekInit <= PHASE.NUM_WEEK) or $numYearInit < PHASE.NUM_YEAR) PHASE_FILTRE " + \
                                        "where ASSIGNMENT.ID_PHASE = PHASE_FILTRE.ID_PHASE")
        # Construit la requÃªte SQL
        request = TEMPLATE_WHERE_NAT.substitute(numYearInit = numYearInit, numYearEnd = numYearEnd, numWeekInit = numWeekInit, numWeekEnd = numWeekEnd)
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
                #print(x)
                #print(self._buildPartObject(x).serial())
                res.add(deepcopy(self._buildPartObject(x)))
            return res
        else:
            return None
