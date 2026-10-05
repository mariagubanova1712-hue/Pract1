"""Виртуальная файловая система (VFS), полностью хранящаяся в памяти.

Источник данных VFS — ZIP-архив. Архив читается в память целиком
и не распаковывается на диск.
"""

import hashlib
import io
import os
import zipfile

DEFAULT_VFS_NAME = "myvfs"


class VFSError(Exception):
    """Ошибка загрузки или изменения VFS."""


def vfs_name(path):
    """Возвращает имя VFS по пути: имя файла без расширения."""
    if not path:
        return DEFAULT_VFS_NAME
    base = os.path.basename(os.path.normpath(path))
    return os.path.splitext(base)[0]


def empty_zip():
    """Возвращает байты пустого ZIP-архива (VFS по умолчанию)."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w"):
        pass
    return buffer.getvalue()


def add_entry(root, info, archive):
    """Добавляет в дерево каталогов один элемент ZIP-архива.

    Каталог хранится как словарь {имя: узел}, файл — как байты.
    """
    parts = [part for part in info.filename.split("/") if part]
    if not parts:
        return
    node = root
    for part in parts[:-1]:
        node = node.setdefault(part, {})
        if not isinstance(node, dict):
            raise VFSError(f"конфликт имён в архиве: {info.filename}")
    if info.is_dir():
        node.setdefault(parts[-1], {})
    else:
        node[parts[-1]] = archive.read(info)


def build_tree(data):
    """Строит дерево каталогов в памяти из байтов ZIP-архива."""
    try:
        archive = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as error:
        raise VFSError("файл не является ZIP-архивом") from error
    root = {}
    with archive:
        for info in archive.infolist():
            add_entry(root, info, archive)
    return root


class VFS:
    """Виртуальная файловая система: имя, исходные данные и дерево."""

    def __init__(self, name=DEFAULT_VFS_NAME, data=None, path=None):
        """Создаёт VFS из байтов ZIP-архива (по умолчанию — пустую)."""
        self.name = name
        self.path = path
        self.data = empty_zip() if data is None else data
        self.root = build_tree(self.data)

    @classmethod
    def load(cls, path):
        """Загружает VFS из ZIP-архива по пути path."""
        try:
            with open(path, "rb") as file:
                data = file.read()
        except OSError as error:
            raise VFSError(
                f"не удалось открыть {path}: {error.strerror}") from error
        return cls(vfs_name(path), data, path)

    def sha256(self):
        """Возвращает SHA-256 хеш данных VFS в шестнадцатеричном виде."""
        return hashlib.sha256(self.data).hexdigest()

    def reset(self):
        """Заменяет VFS на пустую и очищает её физическое представление."""
        self.data = empty_zip()
        self.root = {}
        if not self.path:
            return
        try:
            with open(self.path, "wb") as file:
                file.write(self.data)
        except OSError as error:
            raise VFSError(
                f"не удалось очистить {self.path}: {error.strerror}"
            ) from error
