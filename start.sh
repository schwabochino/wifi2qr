#!/bin/bash

# WiFi2QR - Einfaches Startskript
# Startet das Programm in der virtuellen Umgebung

cd "$(dirname "$0")"

# Prüfe ob Installation vorhanden ist
if [ ! -d "venv" ]; then
    echo "❌ Virtuelle Umgebung nicht gefunden!"
    echo "Bitte führen Sie zuerst die Installation aus:"
    echo "  ./install.sh"
    exit 1
fi

# Aktiviere virtuelle Umgebung und starte Programm
source venv/bin/activate
python wifi2qr/wifi2qr.py 