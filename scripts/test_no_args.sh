#!/bin/sh
# Запуск без параметров
cd "$(dirname "$0")/.." || exit 1
python3 src/emulator.py
