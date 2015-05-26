# coding=utf8

from interfacebdd.Connexion import Connexion
from interfacebdd.ShuttleDAO import ShuttleDAO
from interfacebdd.PhaseDAO import PhaseDAO

from system.Car import Car
from interfacebdd.CarDAO import CarDAO

from flask import Blueprint, request, json
import pymysql

car_api = Blueprint('car_api', __name__ )

    
@car_api.route('/car/create/', methods=['POST'])
def createCar():
    try:
        conn = Connexion().connect()
        car = CarDAO()
        s = Car(plate=request.form['plate'], model=request.form['model'], nbPlace=request.form['nbPlace'])
        idCar = car.insert(conn, s)
        if idCar == -1:
            resp = {"code" : -1,
                    "message" : "Échec de la création du véhicule"}
        else:
            resp = {"code":1,
                    "message":"Création du véhicule effectuée"}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur de connexion lors de la création du véhicule"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    
@car_api.route('/car/delete/', methods=['POST'])
def deleteCar():
    try:
        car = CarDAO()
        conn = Connexion().connect()
        if request.method == 'POST':
            idCar = car.deleteById(conn, int(request.form['num']))
        if idCar == -1:
            resp = {"code":-1,
                    "message":"Échec de la suppression"}
        else:
            resp = {"code":1,
                    "message":"Suppression effectuée"}
    except:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur de connexion lors de la suppression du véhicule"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    

@car_api.route('/car/used/fromweek/', methods=['POST'])
def carUsedFromWeek():
    try:
        shuttle = ShuttleDAO()
        phase = PhaseDAO()
        conn = Connexion().connect()
        s = []
        for p in phase.getAllByFilterExtended(conn, False, [], ("numWeek", '>=',  request.form['week']), ("numYear", '>=', request.form['year'])):
            for i in shuttle.getAllByFilter(conn, False, [], ("phase", str(p.num))):
                s.append(i.car.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : 1,
                "message" : "Erreur de connexion lors de la récupération des véhicules utilisés"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")

@car_api.route('/car/unused/forweek/', methods=['POST'])
def carUnusedForWeek():
    try:
        shuttle = ShuttleDAO()
        phase = PhaseDAO()
        conn = Connexion().connect()
        used = []
        s = []
        for p in phase.getAllByFilter(conn, False, [], ("numWeek",  request.form['week']), ("numYear", request.form['year'])):
            for i in shuttle.getAllByFilter(conn, False, [], ("phase", str(p.num))):
                if int(request.form['idSite']) != p.numSite:
                    used.append(i.car.num)
        for c in CarDAO().getAll(conn, False, []):
            if c.num not in used:
                s.append(c.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : 1,
                "message" : "Erreur de connexion lors de la récupération des véhicules utilisés"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")

@car_api.route('/car/isused/forweek/', methods=['POST'])
def carIsUsedForWeek():
    try:
        shuttle = ShuttleDAO()
        phase = PhaseDAO()
        conn = Connexion().connect()
        s = False
        for p in phase.getAllByFilter(conn, False, [], ("numWeek",  request.form['week']), ("numYear", request.form['year'])):
            for i in shuttle.getAllByFilter(conn, False, [], ("phase", str(p.num))):
                if int(request.form['idCar']) == i.car.num:
                    s = True
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : 1,
                "message" : "Erreur de connexion lors de la récupération des véhicules utilisés"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")

@car_api.route('/car/all/')
def allCar():
    try:
        conn = Connexion().connect()
        car = CarDAO()
        s = []
        for i in car.getAll(conn, False, []):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur de connexion lors de la récupération des véhicules"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")


"""
@app.route('/car/all/lazy/')
def allLazyCar():
    try:
        conn = Connexion().connect()
        car = CarDAO()
        s = []
        for i in car.getAll(conn, True, []):
            s.append(i.serial())
        return json.dumps(s, encoding="utf-8")
    except:
        Connexion().exception()
    finally:
        Connexion().disconnect(conn)
"""
"""
@car_api.route('/car/used/')
def usedCar():
    '''
    Retourne la liste des véhicules utilisés
    '''
    try:
        conn = Connexion().connect()
        car = CarDAO()
        s = []
        for i in car.getUsedCar(conn, True, []):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur de connexion lors de la récupération des véhicules utilisés"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")

"""
"""
@car_api.route('/car/unused/')
def unusedCar():
    '''
    Retourne la liste des véhicules inutilisés
    '''
    try:
        conn = Connexion().connect()
        car = CarDAO()
        s = []
        for i in car.getUnUsedCar(conn, False, []):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur de connexion lors de la récupération des véhicules inutilisés"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
"""
"""
@app.route('/car/used/lazy/')
def usedLazyCar():
    try:
        conn = Connexion().connect()
        car = CarDAO()
        s = []
        for i in car.getUsedCar(conn, False, []):
            s.append(i.serial())
        return json.dumps(s, encoding="utf-8")
    except:
        Connexion().exception()
    finally:
        Connexion().disconnect(conn)
"""