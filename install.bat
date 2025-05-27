@echo off
REM WiFi2QR - Automatisches Installationsskript für Windows
REM Dieses Skript richtet alles automatisch ein und startet das Programm

echo 🚀 WiFi2QR Installation wird gestartet...
echo.

REM Wechsle ins Projektverzeichnis
cd /d "%~dp0"

REM Prüfe Python-Installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python ist nicht installiert oder nicht im PATH!
    echo Bitte installieren Sie Python 3.7 oder höher von:
    echo https://www.python.org/downloads/
    echo.
    echo Stellen Sie sicher, dass "Add Python to PATH" aktiviert ist!
    pause
    exit /b 1
)

echo ✅ Python gefunden
python --version

REM Erstelle virtuelle Umgebung falls nicht vorhanden
if not exist "venv" (
    echo 📦 Erstelle virtuelle Umgebung...
    python -m venv venv
) else (
    echo ✅ Virtuelle Umgebung bereits vorhanden
)

REM Aktiviere virtuelle Umgebung
echo 🔧 Aktiviere virtuelle Umgebung...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Aktualisiere pip...
python -m pip install --upgrade pip --quiet

REM Installiere Abhängigkeiten
echo 📚 Installiere Abhängigkeiten...
pip install -r requirements.txt --quiet

REM Erstelle qrcode Verzeichnis
if not exist "qrcode" mkdir qrcode

echo.
echo 🎉 Installation erfolgreich abgeschlossen!
echo.
echo 📋 Verwendung:
echo   start.bat           - Programm starten
echo   install.bat         - Erneute Installation
echo.

REM Frage ob das Programm gestartet werden soll
set /p "choice=Möchten Sie WiFi2QR jetzt starten? (j/N): "
if /i "%choice%"=="j" (
    echo 🚀 Starte WiFi2QR...
    python wifi2qr\wifi2qr.py
) else if /i "%choice%"=="y" (
    echo 🚀 Starte WiFi2QR...
    python wifi2qr\wifi2qr.py
)

pause 