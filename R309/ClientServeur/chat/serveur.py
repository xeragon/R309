import socket
import threading

host = "localhost"
port = 8080
reply = "serveur hello"
message = ""
quitted = False

def recv(socket,conn):
    global message , quitted
    while(message != "q"):
        message = conn.recv(1024).decode()
        print("received message : " + message)
    conn.close()
    socket.close()
    quitted = True
    exit()


def main():
    global message,quitted
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    receiver = threading.Thread(target=recv,args=[server_socket,conn])
    receiver.daemon = True
    receiver.start()
    
    while(message != "q"):
        if(not receiver.is_alive()):
            break
        try:
            message = input("message : ")
            conn.send(message.encode())
        except:
            if not quitted:
                print("an error occured")
            else:
                print("Quitted")
            

        
    if(not quitted):    
        print('Quited')
    conn.close()
    server_socket.close()
    exit()

      

if __name__ == "__main__":
    main()