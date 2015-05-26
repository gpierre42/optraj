'''
Created on 24 mars 2014

@author: guillaume
'''

import os,sys
from unittest import TestCase
from tests.utils.utils import utils
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")
from interfacebdd.PickupLinkDAO import PickupLinkDAO
from interfacebdd.PickupDAO import PickupDAO
from system.PickupLink import PickupLink
from system.Pickup import Pickup
from system.Shuttle import Shuttle
from system.Position import Position
from system.Phase import Phase
from interfacebdd.Connexion import Connexion
from interfacebdd.SiteDAO import SiteDAO
from interfacebdd.ShuttleDAO import ShuttleDAO
from interfacebdd.WorkerDAO import WorkerDAO
from interfacebdd.CarDAO import CarDAO
from interfacebdd.PhaseDAO import PhaseDAO



class test_pickupLinkDAO(TestCase):
    """Test the stand-alone module functions."""
    
    def test_insert(self):
        d = Connexion().connect()
        try:
            pos = Position(num=-1, long=001, lat=002, address="test")
            idSite = SiteDAO().getAll(d, False, []).pop().num
            puIns = Pickup(num=-1, position=pos, idSite=idSite)
            resPickup = PickupDAO().insert(d, puIns)
            puIns = PickupDAO().getById(d, False, [], resPickup)
            p = Phase(num=-1, numSite=SiteDAO().getAll(d, False, []).pop().num, \
                      numWeek=25, numYear=2014, needs=[], nbWorkers=0, totalWorkers=0)
            numPhase = PhaseDAO().insert(d, p)
            p = PhaseDAO().getById(d, False, [], numPhase)
            s = Shuttle(num=-1, driver=WorkerDAO().getAll(d, False, []).pop(),\
                        car=CarDAO().getAll(d, False, []).pop(), \
                        phase=p, \
                        pickups=[], passengers=[])
            numShuttle = ShuttleDAO().insert(d, s)
            pulIns = PickupLink(num=-1, pickup=puIns, numShuttle=numShuttle)
            res = PickupLinkDAO().insert(d, pulIns)
            pulRes = PickupLinkDAO().getById(d, False, [], res)
            pulIns.num = pulRes.num
            pulIns.pickup.num = pulRes.pickup.num
            pulIns.pickup.position.num = pulRes.pickup.position.num
            utils().equal(self, pulIns, pulRes)
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
            resPickup = PickupDAO().insert(d, puIns)
            puIns = PickupDAO().getById(d, False, [], resPickup)
            p = Phase(num=-1, numSite=SiteDAO().getAll(d, False, []).pop().num, \
                      numWeek=25, numYear=2014, needs=[], nbWorkers=0, totalWorkers=0)
            numPhase = PhaseDAO().insert(d, p)
            p = PhaseDAO().getById(d, False, [], numPhase)
            s = Shuttle(num=-1, driver=WorkerDAO().getAll(d, False, []).pop(),\
                        car=CarDAO().getAll(d, False, []).pop(), \
                        phase=p, \
                        pickups=[], passengers=[])
            numShuttle = ShuttleDAO().insert(d, s)
            pulIns = PickupLink(num=-1, pickup=puIns, numShuttle=numShuttle)
            res = PickupLinkDAO().insert(d, pulIns)
            pulRes = PickupLinkDAO().getById(d, False, [], res)
            pulIns.num = pulRes.num
            pulIns.pickup.num = pulRes.pickup.num
            pulIns.pickup.position.num = pulRes.pickup.position.num
            utils().equal(self, pulIns, pulRes)
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
            resPickup = PickupDAO().insert(d, puIns)
            puIns = PickupDAO().getById(d, False, [], resPickup)
            p = Phase(num=-1, numSite=SiteDAO().getAll(d, False, []).pop().num, \
                      numWeek=25, numYear=2014, needs=[], nbWorkers=0, totalWorkers=0)
            numPhase = PhaseDAO().insert(d, p)
            p = PhaseDAO().getById(d, False, [], numPhase)
            s = Shuttle(num=-1, driver=WorkerDAO().getAll(d, False, []).pop(),\
                        car=CarDAO().getAll(d, False, []).pop(), \
                        phase=p, \
                        pickups=[], passengers=[])
            numShuttle = ShuttleDAO().insert(d, s)
            pulIns = PickupLink(num=-1, pickup=puIns, numShuttle=numShuttle)
            res = PickupLinkDAO().insert(d, pulIns)
            PickupLinkDAO().deleteById(d,res)
            posRes =self.assertRaises(AttributeError, PickupLinkDAO().getById, d, False, [], res)
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
            print idSite
            puIns = Pickup(num=-1, position=pos, idSite=idSite)
            resPickup = PickupDAO().insert(d, puIns)
            puIns = PickupDAO().getById(d, False, [], resPickup)
            p = Phase(num=-1, numSite=SiteDAO().getAll(d, False, []).pop().num, \
                      numWeek=25, numYear=2014, needs=[], nbWorkers=0, totalWorkers=0)
            numPhase = PhaseDAO().insert(d, p)
            p = PhaseDAO().getById(d, False, [], numPhase)
            s = Shuttle(num=-1, driver=WorkerDAO().getAll(d, False, []).pop(),\
                        car=CarDAO().getAll(d, False, []).pop(), \
                        phase=p, \
                        pickups=[], passengers=[])
            numShuttle = ShuttleDAO().insert(d, s)
            pulIns = PickupLink(num=-1, pickup=puIns, numShuttle=numShuttle)
            res = PickupLinkDAO().insert(d, pulIns)
            pulRes = PickupLinkDAO().getById(d, False, [], res)
            pulRes.pickup.position.address = "toto"
            PickupLinkDAO().update(d, pulRes)
            pulRes2 = PickupLinkDAO().getById(d, False, [], res)
            utils().equal(self, pulRes, pulRes2)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)