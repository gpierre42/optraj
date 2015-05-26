# coding=utf8
from interfacebdd.Connexion import Connexion
from interfacebdd.CraftDAO import CraftDAO
from flask import Blueprint, request, json
import pymysql

craft_api = Blueprint('craft_api', __name__ )


@craft_api.route('/craft/all/')
def allCraft():
    """
    Récupère la liste de tous les métiers
    
    Returns:
        code 1, data : data contient la liste des métiers
        code -1, message : erreur lors de la récupération
    """
    try:
        conn = Connexion().connect()
        craft = CraftDAO()
        s = []
        for i in craft.getAll(conn, False, []):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des métiers."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")