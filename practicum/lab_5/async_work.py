import argparse
import threading
import time
import asyncio

def long_sync_task(task_id: int, duration: int):
    """Синхронная длительная задача"""
    print(f"[Thread {task_id}] 🕒 Начало задачи ({duration} сек)")
    time.sleep(duration)
    print(f"[Thread {task_id}] ✅ Завершено за {duration} сек")

async def long_async_task(task_id: int, duration: int):
    """Асинхронная длительная задача"""
    print(f"[Async {task_id}] 🕒 Начало задачи ({duration} сек)")
    await asyncio.sleep(duration)
    print(f"[Async {task_id}] ✅ Завершено за {duration} сек")

def run_threads(num_tasks: int, duration: int):
    """Запуск синхронных задач в потоках"""
    threads = []
    for i in range(num_tasks):
        thread = threading.Thread(
            target=long_sync_task,
            args=(i+1, duration))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

async def run_async(num_tasks: int, duration: int):
    """Запуск асинхронных задач"""
    tasks = [
        long_async_task(i+1, duration)
        for i in range(num_tasks)
    ]
    await asyncio.gather(*tasks)

def main():
    parser = argparse.ArgumentParser(description="Параллельное выполнение задач")
    subparsers = parser.add_subparsers(dest='mode', required=True)

    # Парсер для многопоточного режима
    thread_parser = subparsers.add_parser('thread', help='Многопоточные задачи')
    thread_parser.add_argument('-n', '--num-tasks', type=int, default=3,
                             help='Количество задач (по умолчанию 3)')
    thread_parser.add_argument('-d', '--duration', type=int, default=2,
                             help='Длительность задачи в сек (по умолчанию 2)')

    # Парсер для асинхронного режима
    async_parser = subparsers.add_parser('async', help='Асинхронные задачи')
    async_parser.add_argument('-n', '--num-tasks', type=int, default=3,
                            help='Количество задач (по умолчанию 3)')
    async_parser.add_argument('-d', '--duration', type=int, default=2,
                            help='Длительность задачи в сек (по умолчанию 2)')

    args = parser.parse_args()

    try:
        if args.mode == 'thread':
            print(f"🧵 Запуск {args.num_tasks} потоков:")
            run_threads(args.num_tasks, args.duration)
        elif args.mode == 'async':
            print(f"🌀 Запуск {args.num_tasks} асинхронных задач:")
            asyncio.run(run_async(args.num_tasks, args.duration))
        
        print("\nВсе задачи успешно завершены!")
    except KeyboardInterrupt:
        print("\n🚫 Выполнение прервано пользователем")

if __name__ == "__main__":
    main()
