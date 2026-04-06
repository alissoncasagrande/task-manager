'''
task_window.py
-------

This module provides the TaskFormWindow class, which handles a secondary window
for creating new tasks or updating existing ones within the Task Manager.

Author: Alisson Guindo Casagrande (https://github.com/AlissonCasagrande/task-manager)
Date: 2026-04-06
License: MIT License
'''

import sqlite3
import tkinter  as tk
from tkinter    import ttk
from tkinter    import messagebox
from tasks      import Task
from datetime   import datetime

class TaskFormWindow(tk.Toplevel):
    def __init__(self, parent, conn, task_id=None, on_success_do=None):
        super().__init__(parent)
        self.withdraw() #keep the window invisible, to not blink on wrong place.

        #parameters
        self.conn = conn
        self.task_id = task_id
        self.on_success_do = on_success_do
        
        # Adjust the window title
        self.title("Edit Task" if self.task_id else "New Task")
        
        # wait for the main window update before handle with it
        parent.update_idletasks() 
        main_x = parent.winfo_x()
        main_y = parent.winfo_y()

        # set position of the secondary window relative to the main one
        self.geometry(f"+{main_x + 50}+{main_y + 50}")

        # Be a modal window.
        self.transient(parent)
        self.grab_set()

        self._draw_mywin()

        # if editing load the data..
        if self.task_id is not None:
            self._load_task_data()

        self.deiconify() #show the window now.

    ## end init

    def _draw_mywin(self):
        # lets put everything on the this secondary window..
        self.title("Task Details")
        '''
        tk.Label(self, text="Title:").pack(padx=10, pady=5)
        self.ent_title = tk.Entry(self)
        self.ent_title.pack(padx=10, pady=5)

        # O botão que chamará a lógica de salvar
        btn_text = "Save Changes" if self.task_id else "Create Task"
        self.btn_save = tk.Button(self, text=btn_text, command=self._save_task)
        self.btn_save.pack(pady=10)
        '''

        # adjust the title of the window
        self.title("Update Task" if self.task_id else "Create New Task")

        # create a metadata variable (for updating)
        if self.task_id:
            meta_frame = tk.LabelFrame(self, text=" Info ", padx=10, pady=5)
            meta_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
            
            # a label for ID and the Created/Updated data
            self.lbl_info = tk.Label(meta_frame, text="Loading metadata...", font=("Arial", 8, "italic"))
            self.lbl_info.pack(anchor="w")

        # create editable fields..
        # 1. Title
        tk.Label(self, text="Title:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.ent_title = tk.Entry(self, width=45)
        self.ent_title.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # 2. Status
        tk.Label(self, text="Status:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.combo_status = ttk.Combobox(self, values=Task.valid_status, state="readonly")
        self.combo_status.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.combo_status.set(Task.valid_status[0]) # Valor padrão "Todo"

        # 3. Description
        tk.Label(self, text="Description:").grid(row=3, column=0, padx=10, pady=5, sticky="ne")
        self.txt_desc = tk.Text(self, width=34, height=6, wrap="word")
        self.txt_desc.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # buttons..
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=15)

        # 4. Save button.
        self.btn_save = tk.Button(btn_frame, text="Save Task", width=15, command=self._save_task)
        self.btn_save.pack(side="left", padx=5)

        # 5. Cancel button
        self.btn_cancel = tk.Button(btn_frame, text="Cancel", width=10, command=self.destroy)
        self.btn_cancel.pack(side="left", padx=5)

    ## end _draw_mywin

    def _save_task(self):
        # bring the data from the form fields
        new_title = self.ent_title.get().strip()
        new_status = self.combo_status.get()
        # get=linha.coluna de inicio, end (final do conteudo com quebra de linha). -1c (para de ler antes do ultimo caractere)
        new_desc = self.txt_desc.get("1.0", "end-1c").strip()

        # check the constraints, before the database..
        if not new_title:
            messagebox.showwarning("Validation Error", "The Title field cannot be empty.")
            return

        try:
            if self.task_id: #  UPDATE
                task_to_update = Task.get_task_by_id(self.conn, self.task_id)
                if task_to_update is not None:
                    task_to_update.title = new_title
                    task_to_update.status = new_status
                    task_to_update.description = new_desc
                    task_to_update.update_task(self.conn) #using the SQL Update from the Task class
                    messagebox.showinfo("Success", f"Task {self.task_id} updated successfully!")
                    
                    #reload the main window list
                    if (self.on_success_do is not None): self.on_success_do()
            else:  # INSERT (NEW)
                # using the SQL Insert from the Task class
                new_task = Task.create_task(self.conn, title=new_title, description=new_desc, status=new_status)
                messagebox.showinfo("Success", "New task created successfully!")
                #reload the main window list
                if (self.on_success_do is not None): self.on_success_do()

            self.destroy() #close this window

        except sqlite3.IntegrityError as e:
            messagebox.showerror("Integrity Error", f"Integrity error: {e}")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"SQLite error: {e}")
        except Exception as e:
            messagebox.showerror("Generic Error", f"An error occurred: {e}")
    ## end save_task

    def _load_task_data(self):
        try:
            tt = Task.get_task_by_id(self.conn, self.task_id) # connect and load the Task from database (slq)

            if tt is not None:
                # format and load the metadata (Label)
                def fmt(dt_str): #format date
                    if not dt_str: return "N/A"
                    dt=datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                    return dt.strftime("%d/%m/%Y %H:%M:%S")
                
                info_text = f"ID: {tt.id}  |  Created: {fmt(tt.create_date)}  |  Updated: {fmt(tt.updated_date)}"
                self.lbl_info.config(text=info_text)

                self.ent_title.delete(0, "end") # Limpa antes de inserir
                self.ent_title.insert(0, tt.title)
                self.combo_status.set(tt.status)
                self.txt_desc.delete("1.0", "end") # Limpa antes de inserir
                self.txt_desc.insert("1.0", tt.description)
            else:
                messagebox.showerror("Error", f"Task with ID {self.task_id} not found.")
                self.destroy()

        except Exception as e:
            messagebox.showerror("Database Error", f"Could not load task data: {e}")
            self.destroy()

    ## end load_task_data

