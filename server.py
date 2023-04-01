import sys
import socket

'''
CONNECT {userId} - Server will create or open file with that userID into memory, return OK to client
PUT {key} value - Server will store the value under the key in memory, to be saved later, return OK to client
GET {key} - Retrieve value from memory, that corresponds to that key, return OK to client
DELETE {key} - Remove the value at given key, return OK to client
DISCONNECT - Disconnect from the client, return OK to client


'''
HOST = ''
PORT = 1234
User = str()  # username
Storage = dict()  # the that is in data in memory


def Connect(userID, sock):
    # TODO read in users file, read map into memory
    User = userID
    print(User + ' has connected')
    sock.sendall(b'CONNECT : OK')
    return None


def Put(data, sock):
    dataItems = data[0].split(",")
    key = dataItems[0]
    value = dataItems[1]
    Storage[key] = value
    sock.sendall(b'PUT : OK')
    print(Storage)
    return None


def Get(data, sock):

    if(data[0] in Storage.keys()):
        print(bytes(Storage[data[0]], 'utf-8'))
        sock.sendall(bytes("GET : " + Storage[data[0]], 'utf-8'))
    else:
        sock.sendall(bytes("GET : ERROR", 'utf-8'))
    return None


def Delete(data, sock):
    # print(data[0])
    try:
        Storage.pop(data[0])
        sock.sendall(bytes("DELETE : OK", 'utf-8'))
    except:
        sock.sendall(bytes("DELETE : ERROR"), 'utf-8')
    print(Storage)

    return None


def Disconnect(userID, sock):
    print('' + userID + ' has disconnected')
    sock.sendall(b'DISCONNECT : OK')
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
        # print('Waiting for data')
        data = conn.recv(2048)
        if data:
            data = data.decode('utf-8')
            dataWords = data.split(' ', 1)
            if dataWords[0] == 'CONNECT':
                Connect(''.join(dataWords[1:]), conn)
            elif dataWords[0] == 'PUT':
                Put(dataWords[1:], conn)
            elif dataWords[0] == 'GET':
                Get(dataWords[1:], conn)
            elif dataWords[0] == 'DELETE':
                Delete(dataWords[1:], conn)
            elif dataWords[0] == 'DISCONNECT':
                Disconnect(User, conn)
                break
            else:
                print('Not a valid input disconnecting from client')
                conn.close()
            # conn.sendall(b'message recieved')

    # print('Connected with ' + address[0] + ':' + str(address[1]))

    clientSoc.close()


if __name__ == '__main__':
    main()
