import tkinter as tk
from pathlib import Path
from random import randint

# ============================
# Logik: Wuerfel, Spieler, Spielfeld
# ============================

class Wuerfel:
    __slots__ = ('augen',)

    def __init__(self):
        self.augen = 0

    def werfen(self) -> int:
        self.augen = randint(1, 6)
        return self.augen

    def getAugen(self) -> int:
        return self.augen


class Spieler:
    def __init__(self, start_geld):
        self.start_geld = start_geld
        self.dollar = start_geld
        self.konto = 0
        self.runden = 0
        self.verlauf = []
        self.feeling = "neutral"

    def setze(self):
        if self.dollar > 0:
            self.dollar -= 1
            return 1
        return 0

    def gewinnVerbuchen(self, gewinn):
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


class Spielfeld:
    """Verwaltet Spielrunde, Auszahlung und Fairness-Statistik von Chuck-a-Luck."""
    def __init__(self, auszahlungs_faktor=1.0):
        self.feld = [1, 2, 3, 4, 5, 6]
        self.wuerfel = [Wuerfel(), Wuerfel(), Wuerfel()]

        # Auszahlung: klassisch wäre 1x pro Treffer. Hier via Faktor erweiterbar.
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
        return sum(1 for a in augen if a == tipp)

    def buchen(self, einsatz, auszahlung):
        self.gesamt_einsatz += einsatz
        self.gesamt_auszahlung += auszahlung

    def berechneAuszahlung(self, einsatz, treffer):
        # Auszahlung pro Treffer: einsatz * treffer * faktor (klassisch faktor=1.0)
        return int(einsatz * treffer * self.auszahlungs_faktor)

    def rundeZocken(self, spieler: Spieler, tipp: int):
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

        theoretische_auszahlungsquote = (
            theoretische_trefferverteilung[0] * 0
            + theoretische_trefferverteilung[1] * 1
            + theoretische_trefferverteilung[2] * 2
            + theoretische_trefferverteilung[3] * 3
        )  # faktor=1.0, klassisch

        if self.runden == 0:
            empirische_trefferverteilung = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
        else:
            empirische_trefferverteilung = {k: self.treffer_histogramm[k] / self.runden for k in self.treffer_histogramm}

        return {
            "runden": self.runden,
            "gesamt_einsatz": self.gesamt_einsatz,
            "gesamt_auszahlung": self.gesamt_auszahlung,
            "hausgewinn": self.gesamt_einsatz - self.gesamt_auszahlung,
            "empirische_auszahlungsquote": empirische_auszahlungsquote,
            "theoretische_auszahlungsquote": theoretische_auszahlungsquote,
            "empirische_trefferverteilung": empirische_trefferverteilung,
            "theoretische_trefferverteilung": theoretische_trefferverteilung,
            "fair": abs(empirische_auszahlungsquote - 1.0) <= 0.05 if self.gesamt_einsatz > 0 else None,
        }

# ============================
# GUI
# ============================

class GUI:
    def __init__(self):
        self.mode = "start"

        self.gui = tk.Tk()
        self.gui.title("Chuck-A-Luck")
        self.gui.geometry("1000x800")

        self.frameGUI = tk.Frame(master=self.gui, bg="#F5F5F5")
        self.frameGUI.place(x=0, y=0, width=1000, height=800)

        self.base = Path(__file__).parent

        # Spielobjekte
        self.spielfeld = Spielfeld(auszahlungs_faktor=1.0)  # klassisch
        self.spieler = Spieler(start_geld=20)

        # Assets-Puffer
        self.images = {}

        self.build_start_view()
        self.gui.mainloop()

    # ---------- Hilfen für Bilder ----------
    def load_img(self, name, subsample=None):
        """Lädt ein Bild (PNG) relativ zum Skriptordner. Hält Referenz in self.images."""
        path = self.base / name
        try:
            img = tk.PhotoImage(file=str(path))
            if subsample:
                img = img.subsample(*subsample)
        except tk.TclError:
            # Platzhalter
            img = tk.PhotoImage(width=64, height=64)
        self.images[name + f"_{subsample}"] = img
        return img

    # ---------- Views ----------
    def build_start_view(self):
        for w in self.frameGUI.winfo_children():
            w.destroy()

        tk.Label(self.frameGUI, bg=self.frameGUI.cget("bg"), font=("Arial", 30),
                 text="CHUCK-A-LUCK").place(relx=0.5, rely=0.20, anchor="center")

        button_frame = tk.Frame(self.frameGUI, bg=self.frameGUI.cget("bg"))
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Button(button_frame, text="Feeling", width=16, height=2,
                  command=self.mode_feeling).grid(row=0, column=0, padx=20, pady=10)
        tk.Button(button_frame, text="Statistik", width=16, height=2,
                  command=self.mode_statistic).grid(row=0, column=1, padx=20, pady=10)

    def mode_feeling(self):
        self.mode = "feeling"
        for w in self.frameGUI.winfo_children():
            w.destroy()

        # Kopf
        tk.Label(self.frameGUI, bg=self.frameGUI.cget("bg"), font=("Arial", 18),
                 text="Modus: Feeling").place(relx=0.5, rely=0.08, anchor="center")

        # Links: Spieler-Coins (2 Spalten à 10)
        self.left_container = tk.Frame(self.frameGUI, bg=self.frameGUI.cget("bg"))
        self.left_container.place(relx=0.12, rely=0.45, anchor="center")

        self.coin_img = self.load_img("stableCoinEuro.png", subsample=(30, 30))
        self.coin_text_var = tk.StringVar(value=f"x {self.spieler.getDollar()}")
        tk.Label(self.left_container, text="Coins:", font=("Arial", 14),
                 bg=self.frameGUI.cget("bg")).grid(row=0, column=0, sticky="w", padx=(0, 4))
        self.coin_text_label = tk.Label(self.left_container, textvariable=self.coin_text_var,
                                        font=("Arial", 14), bg=self.frameGUI.cget("bg"))
        self.coin_text_label.grid(row=0, column=1, sticky="w")

        self.coins_grid = tk.Frame(self.left_container, bg=self.frameGUI.cget("bg"))
        self.coins_grid.grid(row=1, column=0, columnspan=2, pady=(6, 0))
        self.coin_labels = []
        self._rebuild_coin_grid()

        # Mitte oben: Mood-Bild
        containerMood = tk.Frame(self.frameGUI, bg=self.frameGUI.cget("bg"))
        containerMood.place(relx=0.5, rely=0.26, anchor="center")
        self.mood_label = tk.Label(containerMood, bg=self.frameGUI.cget("bg"))
        self.mood_label.pack(pady=(6, 0))
        self._update_mood_image()

        # Tiles (2×3), Klick = Tipp setzen
        containerTiles = tk.Frame(self.frameGUI, bg=self.frameGUI.cget("bg"))
        containerTiles.place(relx=0.5, rely=0.58, anchor="center")

        self.tiles_small = []
        for i in range(1, 7):
            img_small = self.load_img(f"tile_{i}.png", subsample=(10, 10))
            self.tiles_small.append(img_small)

        self.tile_buttons = []
        for i, img_small in enumerate(self.tiles_small, start=1):
            r, c = divmod(i - 1, 3)
            btn = tk.Button(containerTiles, image=img_small,
                            command=lambda n=i: self.on_tile_click(n))
            btn.grid(row=r, column=c, padx=10, pady=10)
            self.tile_buttons.append(btn)

        # Rechts unten: Würfelanzeige (3 Würfel) + „Würfeln“-Button
        dice_container = tk.Frame(self.frameGUI, bg=self.frameGUI.cget("bg"))
        dice_container.place(relx=0.85, rely=0.86, anchor="center")

        self.dice_imgs = {n: self.load_img(f"wuerfel{n}.png", subsample=(4, 4)) for n in range(1, 7)}
        # Startanzeige drei Einsen
        self.dice_labels = []
        for i in range(3):
            lbl = tk.Label(dice_container, image=self.dice_imgs[1], bg=self.frameGUI.cget("bg"))
            lbl.grid(row=0, column=i, padx=4)
            self.dice_labels.append(lbl)

        tk.Button(dice_container, text="Würfeln", command=self.on_roll).grid(row=1, column=0, columnspan=3, pady=(6, 0))

        # Zurück
        tk.Button(self.frameGUI, text="Zurück", command=self.build_start_view
                  ).place(relx=0.5, rely=0.86, anchor="center")

        # Rundenausgabe
        self.status_var = tk.StringVar(value="Setze 1 Coin, indem du auf eine Zahl (Tile) klickst.")
        tk.Label(self.frameGUI, textvariable=self.status_var, bg=self.frameGUI.cget("bg"),
                 font=("Arial", 12)).place(relx=0.5, rely=0.92, anchor="center")

        # Letzten Tipp merken, bis gewürfelt wurde
        self.aktueller_tipp = None
        self.gelegte_muenzen_buttons = set()

    def _rebuild_coin_grid(self):
        # Alte Labels räumen
        for _, _, lbl in getattr(self, "coin_labels", []):
            lbl.destroy()
        self.coin_labels = []

        # 2 Spalten à 10
        dollar = self.spieler.getDollar()
        total = min(dollar, 20)
        for i in range(total):
            c = i // 10
            r = i % 10
            lbl = tk.Label(self.coins_grid, image=self.coin_img, bg=self.frameGUI.cget("bg"))
            lbl.grid(row=r, column=c, padx=2, pady=2, sticky="n")
            self.coin_labels.append((r, c, lbl))

        # Reihenfolge zum Entfernen von unten rechts nach oben links
        self.coin_labels.sort(key=lambda t: (t[1], t[0]), reverse=True)

    def _update_mood_image(self):
        feeling = self.spieler.getFeeling() or "neutral"
        candidates = {
            "neutral": "neutral.png",
            "optimistisch": "optimistisch.png",
            "angespannt": "angespannt.png",
            "frustriert": "frustriert.png",
            "euphorisch": "euphorisch.png",
        }
        name = candidates.get(feeling, "neutral.png")
        img = self.load_img(name, subsample=(4, 4))
        self.mood_label.config(image=img)

    # ---------- Interaktion ----------
    def on_tile_click(self, tipp: int):
        if self.spieler.getDollar() <= 0:
            self._flash_label(self.coin_text_label)
            self.status_var.set("Keine Coins mehr. Würfle oder starte neu.")
            return

        # Einsatz (1 Coin) visuell auf Tile legen (ersetze Bild temporär durch Coin)
        idx = tipp - 1
        self.tile_buttons[idx].config(image=self.coin_img)
        self.gelegte_muenzen_buttons.add(idx)

        # Tipp merken und Spieler setzt im nächsten Schritt beim Würfeln
        self.aktueller_tipp = tipp
        self.status_var.set(f"Einsatz auf {tipp} gesetzt. Klicke 'Würfeln'.")

    def on_roll(self):
        # Falls kein Tipp gelegt, Hinweis
        if not self.aktueller_tipp:
            self.status_var.set("Bitte zuerst auf eine Zahl (Tile) klicken, um zu setzen.")
            return

        # Spiele eine Runde
        result = self.spielfeld.rundeZocken(self.spieler, self.aktueller_tipp)
        if result is None:
            self.status_var.set("Kein Einsatz möglich (kein Dollar mehr).")
            return

        # Coins-UI aktualisieren (Dollar nahm um 1 ab; Gewinne gehen aufs Konto)
        self.coin_text_var.set(f"x {self.spieler.getDollar()}")
        self._rebuild_coin_grid()

        # Zeige Würfelbilder
        a1, a2, a3 = result["augen"]
        for lbl, a in zip(self.dice_labels, [a1, a2, a3]):
            lbl.config(image=self.dice_imgs.get(a, self.dice_imgs[1]))

        # Ergebnistext
        tipp = result["tipp"]
        treffer = result["treffer"]
        einsatz = result["einsatz"]
        ausz = result["auszahlung"]
        netto = result["netto"]
        self.status_var.set(
            f"Runde {result['runde']}: Tipp {tipp}, Würfel {a1}-{a2}-{a3}, Treffer {treffer}, Auszahlung {ausz} (Netto {netto})."
        )

        # Mood aktualisieren
        self._update_mood_image()

        # Tile-Bilder zurücksetzen (nur die, auf denen wir eine Münze gelegt haben)
        for idx in list(self.gelegte_muenzen_buttons):
            original_tile = self.tiles_small[idx]
            self.tile_buttons[idx].config(image=original_tile)
        self.gelegte_muenzen_buttons.clear()

        # Nächste Runde: Tipp zurücksetzen
        self.aktueller_tipp = None

    def _flash_label(self, label: tk.Label):
        orig = label.cget("fg") if label.cget("fg") else "black"
        label.config(fg="red")
        label.after(180, lambda: label.config(fg=orig))

    def mode_statistic(self):
        self.mode = "statistic"
        self.show_info("Modus: Statistik")

        stats = self.spielfeld.fairnessStatistik()
        txt = [
            f"Runden: {stats['runden']}",
            f"Gesamt Einsatz: {stats['gesamt_einsatz']}",
            f"Gesamt Auszahlung: {stats['gesamt_auszahlung']}",
            f"Hausgewinn: {stats['hausgewinn']}",
            f"Emp. Auszahlungsquote: {stats['empirische_auszahlungsquote']:.3f}",
            f"Theor. Auszahlungsquote: {stats['theoretische_auszahlungsquote']:.3f}",
            f"Emp. Trefferverteilung: {stats['empirische_trefferverteilung']}",
            f"Theor. Trefferverteilung: {stats['theoretische_trefferverteilung']}",
            f"Fair (±5%): {stats['fair']}",
        ]
        label = tk.Label(self.frameGUI, text="\n".join(txt), bg=self.frameGUI.cget("bg"), font=("Consolas", 11), justify="left")
        label.place(relx=0.5, rely=0.58, anchor="center")

        tk.Button(self.frameGUI, text="Zurück", command=self.build_start_view
                  ).place(relx=0.5, rely=0.86, anchor="center")

    def show_info(self, text: str):
        for w in self.frameGUI.winfo_children():
            w.destroy()
        tk.Label(self.frameGUI, bg=self.frameGUI.cget("bg"), font=("Arial", 18), text=text
                 ).place(relx=0.5, rely=0.2, anchor="center")

if __name__ == "__main__":
    GUI()

