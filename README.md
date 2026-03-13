# Chuck-A-Luck Game Simulator

Ein interaktives Chuck-A-Luck Würfelspiel mit grafischer Benutzeroberfläche (GUI) und statistischer Analyse.

## Über das Spiel

Chuck-A-Luck ist ein klassisches Würfelspiel, bei dem der Spieler auf eine Zahl (1-6) setzt und drei Würfel geworfen werden. Die Auszahlung hängt davon ab, wie oft die gewählte Zahl erscheint:

- **0 Treffer**: $0 (Verlust von $1)
- **1 Treffer**: $2 (Gewinn von $1)
- **2 Treffer**: $3 (Gewinn von $2)
- **3 Treffer**: $4 (Gewinn von $3)

## Installation

### Voraussetzungen

- Python 3.7 oder höher
- pip (Python Package Manager)

### Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

## Spiel starten

```bash
python3 chuck-a-luck.py
```

## Spielmodi

### 1. FEEL IT! Mode 🎮 (Manuelles Spielen)

Der interaktive Spielmodus bietet:

- **3x2 Spielfeld**: Klicke auf eines der sechs Felder, um deinen Einsatz zu platzieren
- **Drei Würfel**: Sehe die geworfenen Würfel in Echtzeit
- **Emotion-Display**: Dein aktuelles "Feeling" basierend auf deiner Spielperformance:
  - 😐 **Neutral**: Ausgeglichener Spielstand
  - 🙂 **Optimistisch**: Leichte Gewinne
  - 🤩 **Euphorisch**: Große Gewinne oder Gewinnsträhne
  - 😤 **Frustriert**: Mehrere Verluste und negative Bilanz
  - 😰 **Angespannt**: Negative Gesamtbilanz

- **Spielerinformationen**:
  - 💰 Verfügbares Geld
  - 📊 Gesamtbilanz (Gewinn/Verlust)
  - 🎲 Anzahl gespielter Runden

- **Visuelles Feedback**:
  - ✅ **Grüner Blitz**: Bei jedem Gewinn
  - ❌ **Roter Blitz**: Bei jedem Verlust

### 2. STATISTIK Mode 📊 (Theoretisches Spiel)

Der Statistik-Modus ermöglicht:

- **Simulation**: Führe automatisierte Spielrunden durch
- **Anpassbare Parameter**:
  - Anzahl der Runden (Standard: 1000)
  - Startkapital (Standard: $1000)

- **Detaillierte Statistiken**:
  - Endkapital und Netto-Gewinn/Verlust
  - Geldflüsse (Einsätze, Auszahlungen, Hausgewinn)
  - Auszahlungsquoten (empirisch vs. theoretisch)
  - Trefferverteilung (empirisch vs. theoretisch)
  - Fairness-Bewertung
  - Spieler-Feeling am Ende der Simulation

## Projektstruktur

```
.
├── chuck-a-luck.py          # Haupt-GUI Anwendung
├── spieler.py               # Spieler-Klasse (Geld, Verlauf, Feeling)
├── spielfeld.py             # Spielfeld-Klasse (Spiellogik, Statistik)
├── wuerfel.py               # Würfel-Klasse (Zufallsgenerator)
├── graphen.py               # Visualisierungsfunktionen (matplotlib)
├── requirements.txt         # Python-Abhängigkeiten
├── test_gui.py              # Test-Script für Bildressourcen
├── assets/                  # Bildressourcen
│   ├── wuerfel1-6.png      # Würfelbilder
│   ├── tile_1-6.png        # Spielfeldbilder
│   └── stableCoinEuro.png  # Münz-Icon
├── *.svg                    # Emotion-Icons (SVG)
└── graphen/                 # Generierte Statistik-Graphen
```

## Features

### FEEL IT! Mode
✅ Interaktives 3x2 Spielfeld mit klickbaren Tiles
✅ Echtzeit-Würfelanzeige mit PNG-Bildern
✅ Dynamisches Emotion-Display basierend auf Spielerfolg
✅ Coin-Platzierung und Einsatz-Tracking
✅ Gewinn/Verlust-Anzeige mit visuellen Effekten
✅ Grüner Blitz bei Gewinn, roter Blitz bei Verlust
✅ Vollständige Spielerstatistiken

### STATISTIK Mode
✅ Automatische Spielsimulation
✅ Konfigurierbare Rundenzahl und Startkapital
✅ Umfassende statistische Auswertung
✅ Fairness-Analyse
✅ Trefferverteilungs-Vergleich

## Technische Details

- **GUI Framework**: Tkinter
- **Bildverarbeitung**: Pillow (PIL)
- **Datenvisualisierung**: matplotlib
- **Spiellogik**: Objektorientiertes Python

## Lizenz

CC0 1.0 Universal (Public Domain)

## Autor

Entwickelt für das Chuck-A-Luck Simulationsprojekt
