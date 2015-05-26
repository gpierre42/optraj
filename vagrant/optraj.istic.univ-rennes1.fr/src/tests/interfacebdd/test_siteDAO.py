'''
Created on 23 mars 2014

@author: guillaume
'''

import os,sys
from unittest import TestCase
from tests.utils.utils import utils
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")
from interfacebdd.SiteDAO import SiteDAO
from system.Site import Site
from system.Position import Position
from datetime import date
from interfacebdd.Connexion import Connexion

class test_siteDAO(TestCase):
    """Test the stand-alone module functions."""

    def test_insert(self):
        d = Connexion().connect()
        try:
            pos = Position(num=-1, long=001, lat=002, address="test")
            siteIns = Site(num=-1, numSite="FR52005", name="champie", siteMaster="test", siteManager="test2", position=pos, dateInit=date(2013, 1, 1), dateEnd=date(2013, 2, 1), color="#6390df", phases=set())
            res = SiteDAO().insert(d, siteIns)
            siteRes = SiteDAO().getById(d, False, [], res)
            siteIns.num=siteRes.num
            siteIns.position.num = siteRes.position.num
            utils().equal(self, siteIns, siteRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
              
    def test_get(self):
        d = Connexion().connect()
        try:
            pos = Position(num=-1, long=001, lat=002, address="test")
            siteIns = Site(num=-1, numSite="52005", name="champie", siteMaster="test", siteManager="test2", position=pos, dateInit=date(2013, 1, 1), dateEnd=date(2013, 2, 1), color="#6390df", phases=set())
            res = SiteDAO().insert(d, siteIns)
            siteRes = SiteDAO().getById(d, False, [], res)
            siteIns.num = siteRes.num
            siteIns.position.num = siteRes.position.num
            utils().equal(self, siteIns, siteRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
               
    def test_delete(self):
        d = Connexion().connect()
        try:
            pos = Position(num=-1, long=001, lat=002, address="test")
            siteIns = Site(num=-1, numSite="52005", name="champie", siteMaster="test", siteManager="test2", position=pos, dateInit=date(2013, 1, 1), dateEnd=date(2013, 2, 1), color="#6390df", phases=set())
            res = SiteDAO().insert(d, siteIns)
            SiteDAO().deleteById(d, res)
            siteRes =self.assertRaises(AttributeError, SiteDAO().getById, d, False, [], res)
            print(siteRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
             
    def test_update(self):
        d = Connexion().connect()
        try:
            pos = Position(num=-1, long=001, lat=002, address="test")
            siteIns = Site(num=-1, numSite="FR52005", name="champie", siteMaster="test", siteManager="test2", position=pos, dateInit=date(2013, 1, 1), dateEnd=date(2013, 2, 1), color="#6390df", phases=set())
            res = SiteDAO().insert(d, siteIns)
            siteRes = SiteDAO().getById(d, False, [], res)
            siteRes.name = "tutu"
            SiteDAO().update(d, siteRes)
            siteRes2 = SiteDAO().getById(d, False, [], res)
            utils().equal(self, siteRes, siteRes2)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
 
     
