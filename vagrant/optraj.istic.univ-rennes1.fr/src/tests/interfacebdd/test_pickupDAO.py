'''
Created on 24 mars 2014

@author: guillaume
'''

import os,sys
from unittest import TestCase
from tests.utils.utils import utils
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")
from interfacebdd.PickupDAO import PickupDAO
from system.Pickup import Pickup
from system.Position import Position
from interfacebdd.Connexion import Connexion
from interfacebdd.SiteDAO import SiteDAO



class test_pickupDAO(TestCase):
    """Test the stand-alone module functions."""
    
    def test_insert(self):
        d = Connexion().connect()
        try:
            pos = Position(num=-1, long=001, lat=002, address="test")
            idSite = SiteDAO().getAll(d, False, []).pop().num
            puIns = Pickup(num=-1, position=pos, idSite=idSite)
            res = PickupDAO().insert(d, puIns)
            puRes = PickupDAO().getById(d, False, [], res)
            puIns.num = puRes.num
            puIns.position.num = puRes.position.num
            utils().equal(self, puIns, puRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)

    def test_get(self):
        d = Connexion().connect()
        try:
            pos = Position(num=-1, long=001, lat=002, address="test")
            idSite = SiteDAO().getAll(d, False, []).pop().num
            puIns = Pickup(num=-1, position=pos, idSite=idSite)
            res = PickupDAO().insert(d, puIns)
            puRes = PickupDAO().getById(d, False, [], res)
            puIns.num = puRes.num
            puIns.position.num = puRes.position.num
            utils().equal(self, puIns, puRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
           
    def test_delete(self):
        d = Connexion().connect()
        try:
            pos = Position(num=-1, long=001, lat=002, address="test")
            idSite = SiteDAO().getAll(d, False, []).pop().num
            puIns = Pickup(num=-1, position=pos, idSite=idSite)
            res = PickupDAO().insert(d, puIns)
            PickupDAO().deleteById(d,res)
            posRes =self.assertRaises(AttributeError, PickupDAO().getById, d, False, [], res)
            print posRes
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_update(self):
        d = Connexion().connect()
        try:
            pos = Position(num=-1, long=001, lat=002, address="test")
            idSite = SiteDAO().getAll(d, False, []).pop().num
            puIns = Pickup(num=-1, position=pos, idSite=idSite)
            res = PickupDAO().insert(d, puIns)
            puRes = PickupDAO().getById(d, False, [], res)
            puRes.position.address = "toto"
            PickupDAO().update(d, puRes)
            puRes2 = PickupDAO().getById(d, False, [], res)
            utils().equal(self, puRes, puRes2)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)