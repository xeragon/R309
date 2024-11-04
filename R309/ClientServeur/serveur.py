import socket


host = "localhost"
port = 8080
reply = "serveur hello"

def main():
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    message = conn.recv(1024).decode()
    print("received message : " + message)
    conn.send(reply.encode())
    conn.close()
    server_socket.close()   

if __name__ == "__main__":
    main()