import socket
import threading
import sys
import commons as c
import os
import subprocess
import json

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
        original_filename = filename
        try:
            # filename = f"./files/file_{worker.name}_{self.file_index}"
            filename = f"./files/{filename}"
            fo = open(filename,"wb")
        except Exception as e:
            print(f"error {e}")
        while True:
            data = conn.recv(1024)
            print(f"data {data}")
            
            if not data:   
                break
            
            fo.write(data)

            if len(data) < 1024:
                break
            
        fo.close()
        file_extension = filename.split('.')[-1]
        match file_extension:
            case "py":
                s = subprocess.run(["python",filename],capture_output=True,encoding="locale")
                text = f"executed command : {str(s.args)} output : {s.stdout} errors : {s.stderr}"
                res = json.dumps({
                    "command": s.args,
                    "output": s.stdout,
                    "errors": s.stderr
                })                
                print(res)

                conn.send(res.encode())
            case "java":
                try:
                    compile = subprocess.run(["javac",filename],capture_output=True,encoding="locale")
                    if compile.returncode == 0:

                        print(f"org filename {original_filename.split('.')[0]}")
                        s = subprocess.run(["java", "-cp", "./files", original_filename.split('.')[0]],capture_output=True,encoding="locale")
                            
                        text = f"executed command : {str(s.args)} output : {s.stdout} errors : {s.stderr}"
                        res = json.dumps({
                            "command": s.args,
                            "output": s.stdout,
                            "errors": s.stderr
                        })                
                    else:
                        res = json.dumps({
                        "command": f"javac {filename}",
                        "output": compile.stdout,
                        "errors": compile.stderr
                        })
                except Exception as e:
                    res = json.dumps({
                        "command": "error occured",
                        "output": "",
                        "errors": "An error occured while compiling/executing code"  
                    })
        
                print(res)
                conn.send(res.encode())
            case "c":
                try:
                    compile = subprocess.run(["gcc",filename],capture_output=True,encoding="locale")
                    if compile.returncode == 0:

                        if os.name == 'nt':
                            s = subprocess.run(["./a.exe"],capture_output=True,encoding="locale")
                        else:
                            s = subprocess.run(["./a.out"],capture_output=True,encoding="locale")
                        
                        
                        text = f"executed command : {str(s.args)} output : {s.stdout} errors : {s.stderr}"
                        res = json.dumps({
                            "command": s.args,
                            "output": s.stdout,
                            "errors": s.stderr
                        })                
                    else:
                        res = json.dumps({
                        "command": "gcc",
                        "output": compile.stdout,
                        "errors": compile.stderr
                        })
                except Exception as e:
                    res = json.dumps({
                        "command": "error occured",
                        "output": "",
                        "errors": "An error occured while compiling/executing code"  
                    })
                print(f"RESPONSE {res}")
                conn.send(res.encode())

        

if __name__ == "__main__":
    host,port,name = c.getParams()
    if not (port != "" and host != "" and name != ""):
        print(f"usage : python3 WorkerServer.py -h <host> -p <port> -n <name>")
        sys.exit(-1)
    else:
        main(host,int(port),name)
