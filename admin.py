import pyOKD

if __name__ == "__main__":
    user = pyOKD.data_client()
    while(True):
        user_command = raw_input("Client: ")
        if  user_command == "quit":
            user.s.close()
            break
        else:
            print user.data_command(user_command)

        
        
    
