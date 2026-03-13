from spieler import *
from wuerfel import *

class Spielfeld:

      """Verwaltet Spielrunde, Auszahlung und Fairness-Statistik von Chuck-a-Luck.
      Attribute:
        feld (list[int]): Gueltige Tippzahlen (1 bis 6).
        wuerfel (list[Wuerfel]): Die drei im Spiel verwendeten Wuerfel.
        auszahlungs_faktor (float): Multiplikator fuer Auszahlung pro Treffer.
        runden (int): Anzahl bereits gespielter Runden.
        gesamt_einsatz (int): Summe aller gesetzten Dollars.
        gesamt_auszahlung (int): Summe aller ausgezahlten Gewinne.
        treffer_histogramm (dict[int, int]): Zaehlt, wie oft 0/1/2/3 Treffer vorkamen.
    """

    def __init__(self, auszahlungs_faktor=1.0):
        self.feld = [1, 2, 3, 4, 5, 6]
        self.wuerfel = [Wuerfel(), Wuerfel(), Wuerfel()]

        self.auszahlungs_faktor = auszahlungs_faktor
        self.runden = 0
        self.gesamt_einsatz = 0
        self.gesamt_auszahlung = 0
        self.treffer_histogramm = {0: 0, 1: 0, 2: 0, 3: 0}

    def werfen(self):

      """Wirft alle drei Wuerfel und gibt die Augenzahlen als Liste zurück.
        Returns:
      list[int]: Drei Würfelergebnisse in einem Array(Liste) , z. B. [2, 6, 2]."""

        augen = []
        for w in self.wuerfel:
            w.werfen()
            augen.append(w.getAugen())
        return augen

    def trefferZaehlen(self, tipp, augen):

        """Zählt, wie oft der Spielertipp in den drei Würfeln vorkommt.

        Falltests:
            tipp (int): Zahl, auf die der Spieler gesetzt hat.
            augen (list[int]): Die drei geworfenen Augenzahlen.

        Return:
            int: Anzahl Treffer (0 bis 3).
        """
          
        treffer = 0
        for a in augen:
            if tipp == a:
                treffer += 1
        return treffer

    def buchen(self, einsatz, auszahlung):
          
      """Aktualisiert die berechneten Geldströme ueber alle Runden.

            einsatz (int): In dieser Runde gesetzter Betrag.
            auszahlung (int): In dieser Runde ausbezahlter Betrag.
        """
          
        self.gesamt_einsatz += einsatz
        self.gesamt_auszahlung += auszahlung
    
    def berechneAuszahlung(self, einsatz, treffer):
          
        """Berechnet Auszahlung als einsatz * treffer * faktor."""
          
        return int(einsatz * treffer * self.auszahlungs_faktor)

    def rundeZocken(self, spieler, tipp):

        """Spielt genau eine Runde und liefert alle Rundendaten zurueck.

            spieler (Player): Das Spielerobjekt, dessen Konten verändert werden.
            tipp (int): Tippzahl für diese Runde (1 bis 6).

        Return:
            dict | None: Rundendaten als Dictionary oder None bei keinem Einsatz.
        """
          
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
          
        """Erzeugt Kennzahlen für mathematische und theoretische Fairness.

        Return:
            dict: Kennzahlen für Einsatz, Auszahlung, Trefferverteilungen und Fairness.
        """
          
        if self.gesamt_einsatz == 0:
            empirische_auszahlungsquote = 0.0
        else:
            # Beobachtete Quote: Wie viel wurde pro 1 Dollar Einsatz im Mittel ausgezahlt?
            empirische_auszahlungsquote = self.gesamt_auszahlung / self.gesamt_einsatz

        # Binomialverteilung fuer 3 Wuerfel mit Trefferwahrscheinlichkeit 1/6.
        theoretische_trefferverteilung = {
            0: 125 / 216,
            1: 75 / 216,
            2: 15 / 216,
            3: 1 / 216,
        }


        # Theoretische Auszahlungsquote nach aktueller Regel:
        # 0 Treffer -> 0, 1 Treffer -> 2, 2 Treffer -> 3, 3 Treffer -> 4 (jeweils bei Einsatz=1).
        theoretische_auszahlungsquote = (
            theoretische_trefferverteilung[0] * 0
            + theoretische_trefferverteilung[1] * 2
            + theoretische_trefferverteilung[2] * 3
            + theoretische_trefferverteilung[3] * 4
        )

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
