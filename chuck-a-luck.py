import spieler, spielfeld, wuerfel

from tkinter import *

class GUI:
    def __init__(self):
        # Zustände und Widgets als Instanzattribute
        self.mode = "start"

        # Hauptfenster
        self.gui = Tk()
        self.gui.title("Chuck-A-Luck")
        self.gui.geometry("1000x800")

        # Haupt-Frame
        self.frameGUI = Frame(master=self.gui, bg="#F5F5F5")
        self.frameGUI.place(x=0, y=0, width=1000, height=800)

        # Start-Ansicht aufbauen
        self.build_start_view()

        # Ereignisschleife starten
        self.gui.mainloop()

    def build_start_view(self):
        # Optional: vorherige Inhalte entfernen, falls du später umschaltest
        for w in self.frameGUI.winfo_children():
            w.destroy()

        # Titel
        label_title = Label(
            master=self.frameGUI,
            bg=self.frameGUI.cget("bg"),
            font=("Arial", 30),
            text="CHUCK-A-LUCK",
        )
        label_title.place(relx=0.5, rely=0.25, anchor="center")

        # Container für Buttons
        button_frame = Frame(master=self.frameGUI, bg=self.frameGUI.cget("bg"))
        button_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Buttons
        btn_feeling = Button(
            master=button_frame,
            text="Feeling",
            width=16,
            height=2,
            command=self.mode_feeling,  # keine Anführungszeichen!
        )
        btn_feeling.grid(row=0, column=0, padx=20, pady=10)

        btn_stat = Button(
            master=button_frame,
            text="Statistik",
            width=16,
            height=2,
            command=self.mode_statistic,  # keine Anführungszeichen!
        )
        btn_stat.grid(row=0, column=1, padx=20, pady=10)

    def mode_feeling(self):
        # Beispiel: Modus setzen und View wechseln
        self.mode = "feeling"
        self.show_info("Modus: Feeling (hier weitere Widgets aufbauen)")

    def mode_statistic(self):
        self.mode = "statistic"
        self.show_info("Modus: Statistik (hier Statistik-UI aufbauen)")

    def show_info(self, text: str):
        # Einfache Beispiel-Ansicht, wie man umschaltet
        for w in self.frameGUI.winfo_children():
            w.destroy()
        Label(self.frameGUI, bg=self.frameGUI.cget("bg"), font=("Arial", 18), text=text).place(
            relx=0.5, rely=0.5, anchor="center"
        )
        Button(self.frameGUI, text="Zurück", command=self.build_start_view).place(
            relx=0.5, rely=0.65, anchor="center"
        )

# App starten
if __name__ == "__main__":
    GUI()

