import time
from datetime import datetime, timedelta
from task_system import TaskManager, Priority
from time_tracker import TimeTracker

def main():
    print(" Запуск системы управления задачами и учета времени\n")
    
    # 1. Инициализация систем (Интеграция)
    task_manager = TaskManager()
    time_tracker = TimeTracker()

    # 2. Создание задач
    task1 = task_manager.create_task(
        "Разработать модуль аналитики", 
        "Создать классы для сбора метрик", 
        Priority.HIGH, 
        datetime.now() + timedelta(days=7)
    )
    task2 = task_manager.create_task(
        "Написать документацию", 
        "Описать API и методы", 
        Priority.MEDIUM, 
        datetime.now() + timedelta(days=5)
    )
    print(f" Созданы задачи: {task1} и {task2}")

    # 3. Работа с таймером (Задача 1)
    print("\n--- Начало работы над Задачей 1 ---")
    time_tracker.start_timer(task1.task_id)
    time.sleep(2) 
    time_tracker.stop_timer(task1.task_id)

    # 4. Работа с таймером (Задача 2) + Демонстрация валидации - доп. функция
    print("\n--- Начало работы над Задачей 2 ---")
    time_tracker.start_timer(task2.task_id)
    print("Попытка запустить таймер для Задачи 2 второй раз:")
    time_tracker.start_timer(task2.task_id) # Выдаст предупреждение
    
    # 5. Генерация и вывод отчетов 
    print("\n === Итоговый отчет по времени ===")
    report = time_tracker.generate_report()
    for t_id, time_str in report.items():
        task = task_manager.get_task(t_id)
        print(f"Задача #{t_id} '{task.title}': затрачено {time_str}")

    # 6. Дополнительная функция: Экспорт в CSV
    print("\nЭкспорт данных")
    time_tracker.export_report_to_csv("project_time_report.csv")

if __name__ == "__main__":
    main()