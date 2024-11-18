import threading
from time import sleep


def task(i,task_range):
    for x in range(task_range,0,-1):
        print(f"thread {i} index : {x}")
        sleep(0.5)
    
def main():
    threads = []
    for i in range(2):
        T = threading.Thread(target=task,args=[i,(i+1)*2])
        T.start()
        threads.append(T)

    for t in threads:
        t.join()
    
if __name__ == "__main__":
    main()