# -*- coding:utf-8 -*-

'''
Created on 24 mars 2014

@author: guillaume
'''

import os,sys
from unittest import TestCase
from tests.utils.utils import utils
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")
from interfacebdd.ShuttleDAO import ShuttleDAO
from interfacebdd.CarDAO import CarDAO
from system.Car import Car
from interfacebdd.Connexion import Connexion



class test_carDAO(TestCase):
    """Test the stand-alone module functions."""

    def test_getUsedCar(self):
        d = Connexion().connect()
        try:
            res = True
            usedCars = CarDAO().getUsedCar(d, False, [])
            for c in usedCars:
                idShuttle = ShuttleDAO().getByFilter(d, False, [], ("car", str(c.num)))
                if idShuttle == None:
                    res = False
            self.assertTrue(res)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_getUnusedCar(self):
        d = Connexion().connect()
        try:
            res = True
            unusedCars = CarDAO().getUnUsedCar(d, False, [])
            for c in unusedCars:
                idShuttle = ShuttleDAO().getByFilter(d, False, [], ("car", str(c.num)))
                if idShuttle != None:
                    print idShuttle
                    res = False
            self.assertTrue(res)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
    
    def test_insert(self):
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