### Código base
Onde tudo começa!
task_manager_gui.py
```Python
# task_manager_gui.py

import tkinter as tk
from tkinter import messagebox
from task_manager_backend import TaskManagerBackend

class TaskManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Task Manager")

        self.backend = TaskManagerBackend()

        self.task_listbox = tk.Listbox(self.master, selectmode=tk.SINGLE)
        self.task_listbox.pack(pady=10)

        self.refresh_task_list()

        self.add_task_entry = tk.Entry(self.master)
        self.add_task_entry.pack(pady=5)

        add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        add_button.pack(pady=5)

        remove_button = tk.Button(self.master, text="Remove Task", command=self.remove_task)
        remove_button.pack(pady=5)

        complete_button = tk.Button(self.master, text="Complete Task", command=self.complete_task)
        complete_button.pack(pady=5)        

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.backend.tasks):
            task_text = f"{task['task']} {'(Completed)' if task['completed'] else ''}"
            self.task_listbox.insert(tk.END, task_text)    

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.backend.remove_task(selected_index[0])
            self.refresh_task_list()

    def complete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.backend.mark_task_completed(selected_index[0])
            self.refresh_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
```
task_manager_backend.py
```Python
# task_manager_backend.py

import json

class TaskManagerBackend:
    def __init__(self, data_file="tasks.json"):
        self.data_file = data_file
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.data_file, "r") as file:
                tasks = json.load(file)
        except FileNotFoundError:
            tasks = []
        return tasks

    def save_tasks(self):
        with open(self.data_file, "w") as file:
            json.dump(self.tasks, file, indent=2)    

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]["completed"] = True
            self.save_tasks()

```

### Tarefa 1
A ultima tarefa para que a aplicação seja lançada é a implementação da funcionalidade de adição de tarefas. Então...
Dev backend deve adicionar o bloco de código abaixo no arquivo `task_manager_backend.py`
```Python
def add_task(self, task):
    self.tasks.append({"task": task, "completed": False})
    self.save_tasks()
```

Dev Front deve adicionar o bloco de código abaixo no arquivo `task_manager_gui.py`
```Python
def add_task(self):
    new_task = self.add_task_entry.get()        
    self.backend.add_task(new_task)
    self.refresh_task_list()
    self.add_task_entry.delete(0, tk.END)
```

e as linhas abaixo dentro da função `__init__()`

```Python
add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
add_button.pack(pady=5)
```

### Tarefa 2
QA, o experiente membro da equipe, recebeu a missão de testar a aplicação antes de colocá-la em produção. Confiante em sua habilidade, ele fez os testes adicionando e removendo as tarefas e tudo parecia funcionar bem.

No GitHub somente de um pull resquest da branch de Test para a branch de Prod

### Tarefa 3
Funcionalidade implementada, agora o cliente começa a usar a aplicação.
Até que um dia foi notado que o bando de dados havia centenas de tarefas sem nome criadas.

### Tarefa 4
Novo membro na equipe... DevOps
Agora vamos implementar o arquivo YAML para executar o teste, gerar a documentação automaticamente e gerar um arquivo .exe.
```YAML
name: CI/CD

on:
  pull_request:
    branches:
      - Dev
      - Test
      - Prod
  push:
    branches:
      - Test

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

  test:
    runs-on: ubuntu-latest

    needs: build

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Run unit tests
        run: python -m unittest discover

  approve-dev:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Add 'approved' label
        run: |
          echo "label: approved" >> $GITHUB_EVENT_PATH

  approve-test:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Add 'approved' label
        run: |
          echo "label: approved" >> $GITHUB_EVENT_PATH

  build-artifact:
    runs-on: ubuntu-latest

    permissions: write-all

    needs: 
      - approve-dev
      - approve-test

    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8

      - name: Install pyinstaller
        run: pip install pyinstaller

      - name: Build artifact
        run: pyinstaller --onefile task_manager_gui.py

      - name: Upload artifact
        uses: actions/upload-artifact@v2
        with:
          name: task_manager_gui
          path: ./dist/task_manager_gui
```

### Tarefa 5
O QA deve..
Crie um arquivo chamado `test_task_manager.py`

```python
# test_task_manager.py

import unittest
import os
from task_manager_backend import TaskManagerBackend

class TestTaskManagerBackend(unittest.TestCase):
    def setUp(self):
        # Cria um arquivo de dados de teste exclusivo para cada teste
        self.test_data_file = f"test_tasks_{self._testMethodName}.json"
        self.backend = TaskManagerBackend(data_file=self.test_data_file)

    def tearDown(self):
        # Limpar o estado após cada teste
        self.backend = None

        # Remover o arquivo de dados de teste
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)

    def test_add_task(self):
        self.backend.add_task("Test Task 1")
        self.assertEqual(len(self.backend.tasks), 1)

    def test_add_empty_task(self):
        initial_tasks_count = len(self.backend.tasks)
        self.backend.add_task("")
        self.assertEqual(len(self.backend.tasks), initial_tasks_count)  # Deve manter a lista inalterada

    def test_remove_task(self):
        self.backend.add_task("Test Task 2")
        self.assertEqual(len(self.backend.tasks), 1)
        self.backend.remove_task(0)
        self.assertEqual(len(self.backend.tasks), 0)

    def test_mark_task_completed(self):
        self.backend.add_task("Test Task 3")
        self.backend.mark_task_completed(0)
        self.assertTrue(self.backend.tasks[0]["completed"])

if __name__ == "__main__":
    unittest.main()
```

### Tarefa 6
O PO solicita para que o o dev backend inclua a verificação para que tarefas com o nome vazio não sejam colocadas no banco de dados.
Dev Back deve... no aquivo `task_manager_backend.py` modificar a função de add tarefa como abaixo:
```python
def add_task(self, task):
    if task.strip():  # Verifica se a tarefa não está vazia após remover espaços em branco
        self.tasks.append({"task": task, "completed": False})
        self.save_tasks()
        return True
    else:
        return False
```
