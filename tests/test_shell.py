"""Тесты логики оболочки (без графического интерфейса)."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from emulator import (  # noqa: E402
    Shell, parse, parse_args, read_script, strip_comment,
)


class TestParse(unittest.TestCase):
    """Проверка парсера командной строки."""

    def test_command_and_args(self):
        """Строка делится на команду и аргументы."""
        self.assertEqual(parse("ls -l /home"), ("ls", ["-l", "/home"]))

    def test_extra_spaces(self):
        """Лишние пробелы игнорируются."""
        self.assertEqual(parse("  cd   dir  "), ("cd", ["dir"]))

    def test_empty(self):
        """Пустая строка даёт None."""
        self.assertEqual(parse("   "), (None, []))


class TestShell(unittest.TestCase):
    """Проверка выполнения команд."""

    def setUp(self):
        """Создаёт новую оболочку для каждого теста."""
        self.shell = Shell()

    def test_stubs(self):
        """Заглушки выводят имя и аргументы."""
        self.assertEqual(self.shell.execute("ls a b"), "ls ['a', 'b']")
        self.assertEqual(self.shell.execute("cd"), "cd []")

    def test_unknown(self):
        """Неизвестная команда даёт ошибку."""
        self.assertEqual(self.shell.execute("foo"),
                         "foo: команда не найдена")

    def test_exit(self):
        """exit останавливает оболочку."""
        self.shell.execute("exit")
        self.assertFalse(self.shell.running)

    def test_vfs_info(self):
        """vfs-info выводит имя и хеш VFS."""
        result = self.shell.execute("vfs-info")
        self.assertIn("Имя VFS: myvfs", result)
        self.assertIn(self.shell.vfs.sha256(), result)

    def test_vfs_commands_reject_args(self):
        """Служебные команды не принимают аргументы."""
        self.assertIn("не принимает", self.shell.execute("vfs-info x"))
        self.assertIn("не принимает", self.shell.execute("vfs-init x"))


class TestConfig(unittest.TestCase):
    """Проверка параметров командной строки и стартового скрипта."""

    def test_args(self):
        """Оба параметра разбираются."""
        args = parse_args(["--vfs", "a.zip", "--script", "s.txt"])
        self.assertEqual((args.vfs, args.script), ("a.zip", "s.txt"))

    def test_no_args(self):
        """Без параметров оба значения пустые."""
        args = parse_args([])
        self.assertIsNone(args.vfs)
        self.assertIsNone(args.script)

    def test_strip_comment(self):
        """Комментарий в конце строки удаляется."""
        self.assertEqual(strip_comment("ls a  # тест"), "ls a")
        self.assertEqual(strip_comment("# только комментарий"), "")

    def test_read_script(self):
        """Из скрипта остаются только команды."""
        text = "# заголовок\nls a\n\ncd b # переход\n"
        with tempfile.NamedTemporaryFile(
                "w", suffix=".txt", delete=False, encoding="utf-8") as file:
            file.write(text)
        try:
            self.assertEqual(read_script(file.name), ["ls a", "cd b"])
        finally:
            os.remove(file.name)

    def test_missing_script(self):
        """Несуществующий скрипт вызывает ошибку."""
        with self.assertRaises(OSError):
            read_script("нет_такого_файла.txt")


if __name__ == "__main__":
    unittest.main()
