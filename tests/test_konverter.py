"""Konverter-Tests: Excel-Vorlage → CSV/JSON für den Prototyp."""
import csv
import json
import shutil

import pytest
from openpyxl import load_workbook

import excel_zu_prototyp as konv
import felder as fd
import testdaten
from conftest import TEST_EXCEL, TESTORDNER, VORLAGE


def spalte(ws, name):
    for c in ws[1]:
        if c.value == name:
            return c.column
    raise KeyError(name)


def test_vorlage_hat_alle_blaetter_und_spalten():
    wb = load_workbook(VORLAGE)
    assert wb.sheetnames == ["Anleitung", "Varianten", "Strategieprofile", "Felder", "ERP-Datenblöcke (Entwurf)", "Listen"]
    assert wb["Listen"].sheet_state == "hidden"
    kopf = [c.value for c in wb["Varianten"][1]]
    assert kopf == [f["name"] for f in fd.VARIANTEN["felder"]] + ["Pruef_Umsatz_TEUR", "Pruef_Hinweis"]
    assert len(wb["Varianten"].data_validations.dataValidation) >= 10


def test_leere_vorlage_wird_abgelehnt_beispielzeilen_zaehlen_nicht(tmp_path):
    code, bericht = konv.wandle_um(VORLAGE, tmp_path)
    assert code == 1
    assert "3 Beispielzeile(n) übersprungen" in bericht
    assert not (tmp_path / "varianten.csv").exists()


def test_testdatensatz_rundlauf_excel_zu_json(tmp_path):
    code, bericht = konv.wandle_um(TEST_EXCEL, tmp_path)
    assert code == 0, bericht
    assert json.loads((tmp_path / "varianten.json").read_text(encoding="utf-8")) == testdaten.varianten()
    assert json.loads((tmp_path / "strategieprofile.json").read_text(encoding="utf-8")) == testdaten.strategieprofile()


def test_abgelegte_dateien_sind_aktuell(tmp_path):
    konv.wandle_um(TEST_EXCEL, tmp_path)
    for name in ("varianten.csv", "varianten.json", "strategieprofile.json"):
        assert (tmp_path / name).read_bytes() == (TESTORDNER / name).read_bytes(), f"{name} in data/synthetic ist veraltet"


def test_csv_ist_fuer_den_prototyp_lesbar(tmp_path):
    konv.wandle_um(TEST_EXCEL, tmp_path)
    text = (tmp_path / "varianten.csv").read_text(encoding="utf-8")
    zeilen = text.strip().split("\n")
    kopf = zeilen[0].split(",")
    assert kopf[:len(fd.PROTOTYP_SPALTEN)] == fd.PROTOTYP_SPALTEN
    assert ";" not in text and '"' not in text and "\r" not in text
    for z in zeilen[1:]:
        assert len(z.split(",")) == len(kopf), z
    daten = list(csv.DictReader(zeilen))
    assert len(daten) == 14
    assert daten[0]["Umsatz_TEUR"] == "198.4" and daten[0]["FEFCO_Typ"] == "0201"
    assert "Must_Have" not in kopf and "Bemerkung" not in kopf


def _kopie_mit(tmp_path, aendern):
    ziel = tmp_path / "eingabe.xlsx"
    shutil.copy(TEST_EXCEL, ziel)
    wb = load_workbook(ziel)
    aendern(wb)
    wb.save(ziel)
    return ziel


def test_dezimalkomma_als_text_wird_umgewandelt(tmp_path):
    def aendern(wb):
        ws = wb["Varianten"]
        ws.cell(row=3, column=spalte(ws, "Umsatz_TEUR"), value="198,4")
        ws.cell(row=3, column=spalte(ws, "Preis_EUR"), value="0,32")
    code, bericht = konv.wandle_um(_kopie_mit(tmp_path, aendern), tmp_path / "aus")
    assert code == 0, bericht
    v = json.loads((tmp_path / "aus" / "varianten.json").read_text(encoding="utf-8"))
    assert v[0]["Umsatz_TEUR"] == 198.4 and v[0]["Preis_EUR"] == 0.32
    assert "198.4" in (tmp_path / "aus" / "varianten.csv").read_text(encoding="utf-8")


FEHLER_IN_EXCEL = {
    "Kennung doppelt": (lambda ws: ws.cell(row=4, column=spalte(ws, "Variante"), value=ws.cell(row=3, column=spalte(ws, "Variante")).value), "doppelt"),
    "Text statt Zahl": (lambda ws: ws.cell(row=3, column=spalte(ws, "Absatz_Stk"), value="viel"), "keine Zahl"),
    "Kommazahl statt ganzer Zahl": (lambda ws: ws.cell(row=3, column=spalte(ws, "Ruestkosten_Index"), value=2.5), "ganze Zahl"),
    "Pflichtfeld leer": (lambda ws: setattr(ws.cell(row=3, column=spalte(ws, "Status")), "value", None), "'Status' is a required property"),
    "Komma in Bezeichnung": (lambda ws: ws.cell(row=3, column=spalte(ws, "Bezeichnung"), value="Faltkarton, klein"), "CSV-Import"),
    "Spalte unbekannt": (lambda ws: ws.cell(row=1, column=spalte(ws, "Druck"), value="Farbe"), "unbekanntes Feld"),
}


@pytest.mark.parametrize("fall", FEHLER_IN_EXCEL)
def test_fehler_in_excel_stoppen_die_uebergabe(tmp_path, fall):
    aendern, stichwort = FEHLER_IN_EXCEL[fall]
    code, bericht = konv.wandle_um(_kopie_mit(tmp_path, lambda wb: aendern(wb["Varianten"])), tmp_path / "aus")
    assert code == 1
    assert stichwort in bericht, bericht
    assert not (tmp_path / "aus" / "varianten.csv").exists()
    assert (tmp_path / "aus" / "pruefbericht.txt").exists()


def test_umsatzabweichung_ist_hinweis_kein_fehler(tmp_path):
    def aendern(wb):
        ws = wb["Varianten"]
        ws.cell(row=3, column=spalte(ws, "Umsatz_TEUR"), value=500)
    code, bericht = konv.wandle_um(_kopie_mit(tmp_path, aendern), tmp_path / "aus")
    assert code == 0
    assert "HINWEISE (1)" in bericht and "Umsatz_TEUR = 500" in bericht


def test_beispielzeilen_werden_neben_echten_zeilen_uebersprungen(tmp_path):
    ziel = tmp_path / "eingabe.xlsx"
    shutil.copy(VORLAGE, ziel)
    wb = load_workbook(ziel)
    ws = wb["Varianten"]
    neu = {"Variante": "N01_0201_100x100x100_B", "Umsatz_TEUR": 10, "Marge_Pct": 20, "Absatz_Stk": 20000,
           "Ruestkosten_Index": 3, "Status": "Standard"}
    for k, w in neu.items():
        ws.cell(row=6, column=spalte(ws, k), value=w)
    wb.save(ziel)
    code, bericht = konv.wandle_um(ziel, tmp_path / "aus")
    assert code == 0, bericht
    v = json.loads((tmp_path / "aus" / "varianten.json").read_text(encoding="utf-8"))
    assert [x["Variante"] for x in v] == ["N01_0201_100x100x100_B"]
    assert "Must_Have" not in v[0]


def test_spalte_raja_artikelnr_wird_als_referenz_gelesen(tmp_path):
    """Jonas hat die Katalognummer als eigene Spalte 'RAJA-Artikelnr.' ergänzt."""
    def aendern(wb):
        ws = wb["Varianten"]
        sp = spalte(ws, "Referenz_Artikelnr")
        ws.cell(row=1, column=sp, value="RAJA-Artikelnr.")
        ws.cell(row=3, column=sp, value="CAS16")
    code, bericht = konv.wandle_um(_kopie_mit(tmp_path, aendern), tmp_path / "aus")
    assert code == 0, bericht
    v = json.loads((tmp_path / "aus" / "varianten.json").read_text(encoding="utf-8"))
    assert v[0]["Referenz_Artikelnr"] == "CAS16" and "Referenz_Artikelnr" not in v[1]
    kopf = (tmp_path / "aus" / "varianten.csv").read_text(encoding="utf-8").split("\n")[0].split(",")
    assert kopf[:len(fd.PROTOTYP_SPALTEN)] == fd.PROTOTYP_SPALTEN and "Referenz_Artikelnr" in kopf


def test_ja_nein_falsch_im_strategieprofil_stoppt_die_uebergabe(tmp_path):
    def aendern(wb):
        ws = wb["Strategieprofile"]
        for r in range(2, ws.max_row + 1):
            if ws.cell(row=r, column=1).value == "Kernmaerkte_schuetzen":
                ws.cell(row=r, column=4, value="vielleicht")
    code, bericht = konv.wandle_um(_kopie_mit(tmp_path, aendern), tmp_path / "aus")
    assert code == 1 and "ja/nein" in bericht
