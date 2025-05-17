class TodoList:

    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append({'task': task, 'completed': False})

    def complete_task(self,task):
        for t in self.tasks:
            if t['task'] == task and not t['completed']:
                t['completed'] = True
                return True
        return False

    def get_active_tasks(self):
        return [t['task'] for t in self.tasks if not t['completed']]

    def get_completed_tasks(self):
        return [t['task'] for t in self.tasks if t['completed']]
