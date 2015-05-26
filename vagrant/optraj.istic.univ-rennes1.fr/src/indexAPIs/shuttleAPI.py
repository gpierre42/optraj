# coding=utf8

from interfacebdd.ShuttleDAO import ShuttleDAO
from interfacebdd.CarDAO import CarDAO
from interfacebdd.WorkerDAO import WorkerDAO
from interfacebdd.PhaseDAO import PhaseDAO
from interfacebdd.PickupDAO import PickupDAO
from interfacebdd.PassengerDAO import PassengerDAO
from interfacebdd.PickupLinkDAO import PickupLinkDAO
from interfacebdd.Connexion import Connexion
from system.Shuttle import Shuttle
from system.Worker import Worker
from system.Passenger import Passenger
from system.Phase import Phase
from system.Pickup import Pickup
from system.Car import Car

from system.PickupLink import PickupLink

from flask import Blueprint, request, json
from datetime import date
import pymysql
import traceback

shuttle_api = Blueprint('shuttle_api', __name__ )

@shuttle_api.route('/shuttle/create/', methods=['POST'])
def createShuttle():
    """
    Créé une navette
    
    Args:
        request.form doit contenir :
            - idDriver : l'identifiant du conducteur 
            - idCar : l'identifiant du véhicule utilisé 
            - pickupsIds : liste des identifiant des points de passage utilisés
            - passengersIds : liste des couples (idWorker, idPickup)
    
    Returns:
        code 1, message, data : data contient l'id en base de la navette créée
        code -1, message, data : erreur lors de la création
    """
    sdao = ShuttleDAO()
    pldao = PickupLinkDAO()
    pldao.setVerboseMode(True)
    try:
        idDriver = request.form['idDriver']
        idCar = request.form['idCar']
        idPhase = request.form['idPhase']
        pickupsIds = json.loads(request.form['pickupsIds'])
        passengers = json.loads(request.form['passengersIds'])
    except Exception:
        return json.dumps({"code" : -1,
                           "message" : "Requete mal formée pour createShuttle",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    try:
        conn = Connexion().connect() 
        newShuttle = Shuttle(num=-1,
                             driver=Worker(num=idDriver),
                             car=Car(num=idCar),
                             phase=Phase(num=idPhase),
                             pickups=[Pickup(num=x) for x in pickupsIds],
                             passengers=[Passenger(num=-1,
                                                   idShuttle=-1,
                                                   worker=Worker(num=x['idWorker']),
                                                   pickup=(None if x['idPickup'] is None else Pickup(num=x['idPickup']))
                                                   ) for x in passengers])
        
        idShuttle = sdao.insert(conn, newShuttle)
        return json.dumps({"code" : 1,
                           "message" : "Navette créée",
                           "data" : idShuttle}, encoding="utf-8")
    except pymysql.err.Error:
        return json.dumps({"code" : -1,
                           "message" : "Erreur pymysql",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    
@shuttle_api.route('/shuttle/delete/byid', methods=['POST'])
def deleteShuttleById():
    """
    Supprime une navette
    
    Args:
        request.form doit contenir :
            - id : l'identifiant de la navette 
    
    Returns:
        code 1, message, data : opération réussie. data contient l'id en base de la navette créée
        code -1, message, data : erreur lors de la suppression
    """
    sdao = ShuttleDAO()
    try:
        idShuttle = request.form['id']
    except Exception:
        return json.dumps({"code" : -1,
                           "message" : "Requete mal formée pour deleteShuttleById",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    try:
        conn = Connexion().connect()
        num = sdao.deleteById(conn, idShuttle)
        return json.dumps({"code" : 1,
                           "message" : "Navette supprimée",
                           "data" : num}, encoding="utf-8")
    except pymysql.err.Error:
        return json.dumps({"code" : -1,
                           "message" : "Erreur pymysql",
                           "data" : traceback.format_exc()}, encoding="utf-8")
        
@shuttle_api.route('/shuttle/update/', methods=['POST'])
def updateShuttle():
    """
    Mise a jour d'une navette
    
    Args:
        request.form doit contenir :
            - idShuttle : l'identifiant de la navette
            - idPickups : la liste des pickups par lequel passe la navette
            - idCar : l'id du véhicule de la navette
    
    Returns:
        code 1, message, data : opération réussie. data contient l'id en base de la navette mise à jour
        code -1, message, data : erreur lors de la suppression
    """
    try:
        sDAO = ShuttleDAO()
        plDAO = PickupLinkDAO()
        pDAO = PickupDAO()
        conn = Connexion().connect()
        oldShuttle = sDAO.getById(conn, False, [], request.form['idShuttle'])
        oldShuttle.car = CarDAO().getById(conn, False, [], request.form['idCar'])
        
        # on supprime les anciens pickupLink
        for p in oldShuttle.pickups:
            Pl = plDAO.getByFilter(conn, False, [], ('numShuttle', request.form['idShuttle']), ('pickup', str(p.num)))
            plDAO.deleteById(conn, Pl.num)
        oldShuttle.pickups = []    
        
        # on ajoute les nouveau pickup à la navette
        for idP in json.loads(request.form['idPickups']):
            # insertion du nouveau pickupLink
            pickup = pDAO.getById(conn, False, [], idP)
            pl = PickupLink(num=-1, pickup=pickup, numShuttle=request.form['idShuttle'])
            idNewPl = plDAO.insert(conn, pl)
            # ajout du pickup dans la liste de la shuttle
            oldShuttle.pickups.append(pickup)
            
        # update de la navette
        idS = sDAO.update(conn, oldShuttle)
        return json.dumps({"code" : 1,
                           "message" : "Navette mise à jour",
                           "data" : idS}, encoding="utf-8")
    except pymysql.err.Error:
        return json.dumps({"code" : -1,
                           "message" : "Erreur pymysql",
                           "data" : traceback.format_exc()}, encoding="utf-8")
        

@shuttle_api.route('/shuttles/delete/', methods=['POST'])
def deleteShuttles():
    """
    supprime plusieurs navettes
    """
    try:
        sDAO = ShuttleDAO()
        conn = Connexion().connect()
        idShuttle = -1
        shuttles = json.loads(request.form['shuttles'])
        for shuttle in shuttles:
            p = PhaseDAO().getByFilter(conn, False, [], ('numSite', shuttle["idSite"]), ('numWeek', shuttle["numWeek"]), ('numYear', shuttle["numYear"]))
            setShuttles = sDAO.getAllByFilter(conn, False, [], ('phase', str(p.num)))
            for s in setShuttles:
                idShuttle = sDAO.deleteById(conn, s.num)
                if idShuttle == -1:
                    resp = {"code" : -1,
                            "message" : "Une erreur est survenue lors de la suppression des navettes."}
        try:
            resp
        except:
            resp = {"code" : 1,
                    "message" : "Suppression des navettes réussies"}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur de connexion est survenue lors de la suppression des navettes."}
    except Exception as e:
        resp = {"code":-1,
                "message":str(e)}
        raise
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")

@shuttle_api.route('/shuttle/byid/lazy/', methods=['POST'])
def shuttleById():
    """
    Accède à une navette par son id
    
    Args:
        request.form doit contenir :
            - id l'id de la shuttle en base
    
    Returns:
        code 1, data : data contient les navettes
        code -1, message : erreur 
    """
    sdao = ShuttleDAO()
    try:
        num = request.form['id']
    except Exception:
        return json.dumps({"code" : -1,
                           "message" : "Requete mal formée pour shuttleById",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    try:
        conn = Connexion().connect()
        shuttle = sdao.getById(conn, False, [], num)
        if shuttle == None:
            return json.dumps({"code" : -1,
                               "message" : "Cette navette n'existe pas",
                               "data" : traceback.format_exc()}, encoding="utf-8")
        else:
            return json.dumps({"code" : 1,
                               "message" : "OK",
                               "data" : shuttle.serial()}, encoding="utf-8")
    except pymysql.err.Error:
        return json.dumps({"code" : -1,
                           "message" : "Erreur pymysql",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    except:
        return json.dumps({"code" : -1,
                           "message" : "Erreur lors de la récupération d'une navette",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    finally:
        Connexion().disconnect(conn)


@shuttle_api.route('/shuttle/passenger/remove/', methods=['POST'])
def removePassengerFromShuttle():
    """
    enlève un passager d'une navette
    
    Args:
        request.form doit contenir :
            - idShuttle l'id de la shuttle en base
            - idWorker l'id du worker qui n'est plus passager
    
    Returns:
        code 1, data : data contient les navettes
        code -1, message : erreur 
    """
    pdao = PassengerDAO()
    try:
        idShuttle = request.form['idShuttle']
        idWorker = request.form['idWorker']
    except Exception:
        return json.dumps({"code" : -1,
                           "message" : "Requete mal formée pour removePassengerFromShuttle",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    try:
        conn = Connexion().connect()
        pdao.setVerboseMode(True)
        pdao.delete(conn, ("idShuttle",idShuttle), ("worker", idWorker))
        return json.dumps({"code" : 1,
                           "message" : "OK"}, encoding="utf-8")
    except pymysql.err.Error:
        return json.dumps({"code" : -1,
                           "message" : "Erreur pymysql",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    except:
        return json.dumps({"code" : -1,
                           "message" : "Erreur lors de la suppression d'un passager",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    finally:
        Connexion().disconnect(conn)
    
@shuttle_api.route('/shuttle/passenger/insert/', methods=['POST'])
def insertPassenger():
    """
    Ajoute un passager à une navette
    
    Args:
        request.form doit contenir :
            - idShuttle l'id de la shuttle en base
            - idWorker l'id du worker passager
            - idPickup l'id du pickup utilisé (contient null si direct au conducteur)
    
    Returns:
        code 1, data :
        code -1, message : erreur 
    """
    pdao = PassengerDAO()
    try:
        passenger = json.loads(request.form['passenger'])
        idShuttle = passenger["idShuttle"]
        idWorker = passenger["idWorker"]
        idPickup = passenger["idPickup"]
    except Exception:
        return json.dumps({"code" : -1,
                           "message" : "Requete mal formée pour insertPassenger",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    try:
        conn = Connexion().connect()
        pdao.setVerboseMode(True)
        p = Passenger(num=-1,
                      idShuttle=idShuttle,
                      worker=Worker(num=idWorker),
                      pickup=(None if passenger["idPickup"] is None else Pickup(num=passenger["idPickup"])))
        i = pdao.insert(conn, p)
        if i==-1:
            return json.dumps({"code" : -1,
                           "message" : "Erreur lors de l'ajout d'un passager",
                           "data" : traceback.format_exc()}, encoding="utf-8")
        else:
            return json.dumps({"code" : 1,
                               "message" : "OK",
                               "data":i}, encoding="utf-8")
    except pymysql.err.Error:
        return json.dumps({"code" : -1,
                           "message" : "Erreur pymysql",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    except:
        return json.dumps({"code" : -1,
                           "message" : "Erreur lors de l'ajout d'un passager",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    finally:
        Connexion().disconnect(conn)
   
@shuttle_api.route('/shuttle/passenger/update/', methods=['POST'])
def updatePassenger():
    """
    change la navette/pickup d'un passager
    
    Args:
        request.form doit contenir :
            - idWorker l'id du worker a changer
            - oldIdShuttle l'id de la shuttle actuellement utilisée par le worker
            - oldIdPickup l'id du pickup de ramassage actuellement utilisé
            - newIdShuttle l'id de la nouvelle navette
            - newIdPickup l'id du point de ramassage a utiliser
    
    Returns:
        code 1, data : data contient les navettes
        code -1, message : erreur 
    """
    pdao = PassengerDAO()
    try:
        idWorker = request.form['idWorker']
        newIdShuttle = request.form['newIdShuttle']
        newIdPickup = request.form['newIdPickup']
        oldIdShuttle = request.form['oldIdShuttle']
        oldIdPickup = request.form['oldIdPickup']
    except Exception:
        return json.dumps({"code" : -1,
                           "message" : "Requete mal formée pour updatePassenger",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    try:
        conn = Connexion().connect()
        #récupération de l'objet ciblé en base
        oldP = pdao.getByFilter(conn, True, [],
                                       ("idShuttle", oldIdShuttle),
                                        ("worker", idWorker))
        #changment des valeurs
        newP = Passenger(num=oldP.num,
                         idShuttle=newIdShuttle,
                         worker=Worker(num=idWorker),
                         pickup=Pickup(num=newIdPickup))
        pdao.update(conn, newP)
        return json.dumps({"code" : 1,
                           "message" : "OK",
                           "data":newP.num}, encoding="utf-8")
    except pymysql.err.Error:
        return json.dumps({"code" : -1,
                           "message" : "Erreur pymysql",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    except:
        return json.dumps({"code" : -1,
                           "message" : "Erreur lors de l'édition d'un passager",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    finally:
        Connexion().disconnect(conn)

@shuttle_api.route('/shuttle/driver/swap/', methods=['POST'])
def swapDriver():
    """
    échange le conducteur d'une navette parmis ses passagers
    
    Args:
        request.form doit contenir :
            - idShuttle l'id de la shuttle à modifier
            - idDriverNew l'id du nouveau driver
    
    Returns:
        code 1, data : data contient la nouvelle navette complete
        code -1, message : erreur 
    """
    sdao = ShuttleDAO()
    pdao = PassengerDAO()
    try:
        idShuttle = request.form['idShuttle']
        idDriverNew = request.form['idDriverNew']
    except Exception:
        return json.dumps({"code" : -1,
                           "message" : "Requete mal formée pour swapDriver",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    try:
        conn = Connexion().connect()
        #changement du conducteur
        shuttle = sdao.getById(conn, False, [], idShuttle)
        idOldDriver = shuttle.driver.num
        shuttle.driver = WorkerDAO().getById(conn, False, [], idDriverNew)
        sdao.update(conn, shuttle)
        #effacage de l'ancien passager
        pdao.delete(conn, ("worker", idDriverNew), ("idShuttle", idShuttle))
        #ajout du nouveau passager
        p = Passenger(num=-1,
                      idShuttle=idShuttle,
                      worker=Worker(num=idOldDriver),
                      pickup=None)
        pdao.insert(conn, p)
        shuttle = sdao.getById(conn, False, [], idShuttle)
        return json.dumps({"code" : 1,
                           "message" : "OK",
                           "data" : shuttle.serial()}, encoding="utf-8")
    except:
        return json.dumps({"code" : -1,
                           "message" : "Erreur lors de l'échange de conducteur",
                           "data" : traceback.format_exc()}, encoding="utf-8")
    finally:
        Connexion().disconnect(conn)
    


@shuttle_api.route('/shuttle/bysite/byweek/', methods=['POST'])
def shuttleBySiteByWeek():
    """
    Accède à la liste des navette d'un site pour une semaine donnée
    
    Args:
        request.form doit contenir :
            - numSite
            - numWeek
            - numYear
    
    Returns:
        code 1, data : data contient les navettes
        code -1, message : erreur 
    """
    try:
        shuttle = ShuttleDAO()
        phase = PhaseDAO()
        conn = Connexion().connect()
        s = []
        if request.method == 'POST':
            for p in phase.getAllByFilter(conn, False, [], ("numWeek", request.form['week']), ("numYear", request.form['year']), ("numSite", request.form['idSite'])):
                for i in shuttle.getAllByFilter(conn,
                                                False,
                                                [],
                                                ("phase", str(p.num))):
                    s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des navettes."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    
@shuttle_api.route('/shuttle/byweek/', methods=['POST'])
def shuttleByWeek():
    """
    Accède à la liste des navette d'une semaine donnée
    
    Args:
        request.form doit contenir :
            - numWeek
            - numYear
    
    Returns:
        code 1, data : data contient les navettes
        code -1, message : erreur 
    """
    try:
        shuttle = ShuttleDAO()
        phase = PhaseDAO()
        conn = Connexion().connect()
        s = []
        if request.method == 'POST':
            for p in phase.getAllByFilter(conn, False, [], ("numWeek", request.form['week']), ("numYear", request.form['year'])):
                for i in shuttle.getAllByFilter(conn, False, [], ("phase", str(p.num))):
                    s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des navettes."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    
@shuttle_api.route('/shuttle/byCar/', methods=['POST'])
def ShuttleByCarID():
    """
    Récupère la liste des navettes pour lesquelles un véhicule dans une liste donnée est utilisé
    
    Args:
        request.form doit contenir :
            - num : tableau des numéros de voitures qui nous intéressent
    
    Returns:
        code 1, data : data contient les navettes
        code -1, message : erreur 
    """
    try:
        conn = Connexion().connect()
        res = []
        if request.method == 'POST':
            today = date.today()
            phases = PhaseDAO().getAllByFilterExtended(conn, False, [],
                                                 ('numYear', '>=', str(today.year)),
                                                 ('numWeek', '>=', str(today.isocalendar()[1])))
            for p in phases:
                tabIdCar = json.loads(request.form['num'])
                for idCar in tabIdCar:
                    for s in ShuttleDAO().getAllByFilter(conn, False, [], ("car", str(idCar)), ("phase", str(p.num))):
                        res.append(s.serial())
        resp = {"code" : 1,
                "data" : json.dumps(res, encoding="utf-8")}
    except:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des navettes."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")