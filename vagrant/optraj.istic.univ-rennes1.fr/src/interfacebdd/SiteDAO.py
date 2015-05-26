# coding=utf8
'''
Created on 11 Nov 2013

@author: Vivien Lelouette
'''

from AbstractDAO import AbstractDAO
from NaturalJoin import NaturalJoin, INNER_JOIN
from PositionDAO import PositionDAO
from PhaseDAO import PhaseDAO
from system.Site import Site
from Connexion import Connexion
from system.Position import Position
from datetime import date



class SiteDAO(AbstractDAO):
    '''
    Classe SiteDAO :
    Hérite de la classe AbstractDAO
    '''

    MAPPING_COLS = {"ID": "num",
                    "NUM_SITE": "numSite",
                    "NAME": "name",
                    "SITE_MASTER": "siteMaster",
                    "SITE_MANAGER": "siteManager",
                    "DATE_INIT": "dateInit",
                    "DATE_END": "dateEnd",
                    "COLOR": "color"
                    }

    MAPPING_FIL = {"num": "ID",
                   "numSite": "NUM_SITE",
                   "name": "NAME",
                   "siteMaster": "SITE_MASTER",
                   "siteManager": "SITE_MANAGER",
                   "dateInit": "DATE_INIT",
                   "dateEnd": "DATE_END",
                   "color": "COLOR"
                   }

    JOIN_POSITION = NaturalJoin(joinType=INNER_JOIN, tableName="POSITION", alias="_position", joinClauses=["e.ID_POSITION = _position.ID"], joinMappingCols=PositionDAO.MAPPING_COLS, joinId="ID_POSITION")

    def __init__(self):
        super(SiteDAO, self).__init__(tableName="SITE", mappingCols=self.MAPPING_COLS, mappingFil=self.MAPPING_FIL, joins=[self.JOIN_POSITION])
        # Objets DAO utile pour former la jointure
        self._positionDAO = PositionDAO()
        self._dicoAttr = {"_position": self.positionDAO}

    def _createElement(self):
        '''
        Créée un objet de type Site
        '''
        return Site()

    def _buildObjectOld(self, dico):
        s = super(SiteDAO, self)._buildObjectOld(dico)
        p = PhaseDAO().getAllByFilterOld(("numSite", str(s.num)))
        s.phases = p
        return s

    def _buildObject(self, co=None, lazzy=False, partLazzy=[], dico={}):
        s = super(SiteDAO, self)._buildObject(co=co, lazzy=lazzy, partLazzy=partLazzy, dico=dico)
        p = {}
        if(not lazzy):
            p = PhaseDAO().getAllByFilter(co, lazzy, partLazzy, ("numSite", str(s.num)))
        s.phases = p
        return s

    def insert(self, co=None, Obj=None):
        idSite = super(SiteDAO, self).insert(co, Obj)
        p = PhaseDAO()
        for ph in  Obj.phases:
            ph.numSite = idSite
            p.insert(co, ph)
        return idSite

    def update(self, co=None, Obj=None):
        idSite = super(SiteDAO, self).update(co, Obj)
        n = PhaseDAO()
        if idSite != -1:
            for p in Obj.phases:
                idPhase = n.update(co, p)
                if idPhase == -1:
                    p.numSite = idSite
                    n.insert(co, p)
            return idSite
        else:
            return -1

    def deleteById(self, co=None, ident=-1):
        p = PhaseDAO().getAllByFilter(co, False, [], ("numSite", str(ident)))
        for ph in p:
            PhaseDAO().deleteById(co, ph.num)
        super(SiteDAO, self).deleteById(co, ident)

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
    def dicoAttr(self):
        return self._dicoAttr

    @dicoAttr.setter
    def dicoAttr(self, value):
        self._dicoAttr = value
   
if __name__ == '__main__':   
    try:
        d = Connexion().connect()
        pos = Position(num=-1, long=001, lat=002, address="test")
        siteIns = Site(num=-1, numSite="FR52005", name="champie", siteMaster="test", siteManager="test2", position=pos, dateInit=date(2013, 1, 1), dateEnd=date(2013, 2, 1), color="#6390df", phases=set())
        SiteDAO().insert(d, siteIns)
    except:
        Connexion().exception()
    finally:
        Connexion().disconnect(d) 
    