# coding=utf8

class Unavailability(object):
    '''
    Classe Unavailabitily définissant une indisponibilité
    
    attributs publics :
    - worker : l'ouvrier de l'affectation (Worker.Worker)
    - phase : la phase de l'affectation (Phase.Phase)
    '''

    def __init__(self, idWorker=-1, numWeek=-1, numYear=-1, type="Indisponible"):
        self.idWorker = idWorker
        self.numYear = numYear
        self.numWeek = numWeek
        self.type = type

    def __str__(self):
        return "L'ouvrier d'id {} a une indisponibilité de type {} la semaine {}/{}".format(self.idWorker, self.type, self.numWeek, self.numYear)

    '''
    ================ Méthodes publiques ================
    '''

    def serial(self):
        '''
        Sérialise une affectation

        Returns:
            un dict contenant l'affectation serialisé
            
        Example:
            >>> {'phase': {'needs': {33: {'num': 33, '__class__': 'Need', 'need': 10, 'craft': {'num': 2, '__class__': 'Craft', 'name': u'Macon'}, 'qualification': {'num': 4, '__class__': 'Qualification', 'name': u'N3P2'}, 'phase': 19}, 34: {'num': 34, '__class__': 'Need', 'need': 20, 'craft': {'num': 2, '__class__': 'Craft', 'name': u'Macon'}, 'qualification': {'num': 5, '__class__': 'Qualification', 'name': u'N3P1'}, 'phase': 19}, 92: {'num': 92, '__class__': 'Need', 'need': 2, 'craft': {'num': 7, '__class__': 'Craft', 'name': u"Agent d'entretien"}, 'qualification': {'num': 6, '__class__': 'Qualification', 'name': u'N2'}, 'phase': 19}, 79: {'num': 79, '__class__': 'Need', 'need': 2, 'craft': {'num': 10, '__class__': 'Craft', 'name': u"Chef d'\xe9quipe"}, 'qualification': {'num': 2, '__class__': 'Qualification', 'name': u'N4P2'}, 'phase': 19}}, 'num': 19, 'numYear': 2014, 'numWeek': 15, 'totalWorkers': 0, 'nbWorkers': 0, '__class__': 'Phase', 'numSite': 4}, 'num': 391, 'worker': {'num': 101, 'licence': u' ', 'name': u'JOUSSEAUME', 'firstName': u'MICKAEL', 'birthdateY': '1972', '__class__': 'Worker', 'birthdateM': '11', 'craft': {'num': 2, '__class__': 'Craft', 'name': u'Macon'}, 'qualification': {'num': 4, '__class__': 'Qualification', 'name': u'N3P2'}, 'position': {'latitude': 47.9292, '__class__': 'Position', 'longitude': -1.94175, 'address': u'6 RUE DE RENNES  35330 LA CHAPELLE BOUEXIC'}, 'birthdateD': '26'}, '__class__': 'Assignment'}
        '''
        return {"__class__": "Unavailability",
                "idWorker": self.idWorker,
                "numYear": self.numYear,
                "numWeek": self.numWeek,
                "type": self.type
                }
