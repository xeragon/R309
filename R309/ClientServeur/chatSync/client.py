import socket

host = "localhost"
port = 8080
# message = "client hello"

def main():
    client_socket = socket.socket()
    client_socket.connect((host, port))
    while(True):
        message = input("message to send: ")
        client_socket.send(message.encode())
        reply = client_socket.recv(1024).decode()
        print("received reply : " + reply)
        if (reply == "q" or message == "q"):
            break
    print("Quitted")
    client_socket.close()

if __name__ == "__main__":
    main()