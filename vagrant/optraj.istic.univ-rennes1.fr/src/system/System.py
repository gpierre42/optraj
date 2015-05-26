# coding=utf8

class System(object):
    '''
    décrit le systeme cardinal
    - sites : l'ensemble de tous les chantiers (set(Site.Site))
    - workers : l'ensemble de tous les ouvriers (set(Worker.Worker))
    - phases : l'ensemble de toutes les phases (set(Phases.Phases))
    - workerSorted : un dict des ouvriers trié par craft et qualif
    '''

    def __init__(self, sites=set(), workers=set(), phases=set()):
        '''
        Constructeur d'un System

        Un System est un objet référencant l'intégralité des chantiers et des ouvriers de l'entreprise.

        Args:
            sites: les chantiers. (set(Site.Site))
            workers: les ouvriers. (set(Worker.Worker))
            phases: les phases. (set(Phases.Phases))
            workerSorted: un dict des ouvriers trié par craft et qualif (dict(Craft.num, dict(Qualification.num, set(Worker.num))))
        '''
        self._sites = sites
        self._workers = workers
        self._phases = phases
        self._workerSorted = dict()

    '''
    ========================= Setters/accesseurs ==============================
    '''
    @property
    def workers(self):
        return self._workers

    @workers.setter
    def workers(self, value):
        self._workers = value

    @property
    def sites(self):
        return self._sites

    @sites.setter
    def sites(self, value):
        self._sites = value
        
    @property
    def phases(self):
        return self._phases

    @phases.setter
    def phases(self, value):
        self._phases = value
        
    @property
    def workerSorted(self):
        return self._workerSorted

    @workerSorted.setter
    def workerSorted(self, value):
        self._workerSorted = value
        
    def getWorkerById(self, numWorker):
        '''
        Retourne l'ouvrier du systeme avec le numéros numWorker si il existe, None sinon

        Args:
            numWorker : le numéro de l'ouvrier à chercher (int)

        Returns:
            l'ouvrier (un Worker.Worker) si il est trouvé, None sinon.
        '''
        for worker in self.workers:
            if worker.num == numWorker:
                return worker
        return None

    def getSiteById(self, numSite):
        '''
        retourne le chantier du systeme avec le numéros numSite si il existe, None sinon

        Args:
            numSite: le numéro du chantier à chercher (int)

        Returns:
            le chantier (un Site) si il est trouvé, None sinon
        '''
        for site in self.sites:
            if site.num == numSite:
                return site
        return None
    
    def getPhasesBySite(self, numSite):
        '''
        retourne les phases du systeme avec le numéro numSite si ils existent, un ensemble vide sinon

        Args:
            numSite: le numéro du chantier à chercher (int)

        Returns:
            l'ensemble des phases liées au site de numéro numSite si il y en a, un ensemble vide sinon (set(Phase.Phase))
        '''
        res = set()
        for ph in self.phases:
            if ph.numSite == numSite:
                res.add(ph)
        return res
    
    def getPhaseBySiteAndWeek(self, numSite, numWeek, numYear):
        '''
        retourne la phases du systeme avec le numéro numSite et le numWeek=numWeek, numYear=numYear si elle existe, None sinon

        Args:
            numSite : le numéro du chantier à chercher (int)
            numWeek : le numero de semaine des phases a retourner (int)
            numYear : l'année des phases a retourner (int)

        Returns:
            la phase de numSite=numSite, numWeek=numWeek et numYear=numYear si il y en a, None sinon
        '''
        for ph in self.phases:
            if ph.numSite == numSite and ph.numYear == numYear and ph.numWeek == numWeek:
                return ph
        return None
    
    def allPhasesSorted(self):
        '''
        Retourne les phases du systèmes classées par année, semaine, puis n° de chantier dans des dict imbriqués
        
        Returns:
            les phases rangés dans des dict imbriqués dans l'ordre numYear, numWeek, numSite
        '''
        res = dict()
        for p in self._phases:
            if p.numYear not in res.keys():
                res[p.numYear] = dict()
            if p.numWeek not in res[p.numYear].keys():
                res[p.numYear][p.numWeek] = dict()
            if p.numSite not in res[p.numYear][p.numWeek].keys():
                res[p.numYear][p.numWeek][p.numSite] = dict()
            res[p.numYear][p.numWeek][p.numSite] = p
        return res
            
