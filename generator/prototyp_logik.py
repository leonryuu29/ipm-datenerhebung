"""Nachbau der Vorab-Bewertung des Prototyps in Python.

Quelle: updateDashboard() in ki_wrapper_variantenmanagement.html (Umsetzung, Stand 10.11.2026).
Zweck: Erwartungswerte für den Browser-Test und schnelle Vorschau, was der Prototyp
mit einem Datensatz und einem Strategieprofil macht.
"""
from __future__ import annotations


def empfehlung(v: dict, p: dict) -> str:
    if p["Kernmaerkte_schuetzen"] and v["Must_Have"]:
        return "Behalten (Schutz: Kernmarkt)"
    if p["Zukunft_schuetzen"] and v["Status"] == "Zukunft":
        return "Behalten (Schutz: R&D Zukunft)"
    if p["Auslauf_streichen"] and v["Status"] == "Auslauf":
        return "Streichen (Auslaufmodell)"
    if v["Marge_Pct"] < p["Min_Marge_Pct"] or v["Absatz_Stk"] < p["Min_Absatz_Stk"]:
        return "Streichen (Finanz-Ziel verfehlt)"
    if v["Ruestkosten_Index"] > p["Max_Ruestkosten_Index"]:
        return "Modularisieren (Rüstkosten zu hoch)"
    return "Behalten (Optimal)"


def bewerte(varianten: list[dict], profil: dict) -> dict:
    entscheidungen = {v["Variante"]: empfehlung(v, profil) for v in varianten}
    behalten = [v for v in varianten if not entscheidungen[v["Variante"]].startswith("Streichen")]
    umsatz = sum(v["Umsatz_TEUR"] for v in varianten)
    umsatz_behalten = sum(v["Umsatz_TEUR"] for v in behalten)
    n = len(varianten)
    return {
        "entscheidungen": entscheidungen,
        "varianten_behalten": len(behalten),
        "varianten_gesamt": n,
        "komplexitaet_reduktion_pct": (n - len(behalten)) / n * 100 if n else 0.0,
        "umsatzabdeckung_pct": umsatz_behalten / umsatz * 100 if umsatz else 0.0,
        "marge_behalten_pct": sum(v["Marge_Pct"] for v in behalten) / len(behalten) if behalten else 0.0,
        "ziel_umsatzabdeckung_pct": profil["Min_Umsatzabdeckung_Pct"],
        "ziel_erreicht": (umsatz_behalten / umsatz * 100 if umsatz else 0.0) >= profil["Min_Umsatzabdeckung_Pct"],
    }
