from random import randint

class Wuerfel:
    __slots__ = ('augen',)

    def __init__(self):
        """Initialisierung"""
        self.augen = 0                        # Initialisierung von self.augen

    def werfen(self) -> int:
        """Erzeugt eine W6-Zufallszahl."""
        self.augen = randint(1, 6)            # Erzeugt eine W6-Zufallszahl und speichert sie in self.augen.

    def getAugen(self) -> int:
        """Gibt die zuletzt geworfene Zahl zurück."""
        return self.augen
