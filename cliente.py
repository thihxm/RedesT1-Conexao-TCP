# Import socket module
import socket
import pickle
from utils import compute_sha256

def Main():
    # local host IP '127.0.0.1'
    host = '10.181.7.140'

    # Define the port on which you want to connect
    port = 12345

    socket_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # connect to server on local computer
    socket_connection.connect((host,port))

    isChatting = False

    # message you send to server
    #message = "Arquivo"
    while True:

        if not isChatting:
            message = input('\nDigite "Arquivo" para solicitar arquivo, "Chat" para iniciar um chat ou "Sair" para sair: ')

            # message sent to server
            #socket_connection.send(message.encode())

            # message received from server
            #data = socket_connection.recv(4096)

            # print the received message
            # here it would be a reverse of sent message
            if message == 'Arquivo':
                arquivo = input('\nDigite o nome do arquivo: ')
                message = message + ':' + arquivo
                socket_connection.send(message.encode())

                data = socket_connection.recv(4096)
                file_data = pickle.loads(data)

                #testes
                if file_data['status'] != 'ok':
                    print(file_data['content'].decode())
                    continue

                file_checksum = compute_sha256(file_data['content'])
                if(file_checksum != file_data['checksum']):
                    print('\nMensagem nao integra')
                    continue

                print('Received from the server :', file_data)
                with open(f'./arquivos/{file_data["name"]}', 'wb') as file:
                    file.write(file_data['content'])
            elif message == 'Chat':
                isChatting = True
            elif message == 'Sair':
                break

            # ask the client whether he wants to continue
            # ans = input('\nDo you want to continue (y/n): ')
            # if ans == 'y':
            #     continue
            # else:
            #     break
        else:
            data = socket_connection.recv(4096)
            print('\nServidor: ' + data.decode())
            msg = input('\nDigite a mensagem ou "Sair" para sair: ')
            if msg == 'Sair':
                isChatting = False
            socket_connection.send(msg.encode())
    # close the connection
    socket_connection.close()

if __name__ == '__main__':
    Main()
