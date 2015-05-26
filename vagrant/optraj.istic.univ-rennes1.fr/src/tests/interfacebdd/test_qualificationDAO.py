#!/usr/bin/env python
"""Unit tests pour la classe QualificationDAO"""

import os,sys
from unittest import TestCase
from tests.utils.utils import utils
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")
from interfacebdd.QualificationDAO import QualificationDAO
from system.Qualification import Qualification
from interfacebdd.Connexion import Connexion



class test_qualificationDAO(TestCase):
    """Test the stand-alone module functions."""
    
    def test_insert(self):
        d = Connexion().connect()
        try:
            QualificationIns = Qualification(num=-1, name="test")
            res = QualificationDAO().insert(d, QualificationIns)
            QualificationRes = QualificationDAO().getById(d, False, [], res)
            QualificationIns.num = res
            utils().equal(self, QualificationIns, QualificationRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)

    def test_get(self):
        d = Connexion().connect()
        try:
            QualificationIns = Qualification(num=-1, name="test")
            res = QualificationDAO().insert(d, QualificationIns)
            QualificationRes = QualificationDAO().getById(d, False, [], res)
            QualificationIns.num = QualificationRes.num
            utils().equal(self, QualificationIns, QualificationRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
           
    def test_delete(self):
        d = Connexion().connect()
        try:
            QualificationIns = Qualification(num=-1, name="test")
            res = QualificationDAO().insert(d, QualificationIns)
            QualificationDAO().deleteById(d,res)
            posRes =self.assertRaises(AttributeError, QualificationDAO().getById, d, False, [], res)
            print posRes
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_update(self):
        d = Connexion().connect()
        try:
            QualificationIns = Qualification(num=-1, name="test")
            res = QualificationDAO().insert(d, QualificationIns)
            qualifRes = QualificationDAO().getById(d, False, [], res)
            qualifRes.name = "toto"
            QualificationDAO().update(d, qualifRes)
            qualifRes2 = QualificationDAO().getById(d, False, [], res)
            utils().equal(self, qualifRes, qualifRes2)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)