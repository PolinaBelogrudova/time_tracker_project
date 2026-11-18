
"""
Модуль учёта времени 
"""
import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class TimeEntry:
    """Класс, представляющий одну сессию работы над задачей."""
    def __init__(self, task_id: int, start_time: datetime):
        self.task_id = task_id
        self.start_time = start_time
        self.end_time: Optional[datetime] = None
        self.is_active = True

    def stop(self):
        """Останавливает запись и фиксирует время окончания."""
        if self.is_active:
            self.end_time = datetime.now()
            self.is_active = False

    def get_duration(self) -> timedelta:
        """Возвращает длительность сессии (учитывает активные таймеры)."""
        if self.is_active:
            return datetime.now() - self.start_time
        return self.end_time - self.start_time


class TimeTracker:
    """Менеджер учета времени, интегрируемый с TaskManager."""
    def __init__(self):
        self.active_timers: Dict[int, TimeEntry] = {}
        self.completed_entries: List[TimeEntry] = []

    def start_timer(self, task_id: int) -> bool:
        """Требование 1: Старт таймера для задачи."""
        if task_id in self.active_timers:
            print(f" Таймер для задачи #{task_id} уже запущен!")
            return False # Доп. функция: защита от дублирования
        
        self.active_timers[task_id] = TimeEntry(task_id, datetime.now())
        print(f" Таймер для задачи #{task_id} запущен.")
        return True

    def stop_timer(self, task_id: int) -> bool:
        """Требование 1: Остановка таймера для задачи."""
        if task_id not in self.active_timers:
            print(f" Таймер для задачи #{task_id} не был запущен!")
            return False
        
        entry = self.active_timers.pop(task_id)
        entry.stop()
        self.completed_entries.append(entry)
        print(f"Таймер для задачи #{task_id} остановлен. Затрачено: {self._format_time(entry.get_duration())}")
        return True

    def get_total_time(self, task_id: int) -> timedelta:
        """Требование 2: Учёт общего затраченного времени на задачу."""
        total = sum((e.get_duration() for e in self.completed_entries if e.task_id == task_id), timedelta(0))
        if task_id in self.active_timers:
            total += self.active_timers[task_id].get_duration()
        return total

    def generate_report(self) -> Dict[int, str]:
        """Требование 3: Генерация отчетов по времени."""
        report = {}
        all_entries = self.completed_entries + list(self.active_timers.values())
        
        # Группировка по task_id
        task_times: Dict[int, timedelta] = {}
        for entry in all_entries:
            if entry.task_id not in task_times:
                task_times[entry.task_id] = timedelta(0)
            task_times[entry.task_id] += entry.get_duration()
            
        # Форматирование в ЧЧ:ММ:СС
        for task_id, total_time in task_times.items():
            report[task_id] = self._format_time(total_time)
        return report

    def _format_time(self, td: timedelta) -> str:
        """Вспомогательный метод для красивого формата времени."""
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    # === ДОПОЛНИТЕЛЬНАЯ ФУНКЦИЯ НА ДОП. БАЛЛЫ ===
    def export_report_to_csv(self, filename: str = "time_report.csv"):
        """Экспортирует детальный отчет о времени в CSV-файл для бизнес-анализа."""
        all_entries = self.completed_entries + list(self.active_timers.values())
        try:
            with open(filename, mode='w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Task ID", "Start Time", "End Time", "Duration (sec)", "Status"])
                for entry in all_entries:
                    writer.writerow([
                        entry.task_id,
                        entry.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                        entry.end_time.strftime("%Y-%m-%d %H:%M:%S") if entry.end_time else "Active",
                        int(entry.get_duration().total_seconds()),
                        "Active" if entry.is_active else "Completed"
                    ])
            print(f" Отчет успешно экспортирован в {filename}")
        except Exception as e:
            print(f" Ошибка при экспорте в CSV: {e}")