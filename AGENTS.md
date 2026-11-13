# Arbeitsregeln für dieses Repository

- Zuerst `docs/PROJEKTSTAND.md` lesen. Neue Beschlüsse dort mit Datum, Quelle und Status eintragen.
- Beschlüsse, Vorschläge und offene Punkte klar trennen (`BESCHLOSSEN`, `VORSCHLAG`, `OFFEN`).
- Alle erfundenen Daten als `SYNTHETIC` kennzeichnen. Öffentliche Referenzdaten nur mit URL und Abrufdatum in `data/reference/` ablegen.
- Keine Ergebnisse, Kosten oder Wettbewerbsfakten erfinden, die als real ausgegeben werden.
- Datengenerator muss reproduzierbar sein (feste Seeds); Datensätze werden nie von Hand verändert, sondern neu erzeugt.
- Schema-Änderungen nur mit Abstimmung mit Konzept und Umsetzung; Version im Schema hochzählen.
- Team-Dokumente auf Deutsch; für Yu zusätzlich chinesische Fassungen (`*_CN`). Abgaben als DOCX/PDF in `reports/`.
- Arbeitszeiten für das Controlling (Mark) mitführen.
- Felder nur in `generator/felder.py` ändern; danach Schemas und Vorlage neu erzeugen und alle Tests laufen lassen (`docs/AUSFUEHREN_CN.md`).
- Übergabeformat ist JSON; CSV ist nur Nebenausgabe.
- Commits als Yu Zhaoze, ohne Hinweise auf KI-Werkzeuge (keine Co-Authored-By-, Session- oder „Generated with“-Zeilen).
