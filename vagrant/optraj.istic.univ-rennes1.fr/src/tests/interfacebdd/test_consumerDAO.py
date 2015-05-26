#!/usr/bin/env python
"""Unit tests pour la classe consumerDAO"""

import os,sys
from unittest import TestCase
from interfacebdd.Connexion import Connexion
from interfacebdd.ConsumerDAO import ConsumerDAO
from system.Consumer import Consumer
from tests.utils.utils import utils
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")

class test_consumerDAO(TestCase):
    """Test the stand-alone module functions."""
    
    def test_insert(self):
        d = Connexion().connect()
        try:
            cons = ConsumerDAO()
            consIns = Consumer(num=-1, login="testCons")
            res = cons.insert(d, consIns)
            consRes = cons.getById(d, False, [], res)
            consIns.num = res
            utils().equal(self, consIns, consRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_get(self):
        d = Connexion().connect()
        try:
            cons = ConsumerDAO()
            consIns = Consumer(num=-1, login="testCons2")
            res = cons.insert(d, consIns)
            consRes = cons.getById(d, False, [], res)
            consIns.num = res
            utils().equal(self, consIns, consRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_delete(self):
        d = Connexion().connect()
        try:
            cons = ConsumerDAO()
            consIns = Consumer(num=-1, login="testCons3")
            res = cons.insert(d, consIns)
            cons.deleteById(d,res)
            consRes = self.assertRaises(AttributeError, cons.getById, d, False, [], res)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_update(self):
        d = Connexion().connect()
        try:
            cons = ConsumerDAO()
            consIns = Consumer(num=-1, login="testCons4")
            res = cons.insert(d, consIns)
            consRes = cons.getById(d, False, [], res)
            consRes.name = "toto"
            cons.update(d, consRes)
            consRes2 = cons.getById(d, False, [], res)
            utils().equal(self, consRes, consRes2)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
