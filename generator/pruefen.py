"""Prüfung von Varianten und Strategieprofilen.

Zwei Ebenen:
  Fehler   = Datei wird nicht übergeben (Schema verletzt, doppelte Kennung, Zeichen, die den CSV-Import brechen).
  Hinweise = fachlich auffällig, Datei bleibt nutzbar (z. B. Umsatz passt nicht zu Absatz × Preis).
"""
from __future__ import annotations

from jsonschema import Draft202012Validator, FormatChecker

import felder as fd

# Der CSV-Import des Prototyps trennt an Komma UND Semikolon und kennt keine Anführungszeichen.
VERBOTENE_ZEICHEN = [",", ";", "\n", "\r", '"']
UMSATZ_TOLERANZ_REL = 0.02
UMSATZ_TOLERANZ_ABS = 0.1  # Tsd. EUR


def _schema_fehler(daten, schema, was: str) -> list[str]:
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    meldungen = []
    for e in sorted(validator.iter_errors(daten), key=lambda e: list(e.absolute_path)):
        pfad = list(e.absolute_path)
        ort = was
        if pfad and isinstance(pfad[0], int):
            zeile = daten[pfad[0]] if isinstance(daten, list) and pfad[0] < len(daten) else {}
            name = zeile.get("Variante") or zeile.get("Strategie") if isinstance(zeile, dict) else None
            ort = f"{was} {pfad[0] + 1}" + (f" ({name})" if name else "")
            if len(pfad) > 1:
                ort += f", Feld {pfad[1]}"
        meldungen.append(f"{ort}: {e.message}")
    return meldungen


def _zeichen_fehler(zeilen: list[dict], was: str) -> list[str]:
    meldungen = []
    for i, z in enumerate(zeilen, 1):
        if not isinstance(z, dict):
            continue
        for k, v in z.items():
            if isinstance(v, str):
                treffer = [c for c in VERBOTENE_ZEICHEN if c in v]
                if treffer:
                    zeichen = " ".join(repr(c) for c in treffer)
                    meldungen.append(f"{was} {i}, Feld {k}: enthält {zeichen} – das bricht den CSV-Import des Prototyps.")
    return meldungen


def pruefe_varianten(varianten: list[dict]) -> tuple[list[str], list[str]]:
    fehler = _schema_fehler(varianten, fd.schema_varianten(), "Variante")
    hinweise: list[str] = []
    if not isinstance(varianten, list):
        return fehler, hinweise
    fehler += _zeichen_fehler(varianten, "Variante")

    gesehen: dict[str, int] = {}
    for i, v in enumerate(varianten, 1):
        if not isinstance(v, dict):
            continue
        vid = v.get("Variante")
        if isinstance(vid, str):
            if vid in gesehen:
                fehler.append(f"Variante {i} ({vid}): Kennung doppelt, bereits in Zeile {gesehen[vid]}.")
            gesehen.setdefault(vid, i)

        umsatz, absatz, preis = v.get("Umsatz_TEUR"), v.get("Absatz_Stk"), v.get("Preis_EUR")
        if all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in (umsatz, absatz, preis)):
            erwartet = absatz * preis / 1000
            if abs(erwartet - umsatz) > max(UMSATZ_TOLERANZ_ABS, UMSATZ_TOLERANZ_REL * umsatz):
                hinweise.append(f"Variante {i} ({vid}): Umsatz_TEUR = {umsatz}, aber Absatz_Stk × Preis_EUR / 1000 = {erwartet:.1f}.")

        kunden, anteil = v.get("Anzahl_Kunden"), v.get("Hauptkunde_Anteil_Pct")
        if kunden == 1 and anteil is not None and anteil != 100:
            hinweise.append(f"Variante {i} ({vid}): nur ein Kunde, aber Hauptkunde_Anteil_Pct = {anteil} statt 100.")
        if kunden == 0 and (absatz or 0) > 0:
            hinweise.append(f"Variante {i} ({vid}): Absatz vorhanden, aber Anzahl_Kunden = 0.")
        if v.get("Status") == "Auslauf" and v.get("Must_Have") is True:
            hinweise.append(f"Variante {i} ({vid}): Auslauf und Must_Have zugleich – der Prototyp behält sie, wenn Kernmärkte geschützt sind.")
    return fehler, hinweise


def pruefe_strategieprofile(profile: list[dict]) -> tuple[list[str], list[str]]:
    fehler = _schema_fehler(profile, fd.schema_strategieprofile(), "Profil")
    hinweise: list[str] = []
    if not isinstance(profile, list):
        return fehler, hinweise
    fehler += _zeichen_fehler(profile, "Profil")

    namen = [p.get("Strategie") for p in profile if isinstance(p, dict)]
    for n in sorted({n for n in namen if namen.count(n) > 1 and n}):
        fehler.append(f"Strategie {n} kommt mehrfach vor.")
    fehlend = [s for s in fd.STRATEGIEN if s not in namen]
    if fehlend:
        hinweise.append("Noch kein Profil für: " + ", ".join(fehlend) + ".")

    feld_zu_regler = {f["name"]: f["prototyp_id"] for f in fd.STRATEGIEPROFILE["felder"] if f["prototyp_id"]}
    for p in profile:
        if not isinstance(p, dict):
            continue
        for feld, regler in feld_zu_regler.items():
            if regler not in fd.PROTOTYP_REGLER:
                continue
            wert = p.get(feld)
            if not isinstance(wert, int) or isinstance(wert, bool):
                continue
            lo, hi, schritt = fd.PROTOTYP_REGLER[regler]
            if wert < lo or wert > hi or (wert - lo) % schritt:
                hinweise.append(f"Profil {p.get('Strategie')}: {feld} = {wert} lässt sich am Regler des Prototyps "
                                f"nicht einstellen (Bereich {lo}–{hi}, Schritt {schritt}).")
    return fehler, hinweise
