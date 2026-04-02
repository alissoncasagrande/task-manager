import tkinter as tk
from tkinter import ttk

root = tk.Tk()

cols = ("Nome", "Status")
tree = ttk.Treeview(root, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
tree.pack()

# Inserindo um item "pai"
pai = tree.insert("", "end", text="Projeto A", values=("Projeto A", "Em andamento"))

# Inserindo filhos do "pai"
tree.insert(pai, "end", text="Tarefa 1", values=("Tarefa 1", "Todo"))
tree.insert(pai, "end", text="Tarefa 2", values=("Tarefa 2", "In-progress"))
tree.insert(pai, "end", text="Tarefa 3", values=("Tarefa 3", "Done"))

root.mainloop()