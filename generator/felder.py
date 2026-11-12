"""Felddefinitionen des Teilprojekts Datenerhebung (einzige Quelle der Wahrheit).

Aus diesen Definitionen werden erzeugt:
  - schema/*.schema.json          (JSON-Schema, Datenvertrag)
  - schema/felder_v<VERSION>.json (maschinenlesbare Feldliste)
  - vorlagen/*.xlsx               (Excel-Vorlage, Blatt "Felder" und Dropdowns)
  - reports/FELDLISTE_*.docx      (Feldliste für das Team)

Stufe 1 = sofort nutzbar, kompatibel mit dem Prototyp der Umsetzung
          (ki_wrapper_variantenmanagement.html, Stand 10.11.2026).
Stufe 2 = Entwurf für das vollständige Datenpaket (KW47-48), noch abzustimmen.
"""
from __future__ import annotations

VERSION = "0.1"
STAND = "2026-11-11"
KENNZEICHNUNG = "SYNTHETIC"

STRATEGIEN = ["Massenproduzent", "Kostenführer", "Innovationsführer", "Nischenanbieter"]
STATUS = ["Standard", "Sonderlocke", "Auslauf", "Zukunft"]
WELLENARTEN = ["E", "B", "C", "EB", "BC"]
DRUCK = ["ohne", "1-farbig", "2-farbig", "4-farbig"]
PROZESSSCHRITTE = ["Wellpappe", "Zuschnitt", "Druck", "Stanzen", "Kleben", "Konfektionierung"]
ENTKOPPLUNG = ["ATO", "MTS", "ETO"]
SOURCING = ["Single", "Dual"]
PRIORITAET = ["Muss", "Soll", "Kann"]

# Exakte Optionswerte im Prototyp (select-Elemente)
PROTOTYP_ENTKOPPLUNG = {
    "ATO": "Assemble-to-Order (Späte Varianz)",
    "MTS": "Make-to-Stock (Standard)",
    "ETO": "Engineer-to-Order (Losgröße 1)",
}
PROTOTYP_SOURCING = {
    "Single": "Single-Sourcing (Max. Mengenrabatt)",
    "Dual": "Dual-Sourcing (Risikominimierung)",
}


# Regler des Prototyps: id -> (min, max, Schrittweite). Stand 10.11.2026.
PROTOTYP_REGLER = {
    "min_market_cov": (50, 100, 1),
    "max_setup_index": (1, 10, 1),
    "min_margin": (0, 40, 1),
    "min_moq": (0, 1500, 50),
    "min_cop_rate": (10, 90, 1),
}


def F(name, typ, de, cn, *, pflicht=False, einheit="", beispiel=None, enum=None,
      min=None, max=None, pattern=None, herkunft="Erweiterung", prototyp_id=None):
    return dict(name=name, typ=typ, de=de, cn=cn, pflicht=pflicht, einheit=einheit,
                beispiel=beispiel, enum=enum, min=min, max=max, pattern=pattern,
                herkunft=herkunft, prototyp_id=prototyp_id)


ID_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9_.\-]*$"

VARIANTEN = dict(
    id="varianten", stufe=1,
    titel="Varianten (Portfolio-Tabelle)", titel_cn="变体（产品组合表）",
    de="Eine Zeile je Produktvariante. Die ersten sieben Felder liest der Prototyp direkt; "
       "die Erweiterungsfelder werden als Zusatzinformation in den Prompt übernommen.",
    cn="每个产品变体一行。前七个字段原型可以直接读取；扩展字段会作为附加信息写进 Prompt。",
    felder=[
        F("Variante", "string", "Eindeutige Kennung der Variante. Nur Buchstaben, Ziffern, _ . - (kein Komma, kein Semikolon, kein Leerzeichen).",
          "变体的唯一编号。只能用字母、数字、_ . -（不能有逗号、分号、空格）。",
          pflicht=True, beispiel="K02_0201_300x200x150_B", pattern=ID_PATTERN, herkunft="Prototyp"),
        F("Umsatz_TEUR", "number", "Jahresumsatz der Variante.", "该变体的年营收。",
          pflicht=True, einheit="Tsd. EUR / Jahr", beispiel=229.5, min=0, herkunft="Prototyp"),
        F("Marge_Pct", "number", "Deckungsbeitrag in Prozent vom Umsatz.", "边际贡献占营收的百分比。",
          pflicht=True, einheit="%", beispiel=26, min=-100, max=100, herkunft="Prototyp"),
        F("Absatz_Stk", "integer", "Verkaufte Menge pro Jahr.", "年销量。",
          pflicht=True, einheit="Stück / Jahr", beispiel=510000, min=0, herkunft="Prototyp"),
        F("Ruestkosten_Index", "integer", "Rüstaufwand der Variante relativ zum Standard: 1 = sehr gering, 10 = sehr hoch.",
          "该变体的换型成本指数：1 = 很低，10 = 很高。",
          pflicht=True, einheit="1-10", beispiel=2, min=1, max=10, herkunft="Prototyp"),
        F("Status", "string", "Lebenszyklus-Status. Der Prototyp wertet 'Auslauf' und 'Zukunft' gesondert aus.",
          "生命周期状态。原型会单独处理 'Auslauf'（退市）和 'Zukunft'（未来产品）。",
          pflicht=True, beispiel="Standard", enum=STATUS, herkunft="Prototyp"),
        F("Must_Have", "boolean", "Variante ist für einen Kernmarkt oder ein K.O.-Kriterium unverzichtbar und wird vom Prototyp geschützt.",
          "该变体对核心市场或硬性要求不可缺少，原型会保护它不被删除。",
          pflicht=True, beispiel=True, herkunft="Prototyp"),
        F("Bezeichnung", "string", "Lesbarer Name der Variante.", "变体的可读名称。",
          beispiel="Faltkarton 300x200x150 B-Welle"),
        F("FEFCO_Typ", "string", "Konstruktionstyp nach FEFCO-Code (vier Ziffern).", "FEFCO 箱型代码（四位数字）。",
          beispiel="0201", pattern=r"^\d{4}$"),
        F("Laenge_mm", "integer", "Innenmaß Länge.", "内尺寸：长。", einheit="mm", beispiel=300, min=1),
        F("Breite_mm", "integer", "Innenmaß Breite.", "内尺寸：宽。", einheit="mm", beispiel=200, min=1),
        F("Hoehe_mm", "integer", "Innenmaß Höhe.", "内尺寸：高。", einheit="mm", beispiel=150, min=1),
        F("Wellenart", "string", "Wellpappenqualität.", "瓦楞类型。", beispiel="B", enum=WELLENARTEN),
        F("Druck", "string", "Bedruckung.", "印刷方式。", beispiel="ohne", enum=DRUCK),
        F("Preis_EUR", "number", "Durchschnittlicher Verkaufspreis je Stück. Dient der Plausibilitätsprüfung: Umsatz_TEUR ≈ Absatz_Stk × Preis_EUR / 1000.",
          "平均单价。用于合理性检查：Umsatz_TEUR ≈ Absatz_Stk × Preis_EUR / 1000。",
          einheit="EUR / Stück", beispiel=0.45, min=0),
        F("Anzahl_Kunden", "integer", "Anzahl der Kunden, die die Variante im Jahr gekauft haben.", "当年购买该变体的客户数。",
          beispiel=45, min=0),
        F("Hauptkunde_Anteil_Pct", "number", "Anteil des größten Kunden am Umsatz der Variante. Hoher Wert = Abhängigkeit von einem Kunden.",
          "最大客户占该变体营收的比例。数值高 = 依赖单一客户。",
          einheit="%", beispiel=9, min=0, max=100),
        F("Variantenbildung_Schritt", "string", "Prozessschritt, in dem die Variante entsteht (Variantenbildungspunkt). Später = besser.",
          "变体在哪道工序形成（变体形成点）。越靠后越好。",
          beispiel="Zuschnitt", enum=PROZESSSCHRITTE),
        F("Referenz_Artikelnr", "string", "Artikelnummer des öffentlichen Katalogprodukts, an dem sich Maße und Ausführung orientieren. Quelle und Abrufdatum stehen in data/reference.",
          "变体所参考的公开目录产品的货号（尺寸和规格以它为依据）。来源和获取日期记在 data/reference 里。",
          beispiel="CAS16", pattern=ID_PATTERN),
        F("Bemerkung", "string", "Freitext, z. B. Sonderfall oder Annahme. Kein Komma, kein Semikolon.",
          "备注，比如特殊情况或假设。不能有逗号和分号。", beispiel="nahezu identisch mit K02"),
    ],
)

STRATEGIEPROFILE = dict(
    id="strategieprofile", stufe=1,
    titel="Strategieprofile (Leitplanken)", titel_cn="战略画像（约束条件）",
    de="Ein Profil je Unternehmensstrategie. Die Felder entsprechen den Reglern des Prototyps, "
       "sodass jedes Profil dort direkt eingestellt werden kann.",
    cn="每种企业战略一个画像。字段和原型里的滑块一一对应，每个画像都可以直接在原型里设置。",
    felder=[
        F("Strategie", "string", "Strategische Ausrichtung des Unternehmens.", "企业的战略方向。",
          pflicht=True, beispiel="Massenproduzent", enum=STRATEGIEN),
        F("Beschreibung", "string", "Kurzbeschreibung des Profils in einem Satz.", "一句话描述该画像。",
          beispiel="Wenige Standardgrößen in hoher Stückzahl"),
        F("Min_Umsatzabdeckung_Pct", "integer", "Anteil des bisherigen Umsatzes, der mindestens erhalten bleiben muss.",
          "至少要保住的现有营收比例。", pflicht=True, einheit="%", beispiel=85, min=50, max=100,
          herkunft="Prototyp", prototyp_id="min_market_cov"),
        F("Kernmaerkte_schuetzen", "boolean", "Must-Have-Varianten bleiben unabhängig von den Kennzahlen erhalten.",
          "Must-Have 变体不论指标如何都保留。", pflicht=True, beispiel=True,
          herkunft="Prototyp", prototyp_id="protect_must_haves"),
        F("Entkopplungspunkt", "string", "Kundenentkopplungspunkt: ATO = Assemble-to-Order, MTS = Make-to-Stock, ETO = Engineer-to-Order.",
          "客户订单分离点：ATO 按订单装配，MTS 按库存生产，ETO 按订单设计。",
          pflicht=True, beispiel="MTS", enum=ENTKOPPLUNG, herkunft="Prototyp", prototyp_id="decoupling_point"),
        F("Max_Ruestkosten_Index", "integer", "Varianten über diesem Rüstkosten-Index sollen modularisiert werden.",
          "换型成本指数超过该值的变体应做模块化。", pflicht=True, einheit="1-10", beispiel=4, min=1, max=10,
          herkunft="Prototyp", prototyp_id="max_setup_index"),
        F("Ueberspezifikation_erlaubt", "boolean", "Einheitsmodule dürfen verwendet werden, auch wenn sie für einzelne Varianten überdimensioniert sind.",
          "允许使用统一模块，即使对个别变体来说规格偏高。", pflicht=True, beispiel=True,
          herkunft="Prototyp", prototyp_id="over_spec_allowed"),
        F("Min_Marge_Pct", "integer", "Mindestmarge; Varianten darunter verfehlen das Finanzziel.",
          "最低边际贡献率；低于该值的变体不达财务目标。", pflicht=True, einheit="%", beispiel=15, min=0, max=40,
          herkunft="Prototyp", prototyp_id="min_margin"),
        F("Min_Absatz_Stk", "integer", "Mindestabsatz pro Jahr. Hinweis: Der Regler im Prototyp reicht derzeit nur von 0 bis 1500 in 50er-Schritten.",
          "年最低销量。注意：原型的滑块目前只支持 0 到 1500，步长 50。",
          pflicht=True, einheit="Stück / Jahr", beispiel=1500, min=0,
          herkunft="Prototyp", prototyp_id="min_moq"),
        F("Ziel_Gleichteilequote_Pct", "integer", "Angestrebter Anteil gleicher Teile über das Portfolio.",
          "整个产品组合的通用件目标比例。", pflicht=True, einheit="%", beispiel=80, min=10, max=90,
          herkunft="Prototyp", prototyp_id="min_cop_rate"),
        F("Sourcing", "string", "Beschaffungsstrategie.", "采购策略。", pflicht=True, beispiel="Single",
          enum=SOURCING, herkunft="Prototyp", prototyp_id="sourcing_strat"),
        F("Zukunft_schuetzen", "boolean", "Varianten mit Status 'Zukunft' bleiben erhalten.",
          "状态为 'Zukunft' 的变体保留。", pflicht=True, beispiel=False,
          herkunft="Prototyp", prototyp_id="protect_future"),
        F("Auslauf_streichen", "boolean", "Varianten mit Status 'Auslauf' werden gestrichen.",
          "状态为 'Auslauf' 的变体删除。", pflicht=True, beispiel=True,
          herkunft="Prototyp", prototyp_id="kill_phased_out"),
    ],
)

UNTERNEHMEN = dict(
    id="unternehmen", stufe=2,
    titel="Unternehmensprofil", titel_cn="公司画像",
    de="Stammdaten des fiktiven Unternehmens.", cn="虚构公司的基本数据。",
    felder=[
        F("Unternehmen_ID", "string", "Kennung des Unternehmens.", "公司编号。", pflicht=True, beispiel="U01", pattern=ID_PATTERN),
        F("Name", "string", "Name des fiktiven Unternehmens.", "虚构公司的名称。", pflicht=True, beispiel="Musterkarton GmbH"),
        F("Branche", "string", "Branche.", "行业。", pflicht=True, beispiel="Wellpappe-Verpackungen"),
        F("Umsatz_Mio_EUR", "number", "Jahresumsatz.", "年营收。", pflicht=True, einheit="Mio. EUR", beispiel=18.5, min=0),
        F("Mitarbeitende", "integer", "Anzahl Mitarbeitende.", "员工数。", pflicht=True, beispiel=120, min=1),
        F("Standorte", "integer", "Anzahl Produktionsstandorte.", "生产基地数量。", beispiel=1, min=1),
        F("Strategie", "string", "Strategische Ausrichtung.", "战略方向。", pflicht=True, beispiel="Massenproduzent", enum=STRATEGIEN),
        F("Fertigungsart", "string", "Vorherrschende Fertigungsart.", "主要生产方式。", pflicht=True, beispiel="MTS", enum=ENTKOPPLUNG),
        F("Kernmaerkte", "string", "Wichtigste Märkte oder Kundensegmente, durch | getrennt.", "最重要的市场或客户群，用 | 分隔。",
          beispiel="E-Commerce|Lebensmittel"),
    ],
)

STUECKLISTE = dict(
    id="stueckliste", stufe=2,
    titel="Stückliste", titel_cn="物料清单（BOM）",
    de="Eine Zeile je Komponente einer Variante.", cn="变体的每个组件一行。",
    felder=[
        F("Variante", "string", "Verweis auf die Variante.", "对应的变体编号。", pflicht=True, beispiel="K02_0201_300x200x150_B", pattern=ID_PATTERN),
        F("Position", "integer", "Positionsnummer.", "行号。", pflicht=True, beispiel=10, min=1),
        F("Komponente_ID", "string", "Kennung der Komponente.", "组件编号。", pflicht=True, beispiel="WP-B-125", pattern=ID_PATTERN),
        F("Komponente", "string", "Bezeichnung der Komponente.", "组件名称。", pflicht=True, beispiel="Wellpappe B-Welle 125 g"),
        F("Menge", "number", "Einsatzmenge je Stück.", "每件用量。", pflicht=True, beispiel=0.42, min=0),
        F("Einheit", "string", "Mengeneinheit.", "计量单位。", pflicht=True, beispiel="m2"),
        F("Gleichteil", "boolean", "Komponente wird in mehreren Varianten verwendet.", "该组件在多个变体中通用。", pflicht=True, beispiel=True),
        F("Kosten_EUR_je_Einheit", "number", "Einstandspreis je Einheit.", "每单位采购成本。", einheit="EUR", beispiel=0.48, min=0),
    ],
)

ARBEITSPLAN = dict(
    id="arbeitsplan", stufe=2,
    titel="Arbeitsplan", titel_cn="工艺路线",
    de="Eine Zeile je Prozessschritt einer Variante. Zeigt, wo die Variante entsteht.",
    cn="变体的每道工序一行，可以看出变体在哪里形成。",
    felder=[
        F("Variante", "string", "Verweis auf die Variante.", "对应的变体编号。", pflicht=True, beispiel="K02_0201_300x200x150_B", pattern=ID_PATTERN),
        F("Schritt_Nr", "integer", "Reihenfolge des Schritts.", "工序顺序号。", pflicht=True, beispiel=20, min=1),
        F("Prozessschritt", "string", "Art des Prozessschritts.", "工序类型。", pflicht=True, beispiel="Zuschnitt", enum=PROZESSSCHRITTE),
        F("Arbeitsplatz", "string", "Maschine oder Arbeitsplatz.", "机器或工位。", beispiel="Inliner 2"),
        F("Ruestzeit_min", "number", "Rüstzeit je Auftrag.", "每单换型时间。", pflicht=True, einheit="min", beispiel=25, min=0),
        F("Stueckzeit_s", "number", "Bearbeitungszeit je Stück.", "单件加工时间。", pflicht=True, einheit="s", beispiel=0.6, min=0),
        F("Variantenbildend", "boolean", "In diesem Schritt entsteht die Variante (Variantenbildungspunkt).", "变体在这道工序形成（变体形成点）。", pflicht=True, beispiel=True),
    ],
)

AUFTRAEGE = dict(
    id="auftraege", stufe=2,
    titel="Aufträge", titel_cn="订单",
    de="Eine Zeile je Auftragsposition. Grundlage für Absatz, Umsatz und Kundenstruktur.",
    cn="每个订单行一行，是销量、营收和客户结构的基础。",
    felder=[
        F("Auftrag_ID", "string", "Kennung des Auftrags.", "订单编号。", pflicht=True, beispiel="A-2026-00417", pattern=ID_PATTERN),
        F("Datum", "date", "Auftragsdatum.", "订单日期。", pflicht=True, beispiel="2026-03-14"),
        F("Kunde_ID", "string", "Verweis auf den Kunden.", "对应的客户编号。", pflicht=True, beispiel="KD-017", pattern=ID_PATTERN),
        F("Variante", "string", "Verweis auf die Variante.", "对应的变体编号。", pflicht=True, beispiel="K02_0201_300x200x150_B", pattern=ID_PATTERN),
        F("Menge_Stk", "integer", "Bestellte Menge.", "订购数量。", pflicht=True, einheit="Stück", beispiel=12000, min=1),
        F("Preis_EUR_je_Stk", "number", "Verkaufspreis je Stück.", "单价。", pflicht=True, einheit="EUR", beispiel=0.45, min=0),
    ],
)

KOSTEN = dict(
    id="kosten", stufe=2,
    titel="Kosten je Variante", titel_cn="各变体成本",
    de="Kostenbestandteile je Variante; daraus ergeben sich Marge und Rüstkosten-Index.",
    cn="每个变体的成本构成；边际贡献率和换型成本指数由此算出。",
    felder=[
        F("Variante", "string", "Verweis auf die Variante.", "对应的变体编号。", pflicht=True, beispiel="K02_0201_300x200x150_B", pattern=ID_PATTERN),
        F("Materialkosten_EUR_je_Stk", "number", "Materialkosten je Stück.", "单件材料成本。", pflicht=True, einheit="EUR", beispiel=0.21, min=0),
        F("Fertigungskosten_EUR_je_Stk", "number", "Variable Fertigungskosten je Stück.", "单件可变制造成本。", pflicht=True, einheit="EUR", beispiel=0.09, min=0),
        F("Ruestkosten_EUR_je_Auftrag", "number", "Rüstkosten je Fertigungsauftrag.", "每个生产订单的换型成本。", pflicht=True, einheit="EUR", beispiel=85, min=0),
        F("Lagerkosten_EUR_je_Jahr", "number", "Lagerhaltungskosten pro Jahr.", "年库存成本。", einheit="EUR", beispiel=1800, min=0),
        F("Komplexitaetskosten_EUR_je_Jahr", "number", "Variantenabhängige Gemeinkosten (Stammdaten, Planung, Werkzeuge).", "随变体产生的间接成本（主数据、计划、模具）。", einheit="EUR", beispiel=2500, min=0),
    ],
)

KUNDEN = dict(
    id="kunden", stufe=2,
    titel="Kunden", titel_cn="客户",
    de="Eine Zeile je Kunde.", cn="每个客户一行。",
    felder=[
        F("Kunde_ID", "string", "Kennung des Kunden.", "客户编号。", pflicht=True, beispiel="KD-017", pattern=ID_PATTERN),
        F("Segment", "string", "Kundensegment.", "客户类别。", pflicht=True, beispiel="E-Commerce"),
        F("Schluesselkunde", "boolean", "Strategisch wichtiger Kunde.", "战略重要客户。", pflicht=True, beispiel=False),
        F("Kernmarkt", "boolean", "Kunde gehört zu einem Kernmarkt.", "客户属于核心市场。", pflicht=True, beispiel=True),
    ],
)

KUNDENANFORDERUNGEN = dict(
    id="kundenanforderungen", stufe=2,
    titel="Kundenanforderungen", titel_cn="客户需求",
    de="Gewünschte Merkmalsausprägungen der Kunden.", cn="客户想要的特征取值。",
    felder=[
        F("Kunde_ID", "string", "Verweis auf den Kunden.", "对应的客户编号。", pflicht=True, beispiel="KD-017", pattern=ID_PATTERN),
        F("Merkmal", "string", "Produktmerkmal.", "产品特征。", pflicht=True, beispiel="Wellenart"),
        F("Auspraegung", "string", "Gewünschte Ausprägung.", "想要的取值。", pflicht=True, beispiel="B"),
        F("Prioritaet", "string", "Verbindlichkeit der Anforderung.", "需求的强制程度。", pflicht=True, beispiel="Muss", enum=PRIORITAET),
        F("Haeufigkeit_pro_Jahr", "integer", "Wie oft die Anforderung im Jahr auftritt.", "该需求一年出现的次数。", beispiel=14, min=0),
    ],
)

WETTBEWERB = dict(
    id="wettbewerb", stufe=2,
    titel="Wettbewerbsportfolio", titel_cn="竞品组合",
    de="Öffentlich recherchierte Katalogdaten. Jede Zeile braucht Quelle und Abrufdatum.",
    cn="公开查到的目录数据。每一行都要有来源和获取日期。",
    felder=[
        F("Wettbewerber", "string", "Name des Anbieters.", "供应商名称。", pflicht=True, beispiel="Anbieter A"),
        F("Produkt", "string", "Produktbezeichnung laut Katalog.", "目录里的产品名称。", pflicht=True, beispiel="Faltkarton 300x200x150"),
        F("FEFCO_Typ", "string", "Konstruktionstyp, falls angegeben.", "箱型代码（如有）。", beispiel="0201", pattern=r"^\d{4}$"),
        F("Laenge_mm", "integer", "Innenmaß Länge.", "内尺寸：长。", einheit="mm", beispiel=300, min=1),
        F("Breite_mm", "integer", "Innenmaß Breite.", "内尺寸：宽。", einheit="mm", beispiel=200, min=1),
        F("Hoehe_mm", "integer", "Innenmaß Höhe.", "内尺寸：高。", einheit="mm", beispiel=150, min=1),
        F("Wellenart", "string", "Wellpappenqualität, falls angegeben.", "瓦楞类型（如有）。", beispiel="B", enum=WELLENARTEN),
        F("Quelle_URL", "string", "Adresse der Fundstelle.", "来源网址。", pflicht=True, beispiel="https://example.org/katalog"),
        F("Abrufdatum", "date", "Datum des Abrufs.", "获取日期。", pflicht=True, beispiel="2026-11-18"),
    ],
)

BLOECKE = [VARIANTEN, STRATEGIEPROFILE, UNTERNEHMEN, STUECKLISTE, ARBEITSPLAN,
           AUFTRAEGE, KOSTEN, KUNDEN, KUNDENANFORDERUNGEN, WETTBEWERB]
BLOCK = {b["id"]: b for b in BLOECKE}
PROTOTYP_SPALTEN = [f["name"] for f in VARIANTEN["felder"] if f["herkunft"] == "Prototyp"]


def feld_schema(f: dict) -> dict:
    """JSON-Schema-Fragment für ein Feld."""
    if f["typ"] == "date":
        s = {"type": "string", "format": "date"}
    else:
        s = {"type": f["typ"]}
    if f["enum"]:
        s["enum"] = list(f["enum"])
    if f["min"] is not None:
        s["minimum"] = f["min"]
    if f["max"] is not None:
        s["maximum"] = f["max"]
    if f["pattern"]:
        s["pattern"] = f["pattern"]
    if f["typ"] == "string" and not f["enum"] and f["pflicht"]:
        s["minLength"] = 1
    text = f["de"] + (f" Einheit: {f['einheit']}." if f["einheit"] else "")
    s["description"] = text
    return s


def zeilen_schema(block: dict) -> dict:
    """Schema für eine Zeile (ein Objekt) eines Blocks."""
    return {
        "type": "object",
        "properties": {f["name"]: feld_schema(f) for f in block["felder"]},
        "required": [f["name"] for f in block["felder"] if f["pflicht"]],
        "additionalProperties": False,
    }


BASIS_URL = "https://github.com/leonryuu29/ipm-datenerhebung/schema/"


def schema_varianten() -> dict:
    """Flache Variantentabelle: genau das, was der Prototyp als JSON lädt."""
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": BASIS_URL + f"varianten_v{VERSION}.schema.json",
        "title": f"Varianten (Portfolio-Tabelle) v{VERSION}",
        "description": VARIANTEN["de"],
        "type": "array",
        "minItems": 1,
        "items": zeilen_schema(VARIANTEN),
    }


def schema_strategieprofile() -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": BASIS_URL + f"strategieprofile_v{VERSION}.schema.json",
        "title": f"Strategieprofile v{VERSION}",
        "description": STRATEGIEPROFILE["de"],
        "type": "array",
        "minItems": 1,
        "maxItems": len(STRATEGIEN),
        "items": zeilen_schema(STRATEGIEPROFILE),
    }


def schema_datenpaket() -> dict:
    """Entwurf des vollständigen Datenpakets (Stufe 2)."""
    props = {
        "meta": {
            "type": "object",
            "properties": {
                "schema_version": {"const": VERSION},
                "kennzeichnung": {"const": KENNZEICHNUNG, "description": "Alle erfundenen Daten sind als SYNTHETIC gekennzeichnet."},
                "erzeugt_am": {"type": "string", "format": "date"},
                "seed": {"type": "integer", "description": "Startwert des Generators für die Reproduzierbarkeit."},
                "beschreibung": {"type": "string"},
            },
            "required": ["schema_version", "kennzeichnung", "erzeugt_am"],
            "additionalProperties": False,
        },
        "unternehmen": zeilen_schema(UNTERNEHMEN),
        "strategieprofil": zeilen_schema(STRATEGIEPROFILE),
        "varianten": {"type": "array", "minItems": 1, "items": zeilen_schema(VARIANTEN)},
    }
    for b in (STUECKLISTE, ARBEITSPLAN, AUFTRAEGE, KOSTEN, KUNDEN, KUNDENANFORDERUNGEN, WETTBEWERB):
        props[b["id"]] = {"type": "array", "items": zeilen_schema(b)}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": BASIS_URL + f"datenpaket_v{VERSION}.schema.json",
        "title": f"Datenpaket Variantenmanagement v{VERSION} (Entwurf)",
        "description": "Ein Datenpaket je Unternehmen und Strategieprofil. Stufe 1: meta, strategieprofil, varianten. "
                       "Stufe 2 (Entwurf, noch abzustimmen): übrige Blöcke.",
        "type": "object",
        "properties": props,
        "required": ["meta", "strategieprofil", "varianten"],
        "additionalProperties": False,
    }
