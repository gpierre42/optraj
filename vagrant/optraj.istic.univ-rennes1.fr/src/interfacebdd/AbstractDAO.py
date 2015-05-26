# coding=utf8

import ConfigParser
import pymysql
from string import Template
import operator
import os

class AbstractDAO(object):
    '''
    Classe abstraite AbstractDAO représentant une table en base de donnée
    
    Attributs :
    - tableName : nom d'une table de la base de donnée (str)
    - mappingCols : mapping des colonnes de la table sur les attributs d'un objet python (dict)
    - joins::Jointure : permet de gérer les éventuelles jointures
    '''
    # Delete from Chantier where idChantier = '" + idChantier

    TEMPLATE_SEL = Template("SELECT $columns FROM $table e $joins WHERE e.ID=$clauses")
    TEMPLATE_SEL_FIL = Template("SELECT $columns FROM $table e $joins WHERE $clauses")
    TEMPLATE_SEL_ALL = Template("Select $columns FROM $table e $joins")
    TEMPLATE_SEL_ALL_FIL = Template("Select $columns FROM $table e $joins WHERE $clauses")
    TEMPLATE_DEL_ID = Template("DELETE FROM $table  WHERE ID=$clauses")
    TEMPLATE_DEL = Template("DELETE FROM $table  WHERE $clauses")
    TEMPLATE_UPDATE = Template("UPDATE $table SET $value WHERE ID=$clauses")
    TEMPLATE_INSERT = Template("INSERT INTO $table SET $value")

    '''
    TEMPLATE_SEL est une constante permettant de construire une requÃªte SQL de sÃ©lection.
    '''

    def __init__(self, tableName=None, mappingCols=None, mappingFil=None, joins=None):
        '''
        Constructeur

        Args:
            tableName : nom de la table en BDD (str)
            mappingCols : les colonnes à conserver (dict(str:colonneBDD, str:nom attribut))
            mappingFil : remplissage des clauses WHERE pour filtrer  (dict(str:nom attribut, str:colonneBDD))
            joins : liste de NaturalJoin décris les jointures à effectuer
            
        '''

        self._mappingFil = mappingFil
        self._tableName = tableName
        self._mappingCols = mappingCols
        self._joins = joins
        self._dicoJoins = {j.alias: j for j in ([] if self.joins is None else self.joins)}
        self._verboseMode = False

    def _createElement(self):
        '''
        Créé un élément du type système associé au type DAO. doit être surchargée
        
        Fonction surchargée dans chaque classe DAO concrète.
        Permet la création de l'objet Obj Systeme associé à la classe ObjDAO.
        
        Returns:
            None
        '''
        #Exception Ã  gÃ©rer !!!
        return None

    def setVerboseMode(self, mode):
        '''
        Permet de spécifier si l'on souhaite afficher une trace des requêtes effectuées
        
        Args:
            mode : True ou False suivant le choix (affichage ou non)
        '''
        if mode:
            self._verboseMode = True
        else:
            self._verboseMode = False

    #**********************OPTIMISEE******************************

    def _buildObject(self, co=None, lazzy=False, partLazzy=[], dico={}):
        '''
        Construit un Objet du Systeme à partir d'un dico(attribut, valeur) passée en paramètre
        
        Args:
            co la Connexion
            lazzy indique si le chargement se fait en lazzy (bool)
            partLazzy liste des jointures à charger quand meme si on est en lazzy (list(NaturalJoin))
            dico l'ensemble des attributs de l'objet à créer dict(str:nom attribut, X:valeur)
        
        Returns:
            l'objet système construit
        '''
        o = self._createElement()
        # Le for suivant permet la création des objet joins
        # exemple: un Ouvrier a un attribut Position position
        for (key, value) in self._dicoJoins.items():
            if len(key.split("_")) <= 2:
                dicoTemp = {}
                for (k, v) in dico.items():
                    if k.startswith(key):
                        dicoTemp[k.replace(key, "")] = v
        # l'appel rÃ©cursif permet de crÃ©er l'attribut repÃ©rÃ© dans le dicoAttr
                setattr(o, key.replace('_', ''), self.dicoAttr[key]._buildObject(co, lazzy, partLazzy, dicoTemp))
        for (attr, value) in dico.items():
            setattr(o, attr, value)
        return o

    def getById(self, co=None, lazzy=False, partLazzy=[], ident=-1):
        '''
        Permet de récupérer un objet python depuis la base de donnée.
        
        Args:
            co la Connexion
            lazzy indique si le chargement se fait en lazzy (bool)
            partLazzy liste des jointures à charger quand meme si on est en lazzy (list(NaturalJoin))
            ident l'identifiant de l'objet à charger (int)
            
        Returns:
            l'objet récupéré depuis la base
        '''

        # Construit la partie sÃ©lection de la requÃªte SQL
        listCols = ["e." + col + " as " + attr for (col, attr) in self.mappingCols.items()]

        if(lazzy):
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if partLazzy is None else partLazzy)]
            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if partLazzy is None else partLazzy) for (col, attr) in j.joinMappingCols.items()])

        else:
            # Construit la partie jointure de la requÃªte SQL
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if self.joins is None else self.joins)]

            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if self.joins is None else self.joins) for (col, attr) in j.joinMappingCols.items()])

        # Construit la requÃªte SQL
        request = self.TEMPLATE_SEL.substitute(columns=", ".join(listCols), table=self.tableName, joins=" ".join(listJoins), clauses=str(ident))
        if self._verboseMode:
            print(request)

        cursor = co[1]
        cursor.execute(request)

        # construit et retourne un Objet du Systeme
        return self._buildObject(co, lazzy, partLazzy, cursor.fetchone())

    def getAll(self, co=None, lazzy=False, partLazzy=[]):

        '''
        Permet de récupérer un ensemble d'objet(set) python depuis la base de donnÃ©e.
        
        Args:
            co la Connexion
            lazzy indique si le chargement se fait en lazzy (bool)
            partLazzy liste des jointures à charger quand meme si on est en lazzy (list(NaturalJoin))
            
        Returns:
            l'intégralité des objets du type récupérés depuis la BDD
        '''

        # Construit la partie sÃ©lection de la requÃªte SQL
        listCols = ["e." + col + " as " + attr for (col, attr) in self.mappingCols.items()]

        if(lazzy):
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if partLazzy is None else partLazzy)]
            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if partLazzy is None else partLazzy) for (col, attr) in j.joinMappingCols.items()])
        else:
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if self.joins is None else self.joins)]

            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if self.joins is None else self.joins) for (col, attr) in j.joinMappingCols.items()])

        # Construit la requÃªte SQL
        request = self.TEMPLATE_SEL_ALL.substitute(columns=", ".join(listCols), table=self.tableName, joins=" ".join(listJoins))
        if self._verboseMode:
            print(request)

        # execution d'une requete
        cursor = co[1]
        cursor.execute(request)

        # construit et retourne un Objet du Systeme
        return {self._buildObject(co, lazzy, partLazzy, c) for c in cursor.fetchall()}

    def getByFilter(self, co=None, lazzy=False, partLazzy=[], *args):
        '''
        Permet de récupérer un objet python depuis la base de donnée avec un filtre
        
        s'il y a plusieurs filtre, la condition est un AND (il faut satisfaire tous les filtres)
        l'élément retourné est le premier trouvé qui satisfait tous les filtres
        
        Args:
            co la Connexion
            lazzy indique si le chargement se fait en lazzy (bool)
            partLazzy liste des jointures à charger quand meme si on est en lazzy (list(NaturalJoin))
            args la liste des filtres (un tuple de doublet (str:nom attribut, X:valeur))
            
        Returns:
            le premier objet trouvé
        '''

        # Construit la partie sÃ©lection de la requÃªte SQL
        listCols = ["e." + col + " as " + attr for (col, attr) in self.mappingCols.items()]

        # Construit la partie where de la selection
        listWhere = ["e." + self.mappingFil[key] + " = " + "\"" + value + "\"" for (key, value) in args]

        if(lazzy):
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if partLazzy is None else partLazzy)]
            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if partLazzy is None else partLazzy) for (col, attr) in j.joinMappingCols.items()])
        else:
            # Construit la partie jointure de la requÃªte SQL
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if self.joins is None else self.joins)]

            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if self.joins is None else self.joins) for (col, attr) in j.joinMappingCols.items()])

        # Construit la requÃªte SQL
        request = self.TEMPLATE_SEL_FIL.substitute(columns=", ".join(listCols), table=self.tableName, joins=" ".join(listJoins), clauses=" AND ".join(listWhere))
        if self._verboseMode:
            print(request)

        cursor = co[1]

        # execution d'une requete
        cursor.execute(request)

        o = cursor.fetchone()
        if o != None:
            # construit et retourne un Objet du Systeme
            return self._buildObject(co, lazzy, partLazzy, o)
        else:
            return None

    def getAllByFilter(self, co=None, lazzy=False, partLazzy=[], *args):
        '''
        Permet de récupérer un ensemble d'objet(set) python depuis la base de donnée avec un filtre
        
        s'il y a plusieurs filtre, la condition est un AND (il faut satisfaire tous les filtres)
        
        Args:
            co la Connexion
            lazzy indique si le chargement se fait en lazzy (bool)
            partLazzy liste des jointures à charger quand meme si on est en lazzy (list(NaturalJoin))
            args la liste des filtres (un tuple de doublet (str:nom attribut, X:valeur))
            
        Returns:
            l'ensemble des objets correspondants aux filtres
        '''

        # Construit la partie sÃ©lection de la requÃªte SQL
        listCols = ["e." + col + " as " + attr for (col, attr) in self.mappingCols.items()]

        # Construit la partie where de la selection
        listWhere = [self.mappingFil[key] + " = " + "\"" + value + "\"" for (key, value) in args]

        if(lazzy):
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if partLazzy is None else partLazzy)]
            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if partLazzy is None else partLazzy) for (col, attr) in j.joinMappingCols.items()])
        else:
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if self.joins is None else self.joins)]

            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if self.joins is None else self.joins) for (col, attr) in j.joinMappingCols.items()])

        # Construit la requÃªte SQL
        request = self.TEMPLATE_SEL_ALL_FIL.substitute(columns=", ".join(listCols), table=self.tableName, joins=" ".join(listJoins), clauses=" AND ".join(listWhere))
        if self._verboseMode:
            print(request)

        # execution d'une requete
        cursor = co[1]
        cursor.execute(request)

        # construit et retourne un Objet du Systeme
        return {self._buildObject(co, lazzy, partLazzy, c) for c in cursor.fetchall()}

    def getAllByFilterExtended(self, co=None, lazzy=False, partLazzy=[], *args):
        '''
        Permet de récupérer un ensemble d'objet(set) python depuis la base de donnée avec un filtre
        
        s'il y a plusieurs filtre, la condition est un AND (il faut satisfaire tous les filtres)
        
        Args:
            co la Connexion
            lazzy indique si le chargement se fait en lazzy (bool)
            partLazzy liste des jointures à charger quand meme si on est en lazzy (list(NaturalJoin))
            args la liste des filtres (un tuple de triplet (str:nom attribut,str:operateur, X:valeur))
            
        Returns:
            l'ensemble des objets correspondants aux filtres
        '''

        # Construit la partie sÃ©lection de la requÃªte SQL
        listCols = ["e." + col + " as " + attr for (col, attr) in self.mappingCols.items()]

        # Construit la partie where de la selection
        listWhere = [self.mappingFil[str(key)] + str(op) + str(value) for (key, op, value) in args]

        if(lazzy):
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if partLazzy is None else partLazzy)]
            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if partLazzy is None else partLazzy) for (col, attr) in j.joinMappingCols.items()])
        else:
            listJoins = [j.joinType + " JOIN " + j.tableName + " AS " + j.alias + " ON " + " AND ".join(j.joinClauses) for j in ([] if self.joins is None else self.joins)]

            # Ajoute au SELECT les colonnes issue de la jointure
            listCols.extend([j.alias + "." + col + " as " + j.alias + "_" + attr for j in ([] if self.joins is None else self.joins) for (col, attr) in j.joinMappingCols.items()])

        # Construit la requÃªte SQL
        request = self.TEMPLATE_SEL_ALL_FIL.substitute(columns=", ".join(listCols), table=self.tableName, joins=" ".join(listJoins), clauses=" AND ".join(listWhere))
        if self._verboseMode:
            print(request)

        # execution d'une requete
        cursor = co[1]
        cursor.execute(request)

        # construit et retourne un Objet du Systeme
        return {self._buildObject(co, lazzy, partLazzy, c) for c in cursor.fetchall()}

    def deleteById(self, co=None, ident=-1):
        '''
        Supprime un élément en base de donnée
        
        Args:
            co la Connexion
            ident l'identifiant de l'élément à supprimer (int)
        '''
        # Construit la requête SQL
        request = self.TEMPLATE_DEL_ID.substitute(table=self.tableName, clauses=str(ident))
        if self._verboseMode:
            print(request)

        # execution d'une requete
        cursor = co[1]
        cursor.execute(request)

        co[0].commit()
        
    def delete(self, co=None, *args):
        '''
        Supprime un élément en base de donnée
        
        Args:
            co la Connexion
            *args 
        '''
        # Construit la partie where de la selection
        listWhere = [self.mappingFil[key] + " = " + "\"" + str(value) + "\"" for (key, value) in args]

        
        # Construit la requête SQL
        request = self.TEMPLATE_DEL.substitute(table=self.tableName, clauses=" AND ".join(listWhere))
        if self._verboseMode:
            print(request)

        # execution d'une requete
        cursor = co[1]
        cursor.execute(request)

        co[0].commit()


    def insert(self, co=None, Obj=None):
        '''
        Permet d'insérer un objet python dans la base de donnÃ©e.

        Args:
            co la Connexion
            Obj l'objet python à insérer
            
        Returns:
            l'id de l'objet inséré
        '''
        # Construit une liste des valeurs Ã  insÃ©rer dans la base
        listValue = [col + "=" + "\"" + str(operator.attrgetter(attr)(Obj)) + "\"" for (col, attr) in self.mappingCols.items()]

        # Construit les Ã©ventuels appels rÃ©cursifs pour insÃ©rer les objets liÃ©
        for j in ([] if self.joins is None else self.joins):
            attribut = j.alias
            if self._verboseMode:
                print j.alias
            if len(attribut.split("_")) <= 2:
                id_obj = self._dicoAttr[j.alias].insert(co, operator.attrgetter(attribut.replace("_", ""))(Obj))
                listValue.append(j.joinId + "=" + str(id_obj))

        # Construit la requÃªte SQL
        request = self.TEMPLATE_INSERT.substitute(table=self.tableName, value=", ".join(listValue))
        if self._verboseMode:
            print(request)

        cursor = co[1]
        # execution d'une requete
        cursor.execute(request)

        co[0].commit()

        # on retournel'id de l'objet insÃ©rÃ©
        return cursor.lastrowid

    def update(self, co=None, Obj=None):
        '''
        Permet de mettre à jour un objet python dans la base de donnÃ©e.
        
        Args:
            co la Connexion
            Obj l'objet python à insérer
            
        Returns:
            l'id de l'objet mis à jour
        '''
        # Construit une liste des valeurs Ã  modifier dans la base
        listValue = [col + "=" + "\"" + str(operator.attrgetter(attr)(Obj)) + "\"" for (col, attr) in self.mappingCols.items()]
        # Construit les Ã©ventuels appels rÃ©cursifs pour insÃ©rer les objets liÃ©
        for j in ([] if self.joins is None else self.joins):
            attribut = j.alias
            if len(attribut.split("_")) <= 2:
                id_obj = self._dicoAttr[j.alias].update(co, operator.attrgetter(attribut.replace("_", ""))(Obj))
                listValue.append(j.joinId + "=" + str(id_obj))
        # Construit la requÃªte SQL
        # TEMPLATE_UPDATE = Template("UPDATE FROM $table SET $columns=$clauses where e.ID=$clauses")
        request = self.TEMPLATE_UPDATE.substitute(table=self.tableName, value=", ".join(listValue), clauses=Obj.num)
        if self._verboseMode:
            print(request)

        # execution d'une requete
        cursor = co[1]
        
        cursor.execute(request)

        co[0].commit()

        if(Obj.num != None):
            return Obj.num
        # on retournel'id de l'objet mis à jour
        return -1

    '''
    =========== Setteurs/Accesseurs ===============
    '''

    @property
    def tableName(self):
        return self._tableName

    @tableName.setter
    def tableName(self, value):
        self._tableName = value

    @property
    def mappingCols(self):
        return self._mappingCols

    @mappingCols.setter
    def mappingCols(self, value):
        self._mappingCols = value

    @property
    def mappingFil(self):
        return self._mappingFil

    @mappingFil.setter
    def mappingFil(self, value):
        self._mappingFil = value

    @property
    def joins(self):
        return self._joins

    @joins.setter
    def joins(self, value):
        self._joins = value

if __name__ == '__main__':
    '''
    test de la classe
    '''
    pass
