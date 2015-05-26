'''
Created on 24 mars 2014

@author: guillaume
'''

import os,sys
from unittest import TestCase
from tests.utils.utils import utils
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")
from interfacebdd.NeedDAO import NeedDAO
from system.Need import Need
from system.Craft import Craft
from system.Qualification import Qualification
from system.Phase import Phase
from interfacebdd.Connexion import Connexion
from interfacebdd.PhaseDAO import PhaseDAO
from interfacebdd.SiteDAO import SiteDAO



class test_needDAO(TestCase):
    """Test the stand-alone module functions."""

    
    def test_insert(self):
        d = Connexion().connect()
        try:
            craft = Craft(num=-1, name="TestCraft")
            qualif = Qualification(num=-1, name="TestQualif")
            p = Phase(num=-1, numSite=SiteDAO().getAll(d, False, []).pop().num, \
                      numWeek=25, numYear=2014, needs=[], nbWorkers=0, totalWorkers=0)
            numPhase = PhaseDAO().insert(d, p)
            needIns = Need(num=-1, numPhase=numPhase, craft=craft, qualification=qualif, need=3)
            res = NeedDAO().insert(d, needIns)
            needRes = NeedDAO().getById(d, False, [], res)
            needIns.num = res
            needIns.craft.num = needRes.craft.num
            needIns.qualification.num = needRes.qualification.num
            utils().equal(self, needIns, needRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_get(self):
        d = Connexion().connect()
        try:
            craft = Craft(num=-1, name="TestCraft")
            qualif = Qualification(num=-1, name="TestQualif")
            p = Phase(num=-1, numSite=SiteDAO().getAll(d, False, []).pop().num, \
                      numWeek=25, numYear=2014, needs=[], nbWorkers=0, totalWorkers=0)
            numPhase = PhaseDAO().insert(d, p)
            needIns = Need(num=-1, numPhase=numPhase, craft=craft, qualification=qualif, need=3)
            res = NeedDAO().insert(d, needIns)
            needRes = NeedDAO().getById(d, False, [], res)
            needIns.num = res
            needIns.craft.num = needRes.craft.num
            needIns.qualification.num = needRes.qualification.num
            utils().equal(self, needIns, needRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_delete(self):
        d = Connexion().connect()
        try:
            craft = Craft(num=-1, name="TestCraft")
            qualif = Qualification(num=-1, name="TestQualif")
            p = Phase(num=-1, numSite=SiteDAO().getAll(d, False, []).pop().num, \
                      numWeek=25, numYear=2014, needs=[], nbWorkers=0, totalWorkers=0)
            numPhase = PhaseDAO().insert(d, p)
            needIns = Need(num=-1, numPhase=numPhase, craft=craft, qualification=qualif, need=3)
            res = NeedDAO().insert(d, needIns)
            NeedDAO().deleteById(d, res)
            needRes =self.assertRaises(AttributeError, NeedDAO().getById, d, False, [], res)
            print(needRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
              
    def test_update(self):
        d = Connexion().connect()
        try:
            craft = Craft(num=-1, name="TestCraft")
            qualif = Qualification(num=-1, name="TestQualif")
            p = Phase(num=-1, numSite=SiteDAO().getAll(d, False, []).pop().num, \
                      numWeek=25, numYear=2014, needs=[], nbWorkers=0, totalWorkers=0)
            numPhase = PhaseDAO().insert(d, p)
            needIns = Need(num=-1, numPhase=numPhase, craft=craft, qualification=qualif, need=3)
            res = NeedDAO().insert(d, needIns)
            needRes = NeedDAO().getById(d, False, [], res)
            needRes.need = 8
            NeedDAO().update(d, needRes)
            needRes2 = NeedDAO().getById(d, False, [], res)
            utils().equal(self, needRes, needRes2)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)