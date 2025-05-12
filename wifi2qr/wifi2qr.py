#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import datetime
from pathlib import Path
from tkinter import Tk, Label, Button, messagebox, Frame
from tkinter.ttk import Entry, Style
from PIL import Image, ImageDraw, ImageFont
import qrcode

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
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_PATHS:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def generate_wifi_qr(ssid: str, password: str, encryption: str = "WPA") -> Image.Image:
    wifi_string = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(wifi_string)
    qr.make(fit=True)
    return qr.make_image(fill_color=FG_COLOR, back_color=BG_COLOR).convert("RGB")


def get_text_size(draw, text, font):
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height


def compose_final_image(qr_img: Image.Image, ssid: str, password: str) -> Image.Image:
    font = load_font(FONT_SIZE)
    dummy = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(dummy)

    lines = [f"SSID: {ssid}", f"Password: {password}"]
    widths, heights = zip(*(get_text_size(draw, line, font) for line in lines))
    text_width = max(widths)
    text_height = sum(heights) + (len(lines) - 1) * 4

    final_width = max(qr_img.width, text_width + 2 * PADDING)
    final_height = qr_img.height + text_height + 3 * PADDING
    final = Image.new("RGB", (final_width, final_height), BG_COLOR)

    qr_x = (final_width - qr_img.width) // 2
    final.paste(qr_img, (qr_x, PADDING))

    draw_final = ImageDraw.Draw(final)
    y_text = qr_img.height + 2 * PADDING
    for line in lines:
        line_width, line_height = get_text_size(draw_final, line, font)
        x_text = (final_width - line_width) // 2
        draw_final.text((x_text, y_text), line, font=font, fill=FG_COLOR)
        y_text += line_height + 4

    return final


def save_image(img: Image.Image, prefix: str = "wifi2qr") -> Path:
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
    window = Tk()
    window.title("WiFi2QR")

    style = Style()
    style.theme_use("clam")
    style.configure(
        "Custom.TEntry",
        foreground="black",
        fieldbackground="white",
        background="white",
    )

    frame = Frame(window, bg=BG_COLOR)
    frame.pack(padx=10, pady=10)

    Label(frame, text="SSID:", bg=BG_COLOR, fg=FG_COLOR).grid(row=0, column=0, padx=5, pady=5, sticky="e")
    ssid_entry = Entry(frame, width=30, style="Custom.TEntry")
    ssid_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(frame, text="Passwort:", bg=BG_COLOR, fg=FG_COLOR).grid(row=1, column=0, padx=5, pady=5, sticky="e")
    psw_entry = Entry(frame, width=30, show="*", style="Custom.TEntry")
    psw_entry.grid(row=1, column=1, padx=5, pady=5)

    Button(
        frame,
        text="QR erzeugen",
        command=lambda: on_button_click(ssid_entry, psw_entry),
        width=20
    ).grid(row=2, column=0, columnspan=2, pady=10)

    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    try:
        build_gui()
    except Exception as e:
        print(f"Unbekannter Fehler: {e}")
        sys.exit(1)