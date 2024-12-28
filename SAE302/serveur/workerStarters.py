import os
import commons as c
import threading
import sys

def startWorker(host,port,name):
    os.system(f"python WorkerServer.py -h {host} -p {port} -n {name}")
    sys.exit(1)
    
if __name__ == "__main__":
    dict = c.open_json("config.json")["servers"]
    for s in dict:
        t = threading.Thread(target=startWorker,args=[s['host'],s['port'],s['name']])
        t.start()   
