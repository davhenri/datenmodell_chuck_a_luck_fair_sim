from random import randint

class wuerfel(object):

   __slots__ = ('augen',)

    def __init__(self):
        self.augen = 0
 
    def werfen(self):
        self.augen = randint(1, 6)
        return self.augen

    def getAugen(self):
        return self.augen
