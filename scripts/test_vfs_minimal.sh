#!/bin/sh
# Этап 3: минимальная VFS (один файл)
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_vfs.py
python3 src/emulator.py --vfs vfs/minimal.zip --script scripts/stage3.txt
