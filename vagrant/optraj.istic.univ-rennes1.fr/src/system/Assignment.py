# coding=utf8
'''
Created on 29 Oct 2013

@author: Nicolas Poirey
'''
from Worker import Worker
from Phase import Phase

class Assignment(object):
    '''
    Classe Assignment définissant une affectation
    
    attributs publics :
    - num : l'id de l'affectation (int)
    - worker : l'ouvrier de l'affectation (Worker.Worker)
    - phase : la phase de l'affectation (Phase.Phase)
    '''

    def __init__(self, num=-1, worker=Worker(), phase=Phase()):
        '''
        Constructeur d'une affectation d'un ouvrier à un chantier

        Args:
            num : le numero unique identifiant l'affectation. (int)
            worker : l'ouvrier concerné. (Worker.Worker)
            phase : la phase de l'affectation (Phase.Phase)
        '''
        self._num = num
        self._worker = worker
        self._phase = phase

    def __str__(self):
        '''
        Retourne l'affecation sous une forme lisible pour l'humain

        Returns:
            l'affectation sous forme de string.
            
        Examples:
            >>> p.__str__()
            >>> "L'affectation, d'id 3, de l'ouvrier (id 5) Doe John, sur la phase d'id 4"
        '''
        return "L'affectation, d'id {}, de l'ouvrier (id {}) {} {}, sur la phase d'id {}".format(self.num, self.worker.num, self.worker.firstName, self.worker.name, \
                                                                                                            self.phase.num) + " " + str(self._phase)

    '''
    /// @cond
    ========================= Setters/accesseurs ==============================
    '''
    #ifndef DOXYGEN_SHOULD_SKIP_THIS

    @property
    def num(self):
        """
        Getter du num
        """
        return self._num

    @num.setter
    def num(self, value):
        """
        Setter du num
        """
        self._num = value

    @property
    def worker(self):
        """
        Getter du worker
        """
        return self._worker

    @worker.setter
    def worker(self, value):
        """
        Setter du worker
        """
        self._worker = value

    @property
    def phase(self):
        """
        Getter de la phase
        """
        return self._phase

    @phase.setter
    def phase(self, value):
        """
        Setter de la phase
        """
        self._phase = value
        
    #endif /* DOXYGEN_SHOULD_SKIP_THIS */
    
    '''
    /// @endcond 
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
        return {"__class__": "Assignment",
                "num": self.num,
                "worker": self.worker.serial(),
                "phase": self.phase.serial()
                }

    def phaseNumber(self):
        '''
        Retourne le numéro de la phase associée

        Returns:
            numPhase (int).
        '''
        return self._phase.num

    def workerNumber(self):
        '''
        retourne le numéro de l'ouvrier associé

        Returns:
            numWorker (int).
        '''
        return self._worker.num
