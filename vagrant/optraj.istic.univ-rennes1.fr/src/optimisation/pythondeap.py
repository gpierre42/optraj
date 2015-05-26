#coding=utf8

from deap import algorithms
from deap import creator
from deap import base
from deap import tools
from operator import itemgetter, attrgetter
from datetime import date
import random
import copy
import time
import math
import threading
#import dotTransform
from interfacebdd.WorkerDAO import WorkerDAO
from interfacebdd.AssignmentDAO import AssignmentDAO
from interfacebdd.SiteDAO import SiteDAO
from interfacebdd.UnavailabilityDAO import UnavailabilityDAO
from interfacebdd.PhaseDAO import PhaseDAO
from system.System import System
from system.Unavailability import Unavailability
from interfacebdd.Connexion import Connexion
from multiprocessing.pool import worker
#from dotTransform import workerSorted

class algo(object):
    '''
    Classe algo qui définie toutes les fonctions utiles au déroulement de l'algorithme.

    fonctionnement d'un algotithme génétique:
    @image html genetique.png

    Attributs:
    - system : le systeme utilisé dans l'aglorithme (System.System)
    - weights : les poids des différents critères d'évaluation, un triplet de float (distance des navettes, distance des ouvriers aux navettes, nombre de changement d'affectations)
    - cxpb : probalitité qu'un croissement entre deux individus se fasse durant une passe de l'algo (float)
    - mutpb : probalité qu'un individu mute durant une passe de l'algo (float)
    - mu : nombre d'individus sélectionnés à chaque itération (int)
    - lambda : nombre de nouveaux individus créés à chaque itération (int)
    - ngen : nombre d'itérations de l'algorithme (int)
    - randpb : pourcentage d'éléatoire dans la création d'un nouvel individu
    - distanceMax : la distance maximale en mètres du système entre un ouvrier et un chantier
    - distanceMaxPassenger : la distance maximale, en mètre, au delà de laquelle on considère qu'un ouvrier est trop loins du trajet pour être dans la navette
    - must : garde trace des ouvriers déjà affectés et qui doivent le rester
    - issue : stockent les information sur les problèmes rencontrés durant les calculs (par ex. pas assez d'ouvrier par rapport à la demande)
    - nbCurrentGen : le numéro de l'itération actuelle
    '''

    def __init__(self):
        '''
        Constructeur d'une instance d'algo

        Initialise tous les attributs et récupère le système depuis la base de donnée
        '''
        #récupération du système (workers, sites et phases)
        conn = Connexion().connect()
        today = date.today()
        phases = PhaseDAO().getAllByFilterExtended(conn, False, [],
                                                 ('numYear', '=', str(today.year)),
                                                 ('numWeek', '>=', str(today.isocalendar()[1])))
        phases = phases | PhaseDAO().getAllByFilterExtended(conn, False, [],
                                                 ('numYear', '>', str(today.year)))
        self.system = System(SiteDAO().getAll(conn, False, []), WorkerDAO().getAll(conn, False, []), phases)
        unavail = UnavailabilityDAO().getAllByFilterExtended(conn, False, [], ('numWeek', '>=', today.isocalendar()[1]), ('numYear', '=', today.year))
        unavail = unavail | UnavailabilityDAO().getAllByFilterExtended(conn, False, [], ('numYear', '>', today.year))

        self.system.workerSorted = self.lookingForWorkers()

        #définition des valeurs utilisées par l'algorithme
        self.weights = (5,5,5) #poids distanceshuttle, distancePassengers, nbChangements
        self.cxpb = 0.7 # probabilité de croisement
        self.mutpb=0.3 # probabilité de mutation
        self.mu = 100 # nombre d'individu selectionnés a chaque itération
        self.lambda_ = 150 # nombre de nouveaux individus à chaque itération
        self.ngen = 20 # nombre d'itérations
        self.randpb = 0 #pourcentage de random d'un individu
        self.distanceMax = self.distanceMaxMoyenne() #Distance max entre un ouvrier et un chantier
        self.distanceMaxPassenger = 15000 #Distance max qu'un passager peut faire pour se rendre sur une navette (en mètres)

        #définition du must (les ouvriers déjà affectés et qui doivent le rester)
        self.must = dict()
        self.issue = {"disponibility": set([])}
        self.nbCurrentGen = 0
        assigns = AssignmentDAO().getAll(conn, False, [])
        for a in assigns:
            p = a.phase
            # on ne prend que les phases corespondant aux 17 semaines du tableau d'opti
            if (p.numWeek >= today.isocalendar()[1] and p.numYear == today.year) or p.numYear > today.year:
                if p.numYear not in self.must.keys():
                    self.must[p.numYear] = dict()
                resNumYear = self.must[p.numYear]
                if p.numWeek not in resNumYear.keys():
                    resNumYear[p.numWeek] = dict()
                    resNumYear[p.numWeek]["availablesWorkers"] = copy.deepcopy(self.system.workerSorted)
                    resNumYear[p.numWeek]["assigns"] = dict()
                assign = resNumYear[p.numWeek]["assigns"]
                available = resNumYear[p.numWeek]["availablesWorkers"]
                if p.numSite not in assign.keys():
                    assign[p.numSite] = set()
                assign[p.numSite].add(a.worker.num)
                available[a.worker.craft.num][a.worker.qualification.num] = available[a.worker.craft.num][a.worker.qualification.num] - set([a.worker.num])
                #dotTransform.individual(self.must, "must2.dot")
        
        self.unavailabilities = dict()
        for u in unavail:
            if u.numYear not in self.unavailabilities.keys():
                self.unavailabilities[u.numYear] = dict()
            if u.numWeek not in self.unavailabilities[u.numYear].keys():
                self.unavailabilities[u.numYear][u.numWeek] = set()
            self.unavailabilities[u.numYear][u.numWeek].add(u.idWorker)
        #if __name__ == '__main__':
            #dotTransform.unavailabilities(self.unavailabilities, "unavailabilities.dot")
            #dotTransform.workerSorted(self.system.workerSorted, "workerSorted.dot")
            

    def createInd(self, individual):
        '''
        Fonction qui permet de créer un individu valide pour l'algorithme

        forme d'un individu :
        @image html individu.png

        Args:
            individual: la classe de l'objet retourné. Un creator.Individual

        Returns:
            un Individu de la classe individual passée en paramètre.
        '''
        res = individual(copy.deepcopy(self.must))
        for p in sorted(self.system.phases, key=attrgetter('numSite')):
            # initialisation des dictionnaires s'il n'existent pas
            if p.numYear not in res.keys():
                res[p.numYear] = dict()
            resNumYear = res[p.numYear]
            if p.numWeek not in resNumYear.keys():
                resNumYear[p.numWeek] = dict()
                resNumYear[p.numWeek]["availablesWorkers"] = copy.deepcopy(self.system.workerSorted)
                resNumYear[p.numWeek]["assigns"] = dict()
            resNumWeek = resNumYear[p.numWeek]
            
            #on retire les ouvriers en congés
            if p.numYear in self.unavailabilities.keys():
                if p.numWeek in self.unavailabilities[p.numYear].keys():
                    try:
                        for craft in res[p.numYear][p.numWeek]["availablesWorkers"].keys():
                            for qualif in res[p.numYear][p.numWeek]["availablesWorkers"][craft].keys():
                                res[p.numYear][p.numWeek]["availablesWorkers"][craft][qualif] = \
                                    res[p.numYear][p.numWeek]["availablesWorkers"][craft][qualif] - \
                                    self.unavailabilities[p.numYear][p.numWeek]                                    
                    except KeyError:
                        pass #indisponibilités défine sur une semaine sans phase, pas d'incidence pour l'algo


            #remplissage avec des affectations aléatoire
            for n in p.needs:
                workerOfCurrentCraftQualif = set([])
                workerSelected = set()
                try:
                    workerOfCurrentCraftQualif = resNumWeek["availablesWorkers"][n.craft.num][n.qualification.num]
                    nbWorkerToSelect = n.need - len(self.setWorkerInMustCraftQualif(p.numYear, p.numWeek, p.numSite, n.craft.num, n.qualification.num))
                    # selection des ouvriers du plus près au plus loin du chantier
                    sortedWorkerOfCurrentCraftQualif = sorted(self.constructList(self.system.getSiteById(p.numSite), \
                                                                                  list(workerOfCurrentCraftQualif)), \
                                                              key=itemgetter(1))
                    for _ in range(nbWorkerToSelect):
                        randTemp = random.randint(0, 100)
                        if randTemp >= self.randpb:
                            workerSelected.add(sortedWorkerOfCurrentCraftQualif.pop(0)[0].num)
                        else:
                            i = random.randint(0, len(sortedWorkerOfCurrentCraftQualif)-1)
                            workerSelected.add(sortedWorkerOfCurrentCraftQualif.pop(i)[0].num)
                except (ValueError, KeyError, IndexError):
                    self.issue["disponibility"].add(n.num)
                    #print "Pas assez de {} de qualification {}".format(n.craft.name, n.qualification.name)
                #MAJ de l'enemble des ouvriers disponibles
                resNumWeek["availablesWorkers"][n.craft.num][n.qualification.num] = workerOfCurrentCraftQualif - workerSelected
                #ajout des ouvriers séléctionnés au bon endroit
                if p.numSite not in resNumWeek["assigns"].keys():
                    resNumWeek["assigns"][p.numSite] = workerSelected
                else:
                    resNumWeek["assigns"][p.numSite] = resNumWeek["assigns"][p.numSite] | workerSelected
                
        self.randpb = math.floor(self.randpb + 100/self.mu)
        return res

    def setWorkerInMust(self, year, week, site):
        '''
        Renvois l'ensemble des ouvriers devant impérativement être affecté à un site pour une date donnée

        Args:
            year l'année (int)
            week le numéro de semaine (int)
            site int le numéro du chantier (int)

        Returns:
            l'ensemble de tous les ouvriers devant être affectés au site pour cette semaine (set(Worker.num))
        '''
        res = set()
        if year in self.must.keys() and \
            week in self.must[year].keys() and \
            site in self.must[year][week]["assigns"].keys():
                res = self.must[year][week]["assigns"][site]
        return res

    def setWorkerInMustCraftQualif(self, year, week, site, craft, qualif):
        '''
        Renvois l'ensemble des ouvriers devant impérativement être affecté à un site pour une date donnée et ayant un certain metier/qualification

        Args:
            year l'année (int)
            week le numéro de semaine (int)
            site le numéro du chantier (int)

        Returns:
            l'ensemble des ouvriers du bon craft/qualif devant être affectés au site pour cette semaine (set(Worker.num))
        '''
        res = set()
        if year in self.must.keys() and \
            week in self.must[year].keys() and \
            site in self.must[year][week]["assigns"].keys():
                res = self.must[year][week]["assigns"][site] & self.system.workerSorted[craft][qualif]
        return res

    def TransformIndividualIntoAssignments(self, individual):
        '''
        transforme un individu en un set(Assignments)

        L'individu n'est pas changé par l'opération

        Args:
            individual l'individu en question

        Return
            toutes les affectations réprésentées par l'individu dans un set(Assignments)
        '''
        from system.Assignment import Assignment
        phasesSorted = self.system.allPhasesSorted()
        res = set()
        for yearK in individual.keys():
            for weekK in individual[yearK].keys():
                for siteK in individual[yearK][weekK]["assigns"].keys():
                    for workerNum in individual[yearK][weekK]["assigns"][siteK]:
                        res.add(Assignment(worker=self.system.getWorkerById(workerNum),
                                           phase=phasesSorted[yearK][weekK][siteK]))
        return res


    def lookingForWorkers(self, buildDotFile=False):
        '''
        Récupère l'ensemble des workers de la base et les classe par métier puis par qualif

        Si buildDotFile vaut True, on construit également une représentation dotty des ouvriers triés

        Args:
            buildDotFile: booleen definissant si on doit contruire un .dot du dictionaire retourné

        Returns:
            dict(craft number, dict(qualif number, set(worker number))). Tous les éléments sont des ints
        '''
        workers = self.system.workers
        workerSorted = dict()

        for w in workers:
            if w.craft.num not in workerSorted.keys():
                workerSorted[w.craft.num] = dict()
            wCraft = workerSorted[w.craft.num]
            if w.qualification.num not in wCraft.keys():
                wCraft[w.qualification.num] = set()
            wCraft[w.qualification.num].add(w.num)

        #if(buildDotFile):
            #dotTransform.workerSorted(workerSorted)
        return workerSorted

    def constructList(self, site, workers):
        '''
        Trie un ensemble d'ouvriers en liste rangée du plus près au plus loin d'un chantier

        Args:
            site le numéro de chantier référence (int)
            workers l'ensemble des numéros ouvriers à trier (set(int))

        Returns:
            workers sous forme de liste triée du plus proche de site au plus loin.
        '''
        res = []
        for numW in workers:
            worker = self.system.getWorkerById(numW)
            #print numW, worker
            distance = site.position.calcDistance(worker.position)
            res.append((worker, distance))
        return res

    def evaluate(self, individual):
        '''
        Évalue un individu

        A cause la la facon dont sont comparés les tuples par DEAP, seul le premier score du tuple retourné représente vraiment le score de l'individu
        les autres valeurs du tuples sont gardées pour ne pas perdre l'information mais sont déjà prises en compte dans le score

        Args:
            individual l'individu à évaluer

        Returns:
            un tuple de float donnant les scores de l'individu. Seul le premier élément représente le véritable score
        '''
        nbDriverTot = 1
        nbPassengerTot = 1
        distanceShuttle = 1
        distancePassenger = 1
        for year in individual:
            #évaluation des distances
            for week in individual[year]:
                for site in individual[year][week]["assigns"]:
                    curSite = self.system.getSiteById(site)
                    if individual[year][week]["assigns"][site]:
                        listDistance = self.constructList(curSite, individual[year][week]["assigns"][site])
                        for (idWorker, dist) in listDistance:
                            distToSite = dist
                            if distToSite <= self.distanceMaxPassenger:
                                distancePassenger += distToSite
                                listDistance.remove((idWorker, dist))
                            else:
                                break
                        #print "listDistance", listDistance
                        sortedWorker = sorted(listDistance, key=itemgetter(1), reverse=True)
                        #print "listSorted", sortedWorker
                        for driver in sortedWorker:
                            nbDriverTot += 1
                            distanceShuttle += driver[1]
                            sortedWorker.remove(driver)
                            nbPassenger = 0
                            for passenger in sortedWorker:
                                routeInfo = passenger[0].position.routeInfo(driver[0].position, curSite.position, self.distanceMaxPassenger)
                                if routeInfo[0]:
                                    nbPassengerTot += 1
                                    distancePassenger += routeInfo[1]
                                    nbPassenger += 1
                                    sortedWorker.remove(passenger)
                                    if nbPassenger % 5 == 0:
                                        distanceShuttle += driver[1]
        #évaluation des changements d'affectations
        lastAssigns = None
        nbChanges = 0.0 #le nombre de changment d'affectations
        for year in individual:
            for week in individual[year]:
                if lastAssigns == None:
                    lastAssigns = individual[year][week]["assigns"]
                else:
                    for site in lastAssigns:
                        try:
                            nbChanges += len(lastAssigns[site] - individual[year][week]["assigns"][site])
                        except KeyError:
                            pass
                    lastAssigns = individual[year][week]["assigns"]
        '''
        print ((distanceShuttle / (self.distanceMax*nbDriverTot)) * self.weights[0])
        print ((distancePassenger / (self.distanceMaxPassenger*nbPassengerTot)) * self.weights[1])
        print nbChanges, ((nbChanges / len(self.system.workers)) * self.weights[2])
        '''
        return ((distanceShuttle / (self.distanceMax*nbDriverTot)) * self.weights[0]) + \
                ((distancePassenger / (self.distanceMaxPassenger*nbPassengerTot)) * self.weights[1]) + \
                ((nbChanges / len(self.system.workers)) * self.weights[2]),#, distanceShuttle, distancePassenger, nbChanges
        #return nbChanges,

    def evaluate2(self, individual):
        '''
        Évalue un individu

        A cause la la facon dont sont comparés les tuples par DEAP, seul le premier score du tuple retourné représente vraiment le score de l'individu
        les autres valeurs du tuples sont gardées pour ne pas perdre l'information mais sont déjà prises en compte dans le score

        Args:
            individual l'individu à évaluer

        Returns:
            un tuple de float donnant les scores de l'individu. Seul le premier élément représente le véritable score
        '''
        nbDriverTot = 1
        nbPassengerTot = 1
        distanceShuttle = 1
        distancePassenger = 1
        for year in individual:
            #évaluation des distances
            for week in individual[year]:
                for site in individual[year][week]["assigns"]:
                    curSite = self.system.getSiteById(site)
                    if individual[year][week]["assigns"][site]:
                        listDistance = self.constructList(curSite, individual[year][week]["assigns"][site])
                        #print "listDistance", listDistance
                        sortedWorker = sorted(listDistance, key=itemgetter(1), reverse=True)
                        #print "listSorted", sortedWorker
                        for driver in sortedWorker:
                            nbDriverTot += 1
                            distanceShuttle += driver[1]
                            sortedWorker.remove(driver)
                            nbPassenger = 0
                            for passenger in sortedWorker:
                                routeInfo = passenger[0].position.routeInfo(driver[0].position, curSite.position, self.distanceMaxPassenger)
                                if routeInfo[0]:
                                    nbPassengerTot += 1
                                    distancePassenger += routeInfo[1]
                                    nbPassenger += 1
                                    sortedWorker.remove(passenger)
                                    if nbPassenger % 5 == 0:
                                        distanceShuttle += driver[1]
        #évaluation des changements d'affectations
        lastAssigns = None
        nbChanges = 0.0 #le nombre de changment d'affectations
        for year in individual:
            for week in individual[year]:
                if lastAssigns == None:
                    lastAssigns = individual[year][week]["assigns"]
                else:
                    for site in lastAssigns:
                        try:
                            nbChanges += len(lastAssigns[site] - individual[year][week]["assigns"][site])
                        except KeyError:
                            pass
                    lastAssigns = individual[year][week]["assigns"]
        return distanceShuttle, distancePassenger, nbChanges

    def mutate(self, individual):
        '''
        Fonction de mutation d'un individu.

        Une mutation consite à échanger aléatoirement au sein d'une semaines des affectations d'ouvrier.
        On n'échange que des ouvriers de même métier et qualification.
        L'échange est possible aussi bien entre 2 chantiers que entre un chantier et la liste des ouvriers non affectés.

        Args:
            individual: l'individu qui doit être muté

        Returns:
            un tuple de l'individu passé en paramètre

        Examples:
            @image html mutation.png
        '''
        for year in individual:
            for week in individual[year]:
                assign = individual[year][week]["assigns"]
                #on retire des ouvriers aléatoirement de la liste des personnes affectées
                for site in assign:
                    mustHave = self.setWorkerInMust(year, week, site)
                    #rand = random.randint(0, len(assign[site]))
                    #workerRemove = set(random.sample(assign[site], rand)) - mustHave
                    workerRemove = assign[site] - mustHave # pour ne pas retirer des affectations obligatoires
                    individual[year][week]["assigns"][site] -= workerRemove #retrait des affectés
                    for workerId in workerRemove:
                        worker = self.system.getWorkerById(workerId)
                        individual[year][week]["availablesWorkers"][worker.craft.num][worker.qualification.num].add(workerId) #rajout dansles disponibilités

                #une fois l'étape de retrait effectuée, on reremplit les needs non satisfaits
                for site in assign:
                    p = self.system.getPhaseBySiteAndWeek(site, week, year) #récupération de la phase de la semaine courante
                    for n in p.needs:
                        nbWorkerToSelect = 0
                        workerOfCurrentCraftQualif = set([])
                        try:
                            workerOfCurrentCraftQualif = individual[year][week]["availablesWorkers"][n.craft.num][n.qualification.num]
                            nbWorkerToSelect = n.need - len(self.setWorkerInMustCraftQualif(p.numYear, p.numWeek, p.numSite, n.craft.num, n.qualification.num))
                            workerSelected = set(random.sample(workerOfCurrentCraftQualif, nbWorkerToSelect))

                        except (ValueError, KeyError):
                            self.issue["disponibility"].add(n.num)
                            #print "Pas assez de {} de qualification {}".format(n.craft.name, n.qualification.name)
                            '''
                            while nbWorkerToSelect > len(workerOfCurrentCraftQualif):
                                nbWorkerToSelect -= 1
                             '''
                            nbWorkerToSelect = len(workerOfCurrentCraftQualif)
                            workerSelected = set(random.sample(workerOfCurrentCraftQualif, nbWorkerToSelect))
                        individual[year][week]["availablesWorkers"][n.craft.num][n.qualification.num] = workerOfCurrentCraftQualif - workerSelected
                        if p.numSite not in individual[year][week]["assigns"].keys():
                            individual[year][week]["assigns"][p.numSite] = workerSelected
                        else:
                            individual[year][week]["assigns"][p.numSite] = individual[year][week]["assigns"][p.numSite] | workerSelected
        del individual.fitness.values #effacage des valeurs de fitness (inutile?)
        return individual,

    def mate(self, ind1, ind2):
        '''
        Fontion de croisement entre deux individus en un point.

        le croisement se fait en un point.

        Args:
            ind1 le premier individu présent dans le croisement (creator.Individual)
            ind2 le deuxieme individu présent dans le croisement (creator.Individual)

        Returns:
            un tuple des deux individus croisés
        '''
        for year in ind1:
            rand = random.randint(0, math.floor(len(ind1[year]) * self.cxpb / len(ind1)))
            for week in ind1[year]:
                while (rand > 0):
                    temp = ind1[year][week]
                    ind1[year][week] = ind2[year][week]
                    ind2[year][week] = temp
                    rand -= 1
        return ind1, ind2

    def crossMultiPoint(self, ind1, ind2):
        '''
        Fontion de croisement entre deux individus en multi points

        pour chaque semaine, on choisit aléatoirement les affectations de ind1 ou de ind2 à 50%

        Args:
            ind1 : le premier individu présent dans le croisement (creator.Individual)
            ind2 : le deuxieme individu présent dans le croisement (creator.Individual)

        Returns:
            un tuple des deux individus croisés

        Examples:
            @image html croisement.png
        '''
        for year in ind1:
            #rand = random.randint(0, math.floor(len(ind1[year]) * self.cxpb / len(ind1)))
            for week in ind1[year]:
                tirage = random.randint(0, 1)
                if tirage == 1: # on hérite du parent 2 pour l'enfant 1
                    temp = ind1[year][week]
                    ind1[year][week] = ind2[year][week]
                    ind2[year][week] = temp
                else: # on hérite du parent 1 pour l'enfant 1 -> pas de mod
                    pass
        del ind1.fitness.values
        del ind2.fitness.values
        return ind1, ind2

    def selCustom(self, individuals, k):
        '''
        Opérateur de selection de K individus dans une population

        k/2 meilleurs individus sont selectionnés en premier et le reste aléatoirement

        Args:
            individuals : une liste d'individu où ce fait la selection (list(creator.Individual))
            k: Le nombre d'individus à selectionner. (int)

        Returns
            La liste contenant les k/2 meilleurs individus et k/2 random autres individus. (list(creator.Individual))
        '''
        selBest = sorted(individuals, key=attrgetter("fitness"), reverse=True)[:k-k/2]
        del individuals[:k-k/2]
        return selBest+random.sample(individuals, (k/2))

    def equals(self, ind1, ind2):
        '''
        Fonction definissant l'égalité entre deux individus

        Args:
            ind1: individu à tester
            ind2: individu à tester

        Returns:
            un booléen représentant l'égalité entre les deux individus. Ici, deux individus sont égaux
            si leurs valeurs de fitness sont égales
        '''
        for i in range(len(ind1.fitness.values)):
            if ind1.fitness.values[i] != ind2.fitness.values[i]:
                return False
        return True

    def distanceMaxMoyenne(self):
        '''
        Fonction retournant la distance maximale moyenne séparant un ouvrier d'un site

        Returns:
            la distance maximale moyenne
        '''
        distance= 0
        i = 0
        for w in self.system.workers:
            for s in self.system.sites:
                i += 1
                distance += w.position.calcDistance(s.position)
        return distance/i

    def max(self, pop):
        '''
        Évaluation du maximum dans une population

        Args:
            pop: la population à évaluer

        Returns:
            le score de l'individu dont l'évaluation est la plus haute dans pop
        '''
        maxi = 0
        for p in pop:
            dist = self.evaluate(p)
            if dist > maxi:
                maxi = dist
        return maxi

    def min(self, pop):
        '''
        Évaluation du minimum dans une population

        Args:
            pop: la population à évaluer

        Returns:
            le score de l'individu dont l'évaluation est la plus basse dans pop
        '''
        mini = self.evaluate(pop[0])
        for p in pop:
            dist = self.evaluate(p)
            if dist < mini:
                mini = dist
        return mini

    def nbGen(self, pop):
        '''
        Évaluation du nombre de génération déjà effectuées

        Args:
            pop : la population à évaluer

        Returns:
            Le nombre de génération déjà effectuées dans l'algo
        '''
        self.nbCurrentGen += 1
        return self.nbCurrentGen

    def main(self):
        '''
        Fonction principale de l'optimisation

        enregistre les fonctions et types définis précédemment dans la toolbox et lance les calculs

        Returns:
            le hall of fame des meilleurs individus
        '''
        creator.create("Fitness", base.Fitness, weights=(-1,))
        creator.create("Individual", dict, fitness=creator.Fitness)

        toolbox = base.Toolbox()
        toolbox.register("individual", self.createInd, creator.Individual)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("evaluate", self.evaluate)
        toolbox.register("mutate", self.mutate)
        toolbox.register("select", self.selCustom)
        toolbox.register("clone", copy.deepcopy)
        toolbox.register("mate", self.crossMultiPoint)

        stats = tools.Statistics()
        stats.register("max", self.max)
        stats.register("min", self.min)
        stats.register("nbCurrentGen", self.nbGen)
        hof = tools.HallOfFame(10, similar=self.equals)
        pop = toolbox.population(n=self.mu)
        algorithms.eaMuPlusLambda(pop, toolbox, mu=self.mu, lambda_=self.lambda_, cxpb=self.cxpb, mutpb=self.mutpb, ngen=self.ngen, halloffame=hof, stats=stats)
        #print "fini"
        return hof

class ComputationLauncher (threading.Thread):
    '''
    Classe de lancement des calculs

    Cette classe est utilisée pour avoir un point d'appel depuis l'interface afin de lancer les calculs,
    visualiser l'avancement des calculs, et récupérer les résultats une fois fini
    '''
    def __init__(self):
        '''
        constructeur d'un launcher
        '''
        threading.Thread.__init__(self)
        self.assignments = set()
        self.distance = 0
        self.issue = dict()
        self.hallOfFame = None
        self.status = False

    def init(self):
        '''
        Initialisation du launcher

        instancie l'algorithme et récupère les informations nécéssaires en BDD
        '''
        self.algoInst = algo()

    def run(self):
        '''
        Lance les calculs
        '''
        t1 = time.time()
        hof = self.algoInst.main()
        #print (time.time() - t1) / 60
        self.hallOfFame = hof
        self.issue = self.algoInst.issue
        x = self.algoInst.TransformIndividualIntoAssignments(hof[0])
        self.assignments = []
        for elem in x:
            self.assignments.append(elem.serial())
        #self.distance = round((hof[0].fitness.values[1]/1000)+(hof[0].fitness.values[2]/1000), 0)
        self.distance = self.algoInst.evaluate2(hof[0])
        self.status = True
        #dotTransform.individual(hof[0], "individual.dot")

if __name__ == "__main__":
    
    launcher = ComputationLauncher()
    launcher.init()
    print "fin init"

    launcher.start()
    print "calculs lancés"
    launcher.join()
    print launcher.assignments
    print launcher.issue
    print launcher.distance
    
