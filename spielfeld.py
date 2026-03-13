from spieler, wuerfel import *

class Spielfeld:

      """Verwaltet Spielrunde, Auszahlung und Fairness-Statistik von Chuck-a-Luck."""

    def __init__(self, auszahlungs_faktor=2.0):
        self.feld = [1, 2, 3, 4, 5, 6]
        self.wuerfel = [Wuerfel(), Wuerfel(), Wuerfel()]

        self.auszahlungs_faktor = auszahlungs_faktor
        self.runden = 0
        self.gesamt_einsatz = 0
        self.gesamt_auszahlung = 0
        self.treffer_histogramm = {0: 0, 1: 0, 2: 0, 3: 0}

    def werfen(self):
        augen = []
        for w in self.wuerfel:
            w.werfen()
            augen.append(w.getAugen())
        return augen

    def trefferZaehlen(self, tipp, augen):
        treffer = 0
        for a in augen:
            if tipp == a:
                treffer += 1
        return treffer

    def buchen(self, einsatz, auszahlung):
        self.gesamt_einsatz += einsatz
        self.gesamt_auszahlung += auszahlung
    
    def berechneAuszahlung(self, einsatz, treffer):
        return int(einsatz * treffer * self.auszahlungs_faktor)

    def rundeZocken(self, spieler, tipp):
        einsatz = spieler.setze()
        if einsatz == 0:
            return None

        augen = self.werfen()
        treffer = self.trefferZaehlen(tipp, augen)
        auszahlung = self.berechneAuszahlung(einsatz, treffer)

        if auszahlung > 0:
            spieler.gewinnVerbuchen(auszahlung)

        self.buchen(einsatz, auszahlung)
        self.runden += 1
        self.treffer_histogramm[treffer] += 1

        spieler.rundeVerbuchen(tipp, augen, treffer, einsatz, auszahlung)

        return {
            "runde": self.runden,
            "tipp": tipp,
            "augen": augen,
            "treffer": treffer,
            "einsatz": einsatz,
            "auszahlung": auszahlung,
            "netto": auszahlung - einsatz,
        }

    def fairnessStatistik(self):
        if self.gesamt_einsatz == 0:
            empirische_auszahlungsquote = 0.0
        else:
            empirische_auszahlungsquote = self.gesamt_auszahlung / self.gesamt_einsatz

        theoretische_trefferverteilung = {
            0: 125 / 216,
            1: 75 / 216,
            2: 15 / 216,
            3: 1 / 216,
        }

        theoretischer_erwarteter_treffer = 0.5
        theoretische_auszahlungsquote = self.auszahlungs_faktor * theoretischer_erwarteter_treffer

        if self.runden == 0:
            empirische_trefferverteilung = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
        else:
            empirische_trefferverteilung = {
                k: self.treffer_histogramm[k] / self.runden for k in self.treffer_histogramm
            }

        return {
            "runden": self.runden,
            "gesamt_einsatz": self.gesamt_einsatz,
            "gesamt_auszahlung": self.gesamt_auszahlung,
            "hausgewinn": self.gesamt_einsatz - self.gesamt_auszahlung,
            "empirische_auszahlungsquote": empirische_auszahlungsquote,
            "theoretische_auszahlungsquote": theoretische_auszahlungsquote,
            "empirische_trefferverteilung": empirische_trefferverteilung,
            "theoretische_trefferverteilung": theoretische_trefferverteilung,
            "fair": abs(empirische_auszahlungsquote - 1.0) <= 0.05,
        }
