# coding=utf8

INNER_JOIN = "INNER"
LEFT_JOIN = "LEFT"
LEFT_OUTER_JOIN = "LEFT OUTER"
RIGHT_JOIN = "RIGHT"
OUTER_JOIN = "OUTER"

class NaturalJoin:
    '''
    Classe NaturalJoin définissant une jointure SQL
    
    Attributs:
    - joinType : le type de la jointure (INNER, LEFT, etc) (str)
    - tableName : le nom de la table jointe (str)
    - joinClauses : clauses éventuelles de la jointure (str)
    - joinMappingCols : mapping des colonnes de la table tableName (dict(str:nom col à joindre, str:nom col jointe))
    - joinId : l'id de la jointure (int)
    '''

    def __init__(self, joinType=INNER_JOIN, tableName=None, alias=None, joinClauses=None, joinMappingCols=None, joinId=None):
        '''
        Constructeur d'une jointure
        
        Args:
            joinType le type de la jointure (INNER, LEFT, etc) (str)
            tableName le nom de la table jointe (str)
            joinClauses clauses éventuelles de la jointure (str)
            joinMappingCols mapping des colonnes de la table tableName (dict(str:nom col à joindre, str:nom col jointe))
            joinId l'id de la jointure (int)
        '''
        self._joinType = joinType
        self._tableName = tableName
        self._alias = alias
        self._joinClauses = joinClauses
        self._joinMappingCols = joinMappingCols
        self._joinId = joinId

    def __str__(self):
        '''
        affiche la jointure sous une forme lisible par l'humain
        
        Returns:
            la jointure en str
        '''
        return "{} join sur la table {} par la jointure: {}".format(self.joinType, self.tableName, self.joinId)
    '''
    =========== Setteurs/Accesseurs ===============
    '''

    @property
    def joinType(self):
        return self._joinType

    @joinType.setter
    def joinType(self, value):
        self._joinType = value

    @property
    def tableName(self):
        return self._tableName

    @tableName.setter
    def tableName(self, value):
        self._tableName = value

    @property
    def joinClauses(self):
        return self._joinClauses

    @joinClauses.setter
    def joinClauses(self, value):
        self._joinClauses = value

    @property
    def joinMappingCols(self):
        return self._joinMappingCols

    @joinMappingCols.setter
    def joinMappingCols(self, value):
        self._joinMappingCols = value

    @property
    def joinId(self):
        return self._joinId

    @joinId.setter
    def joinId(self, value):
        self._joinId = value

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, value):
        self._alias = value
