# coding=utf8
from interfacebdd.AssignmentDAO import AssignmentDAO
from interfacebdd.WorkerDAO import WorkerDAO
from interfacebdd.PhaseDAO import PhaseDAO
from interfacebdd.SiteDAO import SiteDAO
from interfacebdd.Connexion import Connexion

from system.Assignment import Assignment
from system.Phase import Phase

from flask import Blueprint, request, json
from datetime import date
import pymysql

assignment_api = Blueprint('assigment_api', __name__ )

@assignment_api.route('/assignments/part/', methods=['GET', 'POST'])
def partAssignments():
    """
    Récupère des affectations partielles filtrées suivant la date
    
    les affectations contiennent numWorker, idSite, numWeek, numYear
    
    Args:
        request.form doit contenir :
            - startweek
            - startYear
            - endWeek
            - endYear
    
    Returns:
        code 1, data : data contient les affectations trouvées
        code -1, message : erreur lors de la récupération
    """
    try:
        assign = AssignmentDAO()
        conn = Connexion().connect()
        s = []
        if request.method == 'POST':
            res = assign.getPartAssignment2(conn, request.form["startWeek"], request.form["startYear"], request.form["endWeek"], request.form["endYear"])
        else:
            res = assign.getPartAssignment2(1, 2013, 52, 2040)
        for i in res:
                s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des affectations."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    

@assignment_api.route('/assignments/insert/', methods=['POST'])
def insertAssignments():
    """
    Ajoute et supprime des affectations
    
    Args:
        request.form doit contenir :
            - remove : liste des affectations à supprimer
            - tab : liste des affectations à ajouter
    
    Returns:
        code 1, data : data contient les affectations trouvées
        code -1, message : erreur lors de la récupération
    """
    try:
        conn = Connexion().connect()
        assign = AssignmentDAO()
        Ouv = WorkerDAO()
        Pha = PhaseDAO()
        if request.method == 'POST':
            assignTable = json.loads(request.form['tab'])
            removeTable = json.loads(request.form['remove'])
            for i in xrange(len(removeTable)):
                p = Pha.getByFilter(conn, False, [], ('numWeek', str(removeTable[i]["numWeek"])), ('numSite', str(removeTable[i]["idSite"])), ('numYear', str(removeTable[i]["numYear"])))
                w = Ouv.getById(conn, False, [], removeTable[i]["numWorker"])
                a = assign.getByFilter(conn, False, [], ('phase', str(p.num)), ('worker', str(w.num)))
                idAssign = assign.deleteById(conn, a.num)
                if idAssign == -1:
                    resp = {"code":-1,
                            "message":"Échec de la suppression des affectations"}

            for i in xrange(len(assignTable)):
                p = Pha.getByFilter(conn, False, [], ('numWeek', str(assignTable[i]["numWeek"])), ('numSite', str(assignTable[i]["idSite"])), ('numYear', str(assignTable[i]["numYear"])))
                w = Ouv.getById(conn, False, [], assignTable[i]["numWorker"])
                if p == None:
                    p = Phase(numWeek=str(assignTable[i]["numWeek"]), numSite=str(assignTable[i]["idSite"]), numYear=str(assignTable[i]["numYear"]), needs=[])
                    temp = Pha.insert(conn, p)
                    p = Pha.getById(conn, False, [], temp)
                a = Assignment(num=-1, worker=w, phase=p)
                idAssign = assign.insert(conn, a)
                if idAssign == -1:
                    resp = {"code":-1,
                            "message":"Échec de l'ajout des affectations"}
        try:
            resp
        except NameError:
            resp = {"code":1,
                    "message":"Modifications des affectations validée"}

    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code":-1,
                "message":"Erreur inconnu lors de la modification des affectations"}
    except Exception as e:
        resp = {"code":-1,
                "message":str(e)}
        raise
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
        
@assignment_api.route('/assignment/byworker/', methods=['POST'])
def assignmentsWorkerById():
    """
    Récupère la liste des affectations pour un ouvrier
    """
    try:
        assign = AssignmentDAO()
        site = SiteDAO()
        conn = Connexion().connect()
        s = []
        if request.method == 'POST':
            for p in PhaseDAO().getAllByFilterExtended(conn, False, [], ('numWeek', '>=', request.form['week']), ('numYear', '>=', request.form['year'])):
                for i in assign.getAllByFilter(conn, False, [], ('worker', request.form['num']), ('phase', str(p.num))):
                    dico = i.serial()
                    dico['siteName'] = site.getById(conn, False, [], i.phase.numSite).serial()['name']
                    s.append(dico)
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des affectations."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    
