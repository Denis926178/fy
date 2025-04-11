import os
import sys
import platform
import argparse
import psutil

def system_info():
    """Выводит информацию о системе"""
    print("\n=== Информация о системе ===")
    
    os_info = f"""
    ОС: {platform.system()}
    Версия ОС: {platform.version()}
    Архитектура: {platform.architecture()[0]}
    Процессор: {platform.processor()}
    """
    print(os_info)

    print(f"Версия Python: {sys.version.split()[0]}\n")

    try:
        disk = psutil.disk_usage('/')
        print(f"Общий объем диска: {disk.total // (1024**3)} GB")
        print(f"Использовано: {disk.used // (1024**3)} GB")
        print(f"Свободно: {disk.free // (1024**3)} GB")
        print(f"Заполнено: {disk.percent}%")
    except Exception as e:
        print(f"Ошибка получения информации о диске: {str(e)}")

def os_operations(action=None, path=None, var_name=None):
    """Операции с файловой системой и переменными окружения"""
    print("\n=== Операции с ОС ===")

    if action == "cwd":
        print(f"Текущий каталог: {os.getcwd()}")
    
    # Смена каталога
    elif action == "chdir":
        try:
            os.chdir(path)
            print(f"Каталог изменен на: {os.getcwd()}")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
    
    elif action == "env":
        env_vars = os.environ
        if var_name:
            print(f"{var_name}: {env_vars.get(var_name, 'Не найдена')}")
        else:
            print("Все переменные окружения:")
            for key, value in list(env_vars.items()):
                print(f"{key} = {value}")

def main():
    parser = argparse.ArgumentParser(description="Системные утилиты")
    subparsers = parser.add_subparsers(dest='command', required=True)

    sys_parser = subparsers.add_parser('system', help='Информация о системе')

    os_parser = subparsers.add_parser('os', help='Операции с файловой системой')
    os_subparsers = os_parser.add_subparsers(dest='os_action', required=True)

    cwd_parser = os_subparsers.add_parser('cwd', help='Текущий каталог')
    chdir_parser = os_subparsers.add_parser('chdir', help='Сменить каталог')
    chdir_parser.add_argument('path', help='Новый путь')
    
    env_parser = os_subparsers.add_parser('env', help='Переменные окружения')
    env_parser.add_argument('-n', '--name', help='Имя переменной')

    args = parser.parse_args()

    if args.command == 'system':
        system_info()
    elif args.command == 'os':
        if args.os_action == 'cwd':
            os_operations('cwd')
        elif args.os_action == 'chdir':
            os_operations('chdir', args.path)
        elif args.os_action == 'env':
            os_operations('env', var_name=args.name)

if __name__ == "__main__":
    main()