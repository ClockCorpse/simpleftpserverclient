import socket
import threading
import os

def retrFile(name, sock):
    filename = sock.recv(1024)
    #print(filename.decode('UTF-8'))
    if os.path.isfile(filename.decode('UTF-8')):
        sock.send(bytes("EXISTS "+str(os.path.getsize(filename)),'UTF-8'))
        userResponse = sock.recv(1024)
        userResponse = userResponse.decode('UTF-8') 
        if userResponse[:2]=='OK':
            with open(filename,'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR ")
    sock.close()
def Main():
    host = "127.0.0.1"
    port = 5000
    
    s = socket.socket()
    s.bind((host,port))
        
    s.listen(5)
    print('Server Started')

    while True:
        c,addr = s.accept()
        print("client connected ip <"+str(addr)+">")
        t = threading.Thread(target=retrFile, args=("retrThread",c))
        t.start()
    s.close()
        
if __name__ == '__main__':
    Main()
