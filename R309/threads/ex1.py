import threading
from time import sleep
def task(i):
    for x in range(0,5):
        print(f"thread {i} index : {x}")
        sleep(0.5)
    
def main():
    threads = []
    for i in range(2):
        T = threading.Thread(target=task,args=[i])
        T.start()
        threads.append(T)

    for t in threads:
        t.join()
    
if __name__ == "__main__":
    main()