"""Тесты виртуальной файловой системы."""

import hashlib
import os
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from vfs import (  # noqa: E402
    VFS, VFSError, decode_content, empty_zip, vfs_name,
)


def make_zip_file(files):
    """Создаёт временный ZIP-архив и возвращает путь к нему."""
    handle, path = tempfile.mkstemp(suffix=".zip")
    os.close(handle)
    with zipfile.ZipFile(path, "w") as archive:
        for name, content in files.items():
            archive.writestr(name, content)
    return path


class TestVFS(unittest.TestCase):
    """Проверка загрузки, хеша и сброса VFS."""

    def setUp(self):
        """Создаёт тестовый архив с вложенностью 3 уровня."""
        self.path = make_zip_file({
            "a/b/c/file.txt": "текст",
            "top.bin": bytes([0, 1, 255]),
            "empty/": "",
        })

    def tearDown(self):
        """Удаляет тестовый архив."""
        os.remove(self.path)

    def test_load_tree(self):
        """Дерево каталогов строится в памяти."""
        vfs = VFS.load(self.path)
        file_data = decode_content(vfs.root["a"]["b"]["c"]["file.txt"])
        self.assertEqual(file_data.decode("utf-8"), "текст")
        self.assertEqual(vfs.root["top.bin"], "AAH/")
        self.assertEqual(decode_content("AAH/"), bytes([0, 1, 255]))
        self.assertEqual(vfs.root["empty"], {})

    def test_name_and_hash(self):
        """Имя берётся из файла, хеш — от данных архива."""
        vfs = VFS.load(self.path)
        with open(self.path, "rb") as file:
            expected = hashlib.sha256(file.read()).hexdigest()
        self.assertEqual(vfs.sha256(), expected)
        self.assertEqual(vfs.name, vfs_name(self.path))

    def test_reset(self):
        """Сброс очищает дерево и физический файл."""
        vfs = VFS.load(self.path)
        vfs.reset()
        self.assertEqual(vfs.root, {})
        with open(self.path, "rb") as file:
            self.assertEqual(file.read(), empty_zip())

    def test_missing_file(self):
        """Несуществующий архив вызывает VFSError."""
        with self.assertRaises(VFSError):
            VFS.load("нет_такого_архива.zip")

    def test_not_zip(self):
        """Файл не ZIP вызывает VFSError."""
        with self.assertRaises(VFSError):
            VFS(data=b"not a zip")

    def test_default(self):
        """VFS по умолчанию пустая и называется myvfs."""
        vfs = VFS()
        self.assertEqual((vfs.name, vfs.root), ("myvfs", {}))
        self.assertEqual(vfs_name(None), "myvfs")
        self.assertEqual(vfs_name("vfs/deep.zip"), "deep")


if __name__ == "__main__":
    unittest.main()
