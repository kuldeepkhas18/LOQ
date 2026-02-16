

# to run LOQ
import multiprocessing


def startLOQ():
        # code for process 1
        print("Process 1 is running.")
        from main import start
        start()

# to run hotword
def listenHotword():
        #code for process 2
        print("process 2 is running.")
        from engine.features import hotword
        hotword()


        # start both processes
if __name__ == '__main__':
       p1 = multiprocessing.Process(target=startLOQ)
       p2 = multiprocessing.Process(target=listenHotword)
       p1.start()
       p2.start()
       p1.join()
 
       if p2.is_alive():
           p2.terminate()
           p2.join()

       print("system stop")


       
 