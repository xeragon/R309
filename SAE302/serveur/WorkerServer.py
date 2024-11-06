import socket
import threading
import sys
import commons as c

class WorkerServer():

    def __init__(self,host : str ,port : int,name : str):
        self.host = host
        self.port = port
        self.name = name
    
    def set_connection(self):
        try:
            mysocket = socket.socket()
            mysocket.connect((self.host,self.port))
            self.socket = mysocket
            return 1
        except:
            return 0        
        

        

    def __str__(self) -> str:
        return f"{self.name} {self.host}:{self.port}"
    


    
def main(host,port,name):
    worker = WorkerServer(host,port,name)
    try:
        worker_socket = socket.socket()
        worker_socket.bind((host,port))
        worker_socket.listen(1)
    except Exception as e:
        print(f"error while starting worker {name} {host}:{port}")
        sys.exit(-1)
        
    print(f"worker {name} started on {host}:{port} and waiting for connection")
    conn,adress = worker_socket.accept()
    print(f"worker {worker} got connection")
    
    

if __name__ == "__main__":
    host,port,name = c.getParams()
    if not (port != "" and host != "" and name != ""):
        print(f"usage : python3 WorkerServer.py -h <host> -p <port> -n <name>")
        sys.exit(-1)
    else:
        main(host,int(port),name)
