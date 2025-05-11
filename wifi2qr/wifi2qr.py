#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WiFi2QR – Erzeugt ein kombiniertes QR-Code- und Zutritts-Info-Bild für WLAN-Zugangsdaten.

Benötigte Pakete:
    pip install qrcode[pil] Pillow
"""

import os
import sys
import datetime
import qrcode
from pathlib import Path
from tkinter import Tk, Label, Entry, Button, messagebox
from PIL import Image, ImageDraw, ImageFont

# Konfiguration
OUTPUT_DIR = Path("qrcode")
FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "Arial Unicode.ttf",
]
FONT_SIZE = 16
PADDING = 10
BG_COLOR = "white"
FG_COLOR = "black"


def ensure_output_dir():
    """Legt den Ausgabe-Ordner an, falls er nicht existiert."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    """Versucht, eine TrueType-Schrift zu laden, und verwendet sonst die Default-Schrift."""
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def generate_wifi_qr(ssid: str, password: str, encryption: str = "WPA") -> Image.Image:
    """Erzeugt und gibt ein QR-Code-Image für die WLAN-Zugangsdaten zurück."""
    wifi_string = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
    qr = qrcode.QRCode(
        version=None,  # automatisch anpassen
        box_size=10,
        border=4,
    )
    qr.add_data(wifi_string)
    qr.make(fit=True)
    return qr.make_image(fill_color=FG_COLOR, back_color=BG_COLOR).convert("RGB")


def compose_final_image(qr_img: Image.Image, ssid: str, password: str) -> Image.Image:
    """Erzeugt das Endbild mit QR-Code und Text darunter."""
    font = load_font(FONT_SIZE)
    draw = ImageDraw.Draw(qr_img)

    # Textzeilen vorbereiten
    lines = [f"SSID: {ssid}", f"Password: {password}"]
    # Breite und Höhe des Textblocks berechnen
    text_width = max(draw.textsize(line, font=font)[0] for line in lines)
    text_height = sum(draw.textsize(line, font=font)[1] for line in lines) + (len(lines)-1)*4

    # Neues Bild größer als QR + Text
    final_width = max(qr_img.width, text_width + 2*PADDING)
    final_height = qr_img.height + text_height + 3*PADDING
    final = Image.new("RGB", (final_width, final_height), BG_COLOR)

    # QR-Code einfügen (zentriert)
    qr_x = (final_width - qr_img.width) // 2
    final.paste(qr_img, (qr_x, PADDING))

    # Text darunter zeichnen
    draw_final = ImageDraw.Draw(final)
    y_text = qr_img.height + 2*PADDING
    for line in lines:
        line_width, line_height = draw_final.textsize(line, font=font)
        x_text = (final_width - line_width) // 2
        draw_final.text((x_text, y_text), line, font=font, fill=FG_COLOR)
        y_text += line_height + 4

    return final


def save_image(img: Image.Image, prefix: str = "wifi2qr") -> Path:
    """Speichert das Bild mit Zeitstempel und gibt den Pfad zurück."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUT_DIR / f"{prefix}_{timestamp}.png"
    img.save(filename)
    return filename


def on_button_click(ssid_entry: Entry, psw_entry: Entry):
    ssid = ssid_entry.get().strip()
    password = psw_entry.get().strip()
    if not ssid or not password:
        messagebox.showerror("Fehler", "Bitte SSID und Passwort eingeben!")
        return

    ensure_output_dir()
    qr_img = generate_wifi_qr(ssid, password)
    final_img = compose_final_image(qr_img, ssid, password)
    saved_path = save_image(final_img)
    final_img.show()
    messagebox.showinfo("Erfolgreich", f"Bild gespeichert als:\n{saved_path}")


def build_gui():
    """Erstellt und startet das Tkinter-Fenster."""
    window = Tk()
    window.title("WiFi2QR")

    Label(window, text="SSID:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    ssid_entry = Entry(window, width=30)
    ssid_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(window, text="Passwort:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    psw_entry = Entry(window, width=30, show="*")
    psw_entry.grid(row=1, column=1, padx=5, pady=5)

    Button(
        window,
        text="QR erzeugen",
        command=lambda: on_button_click(ssid_entry, psw_entry),
        width=15
    ).grid(row=2, column=0, columnspan=2, pady=10)

    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    try:
        build_gui()
    except Exception as e:
        print(f"Unbekannter Fehler: {e}", file=sys.stderr)
        sys.exit(1)