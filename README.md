# TASK MANAGER Project
A simple task manager built with Python and SQL Database.

## Description
This project is a simple task manager that stores tasks in a relational database (initially SQLite).  
It allows users to create, view, update, and delete tasks through a basic terminal interface.

## How to Install and Run
*Explain commands to setup and run the project in details*
1. Clone this repository:
   ```bash
   git clone https://github.com/AlissonCasagrande/task-manager.git
   cd task-manager
   ```
2. Create the database by running:
   ```
   python setup_db.py
   ```
3. Start the application:
   ```
   python main.py
   ```
### Requirements
- Python 3.x installed on your system.
- Standard library modules:
   - sqlite3
   - os
   - datetime

> Note: All modules listed above are part of Python's standard library, no extra installation required.

## 🖥️ Como usar (CLI)
A versão atual roda no terminal.  
Fluxo básico:
1. Inicie o programa com `python main.py`
2. Escolha no menu principal:
   - `1` → Listar tarefas
   - `2` → Adicionar tarefa
   - `Q` → Sair
3. Dentro de uma tarefa, você pode editar ou excluir.

## 📸 Screenshots (CLI)

### Menu principal
![Menu principal](docs/img/cli/terminal_menu.png)

### Adicionar tarefa
![Add Task](docs/img/cli/terminal_insert.png)

### Listar tarefas
![List Tasks](docs/img/cli/terminal_list.png)

### Visualizar detalhes
![View Task](docs/img/cli/terminal_details.png)

### Editar tarefa
![Edit Task](docs/img/cli/terminal_update_task.png)

### Deletar tarefa
![Delete Task](docs/img/cli/terminal_delete_task.png)

---

## Interfaces disponíveis
- **CLI (Terminal)** → já implementada (prints acima)
- **Desktop GUI (Tkinter/PyQt)** → em desenvolvimento
- **Mobile (Kivy)** → planejada
- **Web (Django/Flask)** → planejada

## 🚀 Roadmap
- [x] Versão inicial em CLI (terminal)
- [ ] Interface Desktop (Tkinter/PyQt)
- [ ] Interface Web com Django
- [ ] API REST para integração
- [ ] Frontend moderno (React/Vue/Angular)
- [ ] Deploy em AWS (EC2, RDS, S3)

## Credits
[Alisson Guindo Casagrande] (https://github.com/AlissonCasagrande) (2026)

## Contribute
Contributions are welcome!
Please check the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines.

## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Repo size](https://img.shields.io/github/repo-size/AlissonCasagrande/task-manager)
![Last commit](https://img.shields.io/github/last-commit/AlissonCasagrande/task-manager)
![Issues](https://img.shields.io/github/issues/AlissonCasagrande/task-manager)
