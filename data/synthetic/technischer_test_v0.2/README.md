# Technischer Testdatensatz v0.2 – SYNTHETIC (Schema v0.2: ohne Must_Have und Bemerkung)

Alle Werte sind erfunden. Der Datensatz dient nur dem Test von Schema, Excel-Vorlage, Konverter und Prototyp und ist fachlich nicht abgestimmt. Der fachliche Datensatz entsteht in D2/D5.

| Datei | Inhalt |
| --- | --- |
| `technischer_testdatensatz_v0.2.xlsx` | ausgefüllte Excel-Vorlage (14 Kartonvarianten, 4 Strategieprofile) |
| `varianten.csv`, `varianten.json` | Upload-Dateien für den Prototyp, erzeugt mit `generator/excel_zu_prototyp.py` |
| `strategieprofile.json` | die vier Profile, passend zu den Reglern des Prototyps |
| `pruefbericht.txt` | Ergebnis der Prüfung beim Umwandeln |

Quelle der Werte: `generator/testdaten.py`. Nicht von Hand ändern, sondern dort anpassen und neu erzeugen:

```
python generator/vorlage_erzeugen.py
python generator/excel_zu_prototyp.py data/synthetic/technischer_test_v0.2/technischer_testdatensatz_v0.2.xlsx --out data/synthetic/technischer_test_v0.2
```

Eingebaute Testszenarien: T1 Sondergröße für einen einzigen Großkunden (K08) · T2 fast identische Größe neben einem Bestseller (K03) · T3 Auslauf mit schwacher und guter Marge (K10, K11) · T4 Zukunft mit schwacher und guter Marge (K12, K13) · T5 Kleinserie mit hohem Rüstaufwand (K09) · T6 stärkere Welle als nötig (K14).
