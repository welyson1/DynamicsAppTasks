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