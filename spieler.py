class Player:

    def __init__(self, start_geld):
        # Geld zum Setzen
        self.start_geld = start_geld
        self.dollar = start_geld
        
        # Konto für Gewinne
        self.konto = 0
        self.runden = 0
        self.verlauf = []
        self.feeling = "neutral"


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

    def rundeVerbuchen(self, tipp, augen, treffer, einsatz, auszahlung):
        netto = auszahlung - einsatz
        self.runden += 1
        self.verlauf.append(
            {
                "runde": self.runden,
                "tipp": tipp,
                "augen": augen,
                "treffer": treffer,
                "einsatz": einsatz,
                "auszahlung": auszahlung,
                "netto": netto,
                "vermögen": self.getVermoegen(),
            }
        )
        self.feeling = self._feeling_aktualisieren(netto)

    def _feeling_aktualisieren(self, netto):
        letzte = self.verlauf[-3:]
        siege = sum(1 for r in letzte if r["netto"] > 0)
        niederlagen = sum(1 for r in letzte if r["netto"] < 0)
        gesamt_netto = self.getNetto()

        if netto >= 3 or siege >= 2:
            return "euphorisch"
        if netto > 0:
            return "optimistisch"
        if niederlagen >= 2 and gesamt_netto < 0:
            return "frustriert"
        if gesamt_netto < 0:
            return "angespannt"
        return "neutral"

    def getDollar(self):
        return self.dollar

    def getKonto(self):
        return self.konto

    def getVermoegen(self):
        return self.dollar + self.konto


    def getNetto(self):
        return self.getVermoegen() - self.start_geld


    def getFeeling(self):
        return self.feeling


    def getVerlauf(self):
        return list(self.verlauf)
