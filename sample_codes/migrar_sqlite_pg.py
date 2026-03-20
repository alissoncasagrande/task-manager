python
import sqlite3
import psycopg2

# 1. Conectar ao SQLite (Origem)
conn_sqlite = sqlite3.connect('tasks.db')
cursor_sqlite = conn_sqlite.cursor()

# 2. Conectar ao RDS Postgres (Destino)
# Dica: Pegue o Endpoint no console da AWS
conn_rds = psycopg2.connect(
    host="seu-endpoint.rds.amazonaws.com",
    database="seu_db",
    user="seu_usuario",
    password="sua_password",
    port="5432"
)
cursor_rds = conn_rds.cursor()

# 3. Ler dados do SQLite
cursor_sqlite.execute("SELECT id, titulo, descricao, status FROM tasks")
rows = cursor_sqlite.fetchall()

# 4. Inserir no Postgres (Onde seu conhecimento de SQL brilha!)
for row in rows:
    cursor_rds.execute(
        "INSERT INTO tasks (id, titulo, descricao, status) VALUES (%s, %s, %s, %s)",
        row
    )

# 5. Salvar e fechar
conn_rds.commit()
cursor_sqlite.close()
cursor_rds.close()
print("Migração concluída com sucesso!")