
"""
Модульные тесты
"""
import unittest
import time
from time_tracker import TimeTracker

class TestTimeTracker(unittest.TestCase):
    def setUp(self):
        self.tracker = TimeTracker()
        self.task_id = 101

    def test_start_and_stop_timer(self):
        """Тест базового запуска и остановки таймера."""
        self.assertTrue(self.tracker.start_timer(self.task_id))
        time.sleep(1) # Имитация работы
        self.assertTrue(self.tracker.stop_timer(self.task_id))
        
        total_time = self.tracker.get_total_time(self.task_id)
        self.assertGreaterEqual(total_time.total_seconds(), 1.0)

    def test_prevent_double_start(self):
        """Тест валидации: нельзя запустить два таймера на одну задачу."""
        self.tracker.start_timer(self.task_id)
        result = self.tracker.start_timer(self.task_id)
        self.assertFalse(result) # Должен вернуть False

    def test_stop_non_existent_timer(self):
        """Тест валидации: нельзя остановить несуществующий таймер."""
        result = self.tracker.stop_timer(999)
        self.assertFalse(result)

    def test_report_generation_format(self):
        """Тест генерации отчета и проверки формата ЧЧ:ММ:СС."""
        self.tracker.start_timer(1)
        time.sleep(1)
        self.tracker.stop_timer(1)
        
        report = self.tracker.generate_report()
        self.assertIn(1, report)
        self.assertRegex(report[1], r"\d{2}:\d{2}:\d{2}") # Проверка регулярным выражением

if __name__ == "__main__":
    unittest.main(verbosity=2)