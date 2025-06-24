#!/usr/bin/env bash

# Aktualizacja npm do najnowszej wersji
npm install -g npm@latest

# Instalacja zależności Pythona
pip install -r requirements.txt

# Instalacja przeglądarek dla Playwright (wraz z zależnościami systemowymi)
playwright install --with-deps
