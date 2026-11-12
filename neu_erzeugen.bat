@echo off
setlocal
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Bitte zuerst einrichten.bat ausfuehren.
  exit /b 1
)
".venv\Scripts\python.exe" generator\schema_erzeugen.py
".venv\Scripts\python.exe" generator\vorlage_erzeugen.py
".venv\Scripts\python.exe" generator\excel_zu_prototyp.py data\synthetic\technischer_test_v0.1\technischer_testdatensatz_v0.1.xlsx --out data\synthetic\technischer_test_v0.1
