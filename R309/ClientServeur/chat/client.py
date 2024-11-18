import socket
import threading
host = "localhost"
port = 8081

quitted = False

message = ""

shouldQuit = False

def recv(socket):
    global message,quitted 
    while(True):
        message = socket.recv(1024).decode()
        print("received message : " + message)
        if(message == "q"):
            break
    socket.close()
    quitted = True
    exit()

    

def main():
    global message,quitted

    client_socket = socket.socket()
    client_socket.connect((host, port))
    receiver = threading.Thread(target=recv,args=[client_socket])
    receiver.daemon = True
    receiver.start()
    
    while(message != "q"):
        if(not receiver.is_alive()):
            break
        try:
            message = input("message : ") 
            client_socket.send(message.encode())
        except:
            if not quitted:
                print("an error occured")
            else:
                print("Quitted")
                
            

    if(not quitted):    
        print('Quited')
        
    client_socket.close()
    exit()
    
if __name__ == "__main__":
    main()