# pyOKD
Object Key Database for Python 2.7

Simple solution for providing shared information. User defined information is stored in a dictionary that is hosted by an asynchio server.

To start a server run (found in run server script):

pyOKD.Server('0.0.0.0', 8080).loop()


To interact with the server, make a client object:

client = client()

To store information:

client.store( index, data )
index is a string that represents the key to where your data is to be stored.
data can be any data type. Data types are preserved through the use of cPickle

To get information:

client.load( index )
index is a string that represents the key to where your data is stored.


admin.py is a simple script that acts as a shell to the server. Valid commands are set, get, save, and load. Lowercase only.
Note: set and get stores and loads strings only.


