# pyOKD
Object Key Database for Python 2.7

Simple solution for providing shared information. User defined information is stored in a dictionary that is hosted by an asynchio server.

To interact with the server, make a data_client object:

client = data_client()

To store information:

client.data_store( index, data )
index is a string that represents the key to where your data is to be stored.
data can be any data type. Data types are preserved through the use of cPickle

To get information:

client.data_load( index )
index is a string that represents the key to where your data is stored.


