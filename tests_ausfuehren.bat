@echo off
setlocal
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Bitte zuerst einrichten.bat ausfuehren.
  exit /b 1
)
".venv\Scripts\python.exe" -m pytest tests -v -p no:cacheprovider %*
