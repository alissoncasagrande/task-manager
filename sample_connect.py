import sqlite3

# 1. Conecta ao banco de dados (se o arquivo não existir, ele será criado)
conexao = sqlite3.connect('meu_database.db')

# 2. Cria um cursor para executar comandos SQL
cursor = conexao.cursor()

# 3. Cria uma tabela (exemplo: uma tabela de usuários)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        idade INTEGER
    )
''')

# sqlite3.OperationalError: table usuarios already exists


# 2. Verifica manualmente se ela existe agora
'''cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
tabela_existe = cursor.fetchone() # Retorna uma tupla se existir, ou None se não existir'''

# 4. Salva as alterações (commit) e fecha a conexão
conexao.commit()
conexao.close()

print("Banco de dados e tabela criados com sucesso!")