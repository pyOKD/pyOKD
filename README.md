# pyOKD
Object Key Database for Python 2.7

Simple solution for providing shared information between processes, programs, and network. User defined information is stored in a dictionary that is hosted by an asynchio server.

To start a server run (found in run server script):

pyOKD.Server('0.0.0.0', 8080).loop()


To interact with the server, make a client object:

client = client()

To store information:

client.store( index, data )
index is a string that represents the key to where your data is to be stored.
data can be any data type. Data types are preserved through the use of JSON.

To get information:

client.load( index )
index is a string that represents the key to where your data is stored.


admin.py is a simple script that acts as a shell to the server. Valid commands are set, get, save, and load. Lowercase only.
Note: set and get stores and loads strings only.


Want to run a server and client in the same file you say?
Running this code runs the server in a new thread. No further action required. The server will run for as long as the program is running.

import threading

def serve():
    pyOKD.Server('0.0.0.0', 8080).loop()

t = threading.Thread(name="Server", target=serve)
t.daemon =True
t.start()

client = pyOKD.client()

