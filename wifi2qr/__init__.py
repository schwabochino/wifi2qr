#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WiFi2QR - WiFi QR-Code Generator

Ein einfaches Python-Programm zur Erstellung von QR-Codes mit WiFi-Zugangsdaten.
"""

__version__ = "2.0.0"
__author__ = "schwabochino"
__email__ = ""
__description__ = "Ein einfaches Python-Programm zur Erstellung von QR-Codes mit WiFi-Zugangsdaten"

from .wifi2qr import WiFi2QRConfig, WiFi2QRGenerator, WiFi2QRGUI, main

__all__ = [
    "WiFi2QRConfig",
    "WiFi2QRGenerator", 
    "WiFi2QRGUI",
    "main",
] 