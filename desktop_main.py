'''
desktop_main.py
-------

This is the desktop_main entry point for the application on GUI Desktop.
It initializes the application, sets up necessary configurations, and starts the main loop.
Author: Alisson Guindo Casagrande (https://github.com/AlissonCasagrande/task-manager)

Date: 2026-04-01
License: MIT License
'''

import sqlite3
import tkinter  as tk
from tkinter    import ttk
from tkinter    import messagebox
from tasks      import Task
from datetime   import datetime
from task_window import TaskFormWindow


def edit_task():
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])['values']
        task_id = values[0]
        print("Editar tarefa:", task_id)
        #Open a secondary window for editing task.
        task_window = TaskFormWindow(win, conn, task_id=task_id, on_success_do=status_filter)
        task_window.focus_set() # bring the window to front

        #now updating on directly on the TaskFormWindow class, implemented a callback function.
        #status_filter() 

def exclude_task():
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])['values']
        task_id = values[0]

        # Confirmação antes de excluir
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete task {task_id}?")
        if not confirm: #if not YES, return 
            print("Task deletion canceled") #printing on terminal, for debug purpose
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
    try:
        current_status = status.get()
        print("Status selecionado: ", current_status)
        # clear the "tree" table
        for item in tree.get_children():
            tree.delete(item)
        
        # searche for tasks on database (sql)
        tasks = Task.list_tasks(conn)

        if (current_status == "All") or (not current_status):
            selected = tasks
        else:
            selected = [t for t in tasks if t.status == current_status]

        for t in selected:
            try: #try format the date, if an invalid value an exception will be raized.
                update_dt = datetime.strptime(t.updated_date, "%Y-%m-%d %H:%M:%S") 
                update_str = update_dt.strftime("%d/%m/%Y %H:%M:%S")
            except (ValueError, TypeError):
                update_str = "N/A"

            tree.insert("", "end", values=(t.id, t.title, t.status, update_str))
    except Exception as e:
        messagebox.showerror("Database Error", f"Error while listing tasks: {e}")
        print("Error listing tasks: ", e)

## end status_filter

def on_tree_select(event):
    try:
        selected = tree.selection()
        if (not selected): return
        
        item = tree.item(selected[0])
        task_id = item['values'][0]
        
        # Search the task (all fields) on database (use the description, that is not on the "tree" table yet)
        tt = Task.get_task_by_id(conn, task_id)

        desc_content = ""
        if tt:
            #if tt.description: desc_content = tt.description
            
            #i am just trying use pythonic code and learn it
            #desc_content = tt.description if tt.description else ""
            desc_content = tt.description or ""
        else:
            desc_content = "[Task not found] - No description available"

        desc_text.config(state="normal") # can write 
        desc_text.delete("1.0", "end") #clear the field
        desc_text.insert("1.0", desc_content) #write into field
        desc_text.config(state="disabled") # can not write anymore

    except Exception as e:
        #pass
        #messagebox.showerror("Error", f"Error on selection: {e}") #user will not need see this..
        print(f"Erro na seleção: {e}") #debug print.  other error in description field.
## end def on_tree_select

def open_new_task_window():
    #Open a secondary window for editing task.
    task_window = TaskFormWindow(win, conn, task_id=None, on_success_do=status_filter)
    task_window.focus_set() # bring the window to front
## end open_new_task_window


## main ##  --------------------------------------------------  ##
conn = sqlite3.connect("task_manager.db")

#create the window instance
win = tk.Tk()
win.title("Task Manager")

# Button "New" --
btn_new = tk.Button(win, text="+ New Task", command=open_new_task_window)
btn_new.grid(row=0, column=0, padx=10, pady=10, sticky='w')

# STATUS ---
frame_start = tk.Frame(win)
frame_start.grid(row=0, column=1, columnspan=4, sticky='e', padx=20, pady=10)

status = tk.StringVar(value=Task.valid_status[0])
tk.Label(frame_start, text="Status:").pack(side='left')

tk.Radiobutton(frame_start, text="Todo", variable=status, value=Task.valid_status[0], command=status_filter).pack(side='left')
tk.Radiobutton(frame_start, text="In-progress", variable=status, value=Task.valid_status[1], command=status_filter).pack(side='left')
tk.Radiobutton(frame_start, text="Done", variable=status, value=Task.valid_status[2], command=status_filter).pack(side='left')

"""
tk.Label(win, text="Status:").grid(row=0, column=1,padx=5,pady=10)

tk.Radiobutton(win, text="Todo", variable=status, value=Task.valid_status[0], command=status_filter).grid(row=0, column=2, padx=5, pady=10)
tk.Radiobutton(win, text="In-progress", variable=status, value=Task.valid_status[1], command=status_filter).grid(row=0, column=3, padx=5, pady=10)
tk.Radiobutton(win, text="Done", variable=status, value=Task.valid_status[2], command=status_filter).grid(row=0, column=4, padx=5, pady=10)
"""

# Table ---
frame_table=tk.Frame(win)
frame_table.grid(row=4,column=0, columnspan=4,padx=5, pady=5)

cols = ("id", "title", "status", "updated")
tree = ttk.Treeview(frame_table, columns=cols, show="headings",selectmode="browse")
tree.bind("<<TreeviewSelect>>", on_tree_select) #action when click over a line of the table "tree"

tree.heading("id", text="ID")
tree.column("id", width=30,anchor="center")
tree.heading("title", text="Title")
tree.column("title", width=200, anchor="w")
tree.heading("status", text="Status")
tree.column("status", width=100, anchor="center")
tree.heading("updated", text="Updated")
tree.column("updated", width=150, anchor="center")

#debug print
#tree.bind("<Double-1>", lambda e: print(tree.item(tree.selection()[0])['values'][1]))

tree.pack(side="left", fill="both", expand=True)
#tree.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

verticalSB = tk.Scrollbar(frame_table,orient="vertical",command=tree.yview)
tree.configure(yscrollcommand=verticalSB.set)
#verticalSB.grid(row=4, column=5, sticky="ns")
verticalSB.pack(side="right", fill="y")


# Description ---
tk.Label(win, text="Description:").grid(row=6, column=0, sticky="w", padx=5, pady=(5,0))

# A frame with Description field and scrollbar
frame_desc = tk.Frame(win)
frame_desc.grid(row=7, column=0, columnspan=3, sticky="w", padx=5, pady=(0,5))

# Field of description value
desc_text = tk.Text(frame_desc, height=5, width=40, wrap="word")
desc_text.pack(side="left", fill="both", expand=True)

# description scrollbar
scroll_desc = tk.Scrollbar(frame_desc, orient="vertical", command=desc_text.yview)
scroll_desc.pack(side="right", fill="y")
desc_text.configure(yscrollcommand=scroll_desc.set)


# Buttons - Update and Delete ---
frame_buttons = tk.Frame(win)
frame_buttons.grid(row=7, column=3, sticky="wn", padx=5, pady=5)

btn_update = tk.Button(frame_buttons, text="Update", command=edit_task)
btn_update.pack(side="top", padx=5, pady=5)

btn_delete = tk.Button(frame_buttons, text="Delete", command=exclude_task)
btn_delete.pack(side="top", padx=5, pady=5)


#load of the table (first time).
status_filter()

# start the main loop
win.mainloop()
## end main #####

## END desktop_main.py ##