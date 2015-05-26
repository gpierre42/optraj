# -*- coding: utf-8 -*-

'''
Module d'importations des données depuis des fichiers csv fournis par la base de paie

 -  salaries.csv au format nom;prénom;date de naissance(jj/mm/aaaa);adresse;CP;ville;métier;qualif;
'''
from __future__ import unicode_literals
import sys
sys.path.append('/vagrant/optraj.istic.univ-rennes1.fr/src')
from importData.CheckFile import CheckFile
import time
import os
from pygeocoder import Geocoder
import pymysql
from interfacebdd.Connexion import Connexion
from interfacebdd.CraftDAO import CraftDAO
from interfacebdd.WorkerDAO import WorkerDAO
from interfacebdd.QualificationDAO import QualificationDAO
from interfacebdd.PositionDAO import PositionDAO
from system.Worker import Worker
from system.Craft import Craft
from system.Qualification import Qualification
from system.Position import Position
import codecs


class GenerateWorkers(object):
    '''
    Classe créant ou modifiant des ouvriers depuis d'un fichier csv.
    
    Elle vérifie au préalable si l'ouvrier existe ou non
    '''

    def existsInBDD(self, worker, conn):
        '''
        permet de verifier si un ouvrier existe en base de donnée
        
        Args:
            worker l'ouvrier à chercher (system.Worker.Worker)
            conn connexion à la base de donnée (interfacebdd.Connexion.Connexion)

        Returns:
            un boolean représentant l'existence de l'ouvrier
        '''

        workDAO = WorkerDAO()
        res = workDAO.getByFilter(conn, False, [], ('name', worker.name), ('firstName', worker.firstName), ('birthdate', worker.birthdate))
        return res

    def createInBDD(self, worker, conn):
        '''
        Permet de créer un ouvrier en base de donnée
        
        Args:
            worker l'ouvrier à chercher (system.Worker.Worker)
            conn connexion à la base de donnée (interfacebdd.Connexion.Connexion)
        '''
        workDAO = WorkerDAO()
        workDAO.insert(worker, conn)

    def updateInBDD(self, worker, conn):
        '''
        Met à jour un ouvrier en bdd
        
        Args:
            worker l'ouvrier à chercher (system.Worker.Worker)
            conn connexion à la base de donnée (interfacebdd.Connexion.Connexion)
        '''
        workDAO = WorkerDAO()
        workDAO.update(worker, conn)

    def searchAndReturnPosition(self, strPos):
        '''
        Permet de verifier via googleMap  une position
        
        Args:
            strPos l'addresse à résoudre (str)

        Returns:
            la position correspondante à l'adresse (system.Position.Position)
        '''
        arg = strPos.split(';')
        # On attend pour être sûr de pas surcharger GM
        time.sleep(0.25)
        # adresse, CP, Ville
        argument = arg[0] + ' ' + arg[2] + ' ' + arg[1]
        try:
                results = Geocoder.geocode(argument)
        except:
                argument = arg[1] + ' ' + arg[2]
                results = Geocoder.geocode(argument)
        pos = Position(lat=results[0].coordinates[0], long=results[0].coordinates[1], address=argument.encode('utf-8'))
        return pos

    def strToNumQualification(self, strQuali):
        '''
        renvoie l'identifiant d'une qualification depuis une chaine de caractères

        Args:
            strQualif le nom de la qualification (str)
        
        Returns:
            le num de la qualification
        '''
        qualif = 0
        if strQuali.count('ETAM') > 0:
            qualif = 1
        else:
            if strQuali.count('N4P2') > 0:
                qualif = 2
            else:
                if strQuali.count('N4P1') > 0:
                    qualif = 3
                else:
                    if strQuali.count('N3P2') > 0:
                        qualif = 4
                    else:
                        if strQuali.count('N3P1') > 0:
                            qualif = 5
                        else:
                            if strQuali.count('N2') > 0:
                                qualif = 6
                            else:
                                if strQuali.count('N1P2') > 0:
                                    qualif = 7
                                else:
                                    qualif = 8
        return qualif

    def manageDate(self, date):
        birthdate = date.split("/")
        # On test si on est au format jj/mm/aaa
        if len(birthdate) == 3:
            return birthdate[2]+"-"+birthdate[1]+"-"+birthdate[0]
        else:
            return date

    def manageCraft(self, strCraft, conn):
        '''
        Fonction qui va voir le fichier de règles pour retourner un metier
        
        Si aucune règle ne correspond on l'associe à "non référencé"
        Sinon on va en BDD et on renvoie l'id du métier correspondant
        
        Args:
            strCraft
            
        Returns:
            l'identifiant du metier
        '''
        res = None
        cf = CheckFile(pathField="/vagrant/DonneesBDD/reglesMetiers.txt")
        cf.fileExists()
        cf.isWellBuildRules()

        myFile = codecs.open(cf.pathField, 'r', 'utf-8')
        content = myFile.read()
        myFile.close()
        myLines = content.split('\n')
        i = 1
        for line in myLines:
            # print i
            part = line.split(':')
            if len(part) != 2:
                print part
                return i
            partG = part[0].split('"')
            partD = part[1].split('"')
            #on trouve un match dans les règles
            if strCraft.upper() in partG:
                myCraft = partD[1]
                craftDAO = CraftDAO()
                res = craftDAO.getByFilter(conn, False, [], ('name', myCraft))
                if res == None:
                    res = craftDAO.insert(conn, Craft(num=-1, name=myCraft))
                    res = craftDAO.getByFilter(conn, False, [], ('name', myCraft))
                break
            i = i + 1
        if res == None:
            myFile = codecs.open(cf.pathField, 'a', 'utf-8')
            myLine = '"' + strCraft.upper() + '" : "' + strCraft.capitalize() + '"'
            myFile.write('\n')
            myFile.write(myLine)
            myFile.close()
            strCraft = strCraft.capitalize()
            res = Craft(num=-1, name=strCraft)
            craftDAO = CraftDAO()
            res = craftDAO.insert(conn, res)
            res = craftDAO.getByFilter(conn, False, [], ('name', strCraft))
        return res

    def manageWorker(self, strWorker, conn):
        '''
        Fonction qui créé ou met à jour un ouvrier
        
        Args:
            strWorker le contenu de la ligne tirée du csv
        '''
        # print strWorker
        arg = strWorker.split(";")
        workerDAO = WorkerDAO()
        worker = Worker(name=arg[0].upper().encode('utf-8'), firstName=arg[1].encode('utf-8'), birthdate=self.manageDate(arg[2]).encode('utf-8'))
        myWorker = self.existsInBDD(worker, conn)
        qualif = QualificationDAO().getById(conn, False, [], self.strToNumQualification(arg[7]))
        pos = self.searchAndReturnPosition(arg[3] + ";" + arg[4] + ";" + arg[5])
        craft = self.manageCraft(arg[6], conn)
        if myWorker == None:
            print "INSERT " + strWorker.encode('ascii', 'ignore')
            # print worker
            # print self
            # print arg[7]
            worker.qualification = qualif
            worker.craft = craft
            # worker.craft.name = worker.craft.name.encode('utf-8')
            worker.position = pos
            worker.licence = ''
            workerDAO.insert(conn, worker)
            # myWorkerInBDD = workerDAO.getById(ident=myId, co=conn)
        else:
            print "UPDATE " + strWorker.encode('ascii', 'ignore')
            posDAO = PositionDAO()
            posDAO.insert(conn, pos)
            myWorker.position = posDAO.getById(conn, False, [], myWorker.position.num)
            myWorker.position.address = pos.address
            myWorker.position.latitude = pos.latitude
            myWorker.position.lontitude = pos.longitude
            # myWorker.position.address = myWorker.position.address.encode('utf-8')
            myWorker.craft = craft
            myWorker.qualification = qualif
            myWorker.firstName = myWorker.firstName.encode('utf-8')
            myWorker.name = myWorker.name.encode('utf-8')
            myWorker.birthdate = myWorker.birthdate
            myWorker.license = ''.encode('utf-8')
            workerDAO.update(conn, myWorker)

if __name__ == '__main__':
    '''
    main de la classe
    Fonctionnement de l'algo de lecture de fichiers :
    
    ->Vérifier existence des fichiers
        Si
            Fichier Ouvrier :
                vérifier non existence ouvrier nom prénom date de naissance
                    si : créer position puis ouvrier
                    sinon verfifier si il a changé si oui on fait un update
            fouv
        Sinon
            Quitter
    '''
    # sys.setdefaultencoding("utf-8")
    print("Lancement du programme de MAJ des ouvriers")
    cf = CheckFile(pathField="/vagrant/DonneesBDD/reglesMetiers.txt")
    cf.fileExists()
    cf.isWellBuildRules()
    
    
    cf1 = CheckFile(pathField="/vagrant/DonneesBDD/salaries.csv",
                   fieldList=[['nom', False], ['prénom', False], ['date de naissance', False], ['adresse', False], ['CP', True], ['Ville', False], ['métier', False], ['qualif', False]])
    cf1.fileExists()
    cf1.isWellBuildCSV()
    
    myFile = codecs.open(cf1.pathField, 'r', 'utf-8')
    content = myFile.read()
    myLines = content.split('\n')
    
    '''
    for i in myLines:
        i = i.encode('utf-8')'''
    
    
    conn = Connexion().connect()
    gw = GenerateWorkers()
    # print myLines[0].upper().encode('utf-8') sys.stdout.encoding .supprime_accent(myLines[0])
    for i in myLines:
        gw.manageWorker(i, conn)
    Connexion().disconnect(conn)
    print unicode('OPERATION EFFECTUEE')