# coding=utf8
'''
Created on 17 mars 2014

@author: alban
'''
import os
import sys

class CheckFile(object):
    '''
    Classe vérifiant la bonne construction d'un fichier csv ou de règles.
    - pathFile : emplacement du fichier (str)
    - fieldList : liste des champs du fichier et si il peuvent être null ou non (list)
    '''

    def __init__(self, pathField="/", fieldList=[]):
        '''
        Constructeur
        '''
        self._pathField = pathField
        self._fieldList = fieldList

    '''
    ================Setteurs/Accesseurs=====================
    '''
    @property
    def pathField(self):
        return self._pathField

    @pathField.setter
    def pathField(self, value):
        self._pathField = value

    @property
    def fieldList(self):
        return self._fieldList

    @fieldList.setter
    def fieldList(self, value):
        self._fieldList = value

    def __str__(self):
        '''
        retourne le checkFile sous une forme lisible pour l'humain.

        Returns:
            le checkFile sous forme de string
        '''
        return "CheckFile de chemin : {} et avec champs : {} ".format(self.pathField, self.fieldList)

    def fileExists(self):
        '''
        vérifie l'existence d'un fichier

        Returns:
            True si le fichier désigné par pathField existe, False sinon.
        '''
        res = os.path.isfile(self.pathField)
        if res == False:
            print("Le fichier " + self.pathField.encode('utf-8') + " n'a pas été trouvé, abandon du programme")
            sys.exit(0)

    def isWellBuildCSV(self):
        '''
        vérifie la bonne construction de chaque ligne d'un fichier CSV selon le fieldList

        Returns:
            0 si le fichier est bien construit (un 6-uplet par ligne) sinon la ligne où on a rencontré un problème
        '''
        # print self
        myFile = open(self.pathField, "r")
        content = myFile.read()
        myLines = content.split('\n')
        i = 1
        for line in myLines:
            arg = line.split(';')
            if len(arg) == len(self.fieldList):
                    j = 0
                    # print 'line : ' + str(i)
                    for elem in arg:
                        if elem == "" and  not self.fieldList[j][1]:
                            print("Le fichier CSV" + self.pathField.encode('utf-8') + " a rencontré un problème à la ligne : " + str(i))
                            sys.exit(0)
                        j = j + 1
            else:
                print arg
                if elem == "" and  not self.fieldList[j][1]:
                            print("Le fichier CSV " + self.pathField.encode('utf-8') + " a rencontré un problème à la ligne : " + str(i))
                            sys.exit(0)
            i = i + 1
        myFile.close()

    def isWellBuildRules(self):
        '''
        vérifie la bonne construction de chaque ligne d'un fichier CSV selon le fieldList
        
        "elem"+ : "elem cible"

        Returns:
            0 si le fichier est bien construit sinon la ligne où on a rencontré un problème
        '''

        myFile = open(self.pathField, "r")
        content = myFile.read()
        myLines = content.split('\n')
        i = 1
        for line in myLines:
            part = line.split(':')
            if len(part) != 2:
                print("Le fichier des règles " + self.pathField.encode('utf-8') + " a rencontré un problème à la ligne : " + str(i))
                sys.exit(0)
            partG = part[0].split('"')
            partD = part[1].split('"')
            if len(partD) != 3:
                print("Le fichier des règles " + self.pathField.encode('utf-8') + " a rencontré un problème à la ligne : " + str(i))
                sys.exit(0)
            if (len(partG) % 2) != 1:
                print("Le fichier des règles " + self.pathField.encode('utf-8') + " a rencontré un problème à la ligne : " + str(i))
                sys.exit(0)
        myFile.close()

        '''
Fonctionnement de l'algo de lecture de fichiers :

->Vérifier existence des fichiers
    Si
        Fichier Ouvrier :
            vérifier non existence ouvrier nom prénom date de naissance
                si : créer position puis ouvrier 
                sinon verfifier si il a changé si oui on fait un update
        fouv 
    Sinon
        Quitter'''
