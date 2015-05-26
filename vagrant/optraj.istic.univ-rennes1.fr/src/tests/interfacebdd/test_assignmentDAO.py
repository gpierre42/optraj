# -*- coding:utf-8 -*-

'''
Created on 24 mars 2014

@author: Jérémy
'''

import os,sys
from unittest import TestCase
from tests.utils.utils import utils
from datetime import date
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")
from interfacebdd.AssignmentDAO import AssignmentDAO
from interfacebdd.WorkerDAO import WorkerDAO
from interfacebdd.PhaseDAO import PhaseDAO
from interfacebdd.SiteDAO import SiteDAO
from interfacebdd.CraftDAO import CraftDAO
from interfacebdd.QualificationDAO import QualificationDAO
from system.Worker import Worker
from system.Phase import Phase
from system.Position import Position
from system.Craft import Craft
from system.Site import Site
from system.Qualification import Qualification
from system.Assignment import Assignment
from interfacebdd.Connexion import Connexion



class test_assignmentDAO(TestCase):
    """Test the stand-alone module functions."""
    
    def test_insert(self):
        d = Connexion().connect()
        try:
            posIns = Position(num=-1, long=001, lat=002, address="test")
            craft = CraftDAO().getById(d, False, [], 1)
            qualif = QualificationDAO().getById(d, False, [], 1)
            worker = Worker(num=-1, name="Bomber", firstName="Jean", birthdate=date(2013, 1, 1), licence="A2", position=posIns, craft=craft, qualification=qualif)
            pos = Position(num=-1, long=001, lat=002, address="test")
            siteIns = Site(num=-1, numSite="FR52005", name="champie", siteMaster="test", siteManager="test2", position=pos, dateInit=date(2013, 1, 1), dateEnd=date(2013, 2, 1), color="#6390df", phases=set())
            res = SiteDAO().insert(d, siteIns)
            phase = Phase(num=-1, numSite=res, numWeek=1, numYear=2013, needs=set([]), nbWorkers=0, totalWorkers=0)
            phaseRes = PhaseDAO().insert(d, phase)
            phase = PhaseDAO().getById(d, False, [], phaseRes)
            resWorker = WorkerDAO().insert(d, worker)
            worker = WorkerDAO().getById(d, False, [], resWorker)
            assign = Assignment(num=-1, worker=worker, phase=phase)
            res = AssignmentDAO().insert(d, assign)
            assignRes = AssignmentDAO().getById(d, False, [], res)
            assign.num = res
            utils().equal(self, assign, assignRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)