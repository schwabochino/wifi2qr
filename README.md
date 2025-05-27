# WiFi2QR - WiFi QR-Code Generator

Ein einfaches Python-Programm zur Erstellung von QR-Codes mit WiFi-Zugangsdaten.

## Features

- ✅ Benutzerfreundliche grafische Oberfläche
- ✅ Automatische QR-Code-Generierung für WiFi-Netzwerke
- ✅ Plattformübergreifende Unterstützung (Windows, macOS, Linux)
- ✅ Automatische Font-Erkennung je nach Betriebssystem
- ✅ Robuste Fehlerbehandlung
- ✅ Escape-Behandlung für Sonderzeichen in SSID/Passwort
- ✅ Zeitstempel-basierte Dateinamen
- ✅ Optimierte PNG-Ausgabe

## 🚀 Schnellstart

### Für macOS/Linux:
```bash
git clone https://github.com/schwabochino/wifi2qr.git
cd wifi2qr
./install.sh
```

### Für Windows:
```cmd
git clone https://github.com/schwabochino/wifi2qr.git
cd wifi2qr
install.bat
```

**Das war's!** Das Installationsskript richtet automatisch alles ein:
- ✅ Prüft Python-Installation
- ✅ Erstellt virtuelle Umgebung
- ✅ Installiert alle Abhängigkeiten
- ✅ Fragt, ob das Programm gestartet werden soll

## 📋 Verwendung

Nach der Installation:

### Programm starten:
```bash
./start.sh      # macOS/Linux
start.bat       # Windows
```

### Programm verwenden:
1. **SSID eingeben**: Name Ihres WiFi-Netzwerks
2. **Passwort eingeben**: WiFi-Passwort
3. **QR-Code erstellen**: Button klicken oder Enter drücken
4. **Fertig**: QR-Code wird angezeigt und gespeichert

### Keyboard-Shortcuts:
- **Enter**: QR-Code erstellen
- **Tab**: Zwischen Feldern wechseln

## 🔧 Erweiterte Installation

### Voraussetzungen
- Python 3.7 oder höher
- pip (Python Package Manager)

### Manuelle Installation
```bash
git clone https://github.com/schwabochino/wifi2qr.git
cd wifi2qr
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# oder: venv\Scripts\activate.bat  # Windows
pip install -r requirements.txt
python wifi2qr/wifi2qr.py
```

### Installation als Paket
```bash
pip install -e .
wifi2qr  # Startet das Programm von überall
```

## 📸 Screenshots

### Benutzeroberfläche
![WiFi2QR GUI](https://raw.githubusercontent.com/schwabochino/wifi2qr/master/exampleimg/wifi2qr.png)

### Ausgabe-Beispiel
![QR-Code Beispiel](https://raw.githubusercontent.com/schwabochino/wifi2qr/master/exampleimg/qrcode.png)

## 🔍 Technische Details

### Unterstützte Verschlüsselungstypen
- WPA/WPA2 (Standard)
- WEP
- Offen (keine Verschlüsselung)

### Ausgabeformat
- PNG-Dateien mit Zeitstempel
- Optimierte Kompression
- Automatische Zentrierung von QR-Code und Text

### Plattform-spezifische Fonts
- **Linux**: DejaVu Sans, Liberation Sans
- **macOS**: Helvetica, Arial
- **Windows**: Arial, Calibri
- **Fallback**: Standard-System-Font

## 🛠️ Fehlerbehebung

### Python nicht gefunden
**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt install python3 python3-pip python3-venv
```

**Windows:**
- Python von https://www.python.org/downloads/ herunterladen
- Bei Installation "Add Python to PATH" aktivieren

### Neuinstallation
```bash
rm -rf venv        # macOS/Linux
rmdir /s venv      # Windows
./install.sh       # macOS/Linux
install.bat        # Windows
```

### QR-Code wird nicht angezeigt
Überprüfen Sie, ob ein Standard-Bildviewer installiert ist.

## 👨‍💻 Entwicklung

### Code-Struktur
- `WiFi2QRConfig`: Konfigurationsklasse
- `WiFi2QRGenerator`: QR-Code-Generierung und Bildkomposition
- `WiFi2QRGUI`: Grafische Benutzeroberfläche

### Abhängigkeiten
- `Pillow`: Bildverarbeitung
- `qrcode`: QR-Code-Generierung
- `tkinter`: GUI (Teil der Python-Standardbibliothek)

### Entwicklungsumgebung
```bash
git clone https://github.com/schwabochino/wifi2qr.git
cd wifi2qr
./install.sh
pip install -e .  # Entwicklungsinstallation
```

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

## 🤝 Beitragen

Pull Requests und Issues sind willkommen! Bitte erstellen Sie ein Issue, bevor Sie größere Änderungen vornehmen.

## 📝 Changelog

### Version 2.1 (Aktuell)
- ✅ **Vereinfachte Installation**: Ein-Klick-Setup mit `install.sh`/`install.bat`
- ✅ **Einfache Startskripte**: `start.sh`/`start.bat`
- ✅ **Automatische Prüfungen**: Python-Installation und Abhängigkeiten
- ✅ **Benutzerfreundliche Ausgaben**: Emojis und klare Anweisungen

### Version 2.0
- ✅ Objektorientierte Architektur
- ✅ Verbesserte Fehlerbehandlung
- ✅ Plattformspezifische Font-Erkennung
- ✅ Escape-Behandlung für Sonderzeichen
- ✅ Keyboard-Shortcuts (Enter-Taste)
- ✅ Responsive GUI-Design
- ✅ Optimierte PNG-Ausgabe
- ✅ Virtuelle Umgebung Support
- ✅ Setup.py für Paketinstallation

### Version 1.0
- ✅ Grundlegende QR-Code-Generierung
- ✅ Einfache GUI
