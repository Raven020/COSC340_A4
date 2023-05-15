import socket
import sys
import hmac
import secrets
import hashlib
''' 
Connect - Upon starting client will retrieve userID from user then
        send 'CONNECT userID' to server to connect
Put - PUT {key} then client will prompt user for value to put before sending
Get - GET {key} then client will send to server to retrieve value if there is one
Delete - DELETE {key} then client will send to server to delete value at given key
Disconnect - DISCONNECT then client will send to server to disconnect from server

'''
HOST = '127.0.0.1'
port = None
PROTOCOL = ['PUT', 'GET', 'DELETE', 'DISCONNECT']
RESPONSES = ['OK', 'ERROR']
KEY = 'LnKfzaiHSt_5EvLcNuSWkCe5J44qvKQQCWNLDt2X0WkDkt3QjuNoRN05jGrncwQ3pD_yI2sZKGKe98OnOOr35PBJYtlzr080Qa_C7FjAXHX90Eeb5MgAkz1RvTWuVc5k52eSm8_Eia4lV_VRihoCsW4E_adROg4Vot0gptuMXf4'


def signMessage(data):
    '''
    signMessage takes data and returns a hmac to be prepended to a message
    before it is sent
    '''
    signedMessage = hmac.new(KEY, bytes(data, 'utf8'), hashlib.sha256).digest()
    return signedMessage


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


'''
ProcessData - takes data entered by user and then verifies whether it is valid or not
'''


def ProcessData(data):
    dataItems = data.split(" : ")
    action = dataItems[0]
    status = dataItems[1]

    if action in PROTOCOL or action != "GET" and status not in RESPONSES:
        if action == "DISCONNECT":
            print(data)
            sys.exit()

        return True
    return False


def main():
    try:
        port = int(sys.argv[1])
    except ValueError:
        print("command line argument needs to contain PORT number, e.g. 1234")
        print("please try again in format python client.py PORT_NUM")
        sys.exit()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, port))

        # get user id and send Connect request to server

        userId = Connect(sock)
        data = sock.recv(2048).decode('utf-8')
        if(data == 'CONNECT : OK'):
            # Main loop, will continue until client DISCONNECT
            while True:
                # wait for input
                userInput = input('Enter input: ')
                if userInput == '' or ' ' not in userInput and userInput.upper() not in PROTOCOL:
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
                    # if input not in protocol then notify user that it was not valid
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
