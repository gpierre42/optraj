# coding=utf8
from interfacebdd.AssignmentDAO import AssignmentDAO
from interfacebdd.UnavailabilityDAO import UnavailabilityDAO
from interfacebdd.WorkerDAO import WorkerDAO
from interfacebdd.PhaseDAO import PhaseDAO
from interfacebdd.SiteDAO import SiteDAO
from interfacebdd.Connexion import Connexion

from system.Unavailability import Unavailability
from system.Phase import Phase

from flask import Blueprint, request, json
from datetime import date
import pymysql

unavailability_api = Blueprint('unavailability_api', __name__ )

    

@unavailability_api.route('/unavailability/insert/', methods=['POST'])
def insertUnavailability():
    """
    Ajoute des affectations
    
    Args:
        request.form doit contenir :
            - insert : liste des affectations à ajouter
    
    Returns:
        code 1, message : ajouts réussis
        code -1, message : erreur lors de la récupération
    """
    try:

        conn = Connexion().connect()
        unavail = UnavailabilityDAO()
        unavail.setVerboseMode(True)
        if request.method == 'POST':
            insertTable = json.loads(request.form['insert'])
            
            for i in xrange(len(insertTable)):
                x = Unavailability(idWorker=insertTable[i]['numWorker'],
                                   numWeek=insertTable[i]["numWeek"],
                                   numYear=insertTable[i]["numYear"],
                                   type=insertTable[i]["type"])
                try:
                    idinsert = unavail.insert(conn, x)
                except Exception as e:
                    resp = {"code":-1,
                            "message":"Une ou plusieurs insertion(s) d'indisponibilité(s) ont échouée(s) : <br/>{}".format(e)}
                if idinsert == -1 :
                    resp = {"code":1,
                            "message":"Une ou plusieurs insertion(s) d'indisponibilité(s) ont échouée(s)"}
        try:
            resp
        except NameError:
            resp = {"code":1,
                    "message":"Suppressions validées"}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code":-1,
                "message":"Erreur pymsql"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")


@unavailability_api.route('/unavailability/delete/', methods=['POST'])
def deleteUnavailability():
    """
    Supprime des affectations
    
    Args:
        request.form doit contenir :
            - remove : liste des affectations à supprimer
    
    Returns:
        code 1, message : Suppressions effectuées
        code -1, message : erreur
    """
    try:
        conn = Connexion().connect()
        unavail = UnavailabilityDAO()
        unavail.setVerboseMode(True)
        #resp = None
        if request.method == 'POST':
            removeTable = json.loads(request.form['remove'])
            for i in xrange(len(removeTable)):
                try:
                    unavail.delete(conn,
                                   ('idWorker', removeTable[i]['numWorker']),
                                   ('numWeek', removeTable[i]["numWeek"]),
                                   ("numYear", removeTable[i]["numYear"]))
                except Exception as e:
                    resp = {"code":-1,
                            "message":"Une ou plusieurs suppression(s) ont échouées : <br/>{}".format(e)}
        try:
            resp
        except NameError:
            resp = {"code":1,
                    "message":"Suppressions validées"}
    except pymysql.err.Error as e:
        Connexion().exception()
        resp = {"code":-1,
                "message":"Erreur de connexion",
                "data":str(e)}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
        

@unavailability_api.route('/unavailability/after/', methods=['POST'])
def getUnavailabilityAfter():
    """
    Retourne la liste des indisponibilités après une semaine donnée
    
    Args:
        request.form doit contenir :
            - numYear : l'année
            - numWeek : la semaine
    
    Returns:
        code 1, data : liste des indisponibilités après une semaine donnée (comprise)
        code -1, message : erreur
    """
    try:
        conn = Connexion().connect()
        unavail = UnavailabilityDAO()
        #unavail.setVerboseMode(True)
        numWeek = json.loads(request.form['numWeek'])
        numYear = json.loads(request.form['numYear'])
        s = []
        for i in unavail.getAllByFilterExtended(conn, False, [], ('numWeek', '>=', numWeek), ('numYear', '=', numYear)):
            s.append(i.serial())
        for i in  unavail.getAllByFilterExtended(conn, False, [], ('numYear', '>', numYear)):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des indisponibilités."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")