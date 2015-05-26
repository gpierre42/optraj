# coding=utf8
from system.Site import Site
from system.Position import Position
from system.Need import Need
from system.Phase import Phase
from interfacebdd.SiteDAO import SiteDAO
from interfacebdd.PhaseDAO import PhaseDAO
from interfacebdd.CraftDAO import CraftDAO
from interfacebdd.QualificationDAO import QualificationDAO
from interfacebdd.Connexion import Connexion

from datetime import date
from flask import Blueprint, request, json
import pymysql

site_api = Blueprint('site_api', __name__ )

"""
API d'accès aux chantiers
"""

@site_api.route('/site/create/', methods=['POST'])
def createSite():
    """
    Créé un nouveau chantier
    
    Args:
        request.form doit contenir :
            - latitude
            - longitude
            - address : l'adresse (chaine)
            - dateInit : chaine au format 
            - dateEnd : chaine au format
            - phases : optionnel, dictionnaire de Phase
            - name : nom du chantier
            - numSite : numéro utilisateur du chantier
            - siteMaster : nom du chef de chantier
            - siteManager : nom du conducteur de travaux
            - color : chaine au format 
    
    Returns:
        code 1, message : ajout réussi
        code -1, message : erreur lors de l'ajout
    """
    try:
        conn = Connexion().connect()
        site = SiteDAO()
        craft = CraftDAO()
        qualif = QualificationDAO()
        if request.method == 'POST':
            pos = Position(request.form['latitude'], request.form['longitude'], request.form['address'])
            dateI = date(int(request.form['dateInit'][-4:]), int(request.form['dateInit'][3:-5]), int(request.form['dateInit'][:2]))
            dateE = date(int(request.form['dateEnd'][-4:]), int(request.form['dateEnd'][3:-5]), int(request.form['dateEnd'][:2]))
            res = []
            if request.form.has_key('phases'):
                pha = json.loads(request.form['phases'])
                for ph in pha:
                    temp = Phase(numWeek=pha[ph]['numWeek'], numYear=pha[ph]['numYear'], needs=[])
                    if pha[ph].has_key('needs'):
                        t = []
                        for ne in pha[ph]['needs']:
                            c = craft.getById(conn, False, [], pha[ph]['needs'][ne]['craft']['num'])
                            q = qualif.getByFilter(conn, False, [], ('name', str(pha[ph]['needs'][ne]['qualification']['name'])))
                            t.append(Need(numPhase=temp.num, craft=c, qualification=q, need=pha[ph]['needs'][ne]['need']))
                        temp.needs = t
                        res.append(temp)

            s = Site(name=request.form['name'],
                     numSite=request.form['numSite'],
                     siteMaster=request.form['siteMaster'],
                     siteManager=request.form['siteManager'],
                     position=pos,
                     dateInit=dateI,
                     dateEnd=dateE,
                     color=request.form['color'],
                     phases=res)
            idSite = site.insert(conn, s)
            if idSite == -1:
                resp = {"code" : -1,
                        "message" : "Échec de la création du chantier"}
            else:
                resp = {"code":1,
                        "message":"Création du chantier effectuée"}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur de connexion lors de la création du chantier"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
    
    
@site_api.route('/site/delete/', methods=['POST'])
def deleteSite():
    """
    Supprime un chantier de la BDD
    
    Args:
        request.form doit contenir :
            - num : l'identifiant du chantier en BDD
            
    Returns:
        code 1, message : suppression réussie
        code -1, message : erreur lors de la suppression
    """
    try:
        site = SiteDAO()
        conn = Connexion().connect()
        if request.method == 'POST':
            idSite = site.deleteById(conn, request.form['num'])
        if idSite == -1:
            resp = {"code" : -1,
                    "message" : "Échec de la suppression du chantier"}
        else:
            resp = {"code":1,
                    "message":"Suppression du chantier effectuée"}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Erreur de connexion lors de la suppression du chantier"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")


@site_api.route('/site/update/', methods=["POST"])
def updateSite():
    """
    Édite un chantier
    
    Args:
        request.form doit contenir :
            - latitude
            - longitude
            - address : l'adresse (chaine)
            - dateInit : chaine au format 
            - dateEnd : chaine au format
            - phases : optionnel, dictionnaire de Phase
            - name : nom du chantier
            - numSite : numéro utilisateur du chantier
            - siteMaster : nom du chef de chantier
            - siteManager : nom du conducteur de travaux
            - color : chaine au format
    
    Returns:
        code 1, message : édition réussie
        code -1, message : erreur lors de l'édition
    """
    try:
        conn = Connexion().connect()
        site = SiteDAO()
        phase = PhaseDAO()
        craft = CraftDAO()
        qualif = QualificationDAO()
        if request.method == 'POST':
            s = site.getById(conn, False, [], request.form["num"])
            idPos = s.position.num
            p = Position(num=idPos, long=request.form['longitude'], lat=request.form['latitude'], address=request.form['address'])
            dateI = date(int(request.form['dateInit'][-4:]), int(request.form['dateInit'][3:-5]), int(request.form['dateInit'][:2]))
            dateE = date(int(request.form['dateEnd'][-4:]), int(request.form['dateEnd'][3:-5]), int(request.form['dateEnd'][:2]))
            res = []
            if request.form.has_key('phases'):
                pha = json.loads(request.form['phases'])
                for y in pha.keys():
                    for w in pha[y].keys():
                        if int(w) >= 0:
                            temp = phase.getById(conn, False, [], pha[y][w]['num'])
                        else :
                            temp = Phase(numSite=request.form['num'], numWeek=pha[y][w]['numWeek'], numYear=pha[y][w]['numYear'], needs=[])
                        if pha[y][w].has_key('needs'):
                            t = []
                            for ne in pha[y][w]['needs']:
                                c = craft.getById(conn, False, [], pha[y][w]['needs'][ne]['craft']['num'])
                                q = qualif.getByFilter(conn, False, [], ('name', str(pha[y][w]['needs'][ne]['qualification']['name'])))
                                if int(ne) >= 0:
                                    t.append(Need(num=pha[y][w]['needs'][ne]['num'], numPhase=temp.num, craft=c, qualification=q, need=pha[y][w]['needs'][ne]['need']))
                                else:
                                    t.append(Need(numPhase=temp.num, craft=c, qualification=q, need=pha[y][w]['needs'][ne]['need']))
                            temp.needs = t
                            res.append(temp)

            s = Site(num=request.form["num"],
                     name=request.form['name'],
                     position=p,
                     dateInit=dateI,
                     dateEnd=dateE,
                     numSite=request.form['numSite'],
                     siteManager=request.form['siteManager'],
                     siteMaster=request.form['siteMaster'],
                     color=request.form['color'],
                     phases=res)

            idSite = site.update(conn, s)
            if idSite == -1:
                resp = {"code" : -1,
                        "message" : "Une erreur est survenue lors de l'édition du chantier"}
            else:
                resp = {"code" : 1,
                        "message": "Modifications enregistrées"}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de l'édition du chantier"}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")
        

@site_api.route('/site/all/lazy/')
def allSitesLazy():
    """
    Récupère une liste de chantiers partiels
    
    Les chantier ne contiennent que les champs atomiques (noms, couleurs, dates)
    
    Returns:
        code 1, data : data contient la liste des chantiers (partiels)
        code -1, message : erreur lors de la récupération
    """
    try:
        conn = Connexion().connect()
        site = SiteDAO()
        s = []
        for i in site.getAll(conn, True, []):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des chantiers."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")


@site_api.route('/site/all/lazyPosition/')
def allSitesLazyPosition():
    """
    Récupère une liste de chantiers partiels (avec position)
    
    Les chantier ne contiennent que les champs atomiques (noms, couleurs, dates) ainsi que la position
    
    Returns:
        code 1, data : data contient la liste des chantiers (partiels)
        code -1, message : erreur lors de la récupération
    """
    try:
        conn = Connexion().connect()
        site = SiteDAO()
        s = []
        for i in site.getAll(conn, True, [SiteDAO.JOIN_POSITION]):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des chantiers."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")

@site_api.route('/site/all/')
def allSites():
    """
    Récupère une liste de chantiers partiels (avec position)
    
    Les chantier ne contiennent que les champs atomiques (noms, couleurs, dates) ainsi que la position
    
    Returns:
        code 1, data : data contient la liste des chantiers (partiels)
        code -1, message : erreur lors de la récupération
    """
    try:
        conn = Connexion().connect()
        site = SiteDAO()
        s = []
        for i in site.getAll(conn, False, []):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des chantiers."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")


@site_api.route('/site/current/')
def currentSite():
    """
    Récupère la liste des chantiers partiels actifs actuellement
    
    Les chantier ne contiennent que les champs atomiques (noms, couleurs, dates) ainsi que la position.
    La liste ne contient que les chantiers actifs à la date d'aujourd'hui.
    
    Returns:
        code 1, data : data contient la liste des chantiers actifs (partiels)
        code -1, message : erreur lors de la récupération
    """
    try:
        site = SiteDAO()
        conn = Connexion().connect()
        s = []
        for i in site.getAllByFilterExtended(conn, True, [site.JOIN_POSITION], ('dateInit', '<', 'NOW()'), ('dateEnd', '>', 'NOW()')):
            s.append(i.serial())
        resp = {"code" : 1,
                "data" : json.dumps(s, encoding="utf-8")}
    except pymysql.err.Error:
        Connexion().exception()
        resp = {"code" : -1,
                "message" : "Une erreur est survenue lors de la récupération de la liste des chantiers."}
    finally:
        Connexion().disconnect(conn)
        return json.dumps(resp, encoding="utf-8")


@site_api.route('/site/byid/', methods=["POST"])
def siteById():
    """
    Accède à un chantier par son identifiant
    
    Args:
        request.form doit contenir :
            - num : l'identifiant du chantier en BDD
            
    Returns:
        code 1, data : data contient le chantier si on le trouve
        code -1, message : erreur lors de la récupération
    """
    try:
        site = SiteDAO()
        conn = Connexion().connect()
        s = site.getById(conn, False, [], request.form['num']).serial()
        if(s == None):
            resp = {"code" : -1,
                    "message" : "Le site d'id {} n'as pas été trouvé".format(request.form['num'])}
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


