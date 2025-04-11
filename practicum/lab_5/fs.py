import os
import argparse

def create_directory(dir_path):
    """Создание директории с проверкой существования"""
    if os.path.exists(dir_path):
        print(f"Директория '{dir_path}' уже существует!")
        return False
    try:
        os.makedirs(dir_path)
        print(f"Директория '{dir_path}' успешно создана!")
        return True
    except Exception as e:
        print(f"Ошибка при создании директории: {str(e)}")
        return False

def list_all_files(directory):
    """Рекурсивный вывод всех файлов в директории"""
    if not os.path.isdir(directory):
        print("Указанный путь не существует или не является директорией")
        return
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.abspath(os.path.join(root, file))
            print(file_path)

def main():
    parser = argparse.ArgumentParser(
        description="Утилита для работы с файловой системой"
    )
    subparsers = parser.add_subparsers(
        dest='command',
        required=True,
        help='Доступные команды'
    )

    mkdir_parser = subparsers.add_parser(
        'mkdir',
        help='Создание новой директории'
    )
    mkdir_parser.add_argument(
        'path',
        type=str,
        help='Путь для создания директории'
    )

    list_parser = subparsers.add_parser(
        'list',
        help='Рекурсивный вывод файлов'
    )
    list_parser.add_argument(
        'target_directory',
        type=str,
        help='Путь для сканирования'
    )

    args = parser.parse_args()

    if args.command == 'mkdir':
        create_directory(args.path)
    elif args.command == 'list':
        list_all_files(args.target_directory)

if __name__ == "__main__":
    main()
