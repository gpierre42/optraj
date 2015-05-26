# coding=utf8

from interfacebdd.PickupDAO import PickupDAO
from interfacebdd.Connexion import Connexion
from system.Position import Position
from system.Pickup import Pickup

from flask import Blueprint, request, json
import pymysql

pickup_api = Blueprint('pickup_api', __name__ )

@pickup_api.route('/pickup/all/')
def allPickup():
    """
    Récupère la liste de tous les pickup
    
    Returns:
        code 1, data : data contient la liste des pickup
        code -1, message : erreur lors de la récupération
    """
    try:
        pu = PickupDAO()
        conn = Connexion().connect()
        s = []
        for i in pu.getAll(conn, False, []):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des pickup."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    
@pickup_api.route('/pickup/bySite/', methods=["POST"])
def allPickupBySite():
    """
    Récupère la liste de tous les pickup associé au site d'idSite
    
    Args:
        request.form doit contenir :
            - idSite
            
    Returns:
        code 1, data : data contient la liste des pickup
        code -1, message : erreur lors de la récupération
    """
    try:
        pu = PickupDAO()
        conn = Connexion().connect()
        s = []
        for i in pu.getAllByFilter(conn, False, [], ("idSite", request.form["idSite"])):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des pickup."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")


@pickup_api.route('/pickup/create/', methods=["POST"])
def createPickup():
    """
    Créé un Pickup
    
    Args:
        request.form doit contenir :
            - latitude
            - longitude
            - address : l'adresse (chaine)
            - idSite : l'id du site lié
            
    Returns:
        code 1, message : ajout réussit
        code -1, message : erreur lors de l'ajout
    """
    pu = PickupDAO()
    p = Position(request.form['latitude'], request.form['longitude'], request.form['address'])
    pickup = Pickup(num=-1, position=p, idSite=request.form['idSite'])
    resp = {"code" : -1,
            "message" : "L'ajout d'un point de ramassage a échoué"}
    try:
        conn = Connexion().connect()
        idPickup = pu.insert(conn, pickup)
        if idPickup != -1:
            resp = {"code" : 1,
                    "message" : "insertion réussie",
                    "data": idPickup}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de l'ajout d'un pickup."}
    finally:
        Connexion().disconnect(conn)
    return json.dumps(resp, encoding="utf-8")
    
@pickup_api.route('/pickup/create/several/', methods=["POST"])
def createSeveralPickup():
    """
    Créé plusieurs pickups
    
    Args:
        request.form doit contenir :
            - pickups : liste des pickups
            
    Returns:
        code 1, message : ajout réussit
        code -1, message : erreur lors de l'ajout
    """
    pu = PickupDAO()
    pickups = json.loads(request.form['pickups'])
    idSite=request.form['idSite']
    errorOccurred=False
    try:
        conn = Connexion().connect()
        for elem in pickups:
            pos = Position(num=-1,
                           lat=elem["position"]["latitude"],
                           long=elem["position"]["longitude"],
                           address=elem["position"]["address"])
            p = Pickup(num=-1,
                       position = pos,
                       idSite=idSite)
            idPickup = pu.insert(conn, p)
            if idPickup == -1:
                errorOccurred=True
        if errorOccurred:
            resp = {"code" : -1,
                        "message" : "erreur"}
        else:
            resp = {"code" : 1,
                    "message" : "ajout réussi"}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de l'ajout d'un pickup."}
    except Exception as e:
        pass
    finally:
        try:
            resp
        except:
            resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de l'ajout d'un pickup."}
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    
@pickup_api.route('/pickup/delete/', methods=["POST"])
def deletePickup():
    """
    Supprime un pickup a partir de son id
    
    Args:
        request.form doit contenir :
            - idPickup
            
    Returns:
        code 1, message : ajout réussit
        code -1, message : erreur lors de l'ajout
    """
    pu = PickupDAO()
    try:
        conn = Connexion().connect()
        idPickup = pu.deleteById(conn, request.form['idPickup'])
        if idPickup == -1:
            resp = {"code" : -1,
                    "message" : "Échec de la suppression du point de ramassage"}
        else:
            resp = {"code":1,
                    "message":"Suppression du point de ramassage effectuée"}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la suppression d'un pickup."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    
@pickup_api.route('/pickup/delete/several', methods=["POST"])
def deleteSeveralPickup():
    """
    Supprime plusieurs pickup a partir de leurs id
    
    Args:
        request.form doit contenir :
            - idsToDelete liste des num de pickup a supprimer
            
    Returns:
        code 1, message : suppression réussie
        code -1, message : erreur lors de la suppression
    """
    pu = PickupDAO()
    idsToDelete = json.loads(request.form['idsToDelete'])
    errorOccurred = False
    try:
        conn = Connexion().connect()
        for idToDelete in idsToDelete:
            idPickup = pu.deleteById(conn, idToDelete)
            if idPickup == -1:
                errorOccurred = True
        if errorOccurred:
            resp = {"code" : -1,
                    "message" : "Échec de la suppression d'un point de ramassage"}
        else:
            resp = {"code":1,
                    "message":"Suppression des points de ramassage effectuée"}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la suppression d'un pickup."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")