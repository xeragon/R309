import socket
import sys 
import getopt
import threading
import json
from WorkerServer import WorkerServer
from time import sleep
import commons as c


connected_workers : list[WorkerServer] = []

def connectionHandler(conn,adress):
    global connected_workers
    
    while True:
        filename = conn.recv(1024).decode()
        if not filename: break
        print(f"received filename {filename}")
        
        if(filename != "end"):
            connected_workers[0].w_socket.send(filename.encode())
            conn.send(("rdy").encode())
            while True:
                data = conn.recv(1024).decode()
                if data == "end":
                    break  
            conn.send(("upload successfull").encode())
        else:
            conn.close()
            print("closed connection")
            break

def connect_to_worker(worker : WorkerServer):
    global connected_workers
    while (True):
        print(f"connecting to worker server -> {worker} ...")
        connected = worker.set_connection()
        if connected:
            print(f"connected to worker server -> {worker}\n")   
            connected_workers.append(worker)
            break   
        else:
            print(f"connection to worker server {worker} failed, retying in 3 seconds \n" )    
        sleep(3)  

def main(host,port): 
    global connected_workers
    print(f"starting socket server on {host}:{port} ...")
    
    MainServSocket = socket.socket()
    try:
        MainServSocket.bind((host, int(port)))
        MainServSocket.listen(1)
    except Exception as e:
        print(f"an error occured while creating the socket : {e}") 
 
    print(f"socket server started on {host}:{port}")


    worker_servers : list[WorkerServer] = extract_workers_config("config.json")
    worker_threads = []
    
    for server in worker_servers:
        t = threading.Thread(target=connect_to_worker,args=[server])
        t.daemon = True
        t.start()
        worker_threads.append(t)
    
    print("waiting for client connection...")
    while(True):
        conn,address = MainServSocket.accept()
        t = threading.Thread(target=connectionHandler,args=[conn,address])
        t.daemon = True
        t.start()

   
   
def extract_workers_config(path) -> list[WorkerServer]:
    result = []
    try: 
        dict = c.open_json(path)
        servers = dict['servers']
        for server in servers:
            result.append(WorkerServer(server['host'],int(server['port']),server['name']))
    except Exception as e:
       print(f"problem occured while exctracting workers config : {e}")
   
    return result



if __name__ == "__main__":
    host,port,name = c.getParams()
    if not (port != "" and host != ""):
        print(f"usage : python3 MainServ.py -h <host> -p <port>")
        sys.exit(-1)
    else:
        main(host,port)