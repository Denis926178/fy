import os
import subprocess
import argparse

def run_ping(host, packets=4):
    """Универсальный ping без проверки ОС"""
    try:
        # Пробуем Unix-стиль команды
        result = subprocess.run(
            ['ping', '-c', str(packets), host],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
    except FileNotFoundError:
        # Если не сработало, пробуем Windows-стиль
        try:
            result = subprocess.run(
                ['ping', '-n', str(packets), host],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=10
            )
        except Exception as e:
            print(f"Ошибка: {str(e)}")
            return
    
    print(result.stdout)
    print("Успешно" if result.returncode == 0 else "Ошибка")

def count_files(directory='.'):
    """Подсчет файлов через os"""
    try:
        files = [
            f for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f))
        ]
        print(f"Файлов в '{directory}': {len(files)}")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Системные утилиты')
    subparsers = parser.add_subparsers(dest='command', required=True)

    ping_parser = subparsers.add_parser('ping', help='Проверка доступности хоста')
    ping_parser.add_argument('host', help='Целевой хост')
    ping_parser.add_argument('-c', '--count', type=int, default=4,
                           help='Количество пакетов')

    count_parser = subparsers.add_parser('count', help='Подсчет файлов')
    count_parser.add_argument('-d', '--dir', default='.', 
                            help='Целевая директория')

    args = parser.parse_args()

    if args.command == 'ping':
        run_ping(args.host, args.count)
    elif args.command == 'count':
        count_files(args.dir)

if __name__ == "__main__":
    main()
