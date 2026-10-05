#!/bin/sh
# Этап 3: ошибка, VFS не является ZIP-архивом
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_vfs.py
python3 src/emulator.py --vfs scripts/stage3.txt --script scripts/stage3.txt
