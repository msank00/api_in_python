import threading, time

def f():
    print "f started"
    time.sleep(3)
    print "f finished"
    
threading.Thread(target=f).start()
