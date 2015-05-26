#!/usr/bin/env python
"""Unit tests pour la classe craftDAO"""

import os,sys
from unittest import TestCase
from tests.utils.utils import utils
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")
from interfacebdd.CraftDAO import CraftDAO
from system.Craft import Craft
from interfacebdd.Connexion import Connexion




class test_craftDAO(TestCase):
    """Test the stand-alone module functions."""
    
    def test_insert(self):
        d = Connexion().connect()
        try:
            cra = CraftDAO()
            craftIns = Craft(num=-1, name="test")
            res = cra.insert(d, craftIns)
            craftRes = cra.getById(d, False, [], res)
            craftIns.num = res
            utils().equal(self, craftIns, craftRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
    
    def test_get(self):
        d = Connexion().connect()
        try:
            cra = CraftDAO()
            craftIns = Craft(num=-1, name="test")
            res = cra.insert(d, craftIns)
            craftRes = cra.getById(d, False, [], res)
            craftIns.num = res
            utils().equal(self, craftIns, craftRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
           
    def test_delete(self):
        d = Connexion().connect()
        try:
            cra = CraftDAO()
            craftIns = Craft(num=-1, name="test")
            res = cra.insert(d, craftIns)
            cra.deleteById(d,res)
            craftRes =self.assertRaises(AttributeError, cra.getById, d, False, [], res)
            print craftRes
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_update(self):
        d = Connexion().connect()
        try:
            cra = CraftDAO()
            craftIns = Craft(num=-1, name="test")
            res = cra.insert(d, craftIns)
            craftRes = cra.getById(d, False, [], res)
            craftRes.name = "toto"
            cra.update(d, craftRes)
            craftRes2 = cra.getById(d, False, [], res)
            utils().equal(self, craftRes, craftRes2)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)