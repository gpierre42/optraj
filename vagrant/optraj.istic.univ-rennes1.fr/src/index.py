# -*- coding:utf-8 -*-

from optimisation.pythondeap import ComputationLauncher

from flask import Flask, request
from flask import json

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


from indexAPIs.userAPI import user_api 
from indexAPIs.siteAPI import site_api 
from indexAPIs.craftAPI import craft_api 
from indexAPIs.qualificationAPI import qualification_api 
from indexAPIs.workerAPI import worker_api
from indexAPIs.assignmentAPI import assignment_api
from indexAPIs.needAPI import need_api
from indexAPIs.shuttleAPI import shuttle_api
from indexAPIs.pickupAPI import pickup_api
from indexAPIs.carAPI import car_api
from indexAPIs.unavailabilityAPI import unavailability_api
import traceback

app = Flask(__name__)
app.register_blueprint(user_api)
app.register_blueprint(site_api)
app.register_blueprint(craft_api)
app.register_blueprint(qualification_api)
app.register_blueprint(worker_api)
app.register_blueprint(assignment_api)
app.register_blueprint(need_api)
app.register_blueprint(shuttle_api)
app.register_blueprint(pickup_api)
app.register_blueprint(car_api)
app.register_blueprint(unavailability_api)

@app.route('/')
def racine():
    return "Le chemin de 'racine' est : " + request.path


optiLauncher = None  # le point d'entrée de l'algo

"""
@app.route('/optimisation/assignments/')
def assignmentsFromOpti():
    try:
        conn = Connexion().connect()
        global optiEntryPoint
        s = []
        for i in optiEntryPoint.getAssignments():
            s.append(i.serial())
        return json.dumps(s, encoding="utf-8")
    except pymysql.err.Error:
        Connexion().exception()
    finally:
        Connexion().disconnect(conn)
"""




@app.route('/optimisation/compute/', methods=['POST'])
def computeOpti():
    """
    lance l'optimisation
    """
    try:
        if request.method == 'POST':
            global optiLauncher
            optiLauncher = ComputationLauncher()
            optiLauncher.init()
            #print "fin init"
            critere = int(request.form['critere'])
            max = int(request.form['max'])
            optiLauncher.algoInst.weights = (critere, critere, max-critere)
            #optiLauncher.algoInst.mu = int(request.form['mu']) # nombre d'individu selectionnés a chaque itération
            #optiLauncher.algoInst.lambda_ = int(request.form['lambda']) # nombre de nouveaux individus à chaque itération
            #optiLauncher.algoInst.ngen = int(request.form['ngen']) # nombre d'itérations
            #print optiLauncher.algoInst.weights
            optiLauncher.start()
            resp = {"code" : 1,
                    "message" : "Calculs lancés"}
        else:
            resp = {"code" : -1,
                    "message" : "Mauvaise construction de requête"}
    except:
        resp = {"code" : -1,
                "message" : "Échec du lancement des calculs"}
    finally:
        return json.dumps(resp, encoding="utf-8")
        
        

@app.route('/optimisation/result/')
def resultOpti():
    try:
        global optiLauncher
        while optiLauncher.isAlive():
            pass
        #print optiLauncher.distance
        resp = {"code" : 1,
                "data" : json.dumps(optiLauncher.assignments, encoding="utf-8")}
    except:
        resp = {"code" : -1,
                "message" : "Échec de la récupération des résultats"}
    finally:
        return json.dumps(resp, encoding="utf-8")


@app.route('/optimisation/progress/')
def getProgress():
    global optiLauncher
    dico = dict()
    if optiLauncher is not None:
        dico["progress"] = optiLauncher.algoInst.nbCurrentGen
        dico["nbGen"] = optiLauncher.algoInst.ngen
        dico["status"] = optiLauncher.status
        return json.dumps(dico, encoding="utf-8")
    else:
        return json.dumps(dico, encoding="utf-8")

@app.route('/optimisation/distance/')
def distanceFromOpti():
    global optiLauncher
    if optiLauncher is not None:
        s = optiLauncher.distance
        optiLauncher = None
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    else:
        resp = {"code" : -1,
                "message" : "Échec de la récupération des indicateurs"}
    return json.dumps(resp, encoding="utf-8")






if __name__ == '__main__':
    app.run(debug=True)
