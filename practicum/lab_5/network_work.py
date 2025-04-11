import argparse
import http.client
import socket
import ssl
from urllib.parse import urlparse

def http_check(url):
    """Проверка доступности сайта через HTTP-запрос"""
    try:
        parsed = urlparse(url)

        if parsed.scheme == 'https':
            conn = http.client.HTTPSConnection(parsed.netloc, timeout=10)
        else:
            conn = http.client.HTTPConnection(parsed.netloc, timeout=10)
            
        conn.request("HEAD", parsed.path or "/")
        response = conn.getresponse()
        print(f"Статус-код: {response.status} {response.reason}")
        conn.close()
        
    except Exception as e:
        print(f"Ошибка: {str(e)}")

def socket_test(host, port, message):
    """Подключение к серверу через raw socket (исправленная версия)"""
    try:
        formatted_message = message.replace('\\r\\n', '\r\n')
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10)

            if port == 443:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    ssock.connect((host, port))
                    print(f"Успешное SSL-подключение к {host}:{port}")
                    ssock.sendall(formatted_message.encode())
                    response = ssock.recv(4096)
            else:
                sock.connect((host, port))
                print(f"Успешное подключение к {host}:{port}")
                sock.sendall(formatted_message.encode())
                response = sock.recv(4096)

            print(f"Ответ сервера:\n{response.decode()[:500]}...")

    except socket.timeout:
        print("Ошибка: Таймаут соединения. Сервер не ответил")
    except Exception as e:
        print(f"Ошибка: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Сетевые утилиты")
    subparsers = parser.add_subparsers(dest='command', required=True)

    http_parser = subparsers.add_parser('http_check', help='Проверка HTTP-статуса')
    http_parser.add_argument('--url', required=True, help='URL для проверки')

    socket_parser = subparsers.add_parser('socket_test', help='Тест TCP-соединения')
    socket_parser.add_argument('--host', required=True, help='Адрес сервера')
    socket_parser.add_argument('--port', type=int, required=True, 
                             help='Порт сервера (1-65535)')
    socket_parser.add_argument('--message', default='Hello Server!',
                             help='Сообщение для отправки')

    args = parser.parse_args()

    if args.command == 'http_check':
        http_check(args.url)
    elif args.command == 'socket_test':
        if not (1 <= args.port <= 65535):
            print("Некорректный порт! Допустимый диапазон: 1-65535")
            return
        socket_test(args.host, args.port, args.message)

if __name__ == "__main__":
    main()
