
import sys 
import getopt
import json

def open_json(path : str):
     with open(path, "r", encoding='utf-8') as read_file:
           dico = json.loads(read_file.read())
           return dico

def dump_json(path : str, dico):
    with open(path, "w") as write_file:
        json.dump(dico, write_file)

        
def getParams():
    try:
        opts,args = getopt.getopt(sys.argv[1:],"h:p:n:",["host=","port=","name="])
        
    except getopt.GetoptError as e:
        print(e.msg)
        sys.exit(-1)
    
    host = ""
    port = ""
    name = ""
    for opt,arg in opts:
        if(opt in ("-h","--host")):
            host = arg
        elif(opt in ("-p","--port")):
            port = arg
        elif(opt in ("-n","--name")):
            name = arg
        
    return host,port,name

