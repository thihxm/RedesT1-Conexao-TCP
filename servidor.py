# import socket programming library
import socket
from pathlib import Path
import os
import pickle

# import thread module
from _thread import *
import threading
import hashlib

print_lock = threading.Lock()

def send_message(client: socket.socket, message: str):
    total_sent = 0
    while total_sent < 4096:
        sent = client.send(message[total_sent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        total_sent = total_sent + sent

# thread function
def threaded(client: socket.socket):
    while True:

        # data received from client
        data = client.recv(4096)
        if not data or data == b'Sair':
            print('Bye')
            
            # lock released on exit
            print_lock.release()
            break
        elif data == b'Arquivo':
            print('Enviando arquivo')
            file_data = convert_file_to_protocol('./textoa.txt')
            client.send(file_data)
        else:
            print('Reenviando mensagem: ', data)

            client.send(data)

    # connection closed
    client.close()

def convert_file_to_protocol(file_path):
    try:    
        with open(file_path, 'rb') as file:
            file_as_path = Path(file.name)
            file_content = file.read()
            file_checksum = compute_sha256(file_content)
            file_name = file_as_path.stem
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
    
def compute_sha256(data):
    hash_sha256 = hashlib.sha256()
    hash_sha256.update(data)
    return hash_sha256.hexdigest()


if __name__ == '__main__':
    Main()
