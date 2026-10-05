#!/bin/sh
# Только стартовый скрипт
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_vfs.py
python3 src/emulator.py --script scripts/stage2.txt
