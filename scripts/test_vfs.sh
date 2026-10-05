#!/bin/sh
# Только путь к VFS
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_vfs.py
python3 src/emulator.py --vfs vfs/minimal.zip
