"""Erzeugt die Excel-Vorlage für die fachliche Datenerfassung (und gefüllte Varianten davon).

Aufruf:  python generator/vorlage_erzeugen.py
Ergebnis: vorlagen/VARIANTEN_VORLAGE_v<VERSION>.xlsx
"""
from __future__ import annotations

import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

import felder as fd
import testdaten

WURZEL = Path(__file__).resolve().parent.parent
ERSTE_DATENZEILE = 3
LETZTE_DATENZEILE = 62
BEISPIEL_PRAEFIX = "BEISPIEL"
BLATT_ERP = "ERP-Datenblöcke (Entwurf)"
PRUEF_SPALTEN = ["Pruef_Umsatz_TEUR", "Pruef_Hinweis"]

DUNKEL, TEAL, HELL, GRAU, GELB = "18323D", "9BC8C4", "F5F4EF", "D9D9D9", "FFF2CC"
SCHRIFT = "Arial"
duenn = Side(style="thin", color="BFBFBF")
RAHMEN = Border(left=duenn, right=duenn, top=duenn, bottom=duenn)


def f(**kw):
    kw.setdefault("name", SCHRIFT)
    kw.setdefault("size", 10)
    return Font(**kw)


def fuell(farbe):
    return PatternFill("solid", start_color=farbe, end_color=farbe)


def hinweis_text(feld: dict) -> str:
    """Kurzer Hinweis für die Zeile unter der Kopfzeile."""
    if feld["typ"] == "boolean":
        return "ja / nein"
    if feld["enum"]:
        return " / ".join(feld["enum"])
    teile = []
    if feld["einheit"]:
        teile.append(feld["einheit"])
    if feld["typ"] == "integer":
        teile.append("ganze Zahl")
    elif feld["typ"] == "number":
        teile.append("Zahl")
    elif feld["typ"] == "date":
        teile.append("JJJJ-MM-TT")
    elif feld["name"] in ("Variante",):
        teile.append("ohne Leerzeichen")
    else:
        teile.append("Text")
    return ", ".join(teile)


def erlaubte_werte(feld: dict) -> str:
    if feld["typ"] == "boolean":
        return "ja / nein"
    if feld["enum"]:
        return " / ".join(feld["enum"])
    if feld["min"] is not None and feld["max"] is not None:
        return f"{feld['min']} bis {feld['max']}"
    if feld["min"] is not None:
        return f"ab {feld['min']}"
    return ""


def typ_de(feld: dict) -> str:
    return {"string": "Text", "integer": "Ganze Zahl", "number": "Zahl", "boolean": "ja/nein", "date": "Datum"}[feld["typ"]]


def zellwert(wert):
    if isinstance(wert, bool):
        return "ja" if wert else "nein"
    return wert


def blatt_listen(wb):
    ws = wb.create_sheet("Listen")
    listen = {
        "Status": fd.STATUS, "JaNein": ["ja", "nein"], "Wellenart": fd.WELLENARTEN, "Druck": fd.DRUCK,
        "Variantenbildung_Schritt": fd.PROZESSSCHRITTE, "Strategie": fd.STRATEGIEN,
        "Entkopplungspunkt": fd.ENTKOPPLUNG, "Sourcing": fd.SOURCING,
    }
    bereiche = {}
    for i, (name, werte) in enumerate(listen.items(), 1):
        c = ws.cell(row=1, column=i, value=name)
        c.font, c.fill = f(bold=True, color="FFFFFF"), fuell(DUNKEL)
        for j, w in enumerate(werte, 2):
            ws.cell(row=j, column=i, value=w).font = f()
        sp = get_column_letter(i)
        bereiche[name] = f"Listen!${sp}$2:${sp}${len(werte) + 1}"
        ws.column_dimensions[sp].width = 24
    ws["A12"] = "Auswahllisten für die Dropdowns. Nicht ändern – Änderungen bitte mit Yu abstimmen (Schema)."
    ws["A12"].font = f(italic=True, color="595959")
    return bereiche


def blatt_varianten(wb, bereiche, zeilen: list[dict], beispiel: bool):
    ws = wb.create_sheet("Varianten")
    felder = fd.VARIANTEN["felder"]
    spalte = {fl["name"]: get_column_letter(i) for i, fl in enumerate(felder, 1)}
    n = len(felder)

    for i, fl in enumerate(felder, 1):
        k = ws.cell(row=1, column=i, value=fl["name"])
        k.font = f(bold=True, color="FFFFFF" if fl["pflicht"] else DUNKEL)
        k.fill = fuell(DUNKEL if fl["pflicht"] else TEAL)
        k.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        k.border = RAHMEN
        text = ("PFLICHT" if fl["pflicht"] else "optional") + " – " + fl["de"]
        if fl["einheit"]:
            text += f"\nEinheit: {fl['einheit']}"
        text += f"\nBeispiel: {zellwert(fl['beispiel'])}"
        k.comment = Comment(text, "Datenerhebung", width=340, height=150)
        h = ws.cell(row=2, column=i, value=hinweis_text(fl))
        h.font, h.fill = f(italic=True, size=8, color="595959"), fuell(HELL)
        h.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        h.border = RAHMEN
    for j, name in enumerate(PRUEF_SPALTEN, n + 1):
        k = ws.cell(row=1, column=j, value=name)
        k.font, k.fill, k.border = f(bold=True, color="404040"), fuell(GRAU), RAHMEN
        k.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        h = ws.cell(row=2, column=j, value="Formel, nicht ausfüllen")
        h.font, h.fill, h.border = f(italic=True, size=8, color="595959"), fuell(GRAU), RAHMEN
        h.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[1].height = 32
    ws.row_dimensions[2].height = 36

    breiten = {"Variante": 30, "Bezeichnung": 44, "Status": 14, "Variantenbildung_Schritt": 20,
               "Hauptkunde_Anteil_Pct": 16, "Ruestkosten_Index": 14, "Referenz_Artikelnr": 18}
    for fl in felder:
        ws.column_dimensions[spalte[fl["name"]]].width = breiten.get(fl["name"], 13)
    ws.column_dimensions[get_column_letter(n + 1)].width = 16
    ws.column_dimensions[get_column_letter(n + 2)].width = 16

    formate = {"Umsatz_TEUR": "#,##0.0", "Preis_EUR": "0.00", "Absatz_Stk": "#,##0", "Marge_Pct": "0.0",
               "Hauptkunde_Anteil_Pct": "0"}
    u, a, p = spalte["Umsatz_TEUR"], spalte["Absatz_Stk"], spalte["Preis_EUR"]
    pu, ph = get_column_letter(n + 1), get_column_letter(n + 2)
    for r in range(ERSTE_DATENZEILE, LETZTE_DATENZEILE + 1):
        for i, fl in enumerate(felder, 1):
            c = ws.cell(row=r, column=i)
            c.font, c.border = f(), RAHMEN
            if fl["name"] in formate:
                c.number_format = formate[fl["name"]]
            if fl["name"] == "FEFCO_Typ":
                c.number_format = "@"
        c1 = ws.cell(row=r, column=n + 1, value=f'=IF(OR({a}{r}="",{p}{r}=""),"",ROUND({a}{r}*{p}{r}/1000,1))')
        c2 = ws.cell(row=r, column=n + 2,
                     value=f'=IF({pu}{r}="","",IF({u}{r}="","Umsatz fehlt",IF(ABS({pu}{r}-{u}{r})>MAX(0.1,0.02*{u}{r}),"Umsatz prüfen","ok")))')
        for c in (c1, c2):
            c.font, c.fill, c.border = f(color="404040"), fuell("F2F2F2"), RAHMEN
        c1.number_format = "#,##0.0"

    for r, z in enumerate(zeilen, ERSTE_DATENZEILE):
        for i, fl in enumerate(felder, 1):
            if fl["name"] in z:
                c = ws.cell(row=r, column=i, value=zellwert(z[fl["name"]]))
                if beispiel:
                    c.font, c.fill = f(italic=True, color="595959"), fuell("EDEDED")

    def liste(feldname, bereich):
        dv = DataValidation(type="list", formula1=f"={bereiche[bereich]}", allow_blank=True)
        dv.error, dv.errorTitle = "Bitte einen Wert aus der Liste wählen.", "Ungültiger Wert"
        dv.showErrorMessage = True
        ws.add_data_validation(dv)
        dv.add(f"{spalte[feldname]}{ERSTE_DATENZEILE}:{spalte[feldname]}{LETZTE_DATENZEILE}")

    liste("Status", "Status"); liste("Wellenart", "Wellenart")
    liste("Druck", "Druck"); liste("Variantenbildung_Schritt", "Variantenbildung_Schritt")

    def zahl(feldname, art, lo, hi=None):
        dv = DataValidation(type=art, operator="between" if hi is not None else "greaterThanOrEqual",
                            formula1=str(lo), formula2=str(hi) if hi is not None else None, allow_blank=True)
        dv.error = f"Erlaubt: {lo} bis {hi}." if hi is not None else f"Erlaubt: ab {lo}."
        dv.errorTitle = "Ungültiger Wert"
        dv.showErrorMessage = True
        ws.add_data_validation(dv)
        dv.add(f"{spalte[feldname]}{ERSTE_DATENZEILE}:{spalte[feldname]}{LETZTE_DATENZEILE}")

    zahl("Ruestkosten_Index", "whole", 1, 10); zahl("Marge_Pct", "decimal", -100, 100)
    zahl("Absatz_Stk", "whole", 0); zahl("Umsatz_TEUR", "decimal", 0); zahl("Preis_EUR", "decimal", 0)
    zahl("Anzahl_Kunden", "whole", 0); zahl("Hauptkunde_Anteil_Pct", "decimal", 0, 100)
    for m in ("Laenge_mm", "Breite_mm", "Hoehe_mm"):
        zahl(m, "whole", 1)

    v = spalte["Variante"]
    dv = DataValidation(type="custom", allow_blank=True,
                        formula1=f"=COUNTIF(${v}${ERSTE_DATENZEILE}:${v}${LETZTE_DATENZEILE},{v}{ERSTE_DATENZEILE})=1")
    dv.error, dv.errorTitle = "Diese Kennung gibt es schon. Jede Variante braucht eine eigene Kennung.", "Kennung doppelt"
    dv.showErrorMessage = True
    ws.add_data_validation(dv)
    dv.add(f"{v}{ERSTE_DATENZEILE}:{v}{LETZTE_DATENZEILE}")

    ws.conditional_formatting.add(
        f"{ph}{ERSTE_DATENZEILE}:{ph}{LETZTE_DATENZEILE}",
        FormulaRule(formula=[f'AND({ph}{ERSTE_DATENZEILE}<>"",{ph}{ERSTE_DATENZEILE}<>"ok")'],
                    font=Font(name=SCHRIFT, size=10, bold=True, color="C00000"), fill=fuell("FCE4D6")))
    ws.freeze_panes = f"B{ERSTE_DATENZEILE}"
    return ws


def blatt_strategieprofile(wb, bereiche, profile: list[dict]):
    ws = wb.create_sheet("Strategieprofile")
    kopf = ["Feld", "Beschreibung", "Erlaubte Werte"] + [f"Profil {i}" for i in range(1, len(fd.STRATEGIEN) + 1)]
    for i, t in enumerate(kopf, 1):
        c = ws.cell(row=1, column=i, value=t)
        c.font, c.fill, c.border = f(bold=True, color="FFFFFF"), fuell(DUNKEL), RAHMEN
        c.alignment = Alignment(horizontal="center", vertical="center")
    listen = {"Strategie": "Strategie", "Entkopplungspunkt": "Entkopplungspunkt", "Sourcing": "Sourcing"}
    for r, fl in enumerate(fd.STRATEGIEPROFILE["felder"], 2):
        a = ws.cell(row=r, column=1, value=fl["name"])
        a.font, a.fill, a.border = f(bold=True, color="FFFFFF" if fl["pflicht"] else DUNKEL), fuell(DUNKEL if fl["pflicht"] else TEAL), RAHMEN
        a.alignment = Alignment(vertical="center")
        b = ws.cell(row=r, column=2, value=fl["de"])
        b.font, b.border, b.alignment = f(size=9), RAHMEN, Alignment(wrap_text=True, vertical="center")
        w = erlaubte_werte(fl) + (f" ({fl['einheit']})" if fl["einheit"] and fl["einheit"] != "1-10" else "")
        c = ws.cell(row=r, column=3, value=w.strip())
        c.font, c.border, c.alignment = f(size=9, italic=True, color="595959"), RAHMEN, Alignment(wrap_text=True, vertical="center")
        for k in range(len(fd.STRATEGIEN)):
            z = ws.cell(row=r, column=4 + k)
            z.font, z.border, z.fill = f(), RAHMEN, fuell(GELB)
            z.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            if k < len(profile) and fl["name"] in profile[k]:
                z.value = zellwert(profile[k][fl["name"]])
        bereich_zeile = f"D{r}:{get_column_letter(3 + len(fd.STRATEGIEN))}{r}"
        if fl["typ"] == "boolean" or fl["name"] in listen:
            dv = DataValidation(type="list", formula1=f"={bereiche['JaNein' if fl['typ'] == 'boolean' else listen[fl['name']]]}", allow_blank=True)
            dv.error, dv.errorTitle = "Bitte einen Wert aus der Liste wählen.", "Ungültiger Wert"
            dv.showErrorMessage = True
            ws.add_data_validation(dv)
            dv.add(bereich_zeile)
        elif fl["typ"] == "integer":
            hi = fl["max"]
            dv = DataValidation(type="whole", operator="between" if hi is not None else "greaterThanOrEqual",
                                formula1=str(fl["min"]), formula2=str(hi) if hi is not None else None, allow_blank=True)
            dv.error, dv.errorTitle = "Wert liegt außerhalb des erlaubten Bereichs.", "Ungültiger Wert"
            dv.showErrorMessage = True
            ws.add_data_validation(dv)
            dv.add(bereich_zeile)
        ws.row_dimensions[r].height = 30
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["B"].width = 62
    ws.column_dimensions["C"].width = 26
    for k in range(len(fd.STRATEGIEN)):
        ws.column_dimensions[get_column_letter(4 + k)].width = 24
    r = len(fd.STRATEGIEPROFILE["felder"]) + 3
    ws.cell(row=r, column=1, value="Gelb = technischer Vorschlag von Yu, fachlich noch nicht abgestimmt. Bitte prüfen und überschreiben.").font = f(italic=True, color="7F6000")
    ws.cell(row=r + 1, column=1, value="Jede Zeile entspricht einem Regler im Prototyp der Umsetzung. Was die Regler bewirken, steht im Blatt Anleitung.").font = f(italic=True, color="595959")
    ws.freeze_panes = "D2"
    return ws


def blatt_felder(wb, titel: str, bloecke: list[dict], vermerk: str):
    ws = wb.create_sheet(titel)
    ws["A1"] = vermerk
    ws["A1"].font = f(italic=True, color="595959")
    kopf = ["Block", "Feld", "Pflicht", "Typ", "Einheit", "Erlaubte Werte", "Beschreibung", "Beispiel", "Herkunft"]
    for i, t in enumerate(kopf, 1):
        c = ws.cell(row=3, column=i, value=t)
        c.font, c.fill, c.border = f(bold=True, color="FFFFFF"), fuell(DUNKEL), RAHMEN
    r = 4
    for b in bloecke:
        for fl in b["felder"]:
            werte = [b["titel"], fl["name"], "ja" if fl["pflicht"] else "nein", typ_de(fl), fl["einheit"],
                     erlaubte_werte(fl), fl["de"], zellwert(fl["beispiel"]), fl["herkunft"]]
            for i, w in enumerate(werte, 1):
                c = ws.cell(row=r, column=i, value=w)
                c.font, c.border = f(size=9, bold=(i == 2)), RAHMEN
                c.alignment = Alignment(wrap_text=True, vertical="top")
                if fl["pflicht"] and i == 3:
                    c.fill = fuell(TEAL)
            r += 1
    for sp, b in zip("ABCDEFGHI", [26, 28, 8, 12, 16, 30, 70, 28, 13]):
        ws.column_dimensions[sp].width = b
    ws.freeze_panes = "C4"
    return ws


def blatt_anleitung(wb, technischer_test: bool):
    ws = wb.create_sheet("Anleitung", 0)
    ws.column_dimensions["A"].width = 3
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 112
    ws.column_dimensions["D"].width = 3
    hintergrund = fuell(HELL)
    for zeile_nr in range(1, 81):
        for sp in range(1, 16):
            ws.cell(row=zeile_nr, column=sp).fill = hintergrund
    linie = Side(style="thin", color="E3E1D9")
    karte = Border(bottom=linie)
    r = 2

    def titel(t):
        nonlocal r
        for sp in (2, 3):
            ws.cell(row=r, column=sp).fill = fuell(DUNKEL)
            ws.cell(row=r + 1, column=sp).fill = fuell(DUNKEL)
        c = ws.cell(row=r, column=2, value=t)
        c.font = f(size=18, bold=True, color="FFFFFF")
        c.alignment = Alignment(vertical="center", indent=1)
        u = ws.cell(row=r + 1, column=2, value="IPM WiSe 2026/27 · Gruppe 6 · Thema 6 Variantenmanagement · Teilprojekt Datenerhebung")
        u.font = f(size=10, color=TEAL)
        u.alignment = Alignment(vertical="top", indent=1)
        ws.row_dimensions[r].height = 36
        ws.row_dimensions[r + 1].height = 22
        r += 3

    def kopf(t):
        nonlocal r
        ws.row_dimensions[r].height = 10
        r += 1
        c = ws.cell(row=r, column=2, value=t)
        c.font, c.fill = f(size=11, bold=True, color=DUNKEL), fuell(TEAL)
        c.alignment = Alignment(vertical="center", indent=1)
        ws.cell(row=r, column=3).fill = fuell(TEAL)
        ws.row_dimensions[r].height = 22
        r += 1

    def zeile(links, rechts, farbe=None, fett=False):
        nonlocal r
        a = ws.cell(row=r, column=2, value=links)
        a.font = f(bold=True, color=DUNKEL)
        a.alignment = Alignment(vertical="center", wrap_text=True, indent=1)
        a.fill = fuell(farbe or "FFFFFF")
        a.border = karte
        b = ws.cell(row=r, column=3, value=rechts)
        b.font = f(bold=fett, color="262626")
        b.alignment = Alignment(vertical="center", wrap_text=True, indent=1)
        b.fill = fuell("FFFFFF")
        b.border = karte
        ws.row_dimensions[r].height = 20 + 13 * (len(str(rechts)) // 108)
        r += 1

    if technischer_test:
        titel("Technischer Testdatensatz – Variantenmanagement")
        zeile("Kennzeichnung", "SYNTHETIC – alle Werte sind erfunden und dienen nur dem Test von Schema, Konverter und Prototyp. "
                               "Fachlich nicht abgestimmt.", farbe=GELB, fett=True)
        ws.cell(row=r - 1, column=3).fill = fuell(GELB)
    else:
        titel("Excel-Vorlage Datenerhebung – Variantenmanagement")
        zeile("Kennzeichnung", "SYNTHETIC – alle Werte in dieser Datei sind erfunden. Echte Referenzdaten nur mit Quelle und Abrufdatum.", farbe=GELB, fett=True)
        ws.cell(row=r - 1, column=3).fill = fuell(GELB)
    zeile("Version / Stand", f"Vorlage v{fd.VERSION}, {fd.STAND} · IPM WiSe 2026/27, Gruppe 6, Teilprojekt Datenerhebung (Jonas Flütebonies, Yu Zhaoze)")
    zeile("Zweck", "Hier entstehen die Beispieldaten des fiktiven Kartonherstellers. Aus dieser Datei erzeugt ein Skript die "
                   "CSV- und JSON-Datei, die der Prototyp der Umsetzung lädt.")

    kopf("Was ist zu tun")
    zeile("1  Strategieprofile", "Blatt Strategieprofile: Die vier Profile sind als Vorschlag vorbefüllt (gelb). Bitte fachlich prüfen und anpassen.")
    zeile("2  Varianten", f"Blatt Varianten: ab Zeile {ERSTE_DATENZEILE} etwa 10 bis 15 Kartonvarianten eintragen, eine Zeile je Variante. "
                          "Die grauen Beispielzeilen überschreiben oder löschen.")
    zeile("3  Prüfen", "Die Spalte Pruef_Hinweis ganz rechts zeigt, ob Umsatz, Absatz und Preis zusammenpassen.")
    zeile("4  Zurückgeben", "Datei an Yu schicken oder im Repo unter data/synthetic ablegen. Yu wandelt sie um und lädt sie in den Prototyp.")

    kopf("Farben")
    zeile("Dunkle Kopfzelle", "Pflichtfeld (sechs Felder). Ohne sie wird die Datei nicht übergeben.", farbe=DUNKEL)
    ws.cell(row=r - 1, column=2).font = f(bold=True, color="FFFFFF")
    zeile("Helle Kopfzelle", "Optionales Feld. Wird als Zusatzinformation in den Prompt übernommen.", farbe=TEAL)
    zeile("Graue Zeilen", f"Beispielvarianten. Zeilen, deren Kennung mit {BEISPIEL_PRAEFIX} beginnt, werden bei der Umwandlung übersprungen.", farbe="EDEDED")
    zeile("Gelbe Zellen", "Vorschlagswerte der Strategieprofile – bitte prüfen und überschreiben.", farbe=GELB)
    zeile("Graue Spalten", "Prüfformeln, nicht ausfüllen.", farbe=GRAU)

    kopf("Regeln für die Eingabe")
    zeile("Kennung", "Feld Variante: eindeutig, nur Buchstaben, Ziffern, Unterstrich, Punkt und Bindestrich. Vorschlag: Nummer_FEFCO_LxBxH_Welle, "
                     "z. B. K02_0201_300x200x150_B.")
    zeile("Texte", "Kein Komma, kein Semikolon und kein Zeilenumbruch in Textfeldern. Der Prototyp trennt CSV-Dateien an beiden Zeichen.")
    zeile("Zahlen", "Als normale Excel-Zahl eingeben. Die Umwandlung schreibt Dezimalpunkte, damit der Prototyp sie richtig liest.")
    zeile("Ja / Nein", "Felder mit ja / nein über das Dropdown wählen.")
    zeile("Umsatz", "Umsatz_TEUR soll zu Absatz_Stk × Preis_EUR / 1000 passen (Abweichung höchstens 2 %).")
    zeile("Quellen", "Annahmen und Quellen bitte kurz in einer eigenen Datei notieren (data/reference). In die Tabelle kommen nur objektive Produktdaten.")

    kopf("Wie der Demo-Prototyp die Daten bewertet (nur Konzeptdemo, Stand 10.11.2026)")
    zeile("Reihenfolge der Regeln", "Der Prototyp prüft jede Variante der Reihe nach. Die erste zutreffende Regel entscheidet.")
    zeile("1  Zukunft", "Status = Zukunft und Zukunftsschutz aktiv → Behalten.")
    zeile("2  Auslauf", "Status = Auslauf und Auslauf streichen aktiv → Streichen.")
    zeile("3  Finanzziel", "Marge_Pct unter Mindestmarge oder Absatz_Stk unter Mindestabsatz → Streichen.")
    zeile("4  Rüstkosten", "Ruestkosten_Index über dem Höchstwert → Modularisieren.")
    zeile("5  Sonst", "Behalten.")
    zeile("Kennzahlen", "Daraus berechnet der Prototyp: Anzahl behaltener Varianten, Umsatzabdeckung in Prozent und die durchschnittliche Marge der behaltenen Varianten.")

    kopf("Welche Fälle in den Daten vorkommen sollten")
    zeile("Bestseller", "Zwei bis drei Standardgrößen mit hohem Absatz und vielen Kunden.")
    zeile("Großkunde", "Eine Sondergröße, die nur ein einziger Großkunde kauft: hoher Umsatz, niedrige Marge, Hauptkunde_Anteil_Pct = 100.")
    zeile("Fast gleich", "Zwei Varianten, die sich nur um wenige Millimeter oder in der Wellenart unterscheiden.")
    zeile("Auslauf", "Mindestens eine Variante mit Status Auslauf.")
    zeile("Zukunft", "Mindestens eine Variante mit Status Zukunft, z. B. neues Material oder neue Konstruktion.")
    zeile("Kleinserie", "Eine Variante mit sehr kleinem Absatz und hohem Rüstaufwand.")

    kopf("Blätter in dieser Datei")
    zeile("Varianten", "Eine Zeile je Variante. Hier eintragen.")
    zeile("Strategieprofile", "Eine Spalte je Strategie. Vorschlag prüfen.")
    zeile("Felder", "Beschreibung aller Felder der Stufe 1 mit Typ, Einheit, erlaubten Werten und Beispiel.")
    zeile(BLATT_ERP, "Entwurf der weiteren Datenblöcke (Stückliste, Arbeitsplan, Aufträge, Kosten, Kunden, Wettbewerb). Noch nicht ausfüllen.")
    zeile("Listen", "Ausgeblendet. Enthält die Werte der Dropdowns. Nicht ändern.")
    ws.sheet_view.showGridLines = False
    return ws


def baue(pfad: Path, zeilen: list[dict], profile: list[dict], *, beispiel: bool, technischer_test: bool = False):
    wb = Workbook()
    wb.remove(wb.active)
    bereiche = blatt_listen(wb)
    blatt_varianten(wb, bereiche, zeilen, beispiel)
    blatt_strategieprofile(wb, bereiche, profile)
    blatt_felder(wb, "Felder", [fd.VARIANTEN, fd.STRATEGIEPROFILE],
                 f"Feldliste Stufe 1, Schema v{fd.VERSION}, Stand {fd.STAND}. Herkunft Prototyp = Feld oder Regler des Prototyps der Umsetzung.")
    blatt_felder(wb, BLATT_ERP, [b for b in fd.BLOECKE if b["stufe"] == 2],
                 f"Entwurf Stufe 2, Schema v{fd.VERSION}, Stand {fd.STAND}. Noch nicht abgestimmt und noch nicht auszufüllen.")
    blatt_anleitung(wb, technischer_test)
    wb._sheets = [wb[n] for n in ["Anleitung", "Varianten", "Strategieprofile", "Felder", BLATT_ERP, "Listen"]]
    wb["Listen"].sheet_state = "hidden"
    wb.active = 0
    wb.calculation.fullCalcOnLoad = True
    wb.properties.creator = "Yu Zhaoze"
    wb.properties.title = "Datenerhebung Variantenmanagement"
    pfad.parent.mkdir(parents=True, exist_ok=True)
    try:
        wb.save(pfad)
    except PermissionError:
        sys.exit(f"Kann {pfad.name} nicht schreiben: Die Datei ist vermutlich in Excel geöffnet. "
                 f"Bitte schließen und noch einmal ausführen.\n"
                 f"无法写入 {pfad.name}：文件可能正在 Excel 里打开。请关闭后再运行一次。")
    return pfad


def beispielzeilen() -> list[dict]:
    """Drei Beispielvarianten für die Vorlage (Bestseller, fast gleiche Größe, Großkunde).

    Die Kennung beginnt mit BEISPIEL_, damit der Konverter die Zeilen überspringt."""
    alle = {z["Variante"]: z for z in testdaten.varianten()}
    namen = ["K02_0201_300x200x150_B", "K03_0201_305x200x150_B", "K08_0201_347x253x118_B_SG"]
    return [dict(alle[k], Variante=f"{BEISPIEL_PRAEFIX}_{k}") for k in namen]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ziel = WURZEL / "vorlagen" / f"VARIANTEN_VORLAGE_v{fd.VERSION}.xlsx"
    baue(ziel, beispielzeilen(), testdaten.strategieprofile(), beispiel=True)
    print("geschrieben:", ziel.relative_to(WURZEL))
    test = WURZEL / "data" / "synthetic" / f"technischer_test_v{fd.VERSION}" / f"technischer_testdatensatz_v{fd.VERSION}.xlsx"
    baue(test, testdaten.varianten(), testdaten.strategieprofile(), beispiel=False, technischer_test=True)
    print("geschrieben:", test.relative_to(WURZEL))


if __name__ == "__main__":
    main()
