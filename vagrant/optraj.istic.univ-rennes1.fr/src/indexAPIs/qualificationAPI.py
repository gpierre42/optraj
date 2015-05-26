# coding=utf8
from interfacebdd.Connexion import Connexion
from interfacebdd.QualificationDAO import QualificationDAO
from flask import Blueprint, request, json
import pymysql

qualification_api = Blueprint('qualification_api', __name__ )

@qualification_api.route('/qualification/all/')
def allQualifications():
    """
    Récupère la liste de toutes les qualifications
    
    Returns:
        code 1, data : data contient la liste des qualifications
        code -1, message : erreur lors de la récupération
    """
    try:
        qualification = QualificationDAO()
        conn = Connexion().connect()
        s = []
        for i in qualification.getAll(conn, False, []):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des qualifications."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")