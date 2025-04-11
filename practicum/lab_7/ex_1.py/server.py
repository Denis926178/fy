import socket
import logging
from datetime import datetime
import threading

logging.basicConfig(filename="server.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def log_message(message):
    print(message)
    logging.info(message)

def handle_client(client_socket, client_address):
    log_message(f"Новое подключение от {client_address}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode("utf-8").strip()
            log_message(f"Сообщение от {client_address}: {message}")

            if message.lower() == "shutdown":
                log_message("Получена команда shutdown. Завершение работы сервера...")
                client_socket.sendall("Сервер завершает работу.\n".encode("utf-8"))
                client_socket.close()
                return

            client_socket.sendall(data)  # Эхо-ответ

    except ConnectionResetError:
        log_message(f"Соединение с {client_address} неожиданно разорвано.")
    finally:
        client_socket.close()
        log_message(f"Клиент {client_address} отключился.")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 9090))
    server_socket.listen()

    log_message("Сервер запущен и ожидает подключений...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True  # Убедимся, что потоки завершатся при остановке сервера
            client_thread.start()

    except KeyboardInterrupt:
        log_message("Сервер принудительно остановлен.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    start_server()
