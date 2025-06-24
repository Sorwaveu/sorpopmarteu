#!/usr/bin/env bash

# Aktualizacja npm do najnowszej wersji
npm install -g npm@latest

# Instalacja zależności Pythona
pip install -r requirements.txt

# Instalacja przeglądarek dla Playwright (wraz z zależnościami systemowymi)
PLAYWRIGHT_BROWSERS_PATH=0 playwright install
