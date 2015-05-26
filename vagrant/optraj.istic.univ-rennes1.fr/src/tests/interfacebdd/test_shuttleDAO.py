'''
Created on 24 mars 2014

@author: guillaume
'''

import os,sys
from unittest import TestCase
from tests.utils.utils import utils
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")
from system.Shuttle import Shuttle
from system.Car import Car
from system.Worker import Worker
from system.Phase import Phase
from system.Position import Position
from system.Site import Site
from interfacebdd.SiteDAO import SiteDAO
from interfacebdd.CraftDAO import CraftDAO
from interfacebdd.QualificationDAO import QualificationDAO
from interfacebdd.ShuttleDAO import ShuttleDAO
from interfacebdd.Connexion import Connexion
from interfacebdd.CarDAO import CarDAO
from interfacebdd.WorkerDAO import WorkerDAO
from interfacebdd.PhaseDAO import PhaseDAO
from datetime import date




class test_shuttleDAO(TestCase):
    """Test the stand-alone module functions."""

     
    def test_insert(self):
        d = Connexion().connect()
        try:
            posIns = Position(num=-1, long=001, lat=002, address="test")
            craft = CraftDAO().getById(d, False, [], 1)
            qualif = QualificationDAO().getById(d, False, [], 1)
            driv = Worker(num=-1, name="toto", firstName="titi", birthdate=date(2013, 1, 1),licence="B1",position =posIns,  craft=craft, qualification=qualif)
            num = WorkerDAO().insert(d, driv)
            driv = WorkerDAO().getById(d, False, [], num)
             
            car = Car(num=-1, model="test1", nbPlace=4)
            num = CarDAO().insert(d, car)
            car = CarDAO().getById(d, False, [], num)
            
            pos = Position(num=-1, long=001, lat=002, address="test")
            siteIns = Site(num=-1, numSite="FR52005", name="champie", siteMaster="test", siteManager="test2", position=pos, dateInit=date(2013, 1, 1), dateEnd=date(2013, 2, 1), color="#6390df", phases=set())
            resSite = SiteDAO().insert(d, siteIns)
            ph = Phase(num=-1, numSite=resSite, numWeek=1, numYear=2014, needs = [], nbWorkers=1, totalWorkers=1)
            num = PhaseDAO().insert(d, ph)
            ph = PhaseDAO().getById(d, False, [], num)
            
            
            s = Shuttle(num=-1, driver=driv, car=car,phase=ph, pickups=set([]), passengers=set([]))
            res = ShuttleDAO().insert(d, s)
            shuRes = ShuttleDAO().getById(d, False, [], res)
            print shuRes
            s.num = res
            print s
            utils().equal(self, s, shuRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
               
    def test_get(self):
        d = Connexion().connect()
        try:
            carIns = Car(num=-1, plate="test", model="test1", nbPlace=4)
            res = CarDAO().insert(d, carIns)
            carRes = CarDAO().getById(d, False, [], res)
            carIns.num = res
            utils().equal(self, carIns, carRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
             
    def test_delete(self):
        d = Connexion().connect()
        try:
            carIns = Car(num=-1, plate="test", model="test1", nbPlace=4)
            res = CarDAO().insert(d, carIns)
            CarDAO().deleteById(d, res)
            carRes =self.assertRaises(AttributeError, CarDAO().getById, d, False, [], res)
            print(carRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
               
    def test_update(self):
        d = Connexion().connect()
        try:
            carIns = Car(num=-1, plate="test", model="test1", nbPlace=4)
            res = CarDAO().insert(d, carIns)
            carRes = CarDAO().getById(d, False, [], res)
            carRes.nbPlace = 8
            CarDAO().update(d, carRes)
            carRes2 = CarDAO().getById(d, False, [], res)
            utils().equal(self, carRes, carRes2)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
