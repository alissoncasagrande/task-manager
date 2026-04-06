'''
main.py
-------

This is the main entry point for the application on terminal. 
It initializes the application, sets up necessary configurations, and starts the main loop.
Author: Alisson Guindo Casagrande (https://github.com/AlissonCasagrande/task-manager)

Date: 2024-06-01
License: MIT License
'''

# Import necessary modules
import os
import sqlite3
from tasks import Task

DATABASE_FILE = 'task_manager.db'  # Define the database file name
# VARIABLES
clear_command = 'cls' if os.name == 'nt' else 'clear'
connection = None

# Initialize the application
def initialize_app():
    print("Initializing Task Manager Application...")
    # Additional initialization code can be added here
    global connection
    connection = setup_database()  # Ensure the database is set up before starting the main loop

def setup_database():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(DATABASE_FILE)
    return conn

def clear_terminal():
    os.system(clear_command)  # Clear the terminal screen
    return

def print_main_menu():
    clear_terminal() # os.system(clear_command) # Clear the terminal screen
    print("TASK MANAGER")
    print("--------------------------------------------------------------")
    print("1 - List Tasks")
    print("2 - Add Task")
    #print("3 - Edit Task")
    #print("4 - Delete Task")
    print("--------------------------------------------------------------")
    key = None
    while True:
        key = input('=> Choose 1, 2 or Q to exit: ').upper()  # Wait for user input
        if (key in ['1', '2', 'Q']):
            break
        else:
            print(f"Invalid input: {key}. Please press 1, 2 or Q to exit.")
    #end loop
    return key

def fill_fields(task=None):
    allowed_status = ['todo', 'in_progress', 'done']

    print("") #just jump 1 line
    title = input(f"New Title [leave blank to {'keep' if task else 'default'}]: ")
    description = input(f"New Description [leave blank to {'keep' if task else 'default'}]: ")

    print('Status must be one of: "todo", "in_progress", "done"')
    status = input(f"New Status [leave blank to {'keep' if task else 'default to todo'}]: ").lower()

    if status and (status not in allowed_status): #check if status is not None and is allowed
        print(f"Invalid status: {status}. Must be one of {allowed_status}.")
        return None

    if task:
        # UPDATE: altera atributos da instância existente
        task.title = title if title else task.title
        task.description = description if description else task.description
        task.status = status if status else task.status
        tt = task
    else:
        # CREATE: cria uma nova instância
        title = title if title else "Untitled"
        description = description if description else ""
        status = status if status else "todo"
        tt = Task(title=title, description=description, status=status)
    return tt

def delete_task(conn, task):
    if (task is not None):
        try:
            return task.delete_task(conn)
        except sqlite3.IntegrityError as e:
            print("Erro de integridade:", e)
            return None
        except sqlite3.Error as e:
            print("Erro geral do SQLite:", e)
            return None
    return None

def update_task(conn, task):
    ff = fill_fields(task) #returns a ff(Task) updated
    if (ff is not None):
        try:
            return ff.update_task(conn) #update database, parameters will not be necessary, filds are ok on ff.
        except sqlite3.IntegrityError as e:
            print("Erro de integridade:", e)
            return None
        except sqlite3.Error as e:
            print("Erro geral do SQLite:", e)
            return None
    return None

def add_task(conn):
    ff = fill_fields(None) #create a new ff(Task) with id = None
    if (ff is not None):
        try:
            return Task.create_task(conn, ff.title, ff.description, ff.status) #insert database, return tt (with id)
        except sqlite3.IntegrityError as e:
            print("Erro de integridade:", e)
            return None
        except sqlite3.Error as e:
            print("Erro geral do SQLite:", e)
            return None
    return None

def print_view_task(connection, task_id, task_list=None):
    tt = None
    for x in task_list:
        if task_id == x.id:
            tt = x
            break
    
    if tt is None:     
        print(f"Task with ID {task_id} not found in the task list.")
        return None
    else:
        clear_terminal()
        print("--------------------------------------------------------------")
        print("Task Details:")
        print("--------------------------------------------------------------")
        print(f"ID: {tt.id} | Created: {tt.create_date} | Updated: {tt.updated_date}")
        print(f"Status: {tt.status}")
        print(f"Title: {tt.title}")
        print(f"Description: {tt.description}")
        print("--------------------------------------------------------------")
        key = None
        while True:
            print("Press * to go back to the main menu.")
            print("Press 1 to edit the task or 2 to delete the task.")
            key = input('=> Press * to exit: ')  # Wait for user input
            if (key == '*'):
                print("Returning to main menu...")
                input("") # Wait for user input before returning to the main menu
                break
            elif (key == '1'):
                print("Updating Task...")
                tt = update_task(connection,tt)
                input("Task updated successfully! [press Enter]")
                if (tt is None):
                    input("Error updating task...[press Enter]")
                break
            elif (key == '2'):
                a = input("It will delete this task. Are you sure? (Y/N): ")               
                if (a.upper() == 'Y'):
                    tt = delete_task(connection, tt)
                    input("Task deleted successfully! [press Enter]")
                    if (tt is None):
                        input("Error deleting task...[press Enter]")
                    break
            else:
                print(f"Invalid input: {key}. Please press * to exit.")
        #end loop
        # *think better about this return
        return key

def list_all_tasks(connection):
    tlist = Task.list_tasks(connection)
    clear_terminal()
    print("Task List:")
    print("--------------------------------------------------------------")

    if (tlist is None or len(tlist) == 0):
        print("No tasks found.")
        return []
    else:
        for t in tlist:
            print(f"ID: {t.id}, Title: {t.title}, Status: {t.status}, Created: {t.create_date}, Updated: {t.updated_date}")
    return tlist

# Main loop of the application
def main_loop():
    try:
        connection = setup_database()
    except sqlite3.Error as e:
        print(f"Error setting up database: {e}")
        print("Please if you already ran setup_db.py, make sure the database file is in the same directory as this script.")
        return

    # Additional main loop code can be added here
    while True:
        key=print_main_menu()
        # Example: Check for a specific key press to exit the application
        c = '*' # variable to control the flow of the application, for example, to return to the main menu after viewing a task'
        if key in ['q', 'Q']:
            print("Exiting Task Manager Application...")
            break
        elif key == '1': # LIST TASKS
            allTasks = list_all_tasks(connection)
            print("--------------------------------------------------------------")
            if allTasks is None or len(allTasks) == 0:
                input ("Press [Enter] key to return to the main menu")
            else:
                while True:
                    print("Press * to return to the main menu, or")
                    c = input("Inform the ID of the task to view details: ")
                    if (c == '*'): break
                    if c != '*' and c.isdigit() and len(allTasks) > 0:
                        print_view_task(connection, int(c), allTasks)
                        break
        elif key == '2':
            print("Adding a new task...")
            t = add_task(connection)
            if (t is None):
                input("Error adding task...[press Enter]")
            else:
                input(f"Task {t.id} added successfully!  [press Enter]")

        # just to see what is happening
        print(f"You pressed: {key}. Processing input...")

# ----- STARTS HERE ------------
if __name__ == "__main__":
    initialize_app()
    main_loop()
# END SCRIPT


##END main.py