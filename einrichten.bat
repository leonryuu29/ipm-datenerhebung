@echo off
setlocal
chcp 65001 >nul
set PYTHONUTF8=1
cd /d "%~dp0"
echo === 1/4 Python suchen ===
set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY where python >nul 2>nul && set PY=python
if not defined PY (
  echo Python wurde nicht gefunden.
  echo Bitte zuerst installieren:  winget install Python.Python.3.12
  echo Danach dieses Fenster schliessen, ein neues oeffnen und einrichten.bat erneut starten.
  exit /b 1
)
%PY% --version
echo.
echo === 2/4 Virtuelle Umgebung .venv anlegen ===
if not exist ".venv\Scripts\python.exe" %PY% -m venv .venv
if not exist ".venv\Scripts\python.exe" (
  echo Die Umgebung .venv konnte nicht angelegt werden.
  exit /b 1
)
echo.
echo === 3/4 Pakete installieren ===
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo Die Installation der Pakete ist fehlgeschlagen.
  exit /b 1
)
echo.
echo === 4/4 Browser fuer den Prototyp-Test laden (Chromium) ===
".venv\Scripts\python.exe" -m playwright install chromium
if errorlevel 1 echo Hinweis: Chromium konnte nicht geladen werden. Die anderen Tests laufen trotzdem.
echo.
echo Fertig. Weiter mit:  tests_ausfuehren.bat
