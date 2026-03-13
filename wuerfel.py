from random import randint

class wuerfel(object):

   __slots__ = ('augen',)

    """Initialisierung"""
    def __init__(self):
        self.augen = 0
 
    """werfen() erzeugt eine W6-Zufallszahl(int)."""
    def werfen(self):
        self.augen = randint(1, 6)

    """getAugen() gibt die Zufallszahl von werfen() aus."""
    def getAugen(self):
        return self.augen
