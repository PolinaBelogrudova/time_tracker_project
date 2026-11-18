
"""
основа для интеграции модуля учета времени.
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Status(Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class Task:
    def __init__(self, task_id: int, title: str, description: str, priority: Priority, due_date: datetime):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.status = Status.TODO

    def __str__(self):
        return f"Task #{self.task_id}: '{self.title}' [{self.status.value}]"

class TaskManager:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_task_id = 1

    def create_task(self, title: str, description: str, priority: Priority, due_date: datetime) -> Task:
        task = Task(self.next_task_id, title, description, priority, due_date)
        self.tasks[self.next_task_id] = task
        self.next_task_id += 1
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.tasks.get(task_id)