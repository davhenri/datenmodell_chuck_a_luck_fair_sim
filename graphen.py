from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:  # pragma: no cover - Laufzeitabhaengig von lokaler Installation.
    plt = None


def graphen_verfuegbar():
    """Prueft, ob matplotlib fuer die Grapherstellung verfuegbar ist."""
    return plt is not None


def _kumulierte_werte(werte):
    kumuliert = []
    laufend = 0
    for wert in werte:
        laufend += wert
        kumuliert.append(laufend)
    return kumuliert


def _format_delta(delta):
    vorzeichen = "+" if delta >= 0 else ""
    return f"{vorzeichen}{delta:.1f}$"


def _annotiere_balken(ax, balken, deltas):
    for balken_obj, delta in zip(balken, deltas):
        hoehe = balken_obj.get_height()
        x = balken_obj.get_x() + balken_obj.get_width() / 2
        ax.text(
            x,
            hoehe + 0.01,
            _format_delta(delta),
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold",
            color="#1f2937",
        )


def erstelle_auswertungsgraphen(spieler, spielfeld, output_dir="graphen", datei_praefix="simulation"):
    """Erstellt Diagramme zur Spiel- und Fairnessauswertung als PNG-Dateien.

    Returns:
        list[str]: Dateipfade der erzeugten Diagramme.
    """
    if not graphen_verfuegbar():
        raise RuntimeError(
            "Grapherstellung nicht moeglich: 'matplotlib' ist nicht installiert."
        )

    verlauf = spieler.getVerlauf()
    if not verlauf:
        return []

    zielordner = Path(output_dir)
    zielordner.mkdir(parents=True, exist_ok=True)

    runden = [eintrag["runde"] for eintrag in verlauf]
    netto_werte = [eintrag["netto"] for eintrag in verlauf]
    kum_netto = _kumulierte_werte(netto_werte)
    vermoegen = [spieler.start_geld + wert for wert in kum_netto]

    auszahlungen = [eintrag["auszahlung"] for eintrag in verlauf]
    einsaetze = [eintrag["einsatz"] for eintrag in verlauf]
    kum_auszahlung = _kumulierte_werte(auszahlungen)
    kum_einsatz = _kumulierte_werte(einsaetze)
    laufende_quote = [
        (kum_auszahlung[i] / kum_einsatz[i]) if kum_einsatz[i] > 0 else 0.0
        for i in range(len(runden))
    ]

    stats = spielfeld.fairnessStatistik()
    emp = [stats["empirische_trefferverteilung"][k] for k in (0, 1, 2, 3)]
    theo = [stats["theoretische_trefferverteilung"][k] for k in (0, 1, 2, 3)]
    runden_gesamt = stats["runden"]

    # Netto pro Trefferklasse bei Einsatz = 1 Dollar nach aktueller Regel:
    # 0 Treffer: -1 | 1 Treffer: +1 | 2 Treffer: +2 | 3 Treffer: +3
    netto_pro_treffer = [-1, 1, 2, 3]
    emp_deltas = [runden_gesamt * emp[i] * netto_pro_treffer[i] for i in range(4)]
    theo_deltas = [runden_gesamt * theo[i] * netto_pro_treffer[i] for i in range(4)]

    dateien = []

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(runden, vermoegen, color="#0b61a4", linewidth=2.2, label="Vermoegen")
    ax.plot(runden, kum_netto, color="#ff6f00", linewidth=1.8, label="Kumuliertes Netto")
    ax.set_title("Spielverlauf: Vermoegen und Netto")
    ax.set_xlabel("Runde")
    ax.set_ylabel("Dollar")
    ax.grid(alpha=0.25)
    ax.legend()
    pfad = zielordner / f"{datei_praefix}_verlauf.png"
    fig.tight_layout()
    fig.savefig(pfad, dpi=150)
    plt.close(fig)
    dateien.append(str(pfad))

    fig, ax = plt.subplots(figsize=(9, 5))
    x = [0, 1, 2, 3]
    balken = ax.bar(x, emp, width=0.6, color="#2c7fb8", label="Empirisch")
    _annotiere_balken(ax, balken, emp_deltas)
    ax.set_title("Trefferverteilung: Nur empirisch")
    ax.set_xlabel("Treffer pro Runde")
    ax.set_ylabel("Wahrscheinlichkeit")
    ax.set_xticks(x)
    ax.set_ylim(0, max(emp) * 1.3)
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    ax.text(
        0.01,
        0.97,
        f"Labels ueber Balken: Gewinn/Verlustbeitrag bei {runden_gesamt} Runden",
        transform=ax.transAxes,
        fontsize=9,
        va="top",
        color="#374151",
    )
    pfad = zielordner / f"{datei_praefix}_treffer_empirisch.png"
    fig.tight_layout()
    fig.savefig(pfad, dpi=150)
    plt.close(fig)
    dateien.append(str(pfad))

    fig, ax = plt.subplots(figsize=(9, 5))
    x = [0, 1, 2, 3]
    breite = 0.38
    balken_emp = ax.bar(
        [i - breite / 2 for i in x],
        emp,
        width=breite,
        color="#2c7fb8",
        label="Empirisch",
    )
    balken_theo = ax.bar(
        [i + breite / 2 for i in x],
        theo,
        width=breite,
        color="#fdae61",
        label="Theoretisch",
    )
    _annotiere_balken(ax, balken_emp, emp_deltas)
    _annotiere_balken(ax, balken_theo, theo_deltas)
    ax.set_title("Trefferverteilung: Empirisch vs. Theoretisch")
    ax.set_xlabel("Treffer pro Runde")
    ax.set_ylabel("Wahrscheinlichkeit")
    ax.set_xticks(x)
    ax.set_ylim(0, max(max(emp), max(theo)) * 1.35)
    ax.grid(axis="y", alpha=0.25)
    ax.legend()
    ax.text(
        0.01,
        0.97,
        f"Labels ueber Balken: Gewinn/Verlustbeitrag bei {runden_gesamt} Runden",
        transform=ax.transAxes,
        fontsize=9,
        va="top",
        color="#374151",
    )
    pfad = zielordner / f"{datei_praefix}_trefferverteilung.png"
    fig.tight_layout()
    fig.savefig(pfad, dpi=150)
    plt.close(fig)
    dateien.append(str(pfad))

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(runden, laufende_quote, color="#1a9850", linewidth=2.2, label="Laufende Auszahlungsquote")
    ax.axhline(1.0, color="#d73027", linestyle="--", linewidth=1.8, label="Fairnesslinie (1.0)")
    ax.set_title("Fairnessverlauf: Laufende Auszahlungsquote")
    ax.set_xlabel("Runde")
    ax.set_ylabel("Quote")
    ax.grid(alpha=0.25)
    ax.legend()
    pfad = zielordner / f"{datei_praefix}_fairnessverlauf.png"
    fig.tight_layout()
    fig.savefig(pfad, dpi=150)
    plt.close(fig)
    dateien.append(str(pfad))

    return dateien
