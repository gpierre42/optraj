# coding=utf8
from system.Position import Position
from system.Worker import Worker
from interfacebdd.Connexion import Connexion
from interfacebdd.WorkerDAO import WorkerDAO
from interfacebdd.CraftDAO import CraftDAO
from interfacebdd.QualificationDAO import QualificationDAO
from flask import Blueprint, request, json
from datetime import date
import pymysql

worker_api = Blueprint('worker_api', __name__ )

@worker_api.route('/worker/create/', methods=['POST'])
def createWorker():
    """
    Créé un nouvel ouvrier
    
    Args:
        request.form doit contenir :
            - latitude
            - longitude
            - address : l'adresse (chaine)
            - name
            - birthdate
            - craft : id du métier
            - qualification : id de la qualification
    
    Returns:
        code 1, message : ajout réussi
        code -1, message : erreur lors de l'ajout
    """
    try:
        conn = Connexion().connect()
        worker = WorkerDAO()
        if request.method == 'POST':
            p = Position(request.form['latitude'], request.form['longitude'], request.form['address'])
            d = date(int(request.form['birthdate'][-4:]), int(request.form['birthdate'][3:-5]), int(request.form['birthdate'][:2]))
            c = CraftDAO()
            cra = c.getById(conn, False, [], request.form['craft'])
            q = QualificationDAO()
            quali = q.getById(conn, False, [], request.form['qualification'])
            w = Worker(name=request.form['name'], firstName=request.form['firstName'], birthdate=d, position=p, craft=cra, qualification=quali)
            idWorker = worker.insert(conn, w)
            if idWorker == -1:
                resp = {"code" : -1,
                        "message" : "Échec de la création de l'ouvrier"}
            else:
                resp = {"code":1,
                        "message":"Création de l'ouvrier validée"}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur de connexion lors de la création de l'ouvrier"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    

@worker_api.route('/worker/delete/', methods=['POST'])
def deleteWorker():
    try:
        worker = WorkerDAO()
        conn = Connexion().connect()
        if request.method == 'POST':
            idWorker = worker.deleteById(conn, request.form['num'])
            if idWorker == -1:
                resp = {"code" : -1,
                        "message" : "Échec de la suppression de l'ouvrier"}
            else:
                resp = {"code":1,
                        "message":"Suppression de l'ouvrier effectuée"}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur de connexion lors de la suppression de l'ouvrier"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")



@worker_api.route('/worker/update/', methods=['POST'])
def updateWorker():
    """
    Édite un ouvrier
    
    Args:
        request.form doit contenir :
            - latitude
            - longitude
            - address : l'adresse (chaine)
            - name
            - birthdate
            - craft : id du métier
            - qualification : id de la qualification
    
    Returns:
        code 1, message : édition réussie
        code -1, message : erreur lors de l'édition
    """
    try:
        worker = WorkerDAO()
        conn = Connexion().connect()
        if request.method == 'POST':

            w = worker.getById(conn, False, [], request.form["num"])
            idPos = w.position.num
            p = Position(num=idPos, lat=request.form['latitude'], long=request.form['longitude'], address=request.form['address'])
            d = date(int(request.form['birthdate'][-4:]), int(request.form['birthdate'][3:-5]), int(request.form['birthdate'][:2]))
            c = CraftDAO()
            cra = c.getById(conn, False, [], request.form['craft'])
            q = QualificationDAO()
            quali = q.getById(conn, False, [], request.form['qualification'])
            w = Worker(num=request.form["num"], name=request.form['name'], firstName=request.form['firstName'], licence=request.form['licence'], birthdate=d, position=p, craft=cra, qualification=quali)
            idWorker = worker.update(conn, w)
            if idWorker == -1:
                resp = {"code" : -1,
                        "message" : "Échec de la modification de l'ouvrier"}
            else:
                resp = {"code":1,
                        "message":"Modification de l'ouvrier validée"}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur de connexion lors de la modification de l'ouvrier"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")

@worker_api.route('/worker/all/')
def allWorker():
    """
    Retourne la liste de tous les ouvriers
    
    Returns:
        code 1, data : data contient la liste des ouvriers
        code -1, message : erreur lors de la récupération
    """
    try:
        worker = WorkerDAO()
        conn = Connexion().connect()
        s = []
        for i in worker.getAll(conn, False, []):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des ouvriers."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")


@worker_api.route('/worker/all/lazy/')
def allLazyWorker():
    """
    Retourne la liste de tous les ouvriers (partiels)
    
    Les ouvriers ne contiennent que les champs atomiques (noms, dates) ainsi que les métiers et qualifications
    
    Returns:
        code 1, data : data contient la liste des ouvriers (partiels)
        code -1, message : erreur lors de la récupération
    """
    try:
        worker = WorkerDAO()
        conn = Connexion().connect()
        s = []
        for i in worker.getAll(conn, True, [worker.JOIN_CRAFT, worker.JOIN_QUALIFICATION]):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des ouvriers."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
      

@worker_api.route('/worker/byid/', methods=["POST"])
def workerById():
    """
    Accède à un ouvrier par son identifiant
    
    Args:
        request.form doit contenir :
            - num : l'identifiant de l'ouvrier en BDD
            
    Returns:
        code 1, data : data contient l'ouvrier si on le trouve
        code -1, message : erreur lors de la récupération
    """
    try:
        worker = WorkerDAO()
        conn = Connexion().connect()
        if request.method == 'POST':
            s = worker.getById(conn, False, [], request.form['num']).serial()
        if(s == None):
            resp = {"code" : -1,
                    "message" : "L'ouvrier d'id {} n'as pas été trouvé".format(request.form['num'])}
        else:
            resp = {"code" : 1,
                    "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération d'un chantier (id {}).".format(request.form['num'])}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    

@worker_api.route('/worker/assignedtosite/byid/', methods=["POST"])
def workerAssignedToSideById():
    """
    Récupération des ouvriers affecté à un site identifié par son id
    
    Args:
        request.form doit contenir :
            - idSite : l'identifiant du chantier en BDD
            
    Returns:
        code 1, data : data contient la liste des ouvriers
        code -1, message : erreur lors de la récupération
    """
    try:
        worker = WorkerDAO()
        conn = Connexion().connect()
        s = []
        if request.method == 'POST':
            res = worker.getAssignedToSite(conn, request.form["idSite"])
            for elem in res:
                s.append(elem.serial())
            resp = {"code" : 1,
                    "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des ouvriers."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    
@worker_api.route('/worker/assigned/bysite/byweek/', methods=["POST"])
def workerAssignedToSiteOnWeek():
    """
    Récupération des ouvriers affecté à un site identifié par son id durant une semaine donnée
    
    Args:
        request.form doit contenir :
            - idSite : l'identifiant du chantier en BDD
            - week : numéro de semaine
            - year : l'année
            
    Returns:
        code 1, data : data contient la liste des ouvriers
        code -1, message : erreur lors de la récupération
    """
    try:
        worker = WorkerDAO()
        conn = Connexion().connect()
        s = []
        if request.method == 'POST':
            res = worker.getAssignedToSiteOnWeek(conn, request.form["idSite"], request.form["week"], request.form["year"])
            for elem in res:
                s.append(elem.serial())
            resp = {"code" : 1,
                    "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des ouvriers."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    
@worker_api.route('/worker/count/bycraftqualif/', methods=["GET"])
def workerCountByCraftQualif():
    """
    Récupération du nombre d'ouvrier par craft et qualif
            
    Returns:
        code 1, data : data le dico des comptages
        code -1, message : erreur lors de la récupération
    """
    try:
        worker = WorkerDAO()
        conn = Connexion().connect()
        res = worker.getCountCraftQualif(conn)
        if res is None:
            resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération du comptage."}
        else:
            resp = {"code" : 1,
                    "data" : json.dumps(res, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération du comptage."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")