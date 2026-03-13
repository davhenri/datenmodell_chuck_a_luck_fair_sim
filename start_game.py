#!/usr/bin/env python3
"""
Chuck-A-Luck GUI Anwendung - Startskript

Dieses Skript startet die Chuck-A-Luck GUI-Anwendung.
Stelle sicher, dass alle Abhängigkeiten installiert sind:
    pip install -r requirements.txt

Verwendung:
    python3 start_game.py
"""

import sys
import os

# Prüfe, ob alle erforderlichen Module installiert sind
try:
    from PIL import Image
    import tkinter
except ImportError as e:
    print("❌ FEHLER: Erforderliche Module nicht installiert!")
    print(f"   {e}")
    print("\nBitte installiere die Abhängigkeiten mit:")
    print("   pip install -r requirements.txt")
    sys.exit(1)

# Prüfe, ob alle Bilder vorhanden sind
def check_resources():
    """Prüft, ob alle Bildressourcen vorhanden sind"""
    base_path = os.path.dirname(os.path.abspath(__file__))
    missing = []

    # Prüfe Würfel
    for i in range(1, 7):
        path = os.path.join(base_path, "assets", f"wuerfel{i}.png")
        if not os.path.exists(path):
            missing.append(f"assets/wuerfel{i}.png")

    # Prüfe Tiles
    for i in range(1, 7):
        path = os.path.join(base_path, "assets", f"tile_{i}.png")
        if not os.path.exists(path):
            missing.append(f"assets/tile_{i}.png")

    # Prüfe Coin
    coin_path = os.path.join(base_path, "assets", "stableCoinEuro.png")
    if not os.path.exists(coin_path):
        missing.append("assets/stableCoinEuro.png")

    # Prüfe Emotions
    emotions = ["neutral", "optimistisch", "euphorisch", "frustriert", "angespannt"]
    for emotion in emotions:
        path = os.path.join(base_path, f"{emotion}.svg")
        if not os.path.exists(path):
            missing.append(f"{emotion}.svg")

    if missing:
        print("❌ FEHLER: Folgende Bildressourcen fehlen:")
        for m in missing:
            print(f"   - {m}")
        return False

    return True

if __name__ == "__main__":
    print("🎲 Chuck-A-Luck Spiel wird gestartet...")
    print("=" * 50)

    # Ressourcen prüfen
    if not check_resources():
        print("\n❌ Bitte stelle sicher, dass alle Bildressourcen vorhanden sind.")
        sys.exit(1)

    print("✓ Alle Ressourcen gefunden")
    print("✓ Module geladen")
    print("=" * 50)
    print("\nStarte GUI...\n")

    # GUI starten
    try:
        # Importiere die GUI (führt __main__ aus)
        exec(open("chuck-a-luck.py").read())
    except Exception as e:
        print(f"\n❌ FEHLER beim Starten der GUI:")
        print(f"   {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
