"""Integrationstest gegen den Prototyp der Umsetzung (echter Browser, Playwright).

Geladen wird die unveränderte Datei tests/prototyp/ki_wrapper_variantenmanagement.html.
Der Test lädt unsere CSV- und JSON-Datei über das Upload-Feld hoch, stellt die vier
Strategieprofile an den Reglern ein und vergleicht Empfehlungen und Kennzahlen mit dem
Nachbau in generator/prototyp_logik.py.

Ergebnisse: tests/ergebnisse/prototyp_lauf.json und Bildschirmfotos je Strategie.
Benötigt Internet (Tailwind und Plotly kommen im Prototyp von einem CDN).
"""
import datetime
import hashlib
import json
import os
import re

import pytest

import felder as fd
import prototyp_logik as logik
from conftest import ERGEBNISSE, PROTOTYP, TESTORDNER

sync_api = pytest.importorskip("playwright.sync_api")

REGLER = {f["name"]: f["prototyp_id"] for f in fd.STRATEGIEPROFILE["felder"] if f["prototyp_id"]}
ASCII = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"})


@pytest.fixture(scope="module")
def protokoll():
    daten = {
        "lauf": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "prototyp": {"datei": PROTOTYP.name, "sha256": hashlib.sha256(PROTOTYP.read_bytes()).hexdigest(),
                     "stand": "2026-11-10", "quelle": "Google Drive, IPM Gruppe 6"},
        "datensatz": str(TESTORDNER.relative_to(TESTORDNER.parents[2])).replace(os.sep, "/"),
        "schema_version": fd.VERSION,
        "strategien": {}, "befunde": {},
    }
    yield daten
    ERGEBNISSE.mkdir(exist_ok=True)
    (ERGEBNISSE / "prototyp_lauf.json").write_text(json.dumps(daten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


@pytest.fixture(scope="module")
def seite():
    if not PROTOTYP.exists():
        pytest.skip("Prototyp-Datei fehlt")
    with sync_api.sync_playwright() as p:
        proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
        browser = p.chromium.launch(proxy={"server": proxy} if proxy else None)
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.meldungen = []
        page.on("dialog", lambda d: (page.meldungen.append(d.message), d.accept()))
        page.on("pageerror", lambda e: page.meldungen.append("pageerror: " + str(e)))
        page.goto(PROTOTYP.as_uri(), wait_until="load")
        try:
            page.wait_for_function("typeof Plotly !== 'undefined' && document.querySelectorAll('#tableBody tr').length > 0", timeout=30000)
        except sync_api.TimeoutError:
            browser.close()
            pytest.skip("Plotly/Tailwind vom CDN nicht erreichbar – Prototyp startet ohne Internet nicht")
        yield page
        browser.close()


def lade(page, pfad, erwartete_zeilen=None):
    page.meldungen.clear()
    page.set_input_files("#fileInput", str(pfad))
    page.wait_for_function("name => document.getElementById('fileStatus').innerText.includes(name)", arg=pfad.name, timeout=10000)
    if erwartete_zeilen is not None:
        page.wait_for_function("n => document.querySelectorAll('#tableBody tr').length === n", arg=erwartete_zeilen, timeout=10000)
    return page.inner_text("#fileStatus")


def stelle_ein(page, profil):
    werte = {}
    for feld, regler in REGLER.items():
        w = profil[feld]
        if feld == "Entkopplungspunkt":
            w = fd.PROTOTYP_ENTKOPPLUNG[w]
        elif feld == "Sourcing":
            w = fd.PROTOTYP_SOURCING[w]
        werte[regler] = w
    page.evaluate(
        """werte => {
            for (const [id, w] of Object.entries(werte)) {
                const el = document.getElementById(id);
                if (el.type === 'checkbox') el.checked = w; else el.value = String(w);
                el.dispatchEvent(new Event(el.type === 'range' ? 'input' : 'change', {bubbles: true}));
            }
        }""", werte)
    # Kontrolle: Der Regler hat den Wert wirklich angenommen (ein Wert außerhalb des Bereichs würde gekappt).
    ist = page.evaluate("ids => Object.fromEntries(ids.map(i => { const e = document.getElementById(i); return [i, e.type === 'checkbox' ? e.checked : e.value]; }))", list(werte))
    for regler, w in werte.items():
        assert str(ist[regler]).lower() == str(w).lower(), f"Regler {regler}: soll {w}, ist {ist[regler]}"


def lies_ergebnis(page):
    zeilen = page.evaluate("[...document.querySelectorAll('#tableBody tr')].map(tr => [...tr.children].map(td => td.innerText.trim()))")
    behalten, gesamt = (int(x) for x in page.inner_text("#kpi_variants").split("/"))
    zahl = lambda s: float(re.search(r"-?\d+(\.\d+)?", s).group())
    return {
        "entscheidungen": {z[0]: z[7] for z in zeilen},
        "varianten_behalten": behalten, "varianten_gesamt": gesamt,
        "umsatzabdeckung_pct": zahl(page.inner_text("#kpi_coverage")),
        "marge_behalten_pct": zahl(page.inner_text("#kpi_margin")),
        "komplexitaet_reduktion_pct": abs(zahl(page.inner_text("#kpi_complexity"))),
        "abweichung_zum_ziel": page.inner_text("#kpi_coverage_diff"),
    }


def test_regler_des_prototyps_passen_zur_feldliste(seite):
    info = seite.evaluate(
        """ids => Object.fromEntries(ids.map(i => { const e = document.getElementById(i);
            return [i, e ? {type: e.type, min: e.min, max: e.max, step: e.step,
                            optionen: e.options ? [...e.options].map(o => o.value) : null} : null]; }))""", list(REGLER.values()))
    assert all(info.values()), [k for k, v in info.items() if not v]
    for regler, (lo, hi, schritt) in fd.PROTOTYP_REGLER.items():
        assert (int(info[regler]["min"]), int(info[regler]["max"]), int(info[regler]["step"] or 1)) == (lo, hi, schritt), regler
    assert info["decoupling_point"]["optionen"] == list(fd.PROTOTYP_ENTKOPPLUNG.values())
    assert info["sourcing_strat"]["optionen"] == list(fd.PROTOTYP_SOURCING.values())


@pytest.mark.parametrize("datei", ["varianten.csv", "varianten.json"])
def test_upload_wird_angenommen(seite, varianten, datei):
    status = lade(seite, TESTORDNER / datei, len(varianten))
    assert status == f"Geladen: {datei} ({len(varianten)} Varianten)"
    assert seite.meldungen == []
    geladen = seite.evaluate("portfolioData")
    for soll, ist in zip(varianten, geladen):
        for spalte in fd.PROTOTYP_SPALTEN:
            assert ist[spalte] == soll[spalte], (soll["Variante"], spalte)


@pytest.mark.parametrize("strategie", fd.STRATEGIEN)
def test_strategieprofil_liefert_erwartete_empfehlungen(seite, varianten, profile, protokoll, strategie):
    profil = next(p for p in profile if p["Strategie"] == strategie)
    soll = logik.bewerte(varianten, profil)
    ergebnisse = {}
    for datei in ("varianten.json", "varianten.csv"):
        lade(seite, TESTORDNER / datei, len(varianten))
        stelle_ein(seite, profil)
        ist = lies_ergebnis(seite)
        assert ist["entscheidungen"] == soll["entscheidungen"], datei
        assert (ist["varianten_behalten"], ist["varianten_gesamt"]) == (soll["varianten_behalten"], soll["varianten_gesamt"])
        for k in ("umsatzabdeckung_pct", "marge_behalten_pct", "komplexitaet_reduktion_pct"):
            assert abs(ist[k] - soll[k]) <= 0.051, (datei, k, ist[k], soll[k])
        ergebnisse[datei] = ist
    assert ergebnisse["varianten.json"] == ergebnisse["varianten.csv"]

    ERGEBNISSE.mkdir(exist_ok=True)
    bild = f"prototyp_{strategie.lower().translate(ASCII)}.png"
    seite.wait_for_selector("#bubbleChart .main-svg")
    seite.evaluate("window.scrollTo(0, 0)")
    seite.screenshot(path=str(ERGEBNISSE / bild))   # nur der obere Bereich: Regler, Kennzahlen, Diagramme
    protokoll["strategien"][strategie] = dict(ergebnisse["varianten.csv"], profil=profil, bildschirmfoto=bild,
                                              ziel_umsatzabdeckung_pct=profil["Min_Umsatzabdeckung_Pct"],
                                              ziel_erreicht=soll["ziel_erreicht"])


def test_zusatzfelder_landen_im_prompt(seite, varianten, protokoll):
    lade(seite, TESTORDNER / "varianten.json", len(varianten))
    prompt = seite.evaluate("document.getElementById('promptOutput').innerText")
    for feld in ("Hauptkunde_Anteil_Pct", "Variantenbildung_Schritt", "FEFCO_Typ", "KI_Empfehlung"):
        assert f'"{feld}"' in prompt, feld
    assert '"Preis_EUR": 0.32' in prompt
    protokoll["befunde"]["zusatzfelder_im_prompt"] = True
    protokoll["befunde"]["prompt_zeichen_json"] = len(prompt)


def test_csv_liefert_zusatzfelder_als_text(seite, varianten, protokoll):
    """Befund: Im CSV-Weg wandelt der Prototyp nur vier Spalten in Zahlen um, alle Zusatzfelder bleiben Text."""
    lade(seite, TESTORDNER / "varianten.csv", len(varianten))
    erste = seite.evaluate("portfolioData[0]")
    assert erste["Preis_EUR"] == "0.32" and erste["Anzahl_Kunden"] == "62"
    assert erste["Umsatz_TEUR"] == 198.4
    protokoll["befunde"]["csv_zusatzfelder_als_text"] = {"Preis_EUR": erste["Preis_EUR"], "Anzahl_Kunden": erste["Anzahl_Kunden"]}


def test_semikolon_csv_mit_dezimalpunkt_funktioniert(seite, varianten, profile, tmp_path, protokoll):
    text = (TESTORDNER / "varianten.csv").read_text(encoding="utf-8")
    datei = tmp_path / "semikolon.csv"
    datei.write_bytes(("﻿" + text.replace(",", ";").replace("\n", "\r\n")).encode("utf-8"))
    lade(seite, datei, len(varianten))
    stelle_ein(seite, profile[0])
    assert lies_ergebnis(seite)["entscheidungen"] == logik.bewerte(varianten, profile[0])["entscheidungen"]
    protokoll["befunde"]["semikolon_bom_crlf_ok"] = True


def test_dezimalkomma_csv_wird_falsch_gelesen(seite, varianten, profile, tmp_path, protokoll):
    """Befund: So speichert ein deutsches Excel eine CSV (Semikolon, Dezimalkomma). Der Prototyp
    trennt auch am Komma, dadurch verrutschen die Spalten – ohne Fehlermeldung."""
    spalten = (TESTORDNER / "varianten.csv").read_text(encoding="utf-8").split("\n")[0].split(",")
    zeilen = [";".join(spalten)]
    for v in varianten:
        zellen = []
        for s in spalten:
            w = v.get(s, "")
            if isinstance(w, bool):
                w = "WAHR" if w else "FALSCH"
            elif isinstance(w, float):
                w = str(w).replace(".", ",")
            zellen.append(str(w))
        zeilen.append(";".join(zellen))
    datei = tmp_path / "excel_deutsch.csv"
    datei.write_text("\r\n".join(zeilen) + "\r\n", encoding="utf-8")

    status = lade(seite, datei, len(varianten))
    assert status == f"Geladen: excel_deutsch.csv ({len(varianten)} Varianten)"   # sieht erfolgreich aus
    assert seite.meldungen == []                                                  # keine Warnung
    erste = seite.evaluate("portfolioData[0]")
    assert erste["Umsatz_TEUR"] == 198 and erste["Marge_Pct"] == 4               # 198,4 → 198 | 4
    assert erste["Absatz_Stk"] == 24 and erste["Ruestkosten_Index"] == 620000    # alles um eine Spalte verrutscht
    assert erste["Status"] == "2"                                                # Rüstkosten-Index statt Status
    stelle_ein(seite, profile[0])
    falsch = lies_ergebnis(seite)
    richtig = logik.bewerte(varianten, profile[0])
    assert falsch["entscheidungen"] != richtig["entscheidungen"]
    protokoll["befunde"]["dezimalkomma_csv"] = {
        "status_im_prototyp": status, "fehlermeldung": None,
        "erste_zeile_gelesen": {k: erste[k] for k in fd.PROTOTYP_SPALTEN},
        "erste_zeile_richtig": {k: varianten[0][k] for k in fd.PROTOTYP_SPALTEN},
        "varianten_behalten_falsch": falsch["varianten_behalten"],
        "varianten_behalten_richtig": richtig["varianten_behalten"],
    }
