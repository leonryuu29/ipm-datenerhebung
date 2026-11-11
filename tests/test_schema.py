"""Schema-Tests: Die Schemas sind gültig, nehmen gute Daten an und lehnen schlechte ab."""
import copy
import json

import pytest
from jsonschema import Draft202012Validator, FormatChecker

import felder as fd
import pruefen
import testdaten
from conftest import WURZEL

SCHEMAS = {
    "varianten": fd.schema_varianten,
    "strategieprofile": fd.schema_strategieprofile,
    "datenpaket": fd.schema_datenpaket,
}


@pytest.mark.parametrize("name", SCHEMAS)
def test_schema_ist_gueltig_und_datei_aktuell(name):
    schema = SCHEMAS[name]()
    Draft202012Validator.check_schema(schema)
    datei = WURZEL / "schema" / f"{name}_v{fd.VERSION}.schema.json"
    assert json.loads(datei.read_text(encoding="utf-8")) == schema, "schema/ ist veraltet: generator/schema_erzeugen.py ausführen"


def test_prototyp_spalten_sind_pflicht():
    schema = fd.schema_varianten()
    assert schema["items"]["required"] == ["Variante", "Umsatz_TEUR", "Marge_Pct", "Absatz_Stk",
                                           "Ruestkosten_Index", "Status", "Must_Have"]


@pytest.mark.parametrize("block", fd.BLOECKE, ids=lambda b: b["id"])
def test_beispielwerte_der_feldliste_passen_zum_schema(block):
    zeile = {f["name"]: f["beispiel"] for f in block["felder"] if f["beispiel"] is not None}
    fehler = list(Draft202012Validator(fd.zeilen_schema(block), format_checker=FormatChecker()).iter_errors(zeile))
    assert fehler == []


def test_technischer_testdatensatz_ist_fehlerfrei():
    assert pruefen.pruefe_varianten(testdaten.varianten()) == ([], [])
    assert pruefen.pruefe_strategieprofile(testdaten.strategieprofile()) == ([], [])


def test_datenpaket_stufe1_wird_angenommen():
    paket = {
        "meta": {"schema_version": fd.VERSION, "kennzeichnung": "SYNTHETIC", "erzeugt_am": "2026-11-11"},
        "strategieprofil": testdaten.strategieprofile()[0],
        "varianten": testdaten.varianten(),
    }
    assert list(Draft202012Validator(fd.schema_datenpaket(), format_checker=FormatChecker()).iter_errors(paket)) == []
    paket["meta"]["kennzeichnung"] = "REAL"
    assert list(Draft202012Validator(fd.schema_datenpaket()).iter_errors(paket)) != []


FEHLERFAELLE = {
    "Pflichtfeld fehlt": lambda v: v[0].pop("Marge_Pct"),
    "Status unbekannt": lambda v: v[0].update(Status="US-Markt"),
    "Rüstkosten-Index 11": lambda v: v[0].update(Ruestkosten_Index=11),
    "Rüstkosten-Index 0": lambda v: v[0].update(Ruestkosten_Index=0),
    "Absatz negativ": lambda v: v[0].update(Absatz_Stk=-1),
    "Absatz als Text": lambda v: v[0].update(Absatz_Stk="510000"),
    "Must_Have als Text": lambda v: v[0].update(Must_Have="ja"),
    "Kennung mit Komma": lambda v: v[0].update(Variante="K01,neu"),
    "Kennung mit Leerzeichen": lambda v: v[0].update(Variante="K01 neu"),
    "Kennung doppelt": lambda v: v[1].update(Variante=v[0]["Variante"]),
    "Komma in Bezeichnung": lambda v: v[0].update(Bezeichnung="Faltkarton, klein"),
    "Semikolon in Bemerkung": lambda v: v[0].update(Bemerkung="a; b"),
    "unbekanntes Feld": lambda v: v[0].update(Farbe="blau"),
    "FEFCO dreistellig": lambda v: v[0].update(FEFCO_Typ="201"),
    "Wellenart unbekannt": lambda v: v[0].update(Wellenart="X"),
    "leere Liste": lambda v: v.clear(),
}


@pytest.mark.parametrize("fall", FEHLERFAELLE)
def test_fehlerhafte_varianten_werden_abgelehnt(fall):
    v = copy.deepcopy(testdaten.varianten())
    FEHLERFAELLE[fall](v)
    fehler, _ = pruefen.pruefe_varianten(v)
    assert fehler, f"{fall}: kein Fehler gemeldet"


HINWEISFAELLE = {
    "Umsatz passt nicht zu Absatz × Preis": (lambda v: v[0].update(Umsatz_TEUR=500.0), "Umsatz_TEUR"),
    "ein Kunde, Anteil unter 100": (lambda v: v[7].update(Hauptkunde_Anteil_Pct=80), "nur ein Kunde"),
    "Auslauf und Must_Have": (lambda v: v[9].update(Must_Have=True), "Auslauf und Must_Have"),
}


@pytest.mark.parametrize("fall", HINWEISFAELLE)
def test_auffaellige_varianten_geben_hinweis(fall):
    aendern, stichwort = HINWEISFAELLE[fall]
    v = copy.deepcopy(testdaten.varianten())
    aendern(v)
    fehler, hinweise = pruefen.pruefe_varianten(v)
    assert fehler == []
    assert any(stichwort in h for h in hinweise), hinweise


def test_umsatz_innerhalb_toleranz_gibt_keinen_hinweis():
    v = copy.deepcopy(testdaten.varianten())
    v[0]["Umsatz_TEUR"] = round(v[0]["Umsatz_TEUR"] * 1.015, 1)
    assert pruefen.pruefe_varianten(v) == ([], [])


PROFILFEHLER = {
    "Strategie unbekannt": lambda p: p[0].update(Strategie="Premium"),
    "Strategie doppelt": lambda p: p[1].update(Strategie=p[0]["Strategie"]),
    "Mindestmarge 41": lambda p: p[0].update(Min_Marge_Pct=41),
    "Entkopplungspunkt unbekannt": lambda p: p[0].update(Entkopplungspunkt="Lager"),
    "Pflichtfeld fehlt": lambda p: p[0].pop("Sourcing"),
}


@pytest.mark.parametrize("fall", PROFILFEHLER)
def test_fehlerhafte_profile_werden_abgelehnt(fall):
    p = copy.deepcopy(testdaten.strategieprofile())
    PROFILFEHLER[fall](p)
    fehler, _ = pruefen.pruefe_strategieprofile(p)
    assert fehler


def test_mindestabsatz_ausserhalb_des_reglers_gibt_hinweis():
    p = copy.deepcopy(testdaten.strategieprofile())
    p[0]["Min_Absatz_Stk"] = 20000
    fehler, hinweise = pruefen.pruefe_strategieprofile(p)
    assert fehler == []
    assert any("Regler" in h for h in hinweise)


def test_fehlendes_profil_gibt_hinweis():
    fehler, hinweise = pruefen.pruefe_strategieprofile(testdaten.strategieprofile()[:3])
    assert fehler == []
    assert any("Nischenanbieter" in h for h in hinweise)
