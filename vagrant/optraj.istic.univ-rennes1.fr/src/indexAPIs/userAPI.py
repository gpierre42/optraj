# coding=utf8
from system.Consumer import Consumer
from interfacebdd.ConsumerDAO import ConsumerDAO
from interfacebdd.Connexion import Connexion
from flask import Blueprint, request, json

user_api = Blueprint('user_api', __name__ )
'''
-------------- LOGIN --------------
'''

@user_api.route('/user/connect/', methods=['POST'])
def connectUser():
    """
    Connecte un utilisateur
    
    Args:
        request.form doit contenir :
            - login : identifiant unique de connexion
            - pwd : le mot de passe crypté en MD5
    
    Returns:
        code 1, message, data : connexion reussie, data contient le niveau d'authentification
        code -1, message : erreur de connexion
    """
    try:
        conn = Connexion().connect()
        consumer = ConsumerDAO()
        if request.method == 'POST':
            login = request.form["login"]
            pwd = request.form["pwd"]
            consFilt = consumer.getByFilter(conn, False, [], ('login', login), ('pwd', pwd))
            if consFilt != None:
                resp = {"code" : 1,
                        "message" : "Utilisateur authentifié",
                        "data" : consFilt.lvl}
            else:
                resp = {"code" : -1,
                        "message" : "L'authentification à échoué, vérifiez vos identifiants"}
    except:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur inconnue lors de l'authentification"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
        

@user_api.route('/user/name/', methods=['POST'])
def userName():
    """
    Récupère le nom et prénom d'un utilisateur
    
    Args:
        request.form doit contenir :
            - login : identifiant unique de connexion
    
    Returns:
        code 1, data : utilisateur trouvé, data contient l'utilisateur avec le nom et prénom
        code -1, message : erreur de connexion
    """
    try:
        conn = Connexion().connect()
        consumer = ConsumerDAO()
        if request.method == 'POST':
            login = request.form["login"]
            consFilt = consumer.getByFilter(conn, False, [], ('login', login))
            if consFilt != None:
                cons = Consumer(firstname=consFilt.firstname, name=consFilt.name)
                resp = {"code" : 1,
                        "data" : json.dumps(cons.serial(), encoding="utf-8")}
            else:
                resp = {"code" : -1,
                        "message" : "Utilisateur inconnu"}
    except:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur inconnue lors de la récupération du nom utilisateur"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")

@user_api.route('/user/create/', methods=['POST'])
def createUser():
    """
    Créé un nouvel utilisateur
    
    Args:
        request.form doit contenir :
            - lvl : niveau d'utilisation (1, 2 ou 3)
            - login : identifiant unique de connexion
            - md5pwd : le mot de passe crypté
            - name : nom de famille
            - firstname : prénom
    
    Returns:
        code 1, message : ajout réussi
        code -1, message : erreur lors de l'ajout
    """
    try:
        conn = Connexion().connect()
        consumer = ConsumerDAO()
        if request.method == 'POST':
            c = Consumer(lvl=request.form['lvl'], login=request.form['login'], pwd=request.form['md5pwd'], name=request.form['name'], firstname=request.form['firstname'])
            idConsumer = consumer.insert(conn, c)
        if idConsumer == -1:
            resp = {"code" : -1, "message" : "Une erreur est survenue lors de l'insertion d'un nouvel utilisateur"}
        else:
            resp = {"code" : 1, "message": "Nouvel utilisateur créé"}
    except:
        Connexion().exception()
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")


@user_api.route('/user/all/')
def allUsers():
    """
    Récupère la liste de tous les utilisateurs
    
    Returns:
        code 1, data : la liste de tous les utilisateurs dans un dictionnaire JSON
        code -1, message : erreur lors de la récupération
    """
    try:
        consumer = ConsumerDAO()
        conn = Connexion().connect()
        s = []
        for i in consumer.getAll(conn, False, []):
            s.append(i.serial())
        resp = {"code" : 1, "data" : json.dumps(s, encoding="utf-8")}
    except:
        Connexion().exception()
        resp = {"code" : -1, "message" : "Une erreur est survenue lors de la récupération de la liste des utilisateurs."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")

@user_api.route('/user/delete/', methods=['POST'])
def deleteUser():
    """
    Supprime un utilisateur
    
    Args:
        request.form doit contenir :
            - num : id de l'utilisateur
    
    Returns:
        code 1, message : suppression réussie
        code -1, message : erreur lors de la suppression
    """
    try:
        consumer = ConsumerDAO()
        conn = Connexion().connect()
        if request.method == 'POST':
            idConsumer = consumer.deleteById(conn, request.form['num'])
        if idConsumer == -1:
            resp = {"code" : -1, "message" : "Une erreur est survenue lors de l'édition de l'utilisateur"}
        else:
            resp = {"code" : 1, "message": "Modifications effectuées"}
    except:
        Connexion().exception()
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")

@user_api.route('/user/update/', methods=['POST'])
def updateUser():
    """
    Édite un utilisateur
    
    Args:
        request.form doit contenir :
            - num : id de l'utilisateur
            - lvl : niveau d'utilisation (1, 2 ou 3)
            - login : identifiant de connexion
            - md5pwd : le mot de passe crypté
            - name : nom de famille
            - firstname : prénom
    
    Returns:
        code 1, message : édition réussie
        code -1, message : erreur lors de l'édition
    """
    try:
        consumer = ConsumerDAO()
        conn = Connexion().connect()
        if request.method == 'POST':
            c = consumer.getById(conn, False, [], request.form["num"])
            c = Consumer(num=request.form["num"],
                         name=request.form['name'],
                         firstname=request.form['firstname'],
                         login=request.form['login'],
                         pwd=request.form['md5pwd'],
                         lvl=request.form['lvl'])
            idConsumer = consumer.update(conn, c)
        if idConsumer == -1:
            resp = {"code" : -1, "message" : "Une erreur est survenue lors de l'édition de l'utilisateur"}
        else:
            resp = {"code" : 1, "message": "Modifications effectuées"}
    except:
        Connexion().exception()
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
