class Player:

    def __init__(self, start_geld):
        # Geld des Spielers in Dollar
        self.dollar = start_geld

    def setze(self):
        """
        Spieler setzt genau 1 Dollar.
        """
        if self.dollar > 0:
            self.dollar -= 1
            return 1
        else:
            print("Kein Geld mehr!")
            return 0

    def gewinne(self, betrag):
        """
        Spieler gewinnt Geld.
        """
        self.dollar += betrag

    def getDollar(self):
        """
        Gibt aktuelles Guthaben zurück.
        """
        return self.dollar
