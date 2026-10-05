"""Эмулятор командной оболочки UNIX с графическим интерфейсом."""

import argparse
import os
import tkinter as tk

DEFAULT_VFS_NAME = "myvfs"
PROMPT = "$ "
COMMENT = "#"


def parse(line):
    """Разбивает строку на команду и список аргументов по пробелам.

    Для пустой строки возвращает (None, []).
    """
    parts = line.split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


def strip_comment(line):
    """Удаляет комментарий: всё от символа # до конца строки."""
    return line.split(COMMENT, 1)[0].strip()


def read_script(path):
    """Читает стартовый скрипт и возвращает список команд.

    Комментарии и пустые строки пропускаются.
    При ошибке чтения выбрасывает OSError или UnicodeDecodeError.
    """
    with open(path, encoding="utf-8") as file:
        lines = [strip_comment(line) for line in file]
    return [line for line in lines if line]


def parse_args(argv=None):
    """Разбирает параметры командной строки эмулятора."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки UNIX")
    parser.add_argument("--vfs", help="путь к физическому расположению VFS")
    parser.add_argument("--script", help="путь к стартовому скрипту")
    return parser.parse_args(argv)


def vfs_name(path):
    """Возвращает имя VFS по пути: имя файла без расширения."""
    if not path:
        return DEFAULT_VFS_NAME
    base = os.path.basename(os.path.normpath(path))
    return os.path.splitext(base)[0]


class Shell:
    """Логика оболочки: выполняет команды и возвращает их вывод."""

    def __init__(self):
        """Создаёт оболочку и таблицу поддерживаемых команд."""
        self.running = True
        self.commands = {
            "ls": self.cmd_stub,
            "cd": self.cmd_stub,
            "exit": self.cmd_exit,
        }

    def execute(self, line):
        """Выполняет одну строку ввода и возвращает текст вывода."""
        cmd, args = parse(line)
        if cmd is None:
            return ""
        handler = self.commands.get(cmd)
        if handler is None:
            return f"{cmd}: команда не найдена"
        return handler(cmd, args)

    def cmd_stub(self, name, args):
        """Заглушка: выводит имя команды и её аргументы."""
        return f"{name} {args}"

    def cmd_exit(self, name, args):
        """Завершает работу оболочки."""
        self.running = False
        return ""


class App:
    """Графическое окно эмулятора."""

    def __init__(self, root, shell, args):
        """Создаёт окно и планирует запуск стартового скрипта."""
        self.root = root
        self.shell = shell
        self.args = args
        root.title(f"Эмулятор — VFS: {vfs_name(args.vfs)}")
        self.output = tk.Text(root, height=20, width=80)
        self.output.pack(fill=tk.BOTH, expand=True)
        self.entry = tk.Entry(root)
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()
        root.after(0, self.start)

    def write(self, text):
        """Добавляет строку текста в поле вывода."""
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def start(self):
        """Выводит параметры запуска и выполняет стартовый скрипт."""
        self.write("Параметры запуска:")
        self.write(f"  --vfs:    {self.args.vfs or 'не задан'}")
        self.write(f"  --script: {self.args.script or 'не задан'}")
        if self.args.script:
            self.run_script(self.args.script)

    def run_script(self, path):
        """Выполняет команды стартового скрипта, показывая ввод и вывод."""
        try:
            commands = read_script(path)
        except (OSError, UnicodeDecodeError) as error:
            self.write(f"Ошибка: не удалось прочитать скрипт: {error}")
            return
        for line in commands:
            self.run_line(line)
            if not self.shell.running:
                return

    def run_line(self, line):
        """Выполняет одну команду и выводит её вместе с результатом."""
        self.write(PROMPT + line)
        result = self.shell.execute(line)
        if result:
            self.write(result)
        if not self.shell.running:
            self.root.destroy()

    def on_enter(self, event):
        """Обрабатывает нажатие Enter: выполняет введённую команду."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.run_line(line)


def main():
    """Точка входа: разбирает параметры и запускает окно эмулятора."""
    args = parse_args()
    root = tk.Tk()
    App(root, Shell(), args)
    root.mainloop()


if __name__ == "__main__":
    main()
