#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from pathlib import Path

# Lese die README-Datei für die lange Beschreibung
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="wifi2qr",
    version="2.0.0",
    author="schwabochino",
    author_email="",
    description="Ein einfaches Python-Programm zur Erstellung von QR-Codes mit WiFi-Zugangsdaten",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/schwabochino/wifi2qr",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities",
        "Topic :: Communications",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.7",
    install_requires=[
        "Pillow>=9.0.0",
        "qrcode[pil]>=7.0.0",
    ],
    entry_points={
        "console_scripts": [
            "wifi2qr=wifi2qr.wifi2qr:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="wifi qr qrcode generator gui tkinter",
    project_urls={
        "Bug Reports": "https://github.com/schwabochino/wifi2qr/issues",
        "Source": "https://github.com/schwabochino/wifi2qr",
    },
) 