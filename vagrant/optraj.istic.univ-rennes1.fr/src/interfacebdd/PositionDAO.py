# coding=utf8
'''
Created on 10 Nov 2013

@author: Vivien Lelouette
'''
from AbstractDAO import AbstractDAO
from system.Position import Position


class PositionDAO(AbstractDAO):
    '''
    Classe PositionDAO :
    Hérite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num",
                    "LATITUDE": "latitude",
                    "LONGITUDE": "longitude",
                    "ADDRESS" : "address"}

    MAPPING_FIL = {"num": "ID",
                    "latitude": "LATITUDE",
                    "longitude": "LONGITUDE",
                    "address": "ADDRESS"}

    def __init__(self):
        super(PositionDAO, self).__init__(tableName="POSITION", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL)

    def _createElement(self):
        '''
        Créée un objet de type Position
        '''
        return Position()
