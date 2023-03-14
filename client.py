import socket

""" 
Connect - Upon starting client will retrieve userID from user then
send 'CONNECT userID' to server to connect
Put - PUT {key} then client will prompt user for value to put before sending
Get - GET {key} then client will send to server to retrieve value if there is one
Delete - DELETE {key} then client will send to server to delete value at given key
Disconnect - DISCONNECT then client will send to server to disconnect from server



"""
HOST = '127.0.0.1'
PORT = 1234
Protocol = ['PUT', 'GET', 'DELETE', 'DISCONNECT']


def Connect(sock):
    userId = input('Please enter in a User id: ')
    sock.sendall(bytes('CONNECT ' + userId, 'utf8'))
    return userId


def Put(key, sock):
    value = input(f"Please enter value you would like to store under {key}: ")
    sock.sendall(bytes('PUT ' + ''.join(key) + " " + value, 'utf8'))
    return None


def Get(key, sock):
    sock.sendall(bytes('GET ' + ''.join(key), 'utf8'))
    return None


def Delete(key, sock):
    sock.sendall(bytes('DELETE ' + ''.join(key), 'utf8'))
    return None


def Disconnect(sock):
    sock.sendall(bytes('DISCONNECT', 'utf8'))
    return None


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))

        # get user id and send Connect request to server

        userId = Connect(userId, sock)

        while True:
            # wait for input
            userInput = input('Enter input: ')
            userWords = userInput.split()
            if(userWords[0] in Protocol and len(userWords) < 4):
                # if input is valid then send data
                # call apropriate function
                if userWords[0] == 'PUT':
                    Put(userWords[1:], sock)
                elif userWords[0] == 'GET':
                    Get(userWords[1:], sock)
                elif userWords[0] == 'DELETE':
                    Delete(userWords[1:], sock)
                elif userWords[0] == 'DISCONNECT':
                    Disconnect(sock)
            else:
                print("Not a valid Input Please try again")
                continue
            data = sock.recv(2048)
            if(data == b'message recieved'):
                print(data)
                data = None
            if(data == b'DISCONNECT: OK'):
                # The case in which the server is disconnecting
                print(data)
                exit()

    # recieve output from server make appropriate action


if __name__ == "__main__":
    main()
