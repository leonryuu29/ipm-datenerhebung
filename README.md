# IPM Thema 6 – Teilprojekt Datenerhebung

Datengrundlage für den Prototyp des KI-gestützten Variantenmanagements (Projektteam 6, HSBI, WiSe 2026/27).
Verantwortlich: Yu Zhaoze (Technik), Jonas F. (Fachlichkeit).

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
| `schema/` | JSON-Schema (Datenvertrag mit Konzept und Umsetzung) |
| `generator/` | Python-Datengenerator (reproduzierbar, Szenario je Strategie) |
| `data/synthetic/` | Erzeugte Datensätze, gekennzeichnet als SYNTHETIC |
| `data/reference/` | Öffentliche Referenzdaten mit Quelle und Abrufdatum |
| `tests/` | Schema- und Plausibilitätsprüfungen, Testszenarien |

## Einstieg

1. [docs/PROJEKTSTAND.md](docs/PROJEKTSTAND.md) lesen – aktueller Stand, Beschlüsse, Termine.
2. [reports/DATENERHEBUNG_AUFGABEN_DE.pdf](reports/DATENERHEBUNG_AUFGABEN_DE.pdf) – Arbeitspakete und Arbeitsteilung.
3. [AGENTS.md](AGENTS.md) – Arbeitsregeln für dieses Repo.

## Verhältnis zum Team-Repo

Das Team-Repo ist [YanOkoli/hsbi-ipm](https://github.com/YanOkoli/hsbi-ipm) (Dokumentation auf `main`, Umsetzung geplant als eigener Branch). Dieses Repo wird zunächst lokal gepflegt und später als Branch bzw. Ordner in das Team-Repo übertragen.
