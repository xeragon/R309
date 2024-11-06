import socket
import sys 
import getopt
import threading
import json
from WorkerServer import WorkerServer
from time import sleep
import commons as c


def connectionHandler(conn,adress):
    print("got a connection")


def main(host,port): 
       
    print(f"starting socket server on {host}:{port} ...")
    
    try:
        MainServSocket = socket.socket()
        MainServSocket.bind((host, int(port)))
        MainServSocket.listen(1)
    except Exception as e:
        print(f"an error occured while creating the socket : {e}") 
 
    print(f"socket server started on {host}:{port}")


    worker_servers : list[WorkerServer] = extract_workers_config("config.json")
    
    for server in worker_servers:
        while (True):
            print(f"connecting to worker server -> {server} ...")
            connected = server.set_connection()
            if connected:
                print(f"connected to worker server -> {server}\n")   
                break   
            else:
                print(f"connection to worker server {server} failed, retying in 3 seconds \n" )    
            sleep(1)  
                
    print("waiting for client connection...")
    while(True):
        conn, address = MainServSocket.accept()
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