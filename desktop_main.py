## desktop_main.py ##

import tkinter as tk
from tkinter import ttk
import sqlite3
from tasks import Task

def list_update():
    # limpa a tabela
    for item in tree.get_children():
        tree.delete(item)
    # busca tarefas do banco
    tasks = Task.list_tasks(conn)
    for t in tasks:
        tree.insert("", "end", values=(t.id, t.title, t.status, t.create_date))


def atualizar_status():
    print("Status selecionado:", status.get())


#main
conn = sqlite3.connect("task_manager.db")

win = tk.Tk()
win.title("Task Manager")

# variável que guarda a escolha
status = tk.StringVar(value="Todo")

tk.Label(win, text="Status:").grid(row=0, column=0,padx=5,pady=5)

tk.Radiobutton(win, text="Todo", variable=status, value="Todo", command=atualizar_status).grid(row=0, column=1, padx=5, pady=5)
tk.Radiobutton(win, text="In-progress", variable=status, value="In-progress", command=atualizar_status).grid(row=0, column=2, padx=5, pady=5)
tk.Radiobutton(win, text="Done", variable=status, value="Done", command=atualizar_status).grid(row=0, column=3, padx=5, pady=5)


cols = ("ID", "Título", "Status", "Criado em")
tree = ttk.Treeview(win, columns=cols, show="headings")
for col in cols:
    tree.heading(col, text=col)
tree.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

# Botão para atualizar lista completa
tk.Button(win, text="Mostrar todas", command=list_update).grid(row=5, column=0, columnspan=4, pady=10)

win.mainloop()

## END desktop_main.py ##