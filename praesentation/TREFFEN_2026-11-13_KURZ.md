# 周五会议速查 – 2026-11-13 09:30

数据采集子项目 · Yu Zhaoze · 详细版见 `TREFFEN_2026-11-13_VORBEREITUNG_CN.pdf`

## 目标

1. 让大家看到纸箱数据能在原型里跑。
2. 问清概念组和实现组还要哪些字段。
3. 定两件事：JSON 还是 CSV；一套数据还是四套。

## 一句话说明我们做了什么

搭好并测通了 Excel → 转换脚本 → 原型 这条数据通路。正式数据还没有，由 Jonas 负责。

| 东西 | 作用 | 位置 |
| --- | --- | --- |
| 字段定义 + JSON Schema | 约定数据有哪些字段、什么类型 | `generator/felder.py`、`schema/` |
| 字段清单 | 给人看的字段说明 | `reports/FELDLISTE_v0.1_DE.pdf` |
| Excel 模板 | Jonas 填数据的入口 | `vorlagen/` |
| 转换脚本 | 检查 Excel 并转成 CSV / JSON | `generator/excel_zu_prototyp.py` |
| 测试数据 | 14 个虚构变体，只测流程 | `data/synthetic/technischer_test_v0.1/` |
| 测试 | 70 个，全部通过 | `tests/` |

架构图：`ARCHITEKTUR_DATENERHEBUNG_CN.png`

## 流程（约 30 分钟）

**1. 演示上传（5 分钟）**
打开原型 → 上传 `varianten.json` → 调滑块。

> Ich habe eine Excel-Vorlage gemacht. Daraus erzeugt ein Skript die Datei für den Prototyp. Ich lade sie jetzt einmal hoch.

**2. 讲架构和字段（10 分钟）**
打开字段清单。7 个必填字段来自原型，12 个可选字段是我们的建议。

> An die Umsetzung: Reichen die sieben Pflichtfelder, oder braucht der Prototyp noch weitere Felder?

> An das Konzept: Welche Informationen braucht ihr noch im Prompt, zum Beispiel die Abhängigkeit von einem Kunden?

**3. 讲三个发现（5 分钟）**

- 德语 Excel 直接存的 CSV 会被原型读错，且不报错 → 一律用脚本生成。
- 最低销量滑块最多 1500 件，纸箱是几万到几十万件。
- 只卖给一个大客户的尺寸每次都被删，原型不看客户依赖度。

> Beim Testen ist mir aufgefallen: Eine CSV aus einem deutschen Excel wird falsch gelesen, ohne Fehlermeldung. Deshalb erzeugen wir die Datei immer mit dem Skript.

**4. 请大家定（5 分钟）**

> Nehmen wir JSON oder CSV als Übergabeformat? Mein Vorschlag ist JSON.

> Machen wir einen Datensatz für alle vier Strategien oder einen pro Strategie?

## 必须说清楚

测试用的 14 个变体和画像数值是占位的，不代表业务结论。正式数字由 Jonas 定并写明理由。

## 会前

- [ ] 拿到 Jonas 的 Excel 并转换；没有就用测试数据
- [ ] 笔记本上备好：原型、`varianten.json`、字段清单 PDF、测试记录 PDF
- [ ] 自己手动上传一次；确认会议室能联网

## 会后

- [ ] 记下决定：字段增减、格式、数据套数、Status 取值
- [ ] 出 Schema v1（KW47 结束前）
- [ ] 小时数报给 Mark
