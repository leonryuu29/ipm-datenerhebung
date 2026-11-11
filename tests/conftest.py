"""Gemeinsame Pfade und Daten für die Tests."""
import json
import sys
from pathlib import Path

import pytest

WURZEL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WURZEL / "generator"))

import felder as fd  # noqa: E402

TESTORDNER = WURZEL / "data" / "synthetic" / f"technischer_test_v{fd.VERSION}"
VORLAGE = WURZEL / "vorlagen" / f"VARIANTEN_VORLAGE_v{fd.VERSION}.xlsx"
TEST_EXCEL = TESTORDNER / f"technischer_testdatensatz_v{fd.VERSION}.xlsx"
PROTOTYP = WURZEL / "tests" / "prototyp" / "ki_wrapper_variantenmanagement.html"
ERGEBNISSE = WURZEL / "tests" / "ergebnisse"


@pytest.fixture(scope="session")
def varianten():
    return json.loads((TESTORDNER / "varianten.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def profile():
    return json.loads((TESTORDNER / "strategieprofile.json").read_text(encoding="utf-8"))
