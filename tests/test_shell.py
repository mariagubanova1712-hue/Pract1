"""Тесты логики оболочки (без графического интерфейса)."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from emulator import Shell, parse  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
