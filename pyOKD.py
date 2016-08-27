import asyncore
import socket
import time
import subprocess
import cPickle as pickle

class DATABASE():
    def __init__(self):
        with open("saved_buffer.pkl", "rb") as f:
            self.info1 = pickle.load(f)

    

class EchoHandler(asyncore.dispatcher_with_send):
    
    def __init__(self, sock, data_class, addr):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.DATABASE = data_class
        self.conn_info = addr
        self.dispatch = {
                "set" : self.set_buffer,
                "get" : self.get_buffer,
                "save" : self.save_buffer,
                "load" : self.load_buffer,
            }

    def handle_read(self):
        data = self.recv(8192)
        if data:
            command = data.split(" ")
            if command[0] == 'save':
                self.send(self.save_buffer())
            elif command[0] == 'load':
                self.send(self.load_buffer())
            elif command[0] in self.dispatch.keys() and len(command) > 1:
                if len(command) == 2:
                    self.send(self.dispatch[command[0]](command[1]))
                elif len(command) == 3:
                    self.send(self.dispatch[command[0]](command[1], command[2]))
                else:
                    self.send("Too many arguments")
            else:
                self.send("Does not exist")

    def handle_close(self):
        self.close()
        print 'Terminated connection from %s' % repr(self.conn_info)


    def set_buffer(self, arg1, arg2 = None):
        if arg2 != None:
            self.DATABASE.info1[arg1] = arg2 
            return arg1
        else:
            return "Error: Requires two arguments"
              
    def get_buffer(self, arg1, arg2 = None):
        if arg1 in self.DATABASE.info1.keys():
            return self.DATABASE.info1[arg1]
        else:
            return "Error: This key does not exist"
    def save_buffer(self, arg1= None, arg2 = None):
        with open("saved_buffer.pkl", "wb") as f:
            pickle.dump(self.DATABASE.info1, f)
            return "Saved buffer"

    def load_buffer(self, arg1 = None, arg2 = None):
        with open("saved_buffer.pkl", "rb") as f:
            self.DATABASE.info1 = pickle.load(f)
            return "Loaded Buffer"



class Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.DATABASE = DATABASE()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock, self.DATABASE, addr)

    def loop(self):
        asyncore.loop()
        print "loop ended"

class data_client():
    def __init__(self):
        self.host = '10.0.0.24'
        self.port = 8080 
        self.size = 1024 
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.s.connect((self.host,self.port))

    def data_command(self, command):
        self.s.send(command) 
        return self.s.recv(self.size)

    def data_get(self, index):
        return self.data_command("get " + str(index))

    def data_set(self, index, data):
        return self.data_command("set " + str(index) + " " + str(data))

    def data_move(self, index, delta):
        data = int(self.data_get(index))
        self.data_set(index, data + delta)
        return "Data move"

    def data_load(self, index):
        data = self.data_get(index)
        return pickle.loads(data)

    def data_store(self, index, data):
        storage = pickle.dumps(data)
        self.data_set(index, storage)

if __name__ == "__main__":
    Server('0.0.0.0', 8080).loop()
