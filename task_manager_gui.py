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
        
        remove_button = tk.Button(self.master, text="Remove Task", command=self.remove_task)
        remove_button.pack(pady=5)

        complete_button = tk.Button(self.master, text="Complete Task", command=self.complete_task)
        complete_button.pack(pady=5)   

        add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        add_button.pack(pady=5)     

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

    def add_task(self):
        new_task = self.add_task_entry.get()        
        self.backend.add_task(new_task)
        self.refresh_task_list()
        self.add_task_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()