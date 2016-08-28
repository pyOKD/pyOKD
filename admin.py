import pyOKD

if __name__ == "__main__":
    user = pyOKD.client()
    while(True):
        user_command = raw_input("Client: ")
        if  user_command == "quit":
            user.s.close()
            break
        else:
            print user.command(user_command)

        
        
    
