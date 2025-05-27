#!/bin/bash

# WiFi2QR - Automatisches Installationsskript
# Dieses Skript richtet alles automatisch ein und startet das Programm

set -e  # Beende bei Fehlern

echo "🚀 WiFi2QR Installation wird gestartet..."
echo ""

# Wechsle ins Projektverzeichnis
cd "$(dirname "$0")"

# Prüfe Python-Installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 ist nicht installiert!"
    echo "Bitte installieren Sie Python 3.7 oder höher:"
    echo "  - macOS: brew install python3"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "  - CentOS/RHEL: sudo yum install python3 python3-pip"
    exit 1
fi

echo "✅ Python 3 gefunden: $(python3 --version)"

# Erstelle virtuelle Umgebung falls nicht vorhanden
if [ ! -d "venv" ]; then
    echo "📦 Erstelle virtuelle Umgebung..."
    python3 -m venv venv
else
    echo "✅ Virtuelle Umgebung bereits vorhanden"
fi

# Aktiviere virtuelle Umgebung
echo "🔧 Aktiviere virtuelle Umgebung..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Aktualisiere pip..."
pip install --upgrade pip --quiet

# Installiere Abhängigkeiten
echo "📚 Installiere Abhängigkeiten..."
pip install -r requirements.txt --quiet

# Erstelle qrcode Verzeichnis
mkdir -p qrcode

echo ""
echo "🎉 Installation erfolgreich abgeschlossen!"
echo ""
echo "📋 Verwendung:"
echo "  ./start.sh          - Programm starten"
echo "  ./install.sh        - Erneute Installation"
echo ""

# Frage ob das Programm gestartet werden soll
read -p "Möchten Sie WiFi2QR jetzt starten? (j/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[JjYy]$ ]]; then
    echo "🚀 Starte WiFi2QR..."
    python wifi2qr/wifi2qr.py
fi 