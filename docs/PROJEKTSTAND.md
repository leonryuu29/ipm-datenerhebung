# Projektstand – Teilprojekt Datenerhebung

**Stand:** 13.11.2026  
**Status-Labels:** `BESCHLOSSEN` (im Team oder mit Betreuer festgelegt) · `VORSCHLAG` (noch abzustimmen) · `OFFEN`

## 1. Auftrag (Thema 6, Steffen Feld)

Wie könnte ein KI-Agent aussehen, der anhand von Stücklisten, Portfolioübersichten, Merkmalsanforderungen und Ausprägungen ein Optimum an Varianten generiert – zwischen ausreichender Marktvarianz (kein Wettbewerbsnachteil) und wettbewerbsfähiger Fertigung (Skaleneffekte)? Quelle: Aufgabenstellung IPM WiSe 2026/27, Folie 15.

## 2. Beschlüsse

| Datum | Beschluss | Quelle | Status |
| --- | --- | --- | --- |
| 05.11. | Produktgruppe frei wählbar; einfache Beispiele (Verpackung, Farben, Größen, Profillängen) empfohlen. Keine Hettich-Daten. | Gespräch Steffen Feld | BESCHLOSSEN |
| 05.11. | Agent soll neue Varianten vorschlagen; Ergebnis 2–3 Vorschläge als Rangfolge plus Empfehlung. | Gespräch Steffen Feld | BESCHLOSSEN |
| 05.11. | Bewertung berücksichtigt Variantenkosten und den Variantenbildungspunkt (möglichst spät, „Tannenbaum“). | Gespräch Steffen Feld | BESCHLOSSEN |
| 05.11. | Nur Produktionsbetriebe; nach Strategie unterscheiden: Massenproduzent, Kostenführer, Innovationsführer, Nischenanbieter. | Gespräch Steffen Feld | BESCHLOSSEN |
| 05.11. | Schnittstelle für Fertigungskomplexität vorsehen, auch wenn sie im Beispiel leer bleibt. | Gespräch Steffen Feld | BESCHLOSSEN |
| 05.11. | Öffentliche Wettbewerbsinformationen zulässig, Quellen immer angeben. | Gespräch Steffen Feld | BESCHLOSSEN |
| 09.11. | Kein eigenes Modelltraining: Interface/Schnittstelle vor bestehendem LLM (ChatGPT, Gemini o. ä.), Daten als JSON. | Teammeeting | BESCHLOSSEN |
| 09.11. | Am Ende lauffähiger Prototyp mit selbst gewählten, fiktiven Daten in kleinem Umfang. | Teammeeting | BESCHLOSSEN |
| 09.11. | Rollen: Yannick (Projektleitung, Umsetzung), Linus (Umsetzung), Lukas + David (Konzeptentwicklung), Mark (Controlling/Wirtschaftlichkeit), Yu + Jonas (Datenerhebung). Marketing und Fertigungsaufwand entfallen. | Teammeeting; IPM Gruppezuteilung 6.xlsx | BESCHLOSSEN |
| 09.11. | Testphase mit synthetischen Daten; Struktur an realen ERP-Exporten orientiert, damit reale Daten später austauschbar sind. | Abstimmung Yu | BESCHLOSSEN |
| 10.11. | Produktfall: fiktiver Kartonagenhersteller mit 3–4 Strategieprofilen. | Aufgabenliste Datenerhebung; Pitch v3 | VORSCHLAG (Freigabe durch Steffen Feld am 20.11. geplant) |
| 11.11. | Arbeitsteilung Datenerhebung: Jonas fachlich (Produktfall, Strategieprofile, Annahmen, Plausibilität), Yu technisch (Schema, Generator, Validierung, Übergabe). | Zusage Jonas per Chat | BESCHLOSSEN |
| 11.11. | Jonas trägt bis zum Treffen am 13.11. etwa 10–15 Kartonvarianten und die vier Strategieprofile in die Excel-Vorlage ein; am 13.11. wird die Tabelle in den Prototyp geladen. | Chat Yu/Jonas | BESCHLOSSEN |
| 11.11. | Feldliste und JSON-Schema v0.1: Stufe 1 = Variantentabelle (sieben Pflichtspalten des Prototyps plus optionale Felder) und Strategieprofile (elf Regler des Prototyps); Stufe 2 = Entwurf der weiteren ERP-Blöcke. | `reports/FELDLISTE_v0.1_DE.pdf`, `schema/` | VORSCHLAG |
| 11.11. | Übergabe an den Prototyp nur über den Konverter (`generator/excel_zu_prototyp.py`), nicht als direkt aus Excel gespeicherte CSV. | Testprotokoll 11.11., Befund B1 | VORSCHLAG |
| 12.11. | Varianten orientieren sich an einem öffentlichen Katalog (RAJA Hauptkatalog 09/2026): Artikelnummer, Maße und Wellenzahl stammen aus dem Katalog, alle Geschäftszahlen bleiben SYNTHETIC. | Vorschlag Jonas per Chat; `data/reference/QUELLEN.md` | VORSCHLAG |
| 12.11. | Neues optionales Feld `Referenz_Artikelnr` in der Variantentabelle (Schema bleibt v0.1, da noch nicht abgestimmt). | `generator/felder.py` | VORSCHLAG |
| 13.11. | Übergabeformat: JSON ist das offizielle Format für die Produktdaten; CSV bleibt vorerst als Nebenausgabe, bis die Umsetzung startet. | Teamtreffen 13.11. | BESCHLOSSEN |
| 13.11. | `Must_Have` wird aus den Daten entfernt; die Auswahl trifft der Nutzer später in der Oberfläche (Maske). | Teamtreffen 13.11. | BESCHLOSSEN |
| 13.11. | Subjektive Beschreibungsfelder entfallen; die Daten enthalten nur objektive Produktinformationen. `Bemerkung` entfällt sicher; über weitere Felder entscheidet das Konzept. | Teamtreffen 13.11. | BESCHLOSSEN (Details OFFEN) |
| 13.11. | Das Konzept erstellt auf Basis unserer Feldliste v0.1 eine eigene vollständige Fassung; danach gemeinsamer Abgleich und Schema v1. | Teamtreffen 13.11.; Gespräch Yannick, Lukas, Yu | BESCHLOSSEN |
| 13.11. | Keine Erzeugung von ERP-Testdaten, bevor die Felder feststehen. | Gespräch Yannick, Lukas, Yu | BESCHLOSSEN |
| 13.11. | Der HTML-Prototyp der Umsetzung ist nur eine Konzeptdemo und wird nicht weiter als Maßstab für die Daten verwendet. | Teamtreffen 13.11. | BESCHLOSSEN |
| 13.11. | Projektname und Logo: vArIanz – KI-basiertes Variantenmanagement (Konzept). | Teamtreffen 13.11.; `logo.jpeg` | BESCHLOSSEN |
| 13.11. | Schema v0.2: `Must_Have` und `Bemerkung` aus Variantentabelle, Vorlage und Testdaten entfernt; Beispielzeilen der Vorlage werden über die Kennung `BEISPIEL_…` erkannt. | `generator/felder.py`, `reports/FELDLISTE_v0.2_DE.pdf` | BESCHLOSSEN (folgt aus dem Treffen) |
| 13.11. | Ein gemeinsamer Datensatz mit vier Strategieprofilen statt eines Datensatzes je Strategie (passt zu Folie 11: gleicher Datensatz, anderes Profil, andere Empfehlung). | Yu | VORSCHLAG |

## 3. Termine

| Termin | Was | Wer |
| --- | --- | --- |
| 10.11., 12:00 | Teilaufgaben je Gruppe in den Share-Ordner | alle Gruppen |
| 11.11., 18:00 | Erste Projektpräsentation per Mail an Prof. Fahrig | Yannick (Integration) |
| 12.11., 16:00 | One-Pager KW46 | Yannick |
| 13.11., 09:30 | Teamtreffen in Präsenz (Protokoll: `docs/PROTOKOLL_2026-11-13_CN.md`) | alle |
| 20.11., mittags | Gespräch mit Michal (Modul) und Steffen Feld vor Ort; jeder stellt seinen Teil vor, eher Fragen als Vortrag | alle |
| nach Feldabgleich mit dem Konzept | Datenmodell und JSON-Schema v1 | Yu |
| danach | Datenpaket v1 an Umsetzung | Yu, Jonas |
| 06.12. | Abschluss Konzeptentwicklung | Konzept |
| 17.12. | Abschlusspräsentation | alle |
| 15.01.2027 | Abgabe Hausarbeit (ca. 8 Seiten pro Person) | alle |

## 4. Stand der Arbeitspakete

| AP | Stand 13.11. |
| --- | --- |
| D1 Mindestfelder | Feldliste v0.1 im Treffen vorgestellt, Rückmeldung positiv. Das Konzept erstellt jetzt eine eigene Fassung; danach Abgleich. |
| D2 Produktfall und Strategieprofile | Jonas hat 15 Varianten aus dem RAJA-Katalog eingetragen. Pausiert, bis die Felder feststehen. |
| D3 Datenmodell und JSON-Schema | v0.2 vorhanden (ohne `Must_Have` und `Bemerkung`); v1 nach dem Feldabgleich mit dem Konzept. |
| D7/D10 Validierung, Integration | Konverter und Prüfregeln vorhanden, 70 Tests für v0.2; im Treffen positiv bewertet. |
| D8 Testszenarien | Testfallkatalog v0.1 mit acht Fällen (Vorschlag). |
| D4, D5, D6, D9, D11 | noch nicht begonnen; D6 (Generator für die ERP-Datenblöcke) wartet auf die Felder. |

## 5. Offene Punkte

1. Felder: Fassung des Konzepts abwarten und abgleichen; welche weiteren subjektiven Felder entfallen (`Bezeichnung`, `Beschreibung`?); `Bemerkung` entfällt sicher.
2. Bleibt `Hauptkunde_Anteil_Pct` drin? Im Treffen positiv bewertet, Entscheidung beim Konzept.
3. Ein Datensatz je Strategie oder ein gemeinsamer Datensatz mit vier Profilen (Vorschlag Yu: gemeinsamer Datensatz). Auf Folie 10 steht noch „ein Datensatz je Strategie“.
4. Analyse je Produktgruppe statt für das ganze Unternehmen (Diskussion im Konzept) – Folgen für die Datenstruktur.
5. Konzept für die ERP-Anbindung (Schnittstellen, API, Abfragen) – liegt beim Konzept, Datenerhebung liefert die Datenblöcke.
6. Freigabe des Pilotfalls Kartonagen durch Steffen Feld (20.11.).
7. Klären, ob später reale oder anonymisierte Daten von Steffen Feld möglich sind.
8. Arbeitszeiten laufend an Mark melden (Projektkosten 100 €/h laut Steffen Feld).

## 6. Quellen

- Aufgabenstellung IPM WiSe 2026/27 (Prof. Fahrig), Folie 15 – Thema 6.
- Transkript Gespräch mit Steffen Feld, 05.11.2026.
- Transkript Teammeeting, 09.11.2026 („11.9分工&计划&实操细节“).
- IPM Gruppezuteilung 6.xlsx (Share-Ordner, Stand 09.11.2026).
- Team-Repo YanOkoli/hsbi-ipm: PROJEKTKONTEXT.md, Pflichtenheft-Entwurf v0.3, PSP-Entwurf.
- Prototyp der Umsetzung `ki_wrapper_variantenmanagement.html`, Stand 10.11.2026 (Share-Ordner); Kopie für Tests in `tests/prototyp/`.
- Testprotokoll `tests/TESTPROTOKOLL_2026-11-11.md`.
- Protokoll Teamtreffen 13.11.2026: `docs/PROTOKOLL_2026-11-13_CN.md`; Aufnahme und Transkript im Projektordner `会议录音（重点看）`.
