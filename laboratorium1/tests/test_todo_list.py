import unittest
from laboratorium1.src.todo_list import TodoList

class TestTodoList(unittest.TestCase):
    def setUp(self):
        self.todo = TodoList()

    def test_add_task(self):
        self.todo.add_task("Buy milk")
        self.assertIn("Buy milk", self.todo.get_active_tasks())

    def test_complete_task(self):
        self.todo.add_task("Buy milk")
        self.assertTrue(self.todo.complete_task("Buy milk"))
        self.assertIn("Buy milk", self.todo.get_completed_tasks())
        self.assertNotIn("Buy milk", self.todo.get_active_tasks())

    def test_complete_nonexistent_task(self):
        self.assertFalse(self.todo.complete_task("Go to the gym"))

    def test_get_active_tasks(self):
        self.todo.add_task("Task 1")
        self.todo.add_task("Task 2")
        self.assertEqual(self.todo.get_active_tasks(), ["Task 1", "Task 2"])

    def test_get_completed_tasks(self):
        self.todo.add_task("Task 1")
        self.todo.complete_task("Task 1")
        self.assertEqual(self.todo.get_completed_tasks(), ["Task 1"])

    def tearDown(self):
        pass