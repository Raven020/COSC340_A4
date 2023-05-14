Hello,

this is Raven's guide to using his COSC340 Client and Server Sockets implementation
Step 1:
    start the server with a command : ./startServer.sh PORT_NUM
    e.g ./startServer.sh 1234

Step 2:
    start the client with a comman : ./startClient.sh PORT_NUM
    e.g ./startClient.sh 1234

Step 3: 
    enter values into the client
    the client will begin by asking for an user id, or username
    enter in your username
    then use:
        Connect - Upon starting client will retrieve userID from user then
                send 'CONNECT userID' to server to connect
        Put - PUT {key} then client will prompt user for value to put before sending
        Get - GET {key} then client will send to server to retrieve value if there is one
        Delete - DELETE {key} then client will send to server to delete value at given key
        Disconnect - DISCONNECT then client will send to server to disconnect from server
    