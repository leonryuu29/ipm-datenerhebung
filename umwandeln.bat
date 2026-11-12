@echo off
setlocal
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Bitte zuerst einrichten.bat ausfuehren.
  exit /b 1
)
if "%~1"=="" (
  echo Aufruf:    umwandeln.bat ^<ausgefuellte_vorlage.xlsx^> ^<zielordner^>
  echo Beispiel:  umwandeln.bat jonas.xlsx data\synthetic\jonas_v1
  exit /b 1
)
if "%~2"=="" (
  echo Bitte auch einen Zielordner angeben, z. B. data\synthetic\jonas_v1
  exit /b 1
)
".venv\Scripts\python.exe" generator\excel_zu_prototyp.py "%~1" --out "%~2"
