# import socket programming library
import socket
from pathlib import Path
import os
import pickle

# import thread module
from _thread import *
import threading
from utils import compute_sha256


print_lock = threading.Lock()

# thread function
def threaded(client: socket.socket):
    is_chatting = False
    while True:

        # data received from client
        if not is_chatting:
            data = client.recv(4096)
            command = data.decode()
            if not data or data == b'Sair':
                print('Bye')
                
                # lock released on exit
                print_lock.release()
                break
            elif command.startswith('Arquivo'):
                [command, file_name] = command.split(':')
                print('Enviando arquivo')
                file_data = convert_file_to_protocol(file_name)
                client.send(file_data)
            elif data == b'Chat':
                print('Enviando mensagem')
                client.send(b'Chat iniciado')
            else:
                print('Reenviando mensagem: ', data)

                client.send(data)
        else:
            data = client.recv(4096)
            message = data.decode()
            if message == 'Sair':
                is_chatting = False
                print('Chat finalizado')
                continue

            print('Client: ', data.decode())
            message = input('Digite a mensagem: ')
            client.send(message.encode())

    # connection closed
    client.close()

def convert_file_to_protocol(file_name):
    file_path = f'./server_files/{file_name}'
    try:    
        with open(file_path, 'rb') as file:
            file_as_path = Path(file.name)
            file_content = file.read()
            file_checksum = compute_sha256(file_content)
            file_size = file_as_path.stat().st_size

        return pickle.dumps({
            'name': file_name,
            'size': file_size,
            'checksum': file_checksum,
            'content': file_content,
            'status': 'ok'
        })
    except FileNotFoundError:
        print(f'File {file_path} not found')
        return pickle.dumps({
            'name': file_path,
            'size': -1,
            'content': f'File {file_path} not found'.encode(),
            'status': 'error'
        })

def Main():
    host = ""

    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server.bind((host, port))
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname_ex(hostname)
    print("socket binded to port", port)
    print(f"Server IP is {ip_address}")
    file_data = convert_file_to_protocol('./texto.txt')
    print(file_data)

    # put the socket into listening mode
    socket_server.listen(5)
    print(f"socket is listening")

    # a forever loop until client wants to exit
    while True:

        # establish connection with client
        client, addr = socket_server.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (client,))
    socket_server.close()


if __name__ == '__main__':
    Main()
