import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Treeview como árvore")

tree = ttk.Treeview(root, columns=("Status",), show="tree headings")
tree.heading("#0", text="Nome")  # coluna especial da árvore
tree.heading("Status", text="Status")

# Inserindo um item pai
pai = tree.insert("", "end", text="Projeto A", values=("Em andamento",))

# Inserindo filhos
tree.insert(pai, "end", text="Tarefa 1", values=("Todo",))
tree.insert(pai, "end", text="Tarefa 2", values=("In-progress",))
tree.insert(pai, "end", text="Tarefa 3", values=("Done",))

tree.pack()
root.mainloop()