import socket


host = "localhost"
port = 8080
# reply = "serveur hello"

def main():
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    
    while True:
        
        message = conn.recv(1024).decode()

        if message == "q":
            break

        print("received message : " + message)
        reply = input("reply :")
        conn.send(reply.encode())
    
        if (reply == "q"):
            break
    
    print("Quitted")
    conn.close()
    server_socket.close()   

if __name__ == "__main__":
    main()