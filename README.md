# IPM Thema 6 – Teilprojekt Datenerhebung

Datengrundlage für den Prototyp des KI-gestützten Variantenmanagements (Projektteam 6, HSBI, WiSe 2026/27).
Verantwortlich: Yu Zhaoze (Technik), Jonas Flütebonies (Fachlichkeit).

> **Kurz (中文):** 数据采集子项目的仓库。我们提供模拟 ERP 导出的虚构数据集和数据约定（JSON Schema），作为团队 Interface/原型的输入。测试阶段用虚构数据；结构按真实 ERP 设计，以后可直接换真实数据。

## Worum es geht

Das Team baut kein eigenes KI-Modell, sondern ein Interface vor einem bestehenden LLM. Unternehmensdaten werden als JSON übergeben, zusammen mit einem System-Prompt (Unternehmensstrategie, gängige Variantenstrategien); das LLM liefert 2–3 gerankte Variantenvorschläge und eine Empfehlung.

```
ERP-Export (synthetisch) → Datenschnittstelle (Validierung, JSON) → Interface / System-Prompt → LLM → Empfehlung
   └── dieses Repo ──────────────────────────┘                    └── Konzept + Umsetzung ──┘
```

## Struktur

| Ordner | Inhalt |
| --- | --- |
| `docs/` | Projektstand, Entscheidungen, offene Punkte, später Datenwörterbuch und Annahmenregister |
| `reports/` | Abgaben und Arbeitsstände als DOCX/PDF (DE + CN) |
| `schema/` | JSON-Schemas v0.1 (Datenvertrag mit Konzept und Umsetzung) und maschinenlesbare Feldliste |
| `vorlagen/` | Excel-Vorlage für die fachliche Datenerfassung |
| `generator/` | Felddefinitionen, Schema- und Vorlagenerzeugung, Prüfung, Konverter Excel → CSV/JSON; später der Datengenerator |
| `data/synthetic/` | Datensätze, gekennzeichnet als SYNTHETIC |
| `data/reference/` | Öffentliche Referenzdaten mit Quelle und Abrufdatum |
| `tests/` | Automatische Tests, Kopie des Prototyps, Ergebnisse und Testprotokolle |

## Daten für den Prototyp erzeugen

```
pip install openpyxl jsonschema pytest playwright
python generator/excel_zu_prototyp.py <ausgefüllte_vorlage.xlsx> --out data/synthetic/<name>
```

Der Konverter prüft die Daten und schreibt `varianten.csv`, `varianten.json`, `strategieprofile.json` und `pruefbericht.txt`. Bei Fehlern schreibt er nur den Prüfbericht. `varianten.json` oder `varianten.csv` wird im Prototyp über „Eigene Stückliste / Portfolio laden“ hochgeladen.

Felder ändern: nur in `generator/felder.py`, danach `python generator/schema_erzeugen.py` und `python generator/vorlage_erzeugen.py`. Tests: `python -m pytest tests -v` (der Browser-Test braucht `playwright install chromium` und Internet).

## Einstieg

1. [docs/PROJEKTSTAND.md](docs/PROJEKTSTAND.md) lesen – aktueller Stand, Beschlüsse, Termine.
2. [reports/DATENERHEBUNG_AUFGABEN_DE.pdf](reports/DATENERHEBUNG_AUFGABEN_DE.pdf) – Arbeitspakete und Arbeitsteilung.
3. [reports/FELDLISTE_v0.1_DE.pdf](reports/FELDLISTE_v0.1_DE.pdf) – Feldliste, erster Entwurf des Datenvertrags.
4. [tests/TESTPROTOKOLL_2026-11-11.md](tests/TESTPROTOKOLL_2026-11-11.md) – was getestet ist und was dabei aufgefallen ist.
5. [AGENTS.md](AGENTS.md) – Arbeitsregeln für dieses Repo.

## Verhältnis zum Team-Repo

Das Team-Repo ist [YanOkoli/hsbi-ipm](https://github.com/YanOkoli/hsbi-ipm) (Dokumentation auf `main`, Umsetzung geplant als eigener Branch). Dieses Repo wird zunächst lokal gepflegt und später als Branch bzw. Ordner in das Team-Repo übertragen.
