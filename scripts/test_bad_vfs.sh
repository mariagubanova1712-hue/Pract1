#!/bin/sh
# Этап 3: ошибка, VFS не существует
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_vfs.py
python3 src/emulator.py --vfs vfs/no_such.zip --script scripts/stage3.txt
