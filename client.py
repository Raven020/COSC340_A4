import socket

''' 
Connect - Upon starting client will retrieve userID from user then
send 'CONNECT userID' to server to connect
Put - PUT {key} then client will prompt user for value to put before sending
Get - GET {key} then client will send to server to retrieve value if there is one
Delete - DELETE {key} then client will send to server to delete value at given key
Disconnect - DISCONNECT then client will send to server to disconnect from server



'''
HOST = '127.0.0.1'
PORT = 1234
PROTOCOL = ['PUT', 'GET', 'DELETE', 'DISCONNECT']
RESPONSES = ['OK', 'ERROR']


def Connect(sock):
    userId = input('Please enter in a User id: ')
    sock.sendall(bytes('CONNECT ' + userId, 'utf8'))
    return userId


def Put(key, sock):
    value = input(f'Please enter value you would like to store under {key}: ')
    toStore = key + "," + value
    sock.sendall(bytes('PUT ' + toStore, 'utf8'))
    return None


def Get(key, sock):
    sock.sendall(bytes('GET ' + ''.join(key[0]), 'utf8'))
    return None


def Delete(key, sock):
    sock.sendall(bytes('DELETE ' + ''.join(key), 'utf8'))
    return None


def Disconnect(sock):
    sock.sendall(bytes('DISCONNECT', 'utf8'))
    return None


def ProcessData(data):
    dataItems = data.split(" : ")
    action = dataItems[0]
    status = dataItems[1]
    # TODO get doesn't return OK just the value. What should the process be for GET actions
    if action in PROTOCOL or action != "GET" and status not in RESPONSES:
        if action == "DISCONNECT":
            print(data)
            exit()
        return True
    return False


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        # get user id and send Connect request to server

        userId = Connect(sock)
        data = sock.recv(2048).decode('utf-8')
        if(data == 'CONNECT : OK'):
            while True:
                # wait for input
                userInput = input('Enter input: ')
                if userInput == '' or ' ' not in userInput:
                    print('Not a valid Input Please try again')
                    continue
                userWords = userInput.split()
                userWords[0] = userWords[0].upper()
                if(userWords[0] in PROTOCOL):
                    # if input is valid then send data
                    # call apropriate function
                    if userWords[0] == 'PUT':
                        Put(''.join(userWords[1:]), sock)
                    elif userWords[0] == 'GET':
                        Get(userWords[1:], sock)
                    elif userWords[0] == 'DELETE':
                        Delete(userWords[1:], sock)
                    elif userWords[0] == 'DISCONNECT':
                        Disconnect(sock)
                else:
                    print('Not a valid Input Please try again')
                    continue
                data = sock.recv(2048).decode('utf-8')
                if(data != None):
                    if ProcessData(data):
                        print(data)

                    else:
                        print(
                            "There was an error with the server, Disconnecting" + data)
                        exit()

    # recieve output from server make appropriate action


if __name__ == '__main__':
    main()
