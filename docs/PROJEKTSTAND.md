# Projektstand – Teilprojekt Datenerhebung

**Stand:** 10.11.2026  
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
| 10.11. | Produktfall: fiktiver Kartonagenhersteller mit 3–4 Strategieprofilen. | Aufgabenliste Datenerhebung | VORSCHLAG |

## 3. Termine

| Termin | Was | Wer |
| --- | --- | --- |
| 10.11., 12:00 | Teilaufgaben je Gruppe in den Share-Ordner | alle Gruppen |
| 11.11., 18:00 | Erste Projektpräsentation per Mail an Prof. Fahrig | Yannick (Integration) |
| 12.11., 16:00 | One-Pager KW46 | Yannick |
| 13.11., 09:30 | Teamtreffen in Präsenz | alle |
| Ende KW47 | Datenmodell und JSON-Schema v1 | Yu |
| Ende KW48 | Datenpaket v1 an Umsetzung | Yu, Jonas |
| 06.12. | Abschluss Konzeptentwicklung | Konzept |
| 17.12. | Abschlusspräsentation | alle |
| 15.01.2027 | Abgabe Hausarbeit (ca. 8 Seiten pro Person) | alle |

## 4. Offene Punkte

1. Produktfall Kartonagen im Team bestätigen.
2. JSON oder YAML mit der Umsetzung festlegen.
3. Mindestfelder aus Sicht der Konzeptentwicklung erhalten.
4. Arbeitsteilung mit Jonas bestätigen (am 09.11. nicht anwesend).
5. Klären, ob später reale oder anonymisierte Daten von Steffen Feld möglich sind.
6. Arbeitszeiten laufend an Mark melden (Projektkosten 100 €/h laut Steffen Feld).

## 5. Quellen

- Aufgabenstellung IPM WiSe 2026/27 (Prof. Fahrig), Folie 15 – Thema 6.
- Transkript Gespräch mit Steffen Feld, 05.11.2026.
- Transkript Teammeeting, 09.11.2026 („11.9分工&计划&实操细节“).
- IPM Gruppezuteilung 6.xlsx (Share-Ordner, Stand 09.11.2026).
- Team-Repo YanOkoli/hsbi-ipm: PROJEKTKONTEXT.md, Pflichtenheft-Entwurf v0.3, PSP-Entwurf.
