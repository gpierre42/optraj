# coding=utf8
'''
Created on 10 fév 2013

@author: Vivien Lelouette
'''

import ConfigParser
import time
import pymysql
import os
# from interfacebdd.WorkerDAO import WorkerDAO
# from interfacebdd.SiteDAO import SiteDAO


class  Connexion(object):
    '''
    Classe représentant une connexion avec une BDD physique    
    '''
    _instance = None  # Attribut statique de classe

    def __new__(cls):  # __new__ classmethod implicite: la classe 1e paramètre
        '''
        fonction appellée automatiquement à chaque instanciation d'une connection
        
        Si une instance est déjà existante, on la retourne au lieu de créer un nouvel objet
        
        Returns:
            l'instance de connexion active
        '''
        "méthode de construction standard en Python"
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def buildpath(self, path):
        '''
        Construit un chemin absolu vers ce fichier (Connexion.py)
        
        Returns:
            le chemin (str)
        '''
        p = os.path.split(path)
        if str(p[0]) == "/":
            return ""
        else:
            if str(p[1]) != 'vagrant':
                return self.buildpath(p[0])
            else:
                return "" + p[0]

    def connect(self):
        '''
        Construit et initialise un objet pour accéder à la bdd
        
        lis le fichier de configuration connexion.ini pour récupérer les paramètres de connexion
        
        Returns:
            un doublet (pymysql.connect, pymysql.cursor)
        '''
        conn = "local"
        # conn = "online"

        config = ConfigParser.RawConfigParser()
        a = self.buildpath(os.getcwd()) + os.path.normcase("/vagrant/optraj.istic.univ-rennes1.fr/src/interfacebdd/connexion.ini")
        #a = "/vagrant/optraj.istic.univ-rennes1.fr/src/interfacebdd/connexion.ini"
        cf = open(a)

        config.readfp(cf)

        h = config.get(conn, "host")
        p = int(config.get(conn, "port"))
        u = config.get(conn, "user")
        pa = config.get(conn, "passwd")
        d = config.get(conn, "db")

        db = pymysql.connect(host=h, port=p, user=u, passwd=pa, db=d, charset='utf8')

        cf.close()

        # declaration d'un objet curseur -> sert Ã  executer des requetes sql sur la base
        cur = db.cursor(pymysql.cursors.DictCursor)

        return (db, cur)

    def disconnect(self, co=None):
        """
        ferme les connexions
        
        ferme les connexions et cursors
        """
        co[1].close()
        co[0].close()

    def exception(self):
        #print(pymysql.Error)
        raise

