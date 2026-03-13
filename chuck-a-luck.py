import spieler, spielfeld, wuerfel
from tkinter import *
from PIL import Image, ImageTk
import os

class GUI:
    def __init__(self):
        # Zustände und Widgets als Instanzattribute
        self.mode = "start"

        # Spielobjekte
        self.spieler = None
        self.spielfeld = None
        self.selected_tile = None
        self.current_bet = 0

        # Bildressourcen laden
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.images = {}
        self.load_images()

        # Hauptfenster
        self.gui = Tk()
        self.gui.title("Chuck-A-Luck")
        self.gui.geometry("1000x800")
        self.gui.resizable(False, False)

        # Haupt-Frame
        self.frameGUI = Frame(master=self.gui, bg="#F5F5F5")
        self.frameGUI.place(x=0, y=0, width=1000, height=800)

        # Start-Ansicht aufbauen
        self.build_start_view()

        # Ereignisschleife starten
        self.gui.mainloop()

    def load_images(self):
        """Lädt alle Bilder für das Spiel"""
        try:
            # Würfelbilder laden
            for i in range(1, 7):
                img = Image.open(os.path.join(self.base_path, "assets", f"wuerfel{i}.png"))
                img = img.resize((100, 100), Image.Resampling.LANCZOS)
                self.images[f"wuerfel{i}"] = ImageTk.PhotoImage(img)

            # Tile-Bilder laden
            for i in range(1, 7):
                img = Image.open(os.path.join(self.base_path, "assets", f"tile_{i}.png"))
                img = img.resize((120, 120), Image.Resampling.LANCZOS)
                self.images[f"tile_{i}"] = ImageTk.PhotoImage(img)

            # Coin-Bild laden
            img = Image.open(os.path.join(self.base_path, "assets", "stableCoinEuro.png"))
            img = img.resize((40, 40), Image.Resampling.LANCZOS)
            self.images["coin"] = ImageTk.PhotoImage(img)

            # Kleinere Coin-Version
            img = Image.open(os.path.join(self.base_path, "assets", "stableCoinEuro.png"))
            img = img.resize((25, 25), Image.Resampling.LANCZOS)
            self.images["coin_small"] = ImageTk.PhotoImage(img)

            # Emotion-SVGs laden (als PNG konvertiert über PIL)
            emotions = ["neutral", "optimistisch", "euphorisch", "frustriert", "angespannt"]
            for emotion in emotions:
                try:
                    # Versuche SVG zu laden (funktioniert nur mit cairosvg)
                    svg_path = os.path.join(self.base_path, f"{emotion}.svg")
                    # Fallback: Erstelle einfache Emotion-Icons als Text
                    self.images[emotion] = None
                except:
                    self.images[emotion] = None

        except Exception as e:
            print(f"Fehler beim Laden der Bilder: {e}")

    def build_start_view(self):
        """Startbildschirm mit Spielmodus-Auswahl"""
        for w in self.frameGUI.winfo_children():
            w.destroy()

        # Titel
        label_title = Label(
            master=self.frameGUI,
            bg=self.frameGUI.cget("bg"),
            font=("Arial", 40, "bold"),
            text="🎲 CHUCK-A-LUCK 🎲",
        )
        label_title.place(relx=0.5, rely=0.2, anchor="center")

        # Untertitel
        label_subtitle = Label(
            master=self.frameGUI,
            bg=self.frameGUI.cget("bg"),
            font=("Arial", 16),
            text="Wähle deinen Spielmodus",
        )
        label_subtitle.place(relx=0.5, rely=0.3, anchor="center")

        # Container für Buttons
        button_frame = Frame(master=self.frameGUI, bg=self.frameGUI.cget("bg"))
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        # FEEL IT! Button
        btn_feeling = Button(
            master=button_frame,
            text="FEEL IT! 🎮\n(Manuelles Spielen)",
            width=20,
            height=3,
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.mode_feeling,
        )
        btn_feeling.grid(row=0, column=0, padx=20, pady=10)

        # Statistik Button
        btn_stat = Button(
            master=button_frame,
            text="STATISTIK 📊\n(Theoretisches Spiel)",
            width=20,
            height=3,
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white",
            command=self.mode_statistic,
        )
        btn_stat.grid(row=0, column=1, padx=20, pady=10)

    def mode_feeling(self):
        """FEEL IT! Mode - Manuelles Spielen"""
        self.mode = "feeling"

        # Spieler und Spielfeld initialisieren
        self.spieler = spieler.Spieler(start_geld=100)
        self.spielfeld = spielfeld.Spielfeld(auszahlungs_faktor=1.0)
        self.selected_tile = None
        self.current_bet = 0

        self.build_feeling_view()

    def build_feeling_view(self):
        """Baut die FEEL IT! Spielansicht auf"""
        for w in self.frameGUI.winfo_children():
            w.destroy()

        # Header
        header_frame = Frame(master=self.frameGUI, bg="#2E7D32", height=80)
        header_frame.pack(fill=X)

        Label(
            master=header_frame,
            text="FEEL IT! MODE",
            font=("Arial", 24, "bold"),
            bg="#2E7D32",
            fg="white"
        ).pack(pady=20)

        # Hauptspielbereich
        game_frame = Frame(master=self.frameGUI, bg="#F5F5F5")
        game_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Linke Seite: Spielfeld und Würfel
        left_frame = Frame(master=game_frame, bg="#F5F5F5")
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Spielfeld (3x2 Grid)
        board_label = Label(
            master=left_frame,
            text="Wähle ein Feld:",
            font=("Arial", 16, "bold"),
            bg="#F5F5F5"
        )
        board_label.pack(pady=10)

        board_frame = Frame(master=left_frame, bg="#F5F5F5")
        board_frame.pack(pady=10)

        # Tiles als 3x2 Grid
        self.tile_buttons = {}
        for row in range(2):
            for col in range(3):
                tile_num = row * 3 + col + 1
                btn = Button(
                    master=board_frame,
                    image=self.images[f"tile_{tile_num}"],
                    command=lambda t=tile_num: self.select_tile(t),
                    relief=RAISED,
                    bd=3
                )
                btn.grid(row=row, column=col, padx=5, pady=5)
                self.tile_buttons[tile_num] = btn

        # Würfel-Anzeige
        dice_label = Label(
            master=left_frame,
            text="Würfel:",
            font=("Arial", 16, "bold"),
            bg="#F5F5F5"
        )
        dice_label.pack(pady=(20, 10))

        dice_frame = Frame(master=left_frame, bg="#F5F5F5")
        dice_frame.pack()

        self.dice_labels = []
        for i in range(3):
            lbl = Label(
                master=dice_frame,
                image=self.images["wuerfel1"],
                bg="#F5F5F5"
            )
            lbl.pack(side=LEFT, padx=10)
            self.dice_labels.append(lbl)

        # Rechte Seite: Spielerinfo, Emotion, Aktionen
        right_frame = Frame(master=game_frame, bg="#FFFFFF", relief=RIDGE, bd=2)
        right_frame.pack(side=RIGHT, fill=BOTH, padx=(20, 0))

        # Spielerinfo
        info_frame = Frame(master=right_frame, bg="#FFFFFF")
        info_frame.pack(pady=20, padx=20)

        self.money_label = Label(
            master=info_frame,
            text=f"💰 Geld: ${self.spieler.getDollar()}",
            font=("Arial", 18, "bold"),
            bg="#FFFFFF"
        )
        self.money_label.pack(pady=5)

        self.balance_label = Label(
            master=info_frame,
            text=f"📊 Bilanz: ${self.spieler.getNetto():+d}",
            font=("Arial", 14),
            bg="#FFFFFF"
        )
        self.balance_label.pack(pady=5)

        self.rounds_label = Label(
            master=info_frame,
            text=f"🎲 Runde: {self.spieler.runden}",
            font=("Arial", 14),
            bg="#FFFFFF"
        )
        self.rounds_label.pack(pady=5)

        # Emotion/Feeling Display
        emotion_frame = Frame(master=right_frame, bg="#FFFFFF")
        emotion_frame.pack(pady=20)

        Label(
            master=emotion_frame,
            text="Dein Feeling:",
            font=("Arial", 14, "bold"),
            bg="#FFFFFF"
        ).pack()

        self.emotion_label = Label(
            master=emotion_frame,
            text=self.get_emotion_emoji(self.spieler.getFeeling()),
            font=("Arial", 48),
            bg="#FFFFFF"
        )
        self.emotion_label.pack(pady=10)

        self.emotion_text = Label(
            master=emotion_frame,
            text=self.spieler.getFeeling().upper(),
            font=("Arial", 12, "bold"),
            bg="#FFFFFF"
        )
        self.emotion_text.pack()

        # Einsatz-Info
        bet_frame = Frame(master=right_frame, bg="#FFE082", relief=RIDGE, bd=2)
        bet_frame.pack(pady=10, padx=20, fill=X)

        self.bet_label = Label(
            master=bet_frame,
            text="Wähle ein Feld!",
            font=("Arial", 14, "bold"),
            bg="#FFE082"
        )
        self.bet_label.pack(pady=10)

        # Gewinn/Verlust Anzeige
        self.result_label = Label(
            master=right_frame,
            text="",
            font=("Arial", 16, "bold"),
            bg="#FFFFFF"
        )
        self.result_label.pack(pady=10)

        # Spiel-Button
        self.play_button = Button(
            master=right_frame,
            text="🎲 WÜRFELN! 🎲",
            font=("Arial", 16, "bold"),
            bg="#FF9800",
            fg="white",
            state=DISABLED,
            command=self.play_round,
            width=15,
            height=2
        )
        self.play_button.pack(pady=20)

        # Zurück-Button
        Button(
            master=right_frame,
            text="← Zurück zum Menü",
            command=self.build_start_view,
            font=("Arial", 10),
            bg="#F5F5F5"
        ).pack(pady=10)

    def select_tile(self, tile_num):
        """Wählt ein Tile für die Wette aus"""
        if self.spieler.getDollar() <= 0:
            self.result_label.config(text="❌ Kein Geld mehr!", fg="red")
            return

        # Vorherige Auswahl zurücksetzen
        if self.selected_tile:
            self.tile_buttons[self.selected_tile].config(relief=RAISED, bd=3)

        # Neue Auswahl
        self.selected_tile = tile_num
        self.tile_buttons[tile_num].config(relief=SUNKEN, bd=5)

        # UI aktualisieren
        self.bet_label.config(text=f"Einsatz: $1 auf Feld {tile_num}")
        self.play_button.config(state=NORMAL)
        self.result_label.config(text="")

    def play_round(self):
        """Spielt eine Runde"""
        if not self.selected_tile:
            return

        # Würfeln
        result = self.spielfeld.rundeZocken(self.spieler, self.selected_tile)

        if not result:
            self.result_label.config(text="❌ Kein Geld mehr!", fg="red")
            return

        # Würfel anzeigen
        augen = result["augen"]
        for i, wert in enumerate(augen):
            self.dice_labels[i].config(image=self.images[f"wuerfel{wert}"])

        # Ergebnis anzeigen
        treffer = result["treffer"]
        netto = result["netto"]

        if netto > 0:
            # Gewinn
            self.result_label.config(
                text=f"🎉 GEWONNEN! +${netto}",
                fg="green"
            )
            self.flash_background("green")
        else:
            # Verlust
            self.result_label.config(
                text=f"❌ Verloren: ${netto}",
                fg="red"
            )
            self.flash_background("red")

        # UI aktualisieren
        self.update_player_info()

        # Auswahl zurücksetzen
        if self.selected_tile:
            self.tile_buttons[self.selected_tile].config(relief=RAISED, bd=3)
        self.selected_tile = None
        self.play_button.config(state=DISABLED)
        self.bet_label.config(text="Wähle ein Feld!")

    def update_player_info(self):
        """Aktualisiert die Spielerinformationen"""
        self.money_label.config(text=f"💰 Geld: ${self.spieler.getDollar()}")
        self.balance_label.config(text=f"📊 Bilanz: ${self.spieler.getNetto():+d}")
        self.rounds_label.config(text=f"🎲 Runde: {self.spieler.runden}")

        feeling = self.spieler.getFeeling()
        self.emotion_label.config(text=self.get_emotion_emoji(feeling))
        self.emotion_text.config(text=feeling.upper())

    def get_emotion_emoji(self, feeling):
        """Gibt das passende Emoji für das Feeling zurück"""
        emotions = {
            "neutral": "😐",
            "optimistisch": "🙂",
            "euphorisch": "🤩",
            "frustriert": "😤",
            "angespannt": "😰"
        }
        return emotions.get(feeling, "😐")

    def flash_background(self, color):
        """Lässt den Hintergrund kurz aufblinken"""
        original_color = self.frameGUI.cget("bg")

        # Farbcodes für die Animation
        if color == "green":
            flash_color = "#4CAF50"
        else:
            flash_color = "#F44336"

        # Blitz-Animation
        self.frameGUI.config(bg=flash_color)
        self.gui.update()
        self.gui.after(200, lambda: self.frameGUI.config(bg=original_color))

    def mode_statistic(self):
        """Statistik Mode - Theoretisches Spiel"""
        self.mode = "statistic"
        self.build_statistic_view()

    def build_statistic_view(self):
        """Baut die Statistik-Ansicht auf"""
        for w in self.frameGUI.winfo_children():
            w.destroy()

        # Header
        header_frame = Frame(master=self.frameGUI, bg="#1976D2", height=80)
        header_frame.pack(fill=X)

        Label(
            master=header_frame,
            text="STATISTIK MODE",
            font=("Arial", 24, "bold"),
            bg="#1976D2",
            fg="white"
        ).pack(pady=20)

        # Hauptbereich
        main_frame = Frame(master=self.frameGUI, bg="#F5F5F5")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Beschreibung
        Label(
            master=main_frame,
            text="Theoretische Simulation des Chuck-A-Luck Spiels",
            font=("Arial", 16),
            bg="#F5F5F5"
        ).pack(pady=20)

        # Eingabebereich
        input_frame = Frame(master=main_frame, bg="#FFFFFF", relief=RIDGE, bd=2)
        input_frame.pack(pady=20, padx=50, fill=X)

        Label(
            master=input_frame,
            text="Anzahl Runden:",
            font=("Arial", 14),
            bg="#FFFFFF"
        ).pack(pady=(20, 5))

        self.rounds_entry = Entry(
            master=input_frame,
            font=("Arial", 14),
            width=10,
            justify=CENTER
        )
        self.rounds_entry.insert(0, "1000")
        self.rounds_entry.pack(pady=(5, 10))

        Label(
            master=input_frame,
            text="Startkapital:",
            font=("Arial", 14),
            bg="#FFFFFF"
        ).pack(pady=(10, 5))

        self.money_entry = Entry(
            master=input_frame,
            font=("Arial", 14),
            width=10,
            justify=CENTER
        )
        self.money_entry.insert(0, "1000")
        self.money_entry.pack(pady=(5, 20))

        # Simulation starten
        Button(
            master=input_frame,
            text="📊 SIMULATION STARTEN",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.run_simulation,
            width=20,
            height=2
        ).pack(pady=20)

        # Ergebnisbereich
        self.stat_result_frame = Frame(master=main_frame, bg="#FFFFFF", relief=RIDGE, bd=2)
        self.stat_result_frame.pack(fill=BOTH, expand=True, pady=20)

        self.stat_text = Text(
            master=self.stat_result_frame,
            font=("Courier", 10),
            bg="#FFFFFF",
            wrap=WORD
        )
        self.stat_text.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Zurück-Button
        Button(
            master=main_frame,
            text="← Zurück zum Menü",
            command=self.build_start_view,
            font=("Arial", 10),
            bg="#F5F5F5"
        ).pack(pady=10)

    def run_simulation(self):
        """Führt eine statistische Simulation durch"""
        try:
            num_rounds = int(self.rounds_entry.get())
            start_money = int(self.money_entry.get())
        except ValueError:
            self.stat_text.delete(1.0, END)
            self.stat_text.insert(END, "❌ Ungültige Eingabe! Bitte Zahlen eingeben.")
            return

        # Simulation durchführen
        sim_player = spieler.Spieler(start_geld=start_money)
        sim_field = spielfeld.Spielfeld(auszahlungs_faktor=1.0)

        self.stat_text.delete(1.0, END)
        self.stat_text.insert(END, "🎲 SIMULATION LÄUFT...\n\n")
        self.gui.update()

        # Spiele Runden (immer auf Feld 1 tippen)
        for _ in range(num_rounds):
            if sim_player.getDollar() <= 0:
                break
            sim_field.rundeZocken(sim_player, 1)

        # Statistiken abrufen
        stats = sim_field.fairnessStatistik()

        # Ergebnisse anzeigen
        self.stat_text.delete(1.0, END)
        self.stat_text.insert(END, "═" * 50 + "\n")
        self.stat_text.insert(END, "   CHUCK-A-LUCK SIMULATIONSERGEBNISSE\n")
        self.stat_text.insert(END, "═" * 50 + "\n\n")

        self.stat_text.insert(END, f"Anzahl Runden:           {stats['runden']}\n")
        self.stat_text.insert(END, f"Startkapital:            ${start_money}\n")
        self.stat_text.insert(END, f"Endkapital:              ${sim_player.getVermoegen()}\n")
        self.stat_text.insert(END, f"Netto Gewinn/Verlust:    ${sim_player.getNetto():+d}\n\n")

        self.stat_text.insert(END, "─" * 50 + "\n")
        self.stat_text.insert(END, "GELDFLÜSSE\n")
        self.stat_text.insert(END, "─" * 50 + "\n")
        self.stat_text.insert(END, f"Gesamt Einsatz:          ${stats['gesamt_einsatz']}\n")
        self.stat_text.insert(END, f"Gesamt Auszahlung:       ${stats['gesamt_auszahlung']}\n")
        self.stat_text.insert(END, f"Hausgewinn:              ${stats['hausgewinn']}\n\n")

        self.stat_text.insert(END, "─" * 50 + "\n")
        self.stat_text.insert(END, "AUSZAHLUNGSQUOTEN\n")
        self.stat_text.insert(END, "─" * 50 + "\n")
        self.stat_text.insert(END, f"Empirische Quote:        {stats['empirische_auszahlungsquote']:.4f}\n")
        self.stat_text.insert(END, f"Theoretische Quote:      {stats['theoretische_auszahlungsquote']:.4f}\n")
        self.stat_text.insert(END, f"Fair (±5%):              {'✓ JA' if stats['fair'] else '✗ NEIN'}\n\n")

        self.stat_text.insert(END, "─" * 50 + "\n")
        self.stat_text.insert(END, "TREFFERVERTEILUNG\n")
        self.stat_text.insert(END, "─" * 50 + "\n")
        self.stat_text.insert(END, f"{'Treffer':<10} {'Empirisch':<15} {'Theoretisch':<15}\n")
        self.stat_text.insert(END, "─" * 50 + "\n")

        for i in range(4):
            emp = stats['empirische_trefferverteilung'][i]
            theo = stats['theoretische_trefferverteilung'][i]
            self.stat_text.insert(END, f"{i:<10} {emp:>6.2%}         {theo:>6.2%}\n")

        self.stat_text.insert(END, "\n")
        self.stat_text.insert(END, "─" * 50 + "\n")
        self.stat_text.insert(END, "SPIELER-FEELING\n")
        self.stat_text.insert(END, "─" * 50 + "\n")
        self.stat_text.insert(END, f"Aktuelles Feeling:       {sim_player.getFeeling().upper()} {self.get_emotion_emoji(sim_player.getFeeling())}\n")
        self.stat_text.insert(END, "\n═" * 50 + "\n")

# App starten
if __name__ == "__main__":
    GUI()

