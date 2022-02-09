import sys, socket, threading
from data.config import HOST, PORT

if len(sys.argv) == 3:
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients_data = dict()


def broadcast(message:str):
    for client in clients_data.values():
        client.send(message.encode('utf-8'))


def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if "[EXIT_MESSAGE]" in message:
                raise Exception('[DISCONNECT]')
            broadcast(message)
        except:
            nickname = str()
            for k, v in clients_data.items():
                if v == client:
                    nickname = k
            client.close()
            del clients_data[nickname]

            broadcast(f"{nickname} покинул чат!")
            print(f"[INFO][DISCONNECT]: {nickname}")
            break


def handle_connections():
    while True:
        client, address = server.accept()
        print(f"[INFO][CONNECT]: {str(address)}")

        client.send("NICKNAME".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        clients_data[nickname] = client

        broadcast(f"{nickname} подключился к чату! ")
        client.send("Успешное подключение к серверу!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    print("[INFO] Запуск сервера...")
    try:
        main_handling_thread = threading.Thread(target=handle_connections)
        main_handling_thread.start()
        print("[INFO] Сервер запущен!")
    except Exception as err:
        print(f"[EXCEPTION] Ошибка исполнения: {str(err)}")