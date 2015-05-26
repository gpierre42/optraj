# coding=utf8

from AbstractDAO import AbstractDAO
from system.Craft import Craft


class CraftDAO(AbstractDAO):
    '''
     Classe CraftDAO :
       Herite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num",
                    "NAME": "name"}

    MAPPING_FIL = {"num": "ID",
                    "name": "NAME"}


    def __init__(self):
        super(CraftDAO, self).__init__(tableName="CRAFT", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL)


    def _createElement(self):
        '''
        Cree un objet de type metier
        '''
        return Craft()

    def insert(self, co=None, Obj=None):
        cDAO = CraftDAO()
        c = cDAO.getByFilter(co, False, [], ("name", Obj.name))
        if c != None:
            return c.num
        else:
            return super(CraftDAO, self).insert(co, Obj)