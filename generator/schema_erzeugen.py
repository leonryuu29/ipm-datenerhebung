"""Erzeugt die JSON-Schemas und die maschinenlesbare Feldliste aus felder.py.

Aufruf:  python generator/schema_erzeugen.py
"""
from __future__ import annotations

import json
from pathlib import Path

import felder as fd

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schema"


def schreibe(pfad: Path, daten) -> None:
    pfad.write_text(json.dumps(daten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("geschrieben:", pfad.relative_to(SCHEMA_DIR.parent))


def feldliste() -> dict:
    return {
        "version": fd.VERSION,
        "stand": fd.STAND,
        "kennzeichnung": fd.KENNZEICHNUNG,
        "prototyp_spalten": fd.PROTOTYP_SPALTEN,
        "bloecke": [
            {
                "id": b["id"], "stufe": b["stufe"], "titel": b["titel"], "titel_cn": b["titel_cn"],
                "beschreibung": b["de"], "beschreibung_cn": b["cn"],
                "felder": [
                    {
                        "name": f["name"], "pflicht": f["pflicht"], "typ": f["typ"], "einheit": f["einheit"],
                        "erlaubte_werte": f["enum"], "minimum": f["min"], "maximum": f["max"],
                        "beispiel": f["beispiel"], "herkunft": f["herkunft"], "prototyp_id": f["prototyp_id"],
                        "beschreibung": f["de"], "beschreibung_cn": f["cn"],
                    }
                    for f in b["felder"]
                ],
            }
            for b in fd.BLOECKE
        ],
    }


def main() -> None:
    SCHEMA_DIR.mkdir(exist_ok=True)
    v = fd.VERSION
    schreibe(SCHEMA_DIR / f"varianten_v{v}.schema.json", fd.schema_varianten())
    schreibe(SCHEMA_DIR / f"strategieprofile_v{v}.schema.json", fd.schema_strategieprofile())
    schreibe(SCHEMA_DIR / f"datenpaket_v{v}.schema.json", fd.schema_datenpaket())
    schreibe(SCHEMA_DIR / f"felder_v{v}.json", feldliste())


if __name__ == "__main__":
    main()
