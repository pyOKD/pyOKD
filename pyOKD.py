import asyncore, json, os, socket, subprocess, time

class DATABASE():
    def __init__(self):
        if os.path.isfile("saved_buffer.json"):
            print "Previous buffer initialized"
            with open("saved_buffer.json", "r") as f:
                self.info1 = json.load(f)
        else:
            self.info1 = {}

class EchoHandler(asyncore.dispatcher_with_send):
    
    def __init__(self, sock, database, addr):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.DATABASE = database
        self.conn_info = addr

    def handle_read(self):
        data = self.recv(8192)
        if data:
            command = data.split(" ")
            if command[0] == 'save':
                self.send(self.save_buffer())
            elif command[0] == 'load':
                self.send(self.load_buffer())
            elif command[0] == 'get':
                if len(command) == 2:
                    self.send(self.get_buffer(command[1]))
                else:
                    self.send("get requires 2 arguments")
            elif command[0] == 'set':
                if len(command) == 3:
                    self.send(self.set_buffer(command[1], command[2]))
                else:
                    self.send("set requires 3 arguments")
                    
            elif command[0] == 'dump':
                self.send(str(self.DATABASE.info1))
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
        with open("saved_buffer.json", "w") as f:
            json.dump(self.DATABASE.info1, f)
            return "Saved buffer"

    def load_buffer(self, arg1 = None, arg2 = None):
        if os.path.isfile("saved_buffer.json"):
            with open("saved_buffer.json", "r") as f:
                self.DATABASE.info1 = json.load(f)
                return "Loaded Buffer"
        else:
            return "No previous saved buffer"



class Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.DATABASE = DATABASE()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        print "Server started at {}:{}".format(host, port)
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

class client():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8080 
        self.size = 1024 
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.s.connect((self.host,self.port))

    def command(self, command):
        self.s.send(command) 
        return self.s.recv(self.size)

    def get(self, index):
        return self.command("get " + str(index))

    def set(self, index, data):
        return self.command("set " + str(index) + " " + str(data))

    def move(self, index, delta):
        data = int(self.get(index))
        self.set(index, data + delta)
        return "Data move"

    def load(self, index):
        data = self.get(index)
        return json.loads(data)

    def store(self, index, data):
        storage = json.dumps(data)
        self.set(index, storage)

if __name__ == "__main__":
    Server('0.0.0.0', 8080).loop()
