# Import socket module
import socket
import pickle


def Main():
    # local host IP '127.0.0.1'
    host = '127.0.0.1'

    # Define the port on which you want to connect
    port = 12345

    socket_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    # connect to server on local computer
    socket_connection.connect((host,port))

    # message you send to server
    message = "Arquivo"
    while True:

        # message sent to server
        socket_connection.send(message.encode())

        # message received from server
        data = socket_connection.recv(4096)

        # print the received message
        # here it would be a reverse of sent message
        if message == 'Arquivo':
            file_data = pickle.loads(data)
            print('Received from the server :', file_data)
            with open('./textob.txt', 'wb') as file:
                file.write(file_data['content'])
        else:
            print('Received from the server :', str(data.decode()))

        # ask the client whether he wants to continue
        ans = input('\nDo you want to continue (y/n): ')
        if ans == 'y':
            continue
        else:
            break
    # close the connection
    socket_connection.close()

if __name__ == '__main__':
    Main()
