#!/bin/sh
# Ошибка: стартовый скрипт не существует
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_vfs.py
python3 src/emulator.py --script scripts/no_such_file.txt
