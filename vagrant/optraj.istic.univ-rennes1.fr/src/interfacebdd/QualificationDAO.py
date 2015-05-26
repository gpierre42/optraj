'''
Created on 21 janv. 2014

@author: Nicolas Carre
'''

from AbstractDAO import AbstractDAO
from system.Qualification import Qualification
from interfacebdd.CraftDAO import CraftDAO
from string import Template

class QualificationDAO(AbstractDAO):
    '''
     Classe QualificationDAO :
       Herite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num",
                    "NAME": "name"}

    MAPPING_FIL = {"num": "ID",
                    "name": "NAME"}

    def __init__(self):
        super(QualificationDAO, self).__init__(tableName="QUALIFICATION", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL)

    def _createElement(self):
        '''
        Cree un objet de type Qualification
        '''
        return Qualification()
    
    def insert(self, co=None, Obj=None):
        qDAO = QualificationDAO()
        q = qDAO.getByFilter(co, False, [], ("name", Obj.name))
        if q != None:
            return q.num
        else:
            return super(QualificationDAO, self).insert(co, Obj)
        
    