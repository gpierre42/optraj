#!/usr/bin/env python
"""Unit tests pour la classe positionDAO"""

import os,sys
from unittest import TestCase
from tests.utils.utils import utils
s = sys.path.append(utils().buildPath(os.getcwd())+"/vagrant/optraj.istic.univ-rennes1.fr/src/")
from interfacebdd.PositionDAO import PositionDAO
from system.Position import Position
from interfacebdd.Connexion import Connexion



class test_positionDAO(TestCase):
    """Test the stand-alone module functions."""

    
    def test_insert(self):
        d = Connexion().connect()
        try:
            posIns = Position(num=-1, long=001, lat=002, address="test")
            res = PositionDAO().insert(d, posIns)
            posRes = PositionDAO().getById(d, False, [], res)
            posIns.num = res
            utils().equal(self, posIns, posRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_get(self):
        d = Connexion().connect()
        try:
            posIns = Position(num=-1, long=001, lat=002, address="test")
            res = PositionDAO().insert(d, posIns)
            posRes = PositionDAO().getById(d, False, [], res)
            posIns.num = res
            utils().equal(self, posIns, posRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
           
    def test_delete(self):
        d = Connexion().connect()
        try:
            posIns = Position(num=-1, long=001, lat=002, address="test")
            res = PositionDAO().insert(d, posIns)
            PositionDAO().deleteById(d, res)
            posRes =self.assertRaises(AttributeError, PositionDAO().getById, d, False, [], res)
            print(posRes)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
            
    def test_update(self):
        d = Connexion().connect()
        try:
            posIns = Position(num=-1, long=001, lat=002, address="test")
            res = PositionDAO().insert(d, posIns)
            posRes = PositionDAO().getById(d, False, [], res)
            posRes.longitude = 003
            PositionDAO().update(d, posRes)
            posRes2 = PositionDAO().getById(d, False, [], res)
            utils().equal(self, posRes, posRes2)
        except:
            Connexion().exception()
        finally:
            Connexion().disconnect(d)
