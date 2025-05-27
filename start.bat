@echo off
REM WiFi2QR - Einfaches Startskript für Windows
REM Startet das Programm in der virtuellen Umgebung

cd /d "%~dp0"

REM Prüfe ob Installation vorhanden ist
if not exist "venv" (
    echo ❌ Virtuelle Umgebung nicht gefunden!
    echo Bitte führen Sie zuerst die Installation aus:
    echo   install.bat
    pause
    exit /b 1
)

REM Aktiviere virtuelle Umgebung und starte Programm
call venv\Scripts\activate.bat
python wifi2qr\wifi2qr.py 