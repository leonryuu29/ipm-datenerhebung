# Testprotokoll 11.11.2026 – Feldliste, Vorlage, Konverter und Prototyp

**Teilprojekt Datenerhebung · IPM WiSe 2026/27 · Gruppe 6 · durchgeführt von Yu Zhaoze**

> Hinweis (13.11.2026): Dieses Protokoll gilt für Schema v0.1 (mit `Must_Have`). Seit v0.2 entfallen `Must_Have` und `Bemerkung`. Die Dateien in `tests/ergebnisse/` werden bei jedem Testlauf überschrieben; die Zahlen unten stammen aus dem Lauf vom 11.11.2026.

## 1. Ergebnis in Kürze

- **70 von 70 automatischen Tests bestanden** (pytest, Laufzeit rund 6 Sekunden).
- Unsere CSV- und unsere JSON-Datei lassen sich in den Prototyp der Umsetzung laden. Mit allen vier Strategieprofilen liefert der Prototyp genau die Empfehlungen und Kennzahlen, die wir aus seinen Regeln berechnet haben.
- Der Weg Excel-Vorlage → Konverter → Prototyp funktioniert von Anfang bis Ende.
- Sechs Befunde für die Abstimmung am 13.11. (Abschnitt 6). Der wichtigste: Eine CSV, die direkt aus einem deutschen Excel gespeichert wird, liest der Prototyp **ohne Fehlermeldung falsch**.

Alle Testdaten sind erfunden (SYNTHETIC) und fachlich nicht abgestimmt. Die Zahlen unten zeigen, dass die Technik funktioniert – sie sind keine fachliche Aussage über Kartonhersteller.

## 2. Was getestet wurde

| Gegenstand | Version / Stand |
| --- | --- |
| Feldliste und JSON-Schemas | v0.1 (`generator/felder.py`, `schema/`) |
| Excel-Vorlage | `vorlagen/VARIANTEN_VORLAGE_v0.1.xlsx` |
| Konverter | `generator/excel_zu_prototyp.py` |
| Technischer Testdatensatz | `data/synthetic/technischer_test_v0.1/` – 14 Kartonvarianten, 4 Strategieprofile |
| Prototyp der Umsetzung | `ki_wrapper_variantenmanagement.html`, Stand 10.11.2026, unveränderte Kopie aus dem Share-Ordner, SHA-256 `cf360e0f297bccb1…` |

Umgebung: Linux, Python 3.13.18, pytest 9.1.1, openpyxl 3.1.5, jsonschema 4.26.0, Playwright 1.63.0 mit Chromium (headless). Der Prototyp lädt Tailwind und Plotly aus dem Internet; ohne Internet startet er nicht.

Wiederholen:

```
python generator/schema_erzeugen.py
python generator/vorlage_erzeugen.py
python generator/excel_zu_prototyp.py data/synthetic/technischer_test_v0.1/technischer_testdatensatz_v0.1.xlsx --out data/synthetic/technischer_test_v0.1
python -m pytest tests -v
```

## 3. Testfälle und Ergebnis

| Nr. | Bereich | Was geprüft wird | Tests | Ergebnis |
| --- | --- | --- | --- | --- |
| S1 | Schema | Die drei Schemas sind gültiges JSON-Schema (Draft 2020-12) und die Dateien in `schema/` sind aktuell | 3 | bestanden |
| S2 | Schema | Die sieben Spalten des Prototyps sind Pflichtfelder | 1 | bestanden |
| S3 | Schema | Die Beispielwerte aller 10 Datenblöcke passen zum Schema | 10 | bestanden |
| S4 | Schema | Der Testdatensatz ist fehlerfrei; das Datenpaket der Stufe 1 wird angenommen, eine Kennzeichnung ungleich SYNTHETIC abgelehnt | 2 | bestanden |
| S5 | Prüfung | 16 fehlerhafte Variantentabellen werden abgelehnt (Pflichtfeld fehlt, Status unbekannt, Index 0 und 11, negative Menge, Zahl als Text, Kennung mit Komma oder Leerzeichen, doppelte Kennung, Komma oder Semikolon im Text, unbekanntes Feld und weitere) | 16 | bestanden |
| S6 | Prüfung | Auffällige, aber nutzbare Daten geben einen Hinweis (Umsatz passt nicht zu Absatz × Preis; ein Kunde mit Anteil unter 100 %; Auslauf und Must-Have zugleich); 1,5 % Abweichung gibt keinen Hinweis | 4 | bestanden |
| S7 | Prüfung | 5 fehlerhafte Strategieprofile werden abgelehnt; Mindestabsatz außerhalb des Reglers und ein fehlendes Profil geben einen Hinweis | 7 | bestanden |
| K1 | Konverter | Die Vorlage hat alle Blätter, Spalten und Dropdowns | 1 | bestanden |
| K2 | Konverter | Die leere Vorlage wird abgelehnt; die drei Beispielzeilen zählen nicht als Daten | 2 | bestanden |
| K3 | Konverter | Rundlauf: Excel → JSON ergibt exakt die Ausgangsdaten; die abgelegten Dateien sind aktuell | 2 | bestanden |
| K4 | Konverter | Die CSV hat die sieben Prototyp-Spalten vorn, Dezimalpunkt, true/false, kein Semikolon, keine Anführungszeichen | 1 | bestanden |
| K5 | Konverter | Ein als Text eingegebenes Dezimalkomma („198,4“) wird richtig umgewandelt | 1 | bestanden |
| K6 | Konverter | 7 Fehler in der Excel-Datei stoppen die Übergabe und stehen im Prüfbericht | 7 | bestanden |
| K7 | Konverter | Eine Umsatzabweichung ist ein Hinweis und kein Fehler | 1 | bestanden |
| P1 | Prototyp | Die Regler des Prototyps (Namen, Bereiche, Auswahlwerte) passen zu unserer Feldliste | 1 | bestanden |
| P2 | Prototyp | Upload von CSV und JSON: Status „Geladen: … (14 Varianten)“, keine Fehlermeldung, alle sieben Spalten richtig gelesen | 2 | bestanden |
| P3 | Prototyp | Je Strategieprofil: Empfehlung für alle 14 Varianten und die Kennzahlen stimmen mit unserer Berechnung überein, über CSV und über JSON | 4 | bestanden |
| P4 | Prototyp | Unsere Zusatzfelder erscheinen im erzeugten Prompt | 1 | bestanden |
| P5 | Prototyp | Befund B3: Über CSV bleiben Zusatzfelder Text | 1 | bestanden |
| P6 | Prototyp | CSV mit Semikolon, Dezimalpunkt, BOM und Windows-Zeilenenden funktioniert | 1 | bestanden |
| P7 | Prototyp | Befund B1: CSV mit Dezimalkomma wird falsch gelesen | 1 | bestanden (Verhalten nachgewiesen) |
| P8 | Prototyp | Befund B2: WAHR/FALSCH wird nicht erkannt | 1 | bestanden (Verhalten nachgewiesen) |

Vollständige Ausgabe: `tests/ergebnisse/pytest_2026-11-11.txt`. Messwerte aus dem Browser: `tests/ergebnisse/prototyp_lauf.json`.

## 4. Lauf im Prototyp – Kennzahlen je Strategieprofil

Eingestellte Profile (technischer Vorschlag, fachlich noch nicht abgestimmt):

| Regler | Massenproduzent | Kostenführer | Innovationsführer | Nischenanbieter |
| --- | --- | --- | --- | --- |
| Min_Umsatzabdeckung_Pct | 85 | 80 | 90 | 95 |
| Kernmaerkte_schuetzen | ja | ja | ja | ja |
| Entkopplungspunkt | MTS | MTS | ATO | ETO |
| Max_Ruestkosten_Index | 4 | 3 | 8 | 9 |
| Ueberspezifikation_erlaubt | ja | ja | nein | nein |
| Min_Marge_Pct | 15 | 20 | 18 | 25 |
| Min_Absatz_Stk | 1500 | 1500 | 500 | 0 |
| Ziel_Gleichteilequote_Pct | 80 | 85 | 50 | 30 |
| Sourcing | Single | Single | Dual | Dual |
| Zukunft_schuetzen | nein | nein | ja | ja |
| Auslauf_streichen | ja | ja | ja | nein |

Vom Prototyp angezeigte Kennzahlen:

| Strategieprofil | Behalten | Umsatzabdeckung | Ziel | Abweichung | Ø Marge behalten | Bildschirmfoto |
| --- | --- | --- | --- | --- | --- | --- |
| Massenproduzent | 8 von 14 | 82,1 % | 85 % | -2,9 Punkte | 25,3 % | `ergebnisse/prototyp_massenproduzent.png` |
| Kostenführer | 6 von 14 | 66,3 % | 80 % | -13,7 Punkte | 27,7 % | `ergebnisse/prototyp_kostenfuehrer.png` |
| Innovationsführer | 8 von 14 | 80,8 % | 90 % | -9,2 Punkte | 24,3 % | `ergebnisse/prototyp_innovationsfuehrer.png` |
| Nischenanbieter | 7 von 14 | 67,2 % | 95 % | -27,8 Punkte | 25,0 % | `ergebnisse/prototyp_nischenanbieter.png` |

Mit diesem Testdatensatz verfehlt jedes der vier Profile sein Ziel für die Umsatzabdeckung. Ein wesentlicher Grund steht in Befund B5.

## 5. Lauf im Prototyp – Empfehlung je Variante

| Variante | Umsatz TEUR | Marge % | Absatz Stk | Rüst | Status | Must | Massenproduzent | Kostenführer | Innovationsführer | Nischenanbieter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| K01_0201_200x150x100_B | 198,4 | 24 | 620000 | 2 | Standard | ja | Behalten (Kernmarkt) | Behalten (Kernmarkt) | Behalten (Kernmarkt) | Behalten (Kernmarkt) |
| K02_0201_300x200x150_B | 229,5 | 26 | 510000 | 2 | Standard | ja | Behalten (Kernmarkt) | Behalten (Kernmarkt) | Behalten (Kernmarkt) | Behalten (Kernmarkt) |
| K03_0201_305x200x150_B | 17,9 | 13 | 38000 | 4 | Standard | nein | Streichen (Finanzziel) | Streichen (Finanzziel) | Streichen (Finanzziel) | Streichen (Finanzziel) |
| K04_0201_400x300x200_BC | 235,2 | 22 | 240000 | 3 | Standard | ja | Behalten (Kernmarkt) | Behalten (Kernmarkt) | Behalten (Kernmarkt) | Behalten (Kernmarkt) |
| K05_0201_600x400x400_BC | 175,8 | 19 | 95000 | 3 | Standard | nein | Behalten | Streichen (Finanzziel) | Behalten | Streichen (Finanzziel) |
| K06_0427_250x175x80_E_1c | 111,6 | 31 | 180000 | 5 | Standard | nein | Modularisieren | Modularisieren | Behalten | Behalten |
| K07_0427_310x220x100_E_4c | 66,0 | 35 | 60000 | 8 | Standard | nein | Modularisieren | Modularisieren | Behalten | Behalten |
| K08_0201_347x253x118_B_SG | 161,2 | 11 | 310000 | 6 | Sonderlocke | nein | Streichen (Finanzziel) | Streichen (Finanzziel) | Streichen (Finanzziel) | Streichen (Finanzziel) |
| K09_0421_180x130x60_E | 0,9 | 7 | 900 | 9 | Sonderlocke | nein | Streichen (Finanzziel) | Streichen (Finanzziel) | Streichen (Finanzziel) | Streichen (Finanzziel) |
| K10_0203_300x200x100_C | 12,1 | 12 | 22000 | 5 | Auslauf | nein | Streichen (Auslauf) | Streichen (Auslauf) | Streichen (Auslauf) | Streichen (Finanzziel) |
| K11_0201_250x200x150_C | 28,7 | 21 | 70000 | 3 | Auslauf | nein | Streichen (Auslauf) | Streichen (Auslauf) | Streichen (Auslauf) | Streichen (Finanzziel) |
| K12_0427_250x175x80_E_GP | 10,9 | 9 | 14000 | 7 | Zukunft | nein | Streichen (Finanzziel) | Streichen (Finanzziel) | Behalten (Zukunft) | Behalten (Zukunft) |
| K13_0711_300x200x150_B_AB | 17,2 | 28 | 26000 | 7 | Zukunft | nein | Modularisieren | Modularisieren | Behalten (Zukunft) | Behalten (Zukunft) |
| K14_0201_300x200x150_EB | 27,8 | 17 | 48000 | 4 | Standard | nein | Behalten | Streichen (Finanzziel) | Streichen (Finanzziel) | Streichen (Finanzziel) |

Der Testdatensatz löst alle sechs Empfehlungen des Prototyps mindestens einmal aus.

## 6. Befunde

| Nr. | Befund | Folge | Vorschlag |
| --- | --- | --- | --- |
| B1 | Der Prototyp trennt CSV-Zeilen an Komma **und** Semikolon. Eine CSV aus einem deutschen Excel (Semikolon als Trenner, Dezimalkomma) wird deshalb falsch gelesen: Aus „198,4“ werden zwei Spalten, alles dahinter verrutscht. Der Prototyp meldet trotzdem „Geladen: … (14 Varianten)“ und zeigt keine Fehlermeldung. Gemessen an der ersten Zeile: Marge 4 statt 24, Absatz 24 statt 620000, Rüstkosten-Index 620000 statt 2. Behalten werden 1 statt 8 Varianten. | Falsche Ergebnisse, die man nicht sofort bemerkt. | Bei uns gelöst: Daten immer über den Konverter erzeugen, nie direkt aus Excel als CSV speichern. An die Umsetzung: beim Einlesen nur ein Trennzeichen verwenden oder die Spaltenzahl prüfen und warnen. |
| B2 | Must_Have erkennt true, 1 und ja, aber nicht WAHR (deutsches Excel). Alle drei Must-Have-Varianten verlieren den Schutz. | Kernmarkt-Varianten können gestrichen werden. | Bei uns gelöst: Der Konverter schreibt true/false. |
| B3 | Über CSV wandelt der Prototyp nur vier Spalten in Zahlen um. Zusatzfelder wie Preis_EUR oder Anzahl_Kunden stehen dann als Text im Prompt („0.32“). Über JSON bleiben sie Zahlen. | Das LLM bekommt Zahlen als Text. | JSON als Übergabeformat festlegen. |
| B4 | Der Regler Mindestabsatz reicht von 0 bis 1.500 Stück pro Jahr. Kartonvarianten liegen im Testdatensatz zwischen 900 und 620.000 Stück. Selbst am Anschlag von 1.500 Stück liegt nur eine einzige Variante darunter (K09). | Der Regler ist für den Kartonfall fast wirkungslos. | Mit der Umsetzung klären: Bereich des Reglers an den Datensatz anpassen. |
| B5 | Die Sondergröße K08 für einen einzigen Großkunden (161,2 TEUR, das sind 12,5 % des Umsatzes, Marge 11 %) wird in allen vier Profilen gestrichen. Die Regeln des Prototyps kennen keine Kundenabhängigkeit; die Felder Anzahl_Kunden und Hauptkunde_Anteil_Pct gehen nur als Zusatzinformation in den Prompt. Bliebe K08 erhalten, würden Massenproduzent und Innovationsführer ihr Ziel für die Umsatzabdeckung erreichen. | Genau der Fall, den wir als Testszenario zeigen wollen: Streichen kostet einen Großkunden. | Mit dem Konzept klären: Soll das LLM diesen Fall über den Prompt erkennen, oder braucht es eine eigene Regel oder ein Pflichtfeld? |
| B6 | Der Prototyp wertet beim Status nur „Zukunft“ und „Auslauf“ aus. In seinen Demo-Daten steht auch ein Markt im Status („US-Markt“). Unsere Liste erlaubt Standard, Sonderlocke, Auslauf und Zukunft. | Demo-Daten des Prototyps wären nach unserem Schema ungültig. | Statuswerte gemeinsam festlegen; Märkte in ein eigenes Feld. |

## 7. Was nicht getestet wurde

- Die Antwort eines echten LLM. Der Prototyp erzeugt den Prompt und zeigt eine simulierte Antwort; es gibt noch keinen LLM-Aufruf.
- Die fachliche Plausibilität der Werte. Das ist Aufgabe von D2, D5 und D7.
- Die Datenblöcke der Stufe 2 (Stückliste, Arbeitsplan, Aufträge, Kosten, Kunden, Wettbewerb). Geprüft ist nur, dass ihr Schema gültig ist und die Beispielwerte dazu passen.
- Die Excel-Vorlage in Microsoft Excel. Formeln wurden mit LibreOffice berechnet (120 Formeln, 0 Fehler); Dropdowns und Eingabeprüfungen sind in der Datei vorhanden, wurden aber nicht in Excel selbst bedient.

## 8. Nächste Schritte

1. Jonas füllt die Vorlage aus (D2); Yu wandelt sie um und lädt sie am 13.11. in den Prototyp.
2. Befunde B1 bis B6 und die Feldliste am 13.11. mit Umsetzung und Konzept besprechen (D1).
3. Danach Schema v1 festlegen (D3, Ende KW47).

---

### 中文摘要

- 70 个自动测试全部通过。我们生成的 CSV 和 JSON 都能上传到实现组的原型里，四个战略画像下原型给出的建议和指标，和我们按它的规则算出来的完全一致。Excel 模板 → 转换脚本 → 原型，这条路从头到尾是通的。
- 测试数据是虚构的（SYNTHETIC），只用来验证技术流程，业务上还没有对齐。
- 六个要在 13 号会上讲的发现：
  - B1 德语版 Excel 直接另存的 CSV（分号分隔、小数逗号）会被原型读错，而且不报错。我们用转换脚本解决，不要直接从 Excel 存 CSV。
  - B2 原型不认识 WAHR/FALSCH，转换脚本统一写成 true/false。
  - B3 走 CSV 时附加字段在 Prompt 里是文本，走 JSON 才是数字，建议交付格式定为 JSON。
  - B4 最低销量滑块最多 1500 件，纸箱销量是几万到几十万，这个滑块对纸箱案例几乎不起作用。
  - B5 只卖给一个大客户的特殊尺寸 K08 在四个画像下都被删掉，原型的规则里没有客户依赖度，这正是我们想展示的测试场景，需要和概念组确定怎么处理。
  - B6 Status 的取值要统一，原型演示数据里把市场（US-Markt）也放在了 Status 里。
- 没有测的：真实 LLM 的回答、数据的业务合理性、第 2 级数据块、在真正的 Microsoft Excel 里操作模板。
