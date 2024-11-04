import socket
import threading

host = "localhost"
port = 8081
reply = "serveur hello"
message = ""


def recv(socket,conn):
    global message 
    while(message != "qs"):
        message = conn.recv(1024).decode()
        print("received message : " + message)
        # conn.send(reply.encode())
    conn.close()
    socket.close()
    quit(1)


def main():
    global message 
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    receiver = threading.Thread(target=recv,args=[server_socket,conn])
    receiver.start()
    
    while(message != "q"):
        message = input("message : ")
        conn.send(message.encode())
    print('quited')
    conn.close()
    socket.close()
    quit(1)

      

if __name__ == "__main__":
    main()