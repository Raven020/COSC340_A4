import sys
import socket

"""
CONNECT {userId} - Server will create or open file with that userID into memory, return OK to client
PUT {key} value - Server will store the value under the key in memory, to be saved later, return OK to client
GET {key} - Retrieve value from memory, that corresponds to that key, return OK to client
DELETE {key} - Remove the value at given key, return OK to client
DISCONNECT - Disconnect from the client, return OK to client


"""
HOST = ''
PORT = 1234


def Connect(userID):
    return None


def Put(key, value):
    return None


def Get(key, value):
    return None


def Delete(key, value):
    return None


def Disconnect():
    return None


def Load_user_file(userId):
    return None


def main():
    clientSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSoc.bind((HOST, PORT))
    except socket.error as message:

        print('Bind Failed')
        exit()

    print('Socket binding complete')

    clientSoc.listen(1)

    conn, address = clientSoc.accept()

    while True:
        print('Waiting for data')
        data = conn.recv(2048)
        if data != None:
            data = str(data)[1:]
            print(data)
            if data == "'DISCONNECT'" or data == '':
                conn.sendall(b'DISCONNECT: OK')
                break
            #conn.sendall(b"message recieved")
            data = None

    print('Connected with' + address[0] + ':' + str(address[1]))

    clientSoc.close()


if __name__ == "__main__":
    main()
