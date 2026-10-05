import tkinter as tk

root = tk.Tk()
root.title("Эмулятор — VFS: myvfs")

output = tk.Text(root, height=20, width=70)
output.pack()
entry = tk.Entry(root, width=70)
entry.pack()

def run(event):
    line = entry.get()
    entry.delete(0, tk.END)
    output.insert(tk.END, "$ " + line + "\n")
    parts = line.split()          # парсер: делим по пробелам
    if not parts:
        return
    cmd, args = parts[0], parts[1:]
    if cmd in ("ls", "cd"):
        output.insert(tk.END, f"{cmd} {args}\n")
    elif cmd == "exit":
        root.destroy()
    else:
        output.insert(tk.END, f"{cmd}: команда не найдена\n")

entry.bind("<Return>", run)
root.mainloop()
