import socket
import threading
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Диффи-Хеллман: Генерация параметров
def generate_dh_parameters():
    parameters = dh.generate_parameters(generator=2, key_size=2048, backend=default_backend())
    return parameters

# Создание общего секретного ключа
def generate_shared_key(private_key, peer_public_key, parameters):
    shared_key = private_key.exchange(dh.ECDH(), peer_public_key)
    return shared_key

# AES шифрование
def aes_encrypt(shared_key, message):
    # Генерация случайного IV для AES
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(shared_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message.encode()) + encryptor.finalize()
    return iv + ciphertext

# AES дешифрование
def aes_decrypt(shared_key, ciphertext):
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(shared_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_message.decode()
    
def client_task(client_id, message):
    """Функция клиента для отправки сообщения серверу."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 9090))
        print(f"Клиент {client_id}: Подключено к серверу.")

        parameters = generate_dh_parameters()
        private_key = parameters.generate_private_key()
        public_key = private_key.public_key()
        client_socket.sendall(public_key.public_bytes())

        # Получение публичного ключа от сервера
        server_public_key_bytes = client_socket.recv(1024)
        server_public_key = load_pem_public_key(server_public_key_bytes, backend=default_backend())

        # Генерация общего секретного ключа
        shared_key = generate_shared_key(private_key, server_public_key, parameters)

        # Шифрование сообщения с использованием AES
        encrypted_message = aes_encrypt(shared_key, message)
        client_socket.sendall(encrypted_message)

        # Получение ответа от сервера
        response = client_socket.recv(1024)
        decrypted_response = aes_decrypt(shared_key, response)
        print(f"Ответ от сервера: {decrypted_response}")

    except ConnectionRefusedError:
        print("Ошибка: невозможно подключиться к серверу.")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()
        print(f"Клиент {client_id}: Соединение закрыто.")

def start_client():
    messages = [
        "Привет от клиента 1",
        "Сообщение от клиента 2",
        "Запрос от клиента 3",
        "Еще один клиент 4",
        "Последний клиент 5"
    ]

    threads = []

    for i, msg in enumerate(messages):
        thread = threading.Thread(target=client_task, args=(i+1, msg))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_client()
