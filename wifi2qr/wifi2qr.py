#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import datetime
import platform
from pathlib import Path
from tkinter import Tk, Label, Button, messagebox, Frame
from tkinter.ttk import Entry, Style
from typing import Optional, List, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont
    import qrcode
except ImportError as e:
    print(f"Fehler beim Importieren der Abhängigkeiten: {e}")
    print("Bitte installieren Sie die Abhängigkeiten mit: pip install -r requirements.txt")
    sys.exit(1)


class WiFi2QRConfig:
    """Konfigurationsklasse für WiFi2QR"""
    
    def __init__(self):
        self.output_dir = Path("qrcode")
        self.font_size = 16
        self.padding = 10
        self.bg_color = "white"
        self.fg_color = "black"
        self.qr_box_size = 10
        self.qr_border = 4
        self.line_spacing = 4
        
        # Plattformspezifische Font-Pfade
        self.font_paths = self._get_platform_fonts()
    
    def _get_platform_fonts(self) -> List[str]:
        """Gibt plattformspezifische Font-Pfade zurück"""
        system = platform.system().lower()
        
        if system == "linux":
            return [
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                "/usr/share/fonts/TTF/DejaVuSans.ttf",
            ]
        elif system == "darwin":  # macOS
            return [
                "/System/Library/Fonts/Helvetica.ttc",
                "/Library/Fonts/Arial.ttf",
                "/System/Library/Fonts/Arial.ttf",
            ]
        elif system == "windows":
            return [
                "C:/Windows/Fonts/arial.ttf",
                "C:/Windows/Fonts/calibri.ttf",
                "Arial Unicode.ttf",
            ]
        else:
            return ["Arial Unicode.ttf"]


class WiFi2QRGenerator:
    """Hauptklasse für die QR-Code-Generierung"""
    
    def __init__(self, config: WiFi2QRConfig):
        self.config = config
        self._ensure_output_dir()
    
    def _ensure_output_dir(self) -> None:
        """Stellt sicher, dass das Output-Verzeichnis existiert"""
        try:
            self.config.output_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise RuntimeError(f"Keine Berechtigung zum Erstellen des Verzeichnisses: {self.config.output_dir}")
    
    def _load_font(self, size: int) -> ImageFont.FreeTypeFont:
        """Lädt eine verfügbare Schriftart"""
        for path in self.config.font_paths:
            try:
                if Path(path).exists():
                    return ImageFont.truetype(path, size)
            except (OSError, IOError):
                continue
        
        # Fallback auf Standard-Font
        try:
            return ImageFont.load_default()
        except Exception:
            # Letzter Fallback - erstelle einen minimalen Font
            return ImageFont.load_default()
    
    def _generate_wifi_qr(self, ssid: str, password: str, encryption: str = "WPA") -> Image.Image:
        """Generiert einen WiFi QR-Code"""
        if not ssid.strip():
            raise ValueError("SSID darf nicht leer sein")
        
        # Escape spezielle Zeichen in SSID und Passwort
        ssid_escaped = ssid.replace(";", "\\;").replace(",", "\\,").replace(":", "\\:")
        password_escaped = password.replace(";", "\\;").replace(",", "\\,").replace(":", "\\:")
        
        wifi_string = f"WIFI:T:{encryption};S:{ssid_escaped};P:{password_escaped};;"
        
        try:
            qr = qrcode.QRCode(
                box_size=self.config.qr_box_size,
                border=self.config.qr_border,
                error_correction=qrcode.constants.ERROR_CORRECT_M
            )
            qr.add_data(wifi_string)
            qr.make(fit=True)
            return qr.make_image(
                fill_color=self.config.fg_color,
                back_color=self.config.bg_color
            ).convert("RGB")
        except Exception as e:
            raise RuntimeError(f"Fehler beim Erstellen des QR-Codes: {e}")
    
    def _get_text_size(self, draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
        """Berechnet die Textgröße"""
        try:
            bbox = draw.textbbox((0, 0), text, font=font)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            return width, height
        except Exception:
            # Fallback für ältere PIL-Versionen
            return draw.textsize(text, font=font)
    
    def _compose_final_image(self, qr_img: Image.Image, ssid: str, password: str) -> Image.Image:
        """Komponiert das finale Bild mit QR-Code und Text"""
        font = self._load_font(self.config.font_size)
        dummy = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(dummy)
        
        lines = [f"SSID: {ssid}", f"Passwort: {password}"]
        widths, heights = zip(*(self._get_text_size(draw, line, font) for line in lines))
        text_width = max(widths)
        text_height = sum(heights) + (len(lines) - 1) * self.config.line_spacing
        
        final_width = max(qr_img.width, text_width + 2 * self.config.padding)
        final_height = qr_img.height + text_height + 3 * self.config.padding
        final = Image.new("RGB", (final_width, final_height), self.config.bg_color)
        
        # QR-Code zentriert einfügen
        qr_x = (final_width - qr_img.width) // 2
        final.paste(qr_img, (qr_x, self.config.padding))
        
        # Text hinzufügen
        draw_final = ImageDraw.Draw(final)
        y_text = qr_img.height + 2 * self.config.padding
        for line in lines:
            line_width, line_height = self._get_text_size(draw_final, line, font)
            x_text = (final_width - line_width) // 2
            draw_final.text((x_text, y_text), line, font=font, fill=self.config.fg_color)
            y_text += line_height + self.config.line_spacing
        
        return final
    
    def _save_image(self, img: Image.Image, prefix: str = "wifi2qr") -> Path:
        """Speichert das Bild mit Zeitstempel"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.config.output_dir / f"{prefix}_{timestamp}.png"
        
        try:
            img.save(filename, "PNG", optimize=True)
            return filename
        except Exception as e:
            raise RuntimeError(f"Fehler beim Speichern der Datei: {e}")
    
    def generate_and_save(self, ssid: str, password: str, encryption: str = "WPA") -> Tuple[Image.Image, Path]:
        """Generiert und speichert einen WiFi QR-Code"""
        qr_img = self._generate_wifi_qr(ssid, password, encryption)
        final_img = self._compose_final_image(qr_img, ssid, password)
        saved_path = self._save_image(final_img)
        return final_img, saved_path


class WiFi2QRGUI:
    """GUI-Klasse für WiFi2QR"""
    
    def __init__(self):
        self.config = WiFi2QRConfig()
        self.generator = WiFi2QRGenerator(self.config)
        self.window = None
        self.ssid_entry = None
        self.psw_entry = None
    
    def _on_button_click(self) -> None:
        """Behandelt den Button-Klick"""
        ssid = self.ssid_entry.get().strip()
        password = self.psw_entry.get().strip()
        
        if not ssid:
            messagebox.showerror("Fehler", "Bitte geben Sie eine SSID ein!")
            return
        
        if not password:
            messagebox.showerror("Fehler", "Bitte geben Sie ein Passwort ein!")
            return
        
        try:
            final_img, saved_path = self.generator.generate_and_save(ssid, password)
            final_img.show()
            messagebox.showinfo("Erfolgreich", f"QR-Code erfolgreich erstellt!\n\nGespeichert als:\n{saved_path}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Erstellen des QR-Codes:\n{str(e)}")
    
    def _setup_styles(self) -> None:
        """Konfiguriert die GUI-Styles"""
        style = Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass  # Fallback auf Standard-Theme
        
        style.configure(
            "Custom.TEntry",
            foreground="black",
            fieldbackground="white",
            background="white",
        )
    
    def build_gui(self) -> None:
        """Erstellt die GUI"""
        self.window = Tk()
        self.window.title("WiFi2QR - WiFi QR-Code Generator")
        self.window.geometry("400x200")
        
        self._setup_styles()
        
        # Hauptframe
        frame = Frame(self.window, bg=self.config.bg_color)
        frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # SSID Eingabe
        Label(
            frame,
            text="SSID:",
            bg=self.config.bg_color,
            fg=self.config.fg_color,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=5, pady=10, sticky="e")
        
        self.ssid_entry = Entry(frame, width=30, style="Custom.TEntry")
        self.ssid_entry.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        
        # Passwort Eingabe
        Label(
            frame,
            text="Passwort:",
            bg=self.config.bg_color,
            fg=self.config.fg_color,
            font=("Arial", 10, "bold")
        ).grid(row=1, column=0, padx=5, pady=10, sticky="e")
        
        self.psw_entry = Entry(frame, width=30, show="*", style="Custom.TEntry")
        self.psw_entry.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
        
        # Button
        Button(
            frame,
            text="QR-Code erstellen",
            command=self._on_button_click,
            width=25,
            font=("Arial", 10, "bold")
        ).grid(row=2, column=0, columnspan=2, pady=20)
        
        # Grid-Konfiguration für responsive Design
        frame.grid_columnconfigure(1, weight=1)
        
        # Enter-Taste Binding
        self.window.bind('<Return>', lambda event: self._on_button_click())
        
        # Fokus auf SSID-Eingabe
        self.ssid_entry.focus()
        
        self.window.resizable(True, False)
    
    def run(self) -> None:
        """Startet die GUI"""
        if self.window:
            self.window.mainloop()


def main():
    """Hauptfunktion"""
    try:
        app = WiFi2QRGUI()
        app.build_gui()
        app.run()
    except KeyboardInterrupt:
        print("\nProgramm wurde vom Benutzer beendet.")
        sys.exit(0)
    except Exception as e:
        print(f"Unbekannter Fehler: {e}")
        messagebox.showerror("Kritischer Fehler", f"Ein unerwarteter Fehler ist aufgetreten:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()