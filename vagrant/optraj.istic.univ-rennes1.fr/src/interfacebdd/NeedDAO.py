# coding=utf8


from AbstractDAO import AbstractDAO
from NaturalJoin import NaturalJoin, INNER_JOIN
from system.Need import Need
from CraftDAO import CraftDAO
from QualificationDAO import QualificationDAO


class NeedDAO(AbstractDAO):
    '''
    Classe SiteDAO :
    Hérite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num",
                    "ID_PHASE": "numPhase",
                    "NEED": "need"}

    MAPPING_FIL = {"num": "ID",
                   "numPhase": "ID_PHASE",
                   "qualification": "ID_QUALIFICATION",
                   "craft": "ID_CRAFT",
                   "need": "NEED"}

    JOIN_CRAFT = NaturalJoin(joinType=INNER_JOIN, tableName="CRAFT", alias="_craft", joinClauses=["e.ID_CRAFT = _craft.ID"], joinMappingCols=CraftDAO.MAPPING_COLS, joinId="ID_CRAFT")
    JOIN_QUALIFICATION = NaturalJoin(joinType=INNER_JOIN, tableName="QUALIFICATION", alias="_qualification", joinClauses=["e.ID_QUALIFICATION = _qualification.ID"], joinMappingCols=QualificationDAO.MAPPING_COLS, joinId="ID_QUALIFICATION")
    
    def __init__(self):
        super(NeedDAO, self).__init__(tableName="NEED", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL, joins=[self.JOIN_CRAFT, self.JOIN_QUALIFICATION])
        self._craftDAO = CraftDAO()
        self._qualificationDAO = QualificationDAO()
        self._dicoAttr = {"_craft": self.craftDAO, "_qualification": self.qualificationDAO}

    def _createElement(self):
        '''
        Créée un objet de type Need
        '''
        return Need()

    def insert(self, co=None, Obj=None):
        nDAO = NeedDAO()
        o = nDAO.getByFilter(co, False, [], ("craft", str(Obj.craft.num)), ("qualification", str(Obj.qualification.num)), ("numPhase", str(Obj.numPhase)))
        #print(o)
        if o != None:
            Obj.num = o.num
            res = super(NeedDAO, self).update(co, Obj)
            return res
        else:
            res = super(NeedDAO, self).insert(co, Obj)
            return res

    '''
    ========================= Setters/accesseurs ==============================
    '''

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
