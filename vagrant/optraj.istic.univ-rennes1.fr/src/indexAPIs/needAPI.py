# coding=utf8

from interfacebdd.PhaseDAO import PhaseDAO
from interfacebdd.NeedDAO import NeedDAO
from interfacebdd.AssignmentDAO import AssignmentDAO
from interfacebdd.Connexion import Connexion

from flask import Blueprint, request, json
import pymysql

need_api = Blueprint('need_api', __name__ )

@need_api.route('/need/bysite/byweek', methods=['POST'])
def needByWeekBySite():
    """
    Récupère les besoins pour un chantier à une semaine donnée
    
    Args:
        request.form doit contenir :
            - numSite
            - numWeek
    
    Returns:
        code 1, data : data contient les need
        code -1, message : erreur 
    """
    try:
        conn = Connexion().connect()
        phase = PhaseDAO()
        need = NeedDAO()
        assign = AssignmentDAO()
        totalAff = 0

        s = []
        p = phase.getByFilter(conn, False, [], ('numSite', request.form['numSite']), ('numWeek', request.form['numWeek']))
        total = 0
        if (p is not None):
            dico = dict()
            for n in need.getAllByFilter(conn, False, [], ('numPhase', str(p.num))):
                dico = n.serial()
                total = total + n.need
    
                totalAff = 0
                dico['numSite'] = p.numSite
                dico['numWeek'] = p.numWeek
                for a in assign.getAllByFilter(conn, False, [], ('phase', str(p.num))):
                    if (a.worker.qualification.num == n.qualification.num) and (a.worker.craft.num == n.craft.num):
                        totalAff = totalAff + 1
                dico['totalAff'] = totalAff
                s.append(dico)
            dico['total'] = total

            # s.append(dico['total'])
            resp = {"code" : 1,
                    "data" : json.dumps(s, encoding="utf-8")}
        try:
            resp
        except NameError:
            resp = {"code" : 1,
                    "data" : json.dumps([], encoding="utf-8")}

    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des besoins."}
    except Exception as e:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : str(e),
                "data" : e}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")