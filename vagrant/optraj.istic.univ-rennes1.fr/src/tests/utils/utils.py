'''
Created on 19 mars 2014

@author: guillaume
'''
import os
from unittest import TestCase
import operator
from collections import Iterable

class utils():

        def buildPath(self, path):
            '''
            construit un chemin absolu
            '''
            p = os.path.split(path)
            if str(p[0]) == "/":
                return ""
            else:
                if str(p[1]) != 'vagrant':
                    return self.buildPath(p[0])
                else:
                    return "" + p[0]
                
        def equal(self, testModule, obj1, obj2):
            for attr in obj1.__dict__:
                t = attr.split('_')
                a = obj1
                b = obj2
                for attr in t:
                    if attr != '':
                        a = operator.attrgetter(attr)(a)
                        b = operator.attrgetter(attr)(b)
                if(not self.hasDict(a)):
                    if(self.isIter(a)):
                        for i in a:
                            self.setEqual(testModule, i, b)
                        for i in b:
                            self.setEqual(testModule, i, b)
                    else:
                        testModule.assertEqual(a, b)
                else:
                    self.equal(testModule, a, b)
               
        def hasDict(self, Obj):
            try:
                Obj.__dict__
                return True
            except AttributeError:
                return False
            
        def isIter(self, Obj):
            try:
#                 (x for x in Obj)
                Obj.difference(Obj)
                return True
            except AttributeError:
                return False
        
        def equalBool(self, testModule, elem1, elem2):
            try:
                self.equal(testModule, elem1, elem2)
                return True
            except AssertionError:
                return False
        
        def iterEqual(self, testModule, itera, elem):
            for j in itera:
                if self.equalBool(testModule, elem, j):
                    return j
                
        def setEqual(self, testModule, e, o2):
            for j in o2:
                if utils().equalBool(testModule, e, j):
                    return True
            raise(AssertionError)
            
                                        
            
                