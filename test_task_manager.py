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
  
