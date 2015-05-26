# coding=utf8

import random
import math

import logging
LOG_FILENAME = '/tmp/logging.out'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG,)

class Position:
    '''
    Classe repérant une position sur le plan

    Attributs publics:
    - longitude : la longitude (int)
    - lattitude : la lattitude (int)
    - address : adresse de l'ouvrier (str)
    - num : identifiant de la position (int) 
    '''


    def __init__(self, lat=None, long=None, address=None, num=-1):
        '''
        Constructeur d'une Position
        
        Args:
            longitude : la longitude (int)
            lattitude : la lattitude (int)
            address : adresse de l'ouvrier (str)
            num : identifiant de la position (int)
        '''
        self._longitude = long
        self._latitude = lat
        self._address = address
        self._num = num
        
    def __eq__(self, other):
        """
        Rediffinition de l'égalité entre 2 positions
        
        Args:
            other la Position à laquelle on se compare
            
        Returns:
            True si les latitudes, les longitudes et les addresses sont toutes identiques
            False sinon
        """
        return (self.num == other.num and self.latitude == other.latitude and self.longitude == other.longitude and self.address == other.address)

    '''
    ================Setteurs/Accesseurs=====================
    '''
    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        self._longitude = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        self._latitude = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value
    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, value):
        self._num = value

    '''
    ================ Méthodes publiques ================
    '''
    @staticmethod
    def randomPosition():
        '''
        Instancie une nouvelle position avec des coordonnées aléatoires entre -100 et +100
 
        Returns:
            une Position aléatoire
        '''
        return Position(random.randint(-100, 100), random.randint(-100, 100))
 
    def calcDistance(self, pos2):
        '''
        retourne la distance en mètres entre 2 positions à vol d'oiseau sur la terre
        
        Args:
            pos2 : la Position distante
            
        Returns:
            la distance en mètres avec 12 chiffres (float)
            
        Examples:
            >>> p1 = Position(48.12059, -1.71347, "3 rue des champs, rennes")
            >>> p2 = Position(48.12053, -1.70849)
            >>> print(p1.calcDistance(p2));
            >>> 554.139159673
        '''
        return self._calcAngularDistance(pos2) * 6374892.5
 
    def _calcAngularDistance(self, pos2):
        '''
        calcule la distance angulaire entre la position courante et celle passée en paramètre
        
        Args:
            pos2 : la position distante
        
        Returns:
            la distance angulaire en radians sur 12 chiffres. (float)
            
        Examples:
            >>> p1 = Position(48.12059, -1.71347, "3 rue des champs, rennes")
            >>> p2 = Position(48.12053, -1.70849)
            >>> print(p1._calcAngularDistance(p2))
            >>> 8.69252555511e-05
        '''

        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(pos2.latitude)
        lon2 = math.radians(pos2.longitude)
        dlon = lon2-lon1
        dlat = lat2 - lat1
        a = math.pow(math.sin(dlat/2),2) + \
             math.cos(lat1) * \
             math.cos(lat2) * \
             math.pow(math.sin(dlon/2),2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return c
#        d = math.acos(round(math.sin(lon1) * math.sin(lon2) + math.cos(lon1) * math.cos(lon2) * math.cos(lat1 - lat2), 12))
        #return d
    
    def routeInfo(self, p2, p3, maxDistance):
        """
        Indique si une position est sur le trajet entre 2 autres
        
        Args:
            p2 : extrèmité 1 du trajet (Position)
            p3 : extrèmité 2 du trajet (Position)
            maxdistance : la distance maximal de ramassage en mètres (int)
        
        Returns:
            un tuple (X, distance)
            avec X = True | False suivant que la position est sur le trajet ou non
            et distance = la distance du point self à la droite p2p3 ou 0
        """
        p1p2 = self.calcDistance(p2)
        p1p3 = self.calcDistance(p3)
        p2p3 = p2.calcDistance(p3)
        if p1p2 > p2p3 + maxDistance or p1p3 > p2p3 + maxDistance:
            return False, 0
        
        gamma = p2.angle(self, p3)
        distToTrajet = math.sin(gamma) * p1p2
        return distToTrajet < maxDistance, distToTrajet
        
    def angle(self, A, B):
        """
        Calcule un angle formé par 3 points
        
        l'angle retourné est celui formé à la Position self (nommée C)
        par les 2 droites CA et CB.
        La valeur retournée est en radians
        
        Args:
            A, B : 2 positions (Position)
            
        Returns:
            l'angle en C (self) en radians (float)
            
        Raise:
            ZeroDivisionError si C est confondu avec A ou B
        """
        a = self.calcDistance(B)
        b = self.calcDistance(A)
        c = A.calcDistance(B)
        try:
            return math.acos(round((math.pow(a, 2) + math.pow(b, 2) - math.pow(c, 2)) / \
                              (2 * a * b), 6))
        except ZeroDivisionError:
            return 0
            #raise ZeroDivisionError("calcul d'angle entre {}, {} et {} provoque une division par 0".format(self.num, A.num, B.num))
        except ValueError:
            logging.exception("calcul d'angle entre {}, {} et {} provoque une division par 0".format(self, A, B))
            #print "calcul d'angle entre {}, {} et {} provoque une division par 0".format(self, A, B)
            return 0
        
    def __str__(self):
        '''
        retourne la Position sous une forme lisible pour l'humain.
 
        Returns:
            la Position sous forme de string
        
        Examples:
            >>> Position(48.12059, -1.71347, "3 rue des champs, rennes")
            >>> "[-1.71347, 48.12059], 3 rue des champs, rennes"
        '''
        return "[{}:{}]".format(self.longitude, self.latitude)
 
    def serial(self):
        '''
        Sérialise une position pour pouvoir la transmettre facilement
 
        Returns:
            un dict contenant la position serialisée
        
        Examples:
            >>> Position(48.12059, -1.71347, "3 rue des champs, rennes").serial()
            >>> {'latitude': 48.12059, '__class__': 'Position', 'longitude': -1.71347, 'address': '3 rue des champs, rennes'}
        '''
        return {"__class__": "Position",
                "longitude": self.longitude,
                "latitude": self.latitude,
                "address": self.address}

if __name__ == '__main__':
    
    p1 = Position(38.898556, -77.037852, "3 rue des champs, rennes")
    print(p1)
    print p1.serial()
    p2 = Position(38.897147, -77.043934)
    print(p2)
    p3 = Position(48.12053, -1.71849)
    print p3
    print p3.serial()
    print(p1._calcAngularDistance(p2))
    print(p1.calcDistance(p2));
    print p1.routeInfo(p2, p3, 20000)
    