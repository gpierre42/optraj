# coding=utf8
'''
Created on 05 fév 2013

@author: Vivien Lelouette
'''
from AbstractDAO import AbstractDAO
from system.Car import Car
from Connexion import Connexion
from string import Template


class CarDAO(AbstractDAO):
    '''
    Classe CarDAO :
    Hérite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num",
                    "PLATE": "plate",
                    "MODEL": "model",
                    "NB_PLACE": "nbPlace"
                    }

    MAPPING_FIL = {"num": "ID",
                    "plate": "PLATE",
                    "model": "MODEL",
                    "nbPlace": "NB_PLACE"
                    }
    TEMPLATE_SEL_IN = Template("Select $columns FROM $table e $joins WHERE $field IN ( $select )")
    TEMPLATE_SEL_NOT_IN = Template("Select $columns FROM $table e $joins WHERE $field NOT IN ( $select )")
    def __init__(self):
        super(CarDAO, self).__init__(tableName="CAR", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL)

    def _createElement(self):
        '''
        Créée un objet de type Site
        '''
        return Car()
    
    def getUsedCar(self, co=None, lazzy=False, partLazzy=[]):

        '''
        Permet de rÃ©cupÃ©rer un ensemble d'objet(set) python depuis la base de donnÃ©e.
        Le type d'objet retournÃ©e varie en fonction de la classe fille qui l'appel.
        '''

        # Construit la partie sÃ©lection de la requÃªte SQL
        listCols = ["e." + col + " as " + attr for (col, attr) in self.mappingCols.items()]

        if(lazzy):
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if partLazzy is None else partLazzy)]
            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if partLazzy is None else partLazzy) for (col, attr) in j.joinMappingCols.items()])
        else:
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if self.joins is None else self.joins)]

            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if self.joins is None else self.joins) for (col, attr) in j.joinMappingCols.items()])

        # Construit la requÃªte SQL
        request = self.TEMPLATE_SEL_IN.substitute(columns=", ".join(listCols), table=self.tableName, joins=" ".join(listJoins),field="ID", select= "SELECT DISTINCT ID_CAR FROM SHUTTLE")
        # print(request)

        # execution d'une requete
        cursor = co[1]
        cursor.execute(request)

        # construit et retourne un Objet du Systeme
        return {self._buildObject(co, lazzy, partLazzy, c) for c in cursor.fetchall()}
    
    def getUnUsedCar(self, co=None, lazzy=False, partLazzy=[]):

        '''
        Permet de rÃ©cupÃ©rer un ensemble d'objet(set) python depuis la base de donnÃ©e.
        Le type d'objet retournÃ©e varie en fonction de la classe fille qui l'appel.
        '''

        # Construit la partie sÃ©lection de la requÃªte SQL
        listCols = ["e." + col + " as " + attr for (col, attr) in self.mappingCols.items()]

        if(lazzy):
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if partLazzy is None else partLazzy)]
            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if partLazzy is None else partLazzy) for (col, attr) in j.joinMappingCols.items()])
        else:
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if self.joins is None else self.joins)]

            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if self.joins is None else self.joins) for (col, attr) in j.joinMappingCols.items()])

        # Construit la requÃªte SQL
        request = self.TEMPLATE_SEL_NOT_IN.substitute(columns=", ".join(listCols), table=self.tableName, joins=" ".join(listJoins),field="ID", select= "SELECT DISTINCT ID_CAR FROM SHUTTLE")
        # print(request)

        # execution d'une requete
        cursor = co[1]
        cursor.execute(request)

        # construit et retourne un Objet du Systeme
        return {self._buildObject(co, lazzy, partLazzy, c) for c in cursor.fetchall()}
    

    '''
    ========================= Setters/accesseurs ==============================
    '''

    @property
    def dicoAttr(self):
        return self._dicoAttr

    @dicoAttr.setter
    def dicoAttr(self, value):
        self._dicoAttr = value
