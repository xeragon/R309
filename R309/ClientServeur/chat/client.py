import socket
import threading

host = "localhost"
port = 8081

message = ""

def recv(socket):
    global message 
    while(message != "qc"):
        message = socket.recv(1024).decode()
        print("received message : " + message)
    socket.close()
    quit(1)



def main():
    global message
    client_socket = socket.socket()
    client_socket.connect((host, port))
    receiver = threading.Thread(target=recv,args=[client_socket])
    receiver.start()

    while(message != "q"):
        message = input("message : ")
        client_socket.send(message.encode())
        
    client_socket.close()
    quit(1)
    
if __name__ == "__main__":
    main()