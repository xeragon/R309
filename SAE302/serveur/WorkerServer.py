import socket
import threading
import sys
import commons as c
import os
import subprocess

class WorkerServer():
    w_socket : socket.socket
    
    def __init__(self,host : str ,port : int,name : str):
        self.host = host
        self.port = port
        self.name = name
        self.file_index = 0
        
    def set_connection(self) -> int:
        try:
            mysocket = socket.socket()
            mysocket.connect((self.host,self.port))
            self.w_socket = mysocket
            return 1
        except:
            return 0
        
    def __str__(self) -> str:
        return f"{self.name} {self.host}:{self.port}"
        
def main(host,port,name):
    worker = WorkerServer(host,port,name)
    
    worker_socket = socket.socket()
    try:
        worker_socket.bind((host,port))
        worker_socket.listen(1)
        
    except Exception as e:
        print(f"error while starting worker {name} {host}:{port}")
        sys.exit(-1)
        
        
    print(f"worker {name} started on {host}:{port} and waiting for connection")
    conn,adress = worker_socket.accept()
    print(f"worker {worker} got connection")
    
    # gestion upload
    while True:
        # il faudrait gerer les erreurs d'extension ici aussi
        filename = conn.recv(1024).decode()
        try:
            # filename = f"./files/file_{worker.name}_{self.file_index}"
            filename = f"./files/{filename}"
            fo = open(filename,"w")
        except Exception as e:
            print(f"error {e}")
        while True:
            data = conn.recv(1024).decode()
            print(f"data {data}")
            if data == "end":   
                break
            fo.write(data)
            
        fo.close()
        file_extension = filename.split('.')[-1]
        match file_extension:
            case "py":
                s = subprocess.run(["python3",filename],capture_output=True)
                print(f"call : {s.__str__()}")
                conn.send(s.__str__().encode())
            case "java":
                pass
        
       

        

if __name__ == "__main__":
    host,port,name = c.getParams()
    if not (port != "" and host != "" and name != ""):
        print(f"usage : python3 WorkerServer.py -h <host> -p <port> -n <name>")
        sys.exit(-1)
    else:
        main(host,int(port),name)
