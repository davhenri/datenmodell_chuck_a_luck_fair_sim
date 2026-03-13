from random import randint

class Wuerfel:
    __slots__ = ('augen',)

    def __init__(self):
        """Initialisierung"""
        self.augen = 0

    def werfen(self) -> int:
        """Erzeugt eine W6-Zufallszahl und speichert sie in self.augen."""
        self.augen = randint(1, 6)

    def getAugen(self) -> int:
        """Gibt die zuletzt geworfene Zahl zurück."""
        return self.augen
