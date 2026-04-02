'''
tasks.py
-----------

This module defines the Task class, which represents a task in the task management system.
The Task class includes methods for creating, listing, retrieving, updating, and deleting tasks from the SQLite database.
Main responsibilities:
- Define the Task class with attributes corresponding to the database schema.
- Implement class methods for CRUD operations that interact with the database.  
- Ensure that the Task class can be easily used by other parts of the application to manage tasks.
This module relies on the database schema defined in setup_db.py, so ensure that the database is set up before using this class.
'''

from datetime import datetime

class Task:
    def __init__(self, id=None, title="", description="", status="todo", create_date=None, updated_date=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.create_date = create_date
        self.updated_date = updated_date

    # Métodos de classe (CRUD geral)
    @classmethod
    def create_task(cls, conn, title, description, status="todo"):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO TASKS (title, description, status) VALUES (?, ?, ?)", (title, description, status))
        conn.commit()
        task_id = cursor.lastrowid # lastrowid retorna o ID da última linha inserida

        cursor.execute("SELECT id, title, description, status, created_date, updated_date FROM TASKS WHERE id=?", (task_id,))
        row = cursor.fetchone()
        # insere no banco e retorna objeto Task
        return cls(id=row[0],title=row[1],description=row[2],status=row[3],create_date=row[4],updated_date=row[5])

    @classmethod
    def list_tasks(cls, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, status, created_date, updated_date FROM TASKS")
        rows = cursor.fetchall()
        tasks = []        
        for row in rows:
            task = cls(id=row[0], title=row[1], description=row[2],
                       status=row[3], create_date=row[4], updated_date=row[5])
            tasks.append(task)
        # retorna uma lista de objetos Task
        return tasks

    @classmethod
    def get_task_by_id(cls, conn, task_id):
        t = None # cria um objeto Task vazio para retornar caso não encontre a tarefa
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, description, status, created_date, updated_date FROM TASKS WHERE id = ?", (task_id,))
        row = cursor.fetchone() # fetchone() retorna uma tupla com os dados da linha, ou None se não encontrar
        if row: # se encontrou a tarefa, preenche o objeto Task com os dados do banco
            t = cls(id=row[0], title=row[1], description=row[2], status=row[3], create_date=row[4], updated_date=row[5])
        # retorna um único objeto Task
        return t

    # Métodos de instância (manipulação de uma linha específica)
    def update_task(self, conn, title=None, description=None, status=None):
        if self.id is None:
            raise ValueError("Task ID is required to update a task.")
            
        cursor = conn.cursor()
        # Atualiza os campos da tarefa apenas se os novos valores forem fornecidos
        new_title = title if title is not None else self.title
        new_description = description if description is not None else self.description
        new_status = status if status is not None else self.status
        new_updated_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE TASKS SET title = ?, description = ?, status = ?, updated_date = ? WHERE id = ?", (new_title, new_description, new_status, new_updated_date, self.id))
        conn.commit()

        if cursor.rowcount > 0: # rowcount retorna o número de linhas afetadas pela última operação
            self.title = new_title
            self.description = new_description
            self.status = new_status
            self.updated_date = new_updated_date

        # atualiza os campos dessa tarefa no banco
        return self

    def delete_task(self, conn):
        ok = False
        if (self.id is None ):
            raise ValueError("Task ID is required to delete a task.")

        cursor = conn.cursor()
        cursor.execute("DELETE FROM TASKS WHERE id = ?", (self.id,))
        conn.commit()
        ok = cursor.rowcount > 0 # rowcount retorna o número de linhas afetadas pela última operação
        # remove essa tarefa do banco
        return ok
        
    # Método de representação para facilitar a visualização dos objetos Task
    # __repr__ formata saida para usar para debug ou printar a tarefa
    def __repr__(self):
        return (f"Task(id={self.id}, title='{self.title}', "
                f"status='{self.status}', created={self.create_date}, "
                f"updated={self.updated_date})")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "create_date": self.create_date,
            "updated_date": self.updated_date
        }
    
# -- END CLASS Task

##END tasks.py