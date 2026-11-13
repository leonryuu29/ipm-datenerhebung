# 运行说明（Windows / PowerShell）

## 各个文件的关系

```
felder.py（字段定义，手写）
   ├─→ schema_erzeugen.py  →  schema/ 里的 4 个文件（规则）
   └─→ vorlage_erzeugen.py →  两个 Excel：
                                ① 空模板（给 Jonas）
        testdaten.py ─────────→ ② 填好 14 个变体的测试 Excel
        （14 个变体 + 4 个画像，手写）
                                      │
                          excel_zu_prototyp.py（用 pruefen.py 检查）
                                      ↓
                 varianten.csv / varianten.json / strategieprofile.json
                                      ↓
                              上传到原型网页
```

所有命令都在仓库目录里运行。每次打开新的 PowerShell 先进入目录：

```
cd "T:\新学期\IPM\项目文件\Datenerhebung\ipm-datenerhebung"
```

> 运行前先把 Excel 里打开的模板和测试表关掉，否则程序写不进去（报错 `PermissionError`）。

## 1. 第一次使用：安装环境（只做一次，已经做过）

```
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m playwright install chromium
```

## 2. 跑生成器

按顺序运行三条：

```
.venv\Scripts\python generator\schema_erzeugen.py
.venv\Scripts\python generator\vorlage_erzeugen.py
.venv\Scripts\python generator\excel_zu_prototyp.py data\synthetic\technischer_test_v0.2\technischer_testdatensatz_v0.2.xlsx --out data\synthetic\technischer_test_v0.2
```

| 命令 | 生成什么 | 正常时显示 |
| --- | --- | --- |
| `schema_erzeugen.py` | `schema\` 里的 4 个 JSON | 4 行 `geschrieben: ...` |
| `vorlage_erzeugen.py` | 空模板 `vorlagen\VARIANTEN_VORLAGE_v0.2.xlsx` 和测试 Excel | 2 行 `geschrieben: ...` |
| `excel_zu_prototyp.py` | `varianten.csv`、`varianten.json`、`strategieprofile.json`、`pruefbericht.txt` | 检查报告，最后一行 `ERGEBNIS: Dateien geschrieben.` |

什么时候需要跑：改了 `generator\felder.py`（字段）或 `generator\testdaten.py`（测试数据）之后。平时不用跑。

## 3. 跑测试

全部测试（浏览器测试需要联网，约 10 秒）：

```
.venv\Scripts\python -m pytest tests -v
```

正常时最后一行是 `71 passed`。中间的 `UserWarning: Data Validation extension ...` 是 openpyxl 的提示，可以忽略。

只跑某一层：

```
.venv\Scripts\python -m pytest tests\test_schema.py -v
.venv\Scripts\python -m pytest tests\test_konverter.py -v
.venv\Scripts\python -m pytest tests\test_prototyp_browser.py -v
```

| 文件 | 测什么 |
| --- | --- |
| `test_schema.py` | 检查规则能不能拦住错误数据 |
| `test_konverter.py` | Excel 转出来的数据对不对 |
| `test_prototyp_browser.py` | 在浏览器里打开原型，上传数据，按四个战略核对结果 |

测试结果和截图会更新到 `tests\ergebnisse\`。

## 4. 转换 Jonas 的表

```
.venv\Scripts\python generator\excel_zu_prototyp.py "T:\新学期\IPM\项目文件\one-drive(共享接口）\VARIANTEN_VORLAGE_v0.2.xlsx" --out data\synthetic\jonas_v1
```

有错误时只写检查报告 `pruefbericht.txt`，不生成 CSV 和 JSON。没错误时生成的 `varianten.json` 就是要上传到原型的文件。

## 5. 跑完以后 git 显示很多改动

正常。生成器和测试会重新写文件，Windows 下换行符和截图会变，内容一般没变。不想保留就还原：

```
git checkout -- data schema tests reports vorlagen
```

## 常见报错

| 报错 | 原因 | 怎么办 |
| --- | --- | --- |
| `PermissionError` / 文件可能正在 Excel 里打开 | 要写的 Excel 正开着 | 关掉 Excel 再跑 |
| `the following arguments are required: excel, --out` | `excel_zu_prototyp.py` 后面没写文件 | 照第 2 或第 4 节写完整 |
| `No module named ...` | 没用 `.venv` 里的 Python | 命令前面要写 `.venv\Scripts\python` |
| 浏览器测试被跳过（`skipped`） | 没联网，原型加载不出来 | 联网后再跑 |
