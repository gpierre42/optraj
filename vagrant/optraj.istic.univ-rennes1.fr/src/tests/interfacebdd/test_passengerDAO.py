'''
Created on 25 mars 2014

@author: guillaume
'''
from system.Worker import Worker
from interfacebdd.QualificationDAO import QualificationDAO
from interfacebdd.CraftDAO import CraftDAO
from system.Position import Position
from system.Shuttle import Shuttle
from system.Car import Car
from system.Pickup import Pickup
from system.PickupLink import PickupLink
from system.Phase import Phase
from system.Site import Site
from interfacebdd.SiteDAO import SiteDAO
from interfacebdd.PhaseDAO import PhaseDAO
from interfacebdd.PickupLinkDAO import PickupLinkDAO
from interfacebdd.PickupDAO import PickupDAO
from interfacebdd.PositionDAO import PositionDAO
from interfacebdd.CarDAO import CarDAO

#!/usr/bin/env python
"""Unit tests pour la classe craftDAO"""

import os,sys
from unittest import TestCase
from tests.utils.utils import utils
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")
from interfacebdd.WorkerDAO import WorkerDAO
from interfacebdd.ShuttleDAO import ShuttleDAO
from interfacebdd.PassengerDAO import PassengerDAO
from system.Passenger import Passenger
from datetime import date
from interfacebdd.Connexion import Connexion




class test_passengerDAO(TestCase):
    """Test the stand-alone module functions."""
    
#     def test_insert(self):
#         d = Connexion().connect()
#         try:
#             posIns = Position(num=-1, long=001, lat=002, address="test")
#             craft = CraftDAO().getById(d, False, [], 1)
#             qualif = QualificationDAO().getById(d, False, [], 1)
#             passe = Worker(num=-1, name="toto", firstName="titi", birthdate=date(2013, 1, 1),licence="B1",position =posIns,  craft=craft, qualification=qualif)
#             num = WorkerDAO().insert(d, passe)
#             passe = WorkerDAO().getById(d, False, [], num)
#             
#             posIns = Position(num=-1, long=001, lat=002, address="test")
#             craft = CraftDAO().getById(d, False, [], 1)
#             qualif = QualificationDAO().getById(d, False, [], 1)
#             driv = Worker(num=-1, name="toto", firstName="titi", birthdate=date(2013, 1, 1),licence="B1",position =posIns,  craft=craft, qualification=qualif)
#             num = WorkerDAO().insert(d, driv)
#             driv = WorkerDAO().getById(d, False, [], num)
#             
#             car = Car(num=-1, model="test1", nbPlace=4)
#             num = CarDAO().insert(d, car)
#             car = CarDAO().getById(d, False, [], num)
#             
#             pos = Position(num=-1, long=001, lat=002, address="test")
#             siteIns = Site(num=-1, numSite="FR52005", name="champie", siteMaster="test", siteManager="test2", position=pos, dateInit=date(2013, 1, 1), dateEnd=date(2013, 2, 1), color="#6390df", phases=set())
#             resSite = SiteDAO().insert(d, siteIns)
#             ph = Phase(num=-1, numSite=resSite, numWeek=1, numYear=2014, needs = [], nbWorkers=1, totalWorkers=1)
#             num = PhaseDAO().insert(d, ph)
#             ph = PhaseDAO().getById(d, False, [], num)
#             
#             pos = Position(num=-1, long=001, lat=002, address="test")
#             pu = Pickup(num=-1, position=pos)
#             pul = PickupLink(num=-1, pickup=pu, numShuttle=1)
#             
#             shut = Shuttle(num=-1, driver=driv, car=car, phase=ph, pickupLinks=set([pul]))
#             resShut = ShuttleDAO().insert(d, shut)
#             shut = ShuttleDAO().getById(d, False, [], resShut)
#             shut.num = -1
#             shut.driver.num = -1
#             shut.driver.position.num = -1
#             shut.car.num = -1
#             shut.phase.num = -1
#             p = shut.pickupLinks.pop()
#             p.num = -1
#             p.pickup.num = -1
#             p.pickup.position.num = -1
#             shut.pickupLinks.add(p)
#             
#             print shut.pickupLinks
#             print passe
#             print ph
#             print shut
#             print p
#             
#             passIns = Passenger(num=-1, shuttle=shut, worker=passe)
#             
#             res = PassengerDAO().insert(d, passIns)
#             passRes = PassengerDAO().getById(d, False, [], res)
#             
#             passIns.num = res
#             passIns.shuttle.num = passRes.shuttle.num
#             passIns.shuttle.driver.num = passRes.shuttle.driver.num
#             passIns.shuttle.driver.position.num = passRes.shuttle.driver.position.num
#             passIns.shuttle.car.num = passRes.shuttle.car.num
#             passIns.shuttle.phase.num = passRes.shuttle.phase.num
#             pIns = passIns.shuttle.pickupLinks.pop()
#             pRes = passRes.shuttle.pickupLinks.pop()
#             pIns.num = pRes.num
#             pIns.pickup.num = pRes.pickup.num
#             pIns.pickup.position.num = pRes.pickup.position.num
#             passIns.shuttle.pickupLinks.add(pIns)
#             passRes.shuttle.pickupLinks.add(pRes)
#             passIns.worker.num = passRes.worker.num
#             passIns.worker.position.num = passRes.worker.position.num
#             print passRes
#             print passIns
#             utils().equal(self, passIns, passRes)
#         except:
#             Connexion().exception()
#         finally:
#             Connexion().disconnect(d)
