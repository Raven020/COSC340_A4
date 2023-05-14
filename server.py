import sys
import socket

'''
CONNECT {userId} - Server will create or open file with that userID into memory, return OK to client
PUT {key} value - Server will store the value under the key in memory, to be saved later, return OK to client
GET {key} - Retrieve value from memory, that corresponds to that key, return OK to client
DELETE {key} - Remove the value at given key, return OK to client
DISCONNECT - Disconnect from the client, return OK to client

'''

'''
    TODO
    HMAC algorithm 
'''


HOST = ''
port = None
User = str()  # username
Storage = dict()  # the that is in data in memory


def Connect(userID, sock):
    User = userID
    print(User + ' has connected')
    sock.sendall(b'CONNECT : OK')
    return None


def Put(data, sock):
    dataItems = data[0].split(",")
    key = dataItems[0]
    value = dataItems[1]
    if key not in Storage:
        try:
            Storage[key] = value
        except MemoryError:
            print("PUT : MEMORY ERROR")
            sock.sendall(b'PUT : ERROR')

        sock.sendall(b'PUT : OK')
        print(Storage)
        return None
    print("PUT : KEY ALREADY EXISTS")
    sock.sendall(b'PUT : ERROR')
    return None


def Get(data, sock):
    if(data[0] in Storage.keys()):
        print(bytes(Storage[data[0]], 'utf-8'))
        sock.sendall(bytes("GET : " + Storage[data[0]], 'utf-8'))
    else:
        sock.sendall(bytes("GET : ERROR", 'utf-8'))
    return None


def Delete(data, sock):
    try:
        Storage.pop(data[0])
        sock.sendall(bytes("DELETE : OK", 'utf-8'))
        print("Found Key, Deleted Key")
    except KeyError:
        print("Could not Find key")
        sock.sendall(bytes("DELETE : ERROR", "utf-8"))

    print(Storage)

    return None


def Disconnect(userID, sock):
    print('' + userID + ' has disconnected')
    sock.sendall(b'DISCONNECT : OK')
    sock.close()
    Storage.clear()
    return None


def main():
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("command line argument needs to contain PORT number, e.g. 1234")
        print("please try again in format python server.py PORT_NUM")
        sys.exit()

    clientSoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        clientSoc.bind((HOST, port))
    except socket.error as message:

        print('Bind Failed')
        print(message)
        exit()

    print('Socket binding complete')
    # loop will continue either servicing a client or waiting for a client
    # until explicitly halted
    while True:
        clientSoc.listen(1)

        conn, address = clientSoc.accept()
        # loop to handle communication while a client is connected
        while True:
            data = conn.recv(2048)
            if data:
                data = data.decode('utf-8')
                dataWords = data.split(' ', 1)
                # call appropriate function for user input
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
                # if data not in protocol then something went wrong and server
                # will close connection and clear data to protect itself
                else:
                    print('Not a valid input disconnecting from client')
                    Storage.clear()
                    conn.close()
                    break


if __name__ == '__main__':
    main()
