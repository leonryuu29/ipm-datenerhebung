# 接下来要做的事（2026-11-14 整理）

## 1. 推送到 GitHub（现在）

在仓库目录里运行：

```
git push
```

## 2. 上传到 Drive 共享文件夹（周日或周一，你自己传）

传到共享文件夹“IPM Gruppe 6”的根目录（现在没有子文件夹）：

| 文件 | 为什么传 |
| --- | --- |
| `reports\FELDLISTE_v0.2_DE.pdf` | 字段清单。第 1 级是变体表和战略画像，第 2 级是 8 个 ERP 数据块。概念组拿它作参考整理字段 |
| `praesentation\ARCHITEKTUR_DATENERHEBUNG_DE.png` | 数据流程图，一眼看出数据从哪来、到哪去 |

不用传：Schema（给程序读的）、Excel 模板（字段还会变）、测试文件。

## 3. 群里发消息（和上传同一天）

> Hi zusammen, ich habe zwei Dateien in den Drive-Ordner gelegt:
> – FELDLISTE_v0.2_DE.pdf: alle Felder, die wir bisher vorschlagen. Teil 2 sind die ERP-Datenblöcke (Stückliste, Arbeitsplan, Aufträge, Kosten, Kunden, Wettbewerb).
> – ARCHITEKTUR_DATENERHEBUNG_DE.png: der Ablauf von den Daten bis zur JSON-Datei.
> Must_Have und Bemerkung sind schon raus, wie am Freitag besprochen.
> @Lukas @David: Nehmt die Feldliste und die ERP-Datenblöcke gern als Grundlage für eure Felder. Auf der letzten Seite stehen ein paar offene Fragen. Sagt Bescheid, wenn eure Fassung fertig ist, dann gleichen wir ab.

中文意思：我在 Drive 放了两个文件：字段清单 v0.2（第 2 部分是 ERP 数据块：物料清单、工艺路线、订单、成本、客户、竞品），以及从数据到 JSON 的流程图。Must_Have 和 Bemerkung 已按周五说的去掉。Lukas、David，可以拿字段清单和 ERP 数据块作为你们整理字段的基础，最后一页有几个待定问题。你们的版本出来后告诉我，我们再核对。

## 4. 给 Jonas 发消息（尽快，他没来开会）

> Hi Jonas, kurzes Update vom Treffen am Freitag:
>
> 1. Ich habe die Feldliste und die Testdaten vorgestellt. Das Feedback war gut, auch zu den ERP-Datenblöcken. Deine Idee mit dem RAJA-Katalog passt gut dazu.
> 2. Wir liefern JSON. Must_Have und Bemerkung sind raus, weil in die Daten nur sachliche Produktinfos sollen. Must_Have wählt später der Nutzer in der Oberfläche. Ich habe die Feldliste schon angepasst (v0.2).
> 3. Lukas und David legen jetzt die Felder fest. Bitte bis dahin nicht weiter an der Excel-Tabelle arbeiten, sonst müssen wir alles noch mal umbauen. Was du schon eingetragen hast, bleibt.
> 4. Der Prototyp war nur eine Demo, daran orientieren wir uns nicht mehr.
>
> Am 20.11. mittags kommen Michal und Steffen Feld zu uns, eher als Gespräch mit Fragen. Ich erkläre Folie 10 (Daten, Ablauf, Ergebnisse) und sage kurz, wer was macht. Magst du Folie 11 mit dem Karton-Beispiel übernehmen? Da passt dein Teil gut rein: der RAJA-Katalog als Quelle für die Maße, die Sonderfälle (z. B. eine Sondergröße nur für einen Großkunden) und wie die Empfehlung je nach Strategie anders ausfällt. Eine Minute reicht.

中文意思：会上反馈不错；交付 JSON，Must_Have 和 Bemerkung 去掉，字段清单已改成 v0.2；概念组在定字段，先别继续填 Excel，已填的保留；原型只是演示；20 号中午教授和 Steffen 来，以提问为主，你讲第 10 页和分工，问他愿不愿意讲第 11 页（纸箱例子、Rajapack 目录、特殊情况、建议随战略变化），一分钟就够。

## 5. 小时数报给 Mark

把这两周花在数据采集上的时间估一下发给他。

## 6. 20 号（周五）中午之前

- [ ] 读 `praesentation\SPRECHTEXT_2026-11-20_DE.pdf`，至少把黄色的句子练熟
- [ ] 看一遍后面的问答
- [ ] 确认 Jonas 讲不讲第 11 页
- [ ] 当天带上笔记本，能打开 Pitch v3 和字段清单

## 7. 之后

等概念组的字段版本 → 对照 → 定 Schema v1 → 生成 ERP 数据块的模拟数据（参考公开数据）→ 交给实现组。
在概念组给出字段之前，数据这边不用做别的。
