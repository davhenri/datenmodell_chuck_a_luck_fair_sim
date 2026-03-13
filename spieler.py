class Player:

    def __init__(self, start_geld):
        # Geld zum Setzen
        self.dollar = start_geld
        
        # Konto für Gewinne
        self.konto = 0


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


    def gewinnVerbuchen(self, gewinn):
        """
        Gewinn wird auf dem Konto verbucht.
        """
        self.konto += gewinn


    def getDollar(self):
        return self.dollar


    def getKonto(self):
        return self.konto
