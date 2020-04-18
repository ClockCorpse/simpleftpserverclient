import socket
import threading
import os

def retrFile(name, sock):
    fileNameRecv = sock.recv(1024)
    curDir=os.path.dirname(os.path.abspath(__file__))
    fileLocation = curDir+'/'+fileNameRecv.decode('UTF-8')
    if os.path.isfile(fileLocation):
        sock.send(bytes("EXISTS "+str(os.path.getsize(fileLocation)),'UTF-8'))
        userResponse = sock.recv(1024)
        userResponse = userResponse.decode('UTF-8') 
        if userResponse[:2]=='OK':
            with open(fileLocation,'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send(bytes("ERR ",'UTF-8'))
    sock.close()
def Main():
    host = "0.0.0.0"
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
