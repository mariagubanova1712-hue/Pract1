#!/bin/sh
# Этап 3: VFS с вложенностью 4 уровня
cd "$(dirname "$0")/.." || exit 1
python3 scripts/make_vfs.py
python3 src/emulator.py --vfs vfs/deep.zip --script scripts/stage3.txt
