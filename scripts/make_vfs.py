"""Создаёт тестовые VFS (ZIP-архивы) в папке vfs/.

Архивы запрещено хранить в репозитории, поэтому они собираются
этим скриптом перед каждым запуском тестовых скриптов ОС.
"""

import os
import zipfile

VFS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "..", "vfs")

TEST_VFS = {
    "minimal": {
        "readme.txt": "Минимальная VFS: один файл.\n",
    },
    "files": {
        "readme.txt": "VFS с несколькими файлами.\n",
        "notes.txt": "Заметки\nвторая строка\n",
        "data.csv": "id,name\n1,Maria\n2,Ivan\n",
        "image.bin": bytes(range(256)),
        "docs/report.txt": "Отчёт по практике.\n",
    },
    "deep": {
        "home/user/docs/work/task.txt": "Задание на 4 уровне.\n",
        "home/user/docs/plan.md": "# План\n",
        "home/user/music/list.txt": "song1\nsong2\n",
        "etc/app/config/settings.ini": "[main]\ndebug=true\n",
        "tmp/": "",
    },
}


def make_zip(path, files):
    """Создаёт ZIP-архив path из словаря {путь в архиве: содержимое}."""
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in files.items():
            archive.writestr(name, content)


def main():
    """Создаёт все тестовые VFS."""
    os.makedirs(VFS_DIR, exist_ok=True)
    for name, files in TEST_VFS.items():
        make_zip(os.path.join(VFS_DIR, name + ".zip"), files)


if __name__ == "__main__":
    main()
