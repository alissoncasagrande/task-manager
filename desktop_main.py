'''
desktop_main.py
-------

This is the desktop_main entry point for the application on GUI Desktop.
It initializes the application, sets up necessary configurations, and starts the main loop.
Author: Alisson Guindo Casagrande (https://github.com/AlissonCasagrande/task-manager)
Date: 2024-06-01
License: MIT License
'''

import sqlite3
import tkinter  as tk
from tkinter    import ttk
from tkinter    import messagebox
from tasks      import Task
from datetime   import datetime

def edit_task():
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])['values']
        task_id = values[0]
        print("Editar tarefa:", task_id)
        # aqui você pode abrir uma janela Toplevel para editar

def exclude_task():
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])['values']
        task_id = values[0]

        # Confirmação antes de excluir
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete task {task_id}?")
        if not confirm: #if not YES, return 
            print("Task deletion canceled")
            return  

        # if the user choose yes, 
        # get the task by id and delete it
        task2del = Task.get_task_by_id(conn, task_id)
        if (task2del is not None):
            try:
                print("Excluir tarefa:", task_id, task2del.title)
                task2del.delete_task(conn)

            except sqlite3.IntegrityError as e:
                print("Erro de integridade:", e)
                messagebox.showinfo("Success", f"Task {task_id} deleted successfully!")
            except sqlite3.IntegrityError as e:
                messagebox.showerror("Integrity Error", f"Integrity error: {e}")
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"SQLite error: {e}")

        #update the table list on screen.
        status_filter()

def status_filter():
    print("Status selecionado:", status.get())
    # limpa a tabela
    for item in tree.get_children():
        tree.delete(item)
    # busca tarefas do banco
    tasks = Task.list_tasks(conn)
    if status.get() is not None:
        selected = [t for t in tasks if t.status == status.get()]

        for t in selected:
            #Parse the string into a date variable
            update_dt = datetime.strptime(t.updated_date, "%Y-%m-%d %H:%M:%S") 
            #format the date for an output format (we can manipulate these formats later for others languages)
            update_str = update_dt.strftime("%d/%m/%Y %H:%M:%S")
            tree.insert("", "end", values=(t.id, t.title, t.status, update_str))

    return


# main #####
conn = sqlite3.connect("task_manager.db")

#create the window instance
win = tk.Tk()
win.title("Task Manager")

#variável que guarda a escolha
status = tk.StringVar(value=Task.valid_status[0])

tk.Label(win, text="Status:").grid(row=0, column=0,padx=5,pady=5)

tk.Radiobutton(win, text="Todo", variable=status, value=Task.valid_status[0], command=status_filter).grid(row=0, column=1, padx=5, pady=5)
tk.Radiobutton(win, text="In-progress", variable=status, value=Task.valid_status[1], command=status_filter).grid(row=0, column=2, padx=5, pady=5)
tk.Radiobutton(win, text="Done", variable=status, value=Task.valid_status[2], command=status_filter).grid(row=0, column=3, padx=5, pady=5)

frame_table=tk.Frame(win)
frame_table.grid(row=4,column=0, columnspan=4,padx=5, pady=5)

cols = ("id", "title", "status", "updated")
tree = ttk.Treeview(frame_table, columns=cols, show="headings",selectmode="browse")

tree.heading("id", text="ID")
tree.column("id", width=30,anchor="center")
tree.heading("title", text="Title")
tree.column("title", width=200, anchor="w")
tree.heading("status", text="Status")
tree.column("status", width=100, anchor="center")
tree.heading("updated", text="Updated")
tree.column("updated", width=150, anchor="center")
#tree.bind("<Double-1>", lambda e: print(tree.item(tree.selection()[0])['values'][1]))

tree.pack(side="left", fill="both", expand=True)
#tree.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

verticalSB = tk.Scrollbar(frame_table,orient="vertical",command=tree.yview)
tree.configure(yscrollcommand=verticalSB.set)
#verticalSB.grid(row=4, column=5, sticky="ns")
verticalSB.pack(side="right", fill="y")


# Label para mostrar descrição
tk.Label(win, text="Description:").grid(row=6, column=0, sticky="w", padx=5, pady=(5,0))

# Criar um frame para manter o texto e a barra de rolagem do texto junto.
frame_desc = tk.Frame(win)
frame_desc.grid(row=7, column=0, columnspan=3, sticky="w", padx=5, pady=(0,5))

# Campo para conter o valor da descricao
desc_text = tk.Text(frame_desc, height=5, width=40, wrap="word")
desc_text.pack(side="left", fill="both", expand=True)

scroll_desc = tk.Scrollbar(frame_desc, orient="vertical", command=desc_text.yview)
scroll_desc.pack(side="right", fill="y")

desc_text.configure(yscrollcommand=scroll_desc.set)



#load of the table (first time).
status_filter()

# Botão para atualizar e deletar, quando selecionado

frame_buttons = tk.Frame(win)
frame_buttons.grid(row=7, column=3, sticky="wn", padx=5, pady=5)

btn_update = tk.Button(frame_buttons, text="Update", command=edit_task)
btn_update.pack(side="top", padx=5, pady=5)

btn_delete = tk.Button(frame_buttons, text="Delete", command=exclude_task)
btn_delete.pack(side="top", padx=5, pady=5)


win.mainloop()

# end main #####

## END desktop_main.py ##