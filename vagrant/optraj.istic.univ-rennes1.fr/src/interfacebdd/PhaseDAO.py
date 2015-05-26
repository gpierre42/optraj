# coding=utf8
'''
Created on 18 janvier 2014

@author: Vivien Lelouette
'''

from AbstractDAO import AbstractDAO
from NaturalJoin import NaturalJoin, INNER_JOIN
from system.Phase import Phase
from NeedDAO import NeedDAO
from Connexion import Connexion


class PhaseDAO(AbstractDAO):
    '''
    Classe PhaseDAO :
    Hérite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num",
                    "ID_SITE": "numSite",
                    "NUM_WEEK": "numWeek",
                    "NUM_YEAR": "numYear"}

    MAPPING_FIL = {"num": "ID",
                   "numSite": "ID_SITE",
                    "numWeek": "NUM_WEEK",
                    "numYear": "NUM_YEAR"}

    def __init__(self):
        super(PhaseDAO, self).__init__(tableName="PHASE", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL, joins=[])

    def _createElement(self):
        '''
        Créée un objet de type Site
        '''
        return Phase()

    def _buildObjectOld(self, dico):
        p = super(PhaseDAO, self)._buildObjectOld(dico)
        n = NeedDAO().getAllByFilterOld(("numPhase", str(p.num)))
        p.needs = n
        return p

    def _buildObject(self, co=None, lazzy=False, partLazzy=[], dico={}):
        p = super(PhaseDAO, self)._buildObject(co, lazzy, partLazzy, dico)
        if(not lazzy):
            n = NeedDAO().getAllByFilter(co, lazzy, partLazzy, ("numPhase", str(p.num)))
            p.needs = n
        return p

    def insert(self, co=None, Obj=None):
        idPhase = super(PhaseDAO, self).insert(co, Obj)
        n = NeedDAO()
        for ne in  Obj.needs:
            ne.numPhase = idPhase
            n.insert(co, ne)
        return idPhase

    def update(self, co=None, Obj=None):
        idPhase = super(PhaseDAO, self).update(co, Obj)
        if self._verboseMode:
            print(idPhase)
        n = NeedDAO()
        if idPhase != -1:
            for ne in Obj.needs:
                idNeed = n.update(co, ne)
                if idNeed == -1:
                    ne.numPhase = idPhase
                    n.insert(co, ne)
            return idPhase
        else:
            return -1

    def deleteById(self, co=None, ident=-1):
        n = NeedDAO().getAllByFilter(co, False, [], ("numPhase", str(ident)))
        for ne in n:
            NeedDAO().deleteById(co, ne.num)
        super(PhaseDAO, self).deleteById(co, ident)

if __name__ == '__main__':
    '''
    test de la classe
    '''

    try:
        d = Connexion().connect()
        phase1 = PhaseDAO()
        p = phase1.getById(d, False, [], 2)
        print (p)
    except:
        Connexion().exception()
    finally:
        Connexion().disconnect(d)
    #PhaseDAO().deleteById(4)
