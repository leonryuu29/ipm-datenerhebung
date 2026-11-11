"""Technischer Testdatensatz v0.1 (SYNTHETIC).

Erfundene Werte, nur zum Testen von Schema, Vorlage, Konverter und Prototyp.
Fachlich NICHT abgestimmt – der fachliche Datensatz kommt aus D2/D5 (Jonas).

Eingebaute Testszenarien:
  T1  Sondergröße für einen einzigen Großkunden mit niedriger Marge (K08)
  T2  nahezu identische Größe neben einem Bestseller (K03 neben K02)
  T3  Auslaufvariante mit schwacher und mit guter Marge (K10, K11)
  T4  Zukunftsvariante mit schwacher und mit guter Marge (K12, K13)
  T5  Kleinserie mit sehr hohem Rüstaufwand (K09)
  T6  stärkere Welle als nötig, Kandidat für Überspezifikation (K14 neben K02)
"""
from __future__ import annotations

SPALTEN = ["Variante", "Bezeichnung", "FEFCO_Typ", "Laenge_mm", "Breite_mm", "Hoehe_mm", "Wellenart", "Druck",
           "Preis_EUR", "Absatz_Stk", "Marge_Pct", "Ruestkosten_Index", "Status", "Must_Have",
           "Anzahl_Kunden", "Hauptkunde_Anteil_Pct", "Variantenbildung_Schritt", "Bemerkung"]

_ROH = [
    ("K01_0201_200x150x100_B", "Faltkarton 200x150x100 B-Welle", "0201", 200, 150, 100, "B", "ohne", 0.32, 620000, 24, 2, "Standard", True, 62, 8, "Zuschnitt", "Bestseller"),
    ("K02_0201_300x200x150_B", "Faltkarton 300x200x150 B-Welle", "0201", 300, 200, 150, "B", "ohne", 0.45, 510000, 26, 2, "Standard", True, 45, 9, "Zuschnitt", "Bestseller"),
    ("K03_0201_305x200x150_B", "Faltkarton 305x200x150 B-Welle", "0201", 305, 200, 150, "B", "ohne", 0.47, 38000, 13, 4, "Standard", False, 3, 71, "Zuschnitt", "T2 nahezu identisch mit K02"),
    ("K04_0201_400x300x200_BC", "Faltkarton 400x300x200 BC-Welle", "0201", 400, 300, 200, "BC", "ohne", 0.98, 240000, 22, 3, "Standard", True, 28, 14, "Wellpappe", ""),
    ("K05_0201_600x400x400_BC", "Faltkarton 600x400x400 BC-Welle", "0201", 600, 400, 400, "BC", "ohne", 1.85, 95000, 19, 3, "Standard", False, 17, 22, "Wellpappe", ""),
    ("K06_0427_250x175x80_E_1c", "Versandschachtel 250x175x80 E-Welle 1-farbig", "0427", 250, 175, 80, "E", "1-farbig", 0.62, 180000, 31, 5, "Standard", False, 21, 18, "Druck", ""),
    ("K07_0427_310x220x100_E_4c", "Versandschachtel 310x220x100 E-Welle 4-farbig", "0427", 310, 220, 100, "E", "4-farbig", 1.10, 60000, 35, 8, "Standard", False, 6, 40, "Druck", "hoher Rüstaufwand durch Vierfarbdruck"),
    ("K08_0201_347x253x118_B_SG", "Faltkarton Sondergröße 347x253x118 B-Welle", "0201", 347, 253, 118, "B", "ohne", 0.52, 310000, 11, 6, "Sonderlocke", False, 1, 100, "Zuschnitt", "T1 Sondergröße für einen Großkunden"),
    ("K09_0421_180x130x60_E", "Aufrichteschachtel 180x130x60 E-Welle", "0421", 180, 130, 60, "E", "2-farbig", 0.95, 900, 7, 9, "Sonderlocke", False, 1, 100, "Stanzen", "T5 Kleinserie"),
    ("K10_0203_300x200x100_C", "Faltkarton 300x200x100 C-Welle", "0203", 300, 200, 100, "C", "ohne", 0.55, 22000, 12, 5, "Auslauf", False, 4, 55, "Wellpappe", "T3 Auslauf mit schwacher Marge"),
    ("K11_0201_250x200x150_C", "Faltkarton 250x200x150 C-Welle", "0201", 250, 200, 150, "C", "ohne", 0.41, 70000, 21, 3, "Auslauf", False, 9, 30, "Wellpappe", "T3 Auslauf mit guter Marge"),
    ("K12_0427_250x175x80_E_GP", "Versandschachtel 250x175x80 E-Welle Graspapier", "0427", 250, 175, 80, "E", "ohne", 0.78, 14000, 9, 7, "Zukunft", False, 3, 60, "Wellpappe", "T4 Zukunft mit schwacher Marge"),
    ("K13_0711_300x200x150_B_AB", "Faltkarton mit Automatikboden 300x200x150 B-Welle", "0711", 300, 200, 150, "B", "ohne", 0.66, 26000, 28, 7, "Zukunft", False, 5, 35, "Kleben", "T4 Zukunft mit guter Marge"),
    ("K14_0201_300x200x150_EB", "Faltkarton 300x200x150 EB-Welle", "0201", 300, 200, 150, "EB", "ohne", 0.58, 48000, 17, 4, "Standard", False, 7, 33, "Wellpappe", "T6 wie K02 mit stärkerer Welle"),
]


def varianten() -> list[dict]:
    zeilen = []
    for roh in _ROH:
        z = dict(zip(SPALTEN, roh))
        z["Umsatz_TEUR"] = round(z["Absatz_Stk"] * z["Preis_EUR"] / 1000, 1)
        if not z["Bemerkung"]:
            del z["Bemerkung"]
        zeilen.append(z)
    return zeilen


def strategieprofile() -> list[dict]:
    """Technischer Vorschlag je Strategie. Fachlich zu prüfen (D2)."""
    return [
        dict(Strategie="Massenproduzent", Beschreibung="Wenige Standardgrößen in hoher Stückzahl",
             Min_Umsatzabdeckung_Pct=85, Kernmaerkte_schuetzen=True, Entkopplungspunkt="MTS", Max_Ruestkosten_Index=4,
             Ueberspezifikation_erlaubt=True, Min_Marge_Pct=15, Min_Absatz_Stk=1500, Ziel_Gleichteilequote_Pct=80,
             Sourcing="Single", Zukunft_schuetzen=False, Auslauf_streichen=True),
        dict(Strategie="Kostenführer", Beschreibung="Niedrigste Stückkosten und strenge Margenziele",
             Min_Umsatzabdeckung_Pct=80, Kernmaerkte_schuetzen=True, Entkopplungspunkt="MTS", Max_Ruestkosten_Index=3,
             Ueberspezifikation_erlaubt=True, Min_Marge_Pct=20, Min_Absatz_Stk=1500, Ziel_Gleichteilequote_Pct=85,
             Sourcing="Single", Zukunft_schuetzen=False, Auslauf_streichen=True),
        dict(Strategie="Innovationsführer", Beschreibung="Neue Konstruktionen und Materialien werden geschützt",
             Min_Umsatzabdeckung_Pct=90, Kernmaerkte_schuetzen=True, Entkopplungspunkt="ATO", Max_Ruestkosten_Index=8,
             Ueberspezifikation_erlaubt=False, Min_Marge_Pct=18, Min_Absatz_Stk=500, Ziel_Gleichteilequote_Pct=50,
             Sourcing="Dual", Zukunft_schuetzen=True, Auslauf_streichen=True),
        dict(Strategie="Nischenanbieter", Beschreibung="Kundenspezifische Lösungen in kleinen Mengen",
             Min_Umsatzabdeckung_Pct=95, Kernmaerkte_schuetzen=True, Entkopplungspunkt="ETO", Max_Ruestkosten_Index=9,
             Ueberspezifikation_erlaubt=False, Min_Marge_Pct=25, Min_Absatz_Stk=0, Ziel_Gleichteilequote_Pct=30,
             Sourcing="Dual", Zukunft_schuetzen=True, Auslauf_streichen=False),
    ]
