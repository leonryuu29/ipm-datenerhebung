"""Wandelt die ausgefüllte Excel-Vorlage in Dateien für den Prototyp um.

Aufruf:
    python generator/excel_zu_prototyp.py <vorlage.xlsx> --out <zielordner>

Ergebnis im Zielordner:
    varianten.csv            für den Upload im Prototyp (Komma als Trenner, Dezimalpunkt, true/false)
    varianten.json           dieselben Daten als JSON (Upload im Prototyp, Schema varianten)
    strategieprofile.json    die Strategieprofile (Schema strategieprofile)
    pruefbericht.txt         Fehler und Hinweise der Prüfung

Bei Fehlern werden keine Daten geschrieben (Rückgabewert 1).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

from openpyxl import load_workbook

import felder as fd
import pruefen

ERSTE_DATENZEILE = 3
BEISPIEL_PRAEFIX = "BEISPIEL"
WAHR = {"ja", "true", "wahr", "1", "x", "yes"}
FALSCH = {"nein", "false", "falsch", "0", "no"}
# Andere Schreibweisen von Spaltenköpfen, die in ausgefüllten Vorlagen vorkommen.
SPALTEN_ALIAS = {"RAJA-Artikelnr.": "Referenz_Artikelnr", "RAJA-Artikelnr": "Referenz_Artikelnr", "Artikelnr.": "Referenz_Artikelnr"}


class Lesefehler(Exception):
    pass


def _wandle(wert, feld: dict, ort: str):
    """Zellwert in den Typ des Feldes umwandeln. None = leer."""
    if wert is None:
        return None
    if isinstance(wert, str):
        wert = wert.strip()
        if wert == "":
            return None
    typ = feld["typ"]
    if typ == "boolean":
        if isinstance(wert, bool):
            return wert
        t = str(wert).strip().lower()
        if t in WAHR:
            return True
        if t in FALSCH:
            return False
        raise Lesefehler(f"{ort}: '{wert}' ist kein ja/nein-Wert.")
    if typ in ("integer", "number"):
        if isinstance(wert, bool):
            raise Lesefehler(f"{ort}: Zahl erwartet, Wahrheitswert gefunden.")
        if isinstance(wert, str):
            text = wert.replace(" ", "")
            if "," in text and "." in text:
                raise Lesefehler(f"{ort}: '{wert}' ist als Zahl nicht eindeutig (Punkt und Komma).")
            try:
                wert = float(text.replace(",", "."))
            except ValueError:
                raise Lesefehler(f"{ort}: '{wert}' ist keine Zahl.") from None
        if typ == "integer":
            if float(wert) != int(wert):
                raise Lesefehler(f"{ort}: ganze Zahl erwartet, gefunden {wert}.")
            return int(wert)
        wert = float(wert)
        return int(wert) if wert == int(wert) else round(wert, 6)
    if typ == "date":
        return wert.strftime("%Y-%m-%d") if hasattr(wert, "strftime") else str(wert)
    if isinstance(wert, float) and wert == int(wert):
        wert = int(wert)
    text = str(wert)
    if feld["name"] == "FEFCO_Typ" and text.isdigit():
        text = text.zfill(4)
    return text


def lies_varianten(wb) -> tuple[list[dict], list[str], list[str]]:
    if "Varianten" not in wb.sheetnames:
        raise Lesefehler("Blatt 'Varianten' fehlt.")
    ws = wb["Varianten"]
    felder = {f["name"]: f for f in fd.VARIANTEN["felder"]}
    kopf = {}
    hinweise, fehler = [], []
    for c in ws[1]:
        if c.value is None:
            continue
        name = str(c.value).strip()
        name = SPALTEN_ALIAS.get(name, name)
        if name.startswith("Pruef_"):
            continue
        if name not in felder:
            fehler.append(f"Blatt Varianten, Spalte {c.column_letter}: unbekanntes Feld '{name}'.")
            continue
        kopf[c.column] = felder[name]
    fehlend = [f["name"] for f in fd.VARIANTEN["felder"] if f["pflicht"] and f["name"] not in [x["name"] for x in kopf.values()]]
    if fehlend:
        fehler.append("Blatt Varianten: Pflichtspalten fehlen: " + ", ".join(fehlend) + ".")
    zeilen, beispiele = [], 0
    for r in range(ERSTE_DATENZEILE, ws.max_row + 1):
        roh = {sp: ws.cell(row=r, column=sp).value for sp in kopf}
        if all(v is None or (isinstance(v, str) and not v.strip()) for v in roh.values()):
            continue
        z = {}
        for sp, feld in kopf.items():
            try:
                w = _wandle(roh[sp], feld, f"Blatt Varianten, Zeile {r}, Feld {feld['name']}")
            except Lesefehler as e:
                fehler.append(str(e))
                continue
            if w is not None:
                z[feld["name"]] = w
        if str(z.get("Bemerkung", "")).upper().startswith(BEISPIEL_PRAEFIX):
            beispiele += 1
            continue
        zeilen.append(z)
    if beispiele:
        hinweise.append(f"{beispiele} Beispielzeile(n) übersprungen (Bemerkung beginnt mit {BEISPIEL_PRAEFIX}).")
    return zeilen, fehler, hinweise


def lies_strategieprofile(wb) -> tuple[list[dict], list[str], list[str]]:
    if "Strategieprofile" not in wb.sheetnames:
        return [], [], ["Blatt 'Strategieprofile' fehlt – es werden keine Profile übergeben."]
    ws = wb["Strategieprofile"]
    felder = {f["name"]: f for f in fd.STRATEGIEPROFILE["felder"]}
    fehler, hinweise, profile = [], [], []
    zeile_von = {}
    for r in range(2, ws.max_row + 1):
        name = ws.cell(row=r, column=1).value
        if isinstance(name, str) and name.strip() in felder:
            zeile_von[name.strip()] = r
    for sp in range(4, ws.max_column + 1):
        p = {}
        for name, r in zeile_von.items():
            try:
                w = _wandle(ws.cell(row=r, column=sp).value, felder[name], f"Blatt Strategieprofile, Spalte {ws.cell(row=1, column=sp).column_letter}, Feld {name}")
            except Lesefehler as e:
                fehler.append(str(e))
                continue
            if w is not None:
                p[name] = w
        if set(p) - {"Strategie"}:
            profile.append(p)
    return profile, fehler, hinweise


def csv_text(varianten: list[dict]) -> str:
    """CSV so, wie sie der Prototyp liest: Komma, Dezimalpunkt, true/false, keine Anführungszeichen."""
    spalten = [f["name"] for f in fd.VARIANTEN["felder"] if any(f["name"] in v for v in varianten)]
    puffer = io.StringIO()
    w = csv.writer(puffer, delimiter=",", lineterminator="\n", quoting=csv.QUOTE_NONE, escapechar=None)
    w.writerow(spalten)
    for v in varianten:
        zeile = []
        for s in spalten:
            x = v.get(s, "")
            if isinstance(x, bool):
                x = "true" if x else "false"
            zeile.append(x)
        w.writerow(zeile)
    return puffer.getvalue()


def wandle_um(excel: Path, ziel: Path) -> tuple[int, str]:
    wb = load_workbook(excel, data_only=True)
    fehler, hinweise = [], []
    try:
        varianten, f1, h1 = lies_varianten(wb)
        profile, f2, h2 = lies_strategieprofile(wb)
        fehler += f1 + f2
        hinweise += h1 + h2
    except Lesefehler as e:
        varianten, profile = [], []
        fehler.append(str(e))
    if not fehler:
        if not varianten:
            fehler.append("Blatt Varianten enthält keine Varianten (Beispielzeilen zählen nicht).")
        else:
            f, h = pruefen.pruefe_varianten(varianten)
            fehler += f
            hinweise += h
        if profile:
            f, h = pruefen.pruefe_strategieprofile(profile)
            fehler += f
            hinweise += h

    kopf = [f"Prüfbericht für {excel.name}", f"Schema v{fd.VERSION} · Kennzeichnung {fd.KENNZEICHNUNG}",
            f"Varianten gelesen: {len(varianten)} · Strategieprofile gelesen: {len(profile)}", ""]
    kopf.append(f"FEHLER ({len(fehler)})")
    kopf += [f"  - {m}" for m in fehler] or ["  keine"]
    kopf.append("")
    kopf.append(f"HINWEISE ({len(hinweise)})")
    kopf += [f"  - {m}" for m in hinweise] or ["  keine"]
    kopf.append("")
    kopf.append("ERGEBNIS: " + ("nicht übergeben – bitte Fehler beheben." if fehler else "Dateien geschrieben."))
    bericht = "\n".join(kopf) + "\n"

    ziel.mkdir(parents=True, exist_ok=True)
    (ziel / "pruefbericht.txt").write_text(bericht, encoding="utf-8")
    if fehler:
        return 1, bericht
    (ziel / "varianten.csv").write_text(csv_text(varianten), encoding="utf-8", newline="")
    (ziel / "varianten.json").write_text(json.dumps(varianten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if profile:
        (ziel / "strategieprofile.json").write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0, bericht


def main(argv=None) -> int:
    """Einstieg für die Kommandozeile."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Excel-Vorlage in CSV/JSON für den Prototyp umwandeln.")
    ap.add_argument("excel", type=Path)
    ap.add_argument("--out", type=Path, required=True, help="Zielordner")
    a = ap.parse_args(argv)
    try:
        code, bericht = wandle_um(a.excel, a.out)
    except PermissionError as e:
        print(f"Kann {e.filename} nicht öffnen oder schreiben: Die Datei ist vermutlich in Excel geöffnet. Bitte schließen.\n"
              f"无法读写 {e.filename}：文件可能正在 Excel 里打开，请关闭后再运行。")
        return 2
    except FileNotFoundError as e:
        print(f"Datei nicht gefunden: {e.filename}\n找不到文件：{e.filename}")
        return 2
    print(bericht)
    return code


if __name__ == "__main__":
    sys.exit(main())
