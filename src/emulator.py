"""Эмулятор командной оболочки UNIX с графическим интерфейсом."""

import tkinter as tk

VFS_NAME = "myvfs"
PROMPT = "$ "


def parse(line):
    """Разбивает строку на команду и список аргументов по пробелам.

    Для пустой строки возвращает (None, []).
    """
    parts = line.split()
    if not parts:
        return None, []
    return parts[0], parts[1:]


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

    def __init__(self, root, shell):
        """Создаёт поле вывода и строку ввода."""
        self.root = root
        self.shell = shell
        root.title(f"Эмулятор — VFS: {VFS_NAME}")
        self.output = tk.Text(root, height=20, width=80)
        self.output.pack(fill=tk.BOTH, expand=True)
        self.entry = tk.Entry(root)
        self.entry.pack(fill=tk.X)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

    def write(self, text):
        """Добавляет строку текста в поле вывода."""
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def on_enter(self, event):
        """Обрабатывает нажатие Enter: выполняет введённую команду."""
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.write(PROMPT + line)
        result = self.shell.execute(line)
        if result:
            self.write(result)
        if not self.shell.running:
            self.root.destroy()


def main():
    """Точка входа: запускает окно эмулятора."""
    root = tk.Tk()
    App(root, Shell())
    root.mainloop()


if __name__ == "__main__":
    main()
