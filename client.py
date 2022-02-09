import sys, socket, threading
from data.config import HOST, PORT
from data.ascii_arts import WELCOME, BYE

if len(sys.argv) == 3:
    HOST = str(sys.argv[1])
    PORT = int(sys.argv[2])

print(WELCOME)
nickname = input("[:3] Введите ваше имя: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def leave_room():
    client.send("[EXIT_MESSAGE]".encode('utf-8'))
    client.close()
    exit()


def handle_receiving():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "NICKNAME":
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print(BYE)
            client.close()
            break


def handle_sending():
    while True:
        message = input("").strip()
        if message == "q":
            leave_room()
        if message != "":
            client.send(f"{nickname}: {message}".encode('utf-8'))


if __name__ == "__main__":
    try:
        receiving_handling_thread = threading.Thread(target=handle_receiving)
        receiving_handling_thread.start()
        sending_handling_thread = threading.Thread(target=handle_sending)
        sending_handling_thread.start()
    except:
        pass
