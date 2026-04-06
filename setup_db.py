"""
setup_db.py
-----------

This script is responsible for initializing the SQLite database used by the Task-Manager project.
It creates a new database file (task_manager.db) from scratch and defines the required tables.

Main responsibilities:
- Establish a connection to the SQLite database.
- Create tables and other structures needed for the application.
- Ensure the database schema is ready before the application runs.

This script should be executed once during project setup, or whenever the database needs to be reset.
Date: 2026-04-01
License: MIT License
"""

import sqlite3

# 1. Conect to database (if the file doesn't exist, it will be created)
conexao = sqlite3.connect('task_manager.db')

# 2. Create a cursor to execute SQL commands
cursor = conexao.cursor()
#id, title, description, status, create_date


# 3. Cria uma tabela (exemplo: uma tabela de usuários)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS TASKS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'todo' CHECK(status IN ('todo', 'in_progress', 'done')),
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# try except sqlite3.OperationalError: table usuarios already exists 
# (not necessary, using IF NOT EXISTS in the CREATE TABLE statement already handles this case)

# 2. Check manually if it exists now. Will not be necessary now.
# If we want to check if the table was created successfully, we can run a query like this:
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
# tabela_existe = cursor.fetchone() # Retorna uma tupla se existir, ou None se não existir

# 4. Save the changes (commit) and close the connection
conexao.commit()
conexao.close()

print("Database and structures created successfully!")

##END setup_db.py