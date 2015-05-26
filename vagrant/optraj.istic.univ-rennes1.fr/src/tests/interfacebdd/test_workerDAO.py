'''
Created on 19 mars 2014

@author: guillaume
'''
#!/usr/bin/env python
"""Unit tests pour la classe workerDAO"""

import os,sys
from unittest import TestCase
from tests.utils.utils import utils
from datetime import date
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")
from interfacebdd.WorkerDAO import WorkerDAO
from system.Worker import Worker
from system.Position import Position
from interfacebdd.Connexion import Connexion
from interfacebdd.CraftDAO import CraftDAO
from interfacebdd.QualificationDAO import QualificationDAO


class test_workerDAO(TestCase):
    """Test the stand-alone module functions."""

 
    def test_insert(self):
        d = Connexion().connect()
        try:
            posIns = Position(num=-1, long=001, lat=002, address="test")
            craft = CraftDAO().getById(d, False, [], 1)
            qualif = QualificationDAO().getById(d, False, [], 1)
            workerIns = Worker(num=-1, name="toto", firstName="titi", birthdate=date(2013, 1, 1),licence="B1",position =posIns,  craft=craft, qualification=qualif)
            res = WorkerDAO().insert(d, workerIns)
            workerRes = WorkerDAO().getById(d, False, [], res)
            workerIns.num=res
            workerIns.position.num = workerRes.position.num
            utils().equal(self, workerIns, workerRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
             
    def test_get(self):
        d = Connexion().connect()
        try:
            posIns = Position(num=-1, long=001, lat=002, address="test")
            craft = CraftDAO().getById(d, False, [], 1)
            qualif = QualificationDAO().getById(d, False, [], 1)
            workerIns = Worker(num=-1, name="toto", firstName="titi", birthdate=date(2013, 1, 1),licence="B1",position =posIns,  craft=craft, qualification=qualif)
            res = WorkerDAO().insert(d, workerIns)
            workerRes = WorkerDAO().getById(d, False, [], res)
            
            workerIns.num = res
            workerIns.position.num = workerRes.position.num 
            utils().equal(self, workerIns, workerRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_delete(self):
        d = Connexion().connect()
        try:
            posIns = Position(num=-1, long=001, lat=002, address="test")
            craft = CraftDAO().getById(d, False, [], 1)
            qualif = QualificationDAO().getById(d, False, [], 1)
            workerIns = Worker(num=-1, name="toto", firstName="titi", birthdate=date(2013, 1, 1),licence="B1",position =posIns,  craft=craft, qualification=qualif)
            res = WorkerDAO().insert(d, workerIns)
            WorkerDAO().deleteById(d, res)
            workerRes =self.assertRaises(AttributeError, WorkerDAO().getById, d, False, [], res)
            print(workerRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_update(self):
        d = Connexion().connect()
        try:
            posIns = Position(num=-1, long=001, lat=002, address="test")
            craft = CraftDAO().getById(d, False, [], 1)
            qualif = QualificationDAO().getById(d, False, [], 1)
            workerIns = Worker(num=-1, name="toto", firstName="titi", birthdate=date(2013, 1, 1),licence="B1",position =posIns,  craft=craft, qualification=qualif)
            res = WorkerDAO().insert(d, workerIns)
            workerRes = WorkerDAO().getById(d, False, [], res)
            workerRes.name = "tutu"
            WorkerDAO().update(d, workerRes)
            workerRes2 = WorkerDAO().getById(d, False, [], res)
            utils().equal(self, workerRes, workerRes2)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
