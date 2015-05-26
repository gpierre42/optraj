#coding=utf8

import unittest
from optimisation.pythondeap import ComputationLauncher
from interfacebdd.AssignmentDAO import AssignmentDAO
from interfacebdd.Connexion import Connexion
from system.System import System
from interfacebdd.SiteDAO import SiteDAO
from interfacebdd.PhaseDAO import PhaseDAO
from interfacebdd.WorkerDAO import WorkerDAO
from operator import xor
from datetime import date

class TestDeap(unittest.TestCase):

    def test_mustInSolution(self):
        '''
        Test si toutes les affectations déja présente en base sont bien dans la solution finale
        '''
        launcher = ComputationLauncher()
        launcher.init()
        launcher.algoInst.ngen = 1
        launcher.start()
        launcher.join()   
        solution = launcher.assignments
        conn = Connexion().connect()
        assignmentsBdd = AssignmentDAO().getAll(conn, False, [])
        today = date.today()
        res = True
        for a in assignmentsBdd:
            p = a.phase
            # on ne prend que les phases corespondant aux 17 semaines du tableau d'opti
            if p.numWeek >= today.isocalendar()[1] and p.numYear >= today.year:
                numWorker = a.worker.num
                numPhase = a.phase.num
                for a2 in solution:
                    if a2.worker.num == numWorker and a2.phase.num == numPhase:
                        res = res & True
        self.assertTrue(res)

    def test_allWorkersInSolution(self):
        '''
        Test de la non disparition ou ajout d'un worker pendant l'algo
        '''
        launcher = ComputationLauncher()
        launcher.init()
        launcher.algoInst.ngen = 1
        launcher.start()
        launcher.join()   
        conn = Connexion().connect()
        system = System(SiteDAO().getAll(conn, False, []), WorkerDAO().getAll(conn, False, []), PhaseDAO().getAll(conn, False, []))
        res = True
        for w in system.workers:
            for h in launcher.hallOfFame:
                for year in h.keys():
                    for week in h[year].keys():
                        boolAssign = False
                        boolAvailable = False
                        boolUnavailable = False
                        if year in launcher.algoInst.unavailabilities.keys():
                            if week in launcher.algoInst.unavailabilities[year].keys():
                                for x in launcher.algoInst.unavailabilities[year][week]:
                                    if x == w.num:
                                        boolUnavailable = True
                        for site in h[year][week]["assigns"].keys():
                            for temp in h[year][week]["assigns"][site]:
                                if temp == w.num:
                                    boolAssign = True
                        for temp2 in h[year][week]["availablesWorkers"][w.craft.num][w.qualification.num]:
                            if temp2 == w.num:
                                boolAvailable = True
                        if not ((boolAssign & (not boolAvailable) & (not boolUnavailable)) |
                                ((not boolAssign) & (boolAvailable) & (not boolUnavailable)) |
                                ((not boolAssign) & (not boolAvailable) & (boolUnavailable))):
                            print boolAssign, boolAvailable, boolUnavailable
                        res = res & ((boolAssign & (not boolAvailable) & (not boolUnavailable)) |
                                ((not boolAssign) & (boolAvailable) & (not boolUnavailable)) |
                                ((not boolAssign) & (not boolAvailable) & (boolUnavailable)))
        self.assertTrue(res)
        
#     def test_allWorkersInIndividual(self):
#         '''
#         Test de la non disparition ou ajout d'un worker pendant l'algo
#         '''
#         from deap import creator
#         from deap import base
#         creator.create("Fitness", base.Fitness, weights=(-1,))
#         creator.create("Individual", dict, fitness=creator.Fitness)
#         launcher = ComputationLauncher()
#         launcher.init()
#         ind = launcher.algoInst.createInd(creator.Individual)
#         conn = Connexion().connect()
#         system = System(SiteDAO().getAll(conn, False, []), WorkerDAO().getAll(conn, False, []), PhaseDAO().getAll(conn, False, []))
#         res = True
#         for w in system.workers:
#             h = ind
#             for year in h.keys():
#                 for week in h[year].keys():
#                     boolAssign = False
#                     boolAvailable = False
#                     boolUnavailable = False
#                     for x in launcher.algoInst.unavailabilities[year][week]:
#                         if x == w.num:
#                             boolUnavailable = True
#                     for site in h[year][week]["assigns"].keys():
#                         for temp in h[year][week]["assigns"][site]:
#                             if temp == w.num:
#                                 boolAssign = True
#                     for temp2 in h[year][week]["availablesWorkers"][w.craft.num][w.qualification.num]:
#                         if temp2 == w.num:
#                             boolAvailable = True
#                     res = res & ((boolAssign & (not boolAvailable) & (not boolUnavailable)) |
#                                 ((not boolAssign) & (boolAvailable) & (not boolUnavailable)) |
#                                 ((not boolAssign) & (not boolAvailable) & (boolUnavailable)))
#         self.assertTrue(res)
    
    def test_needAllSatisfy(self):
        '''
        si les besoins sont tous remplis quand cela est possible, execption sinon
        '''
        launcher = ComputationLauncher()
        launcher.init()
        launcher.algoInst.ngen = 1
        launcher.start()
        launcher.join()   
        conn = Connexion().connect()
        today = date.today()
        pDAO = PhaseDAO().getAllByFilterExtended(conn, False, [],
                                                 ('numYear', '=', str(today.year)),
                                                 ('numWeek', '>=', str(today.isocalendar()[1])))
        pDAO = pDAO | PhaseDAO().getAllByFilterExtended(conn, False, [],
                                                 ('numYear', '>', str(today.year)))
        system = System(SiteDAO().getAll(conn, False, []), WorkerDAO().getAll(conn, False, []), pDAO)
        res = True
        for phase in system.phases:
            for need in phase.needs:
                for hof in launcher.hallOfFame:
                    nbWorkerofCraftQualif = 0
                    for w in hof[phase.numYear][phase.numWeek]["assigns"][phase.numSite]:
                        worker = system.getWorkerById(w)
                        if (worker.craft.num == need.craft.num) & (worker.qualification.num == need.qualification.num):
                            nbWorkerofCraftQualif += 1
                    needRespect = (nbWorkerofCraftQualif == need.need)
                    exception = False
                    for n in launcher.issue["disponibility"]:
                        if need.num == n:
                            exception = True
                    res = res & xor(needRespect, exception)
        self.assertTrue(res)
        
        
        