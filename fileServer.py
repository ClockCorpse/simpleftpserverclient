import socket
import threading
import os
import json

def checkUser(sock):
    #TODO: get user credential
    cred = str(sock.recv(1024).decode('UTF-8'))
    cred = json.loads(cred)
    userName = cred['name']
    userPswd = cred['password']
    currDir = os.path.dirname(__file__)
    userDir = currDir + '//user//user.json'
    print(userDir) 
    with open(userDir) as jsonFile:
        data=json.load(jsonFile)
        for user in data:
            if user['name'] == userName:
                if user['password'] == userPswd:
                    return 1
                else:
                    return 0


def retrFile(fileName, sock):
    #print(filename.decode('UTF-8'))
    if os.path.isfile(fileName):
        sock.send(bytes("EXISTS "+str(os.path.getsize(fileName)),'UTF-8'))
        userResponse = sock.recv(1024)
        userResponse = userResponse.decode('UTF-8') 
        if userResponse[:2]=='OK':
            with open(fileName,'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR ")
    sock.close()

def storFile(fileName,fileSize,sock):
    with open(fileName,'wb')as f:
        sock.send(bytes('OK','UTF-8'))
        data = sock.recv(1024)
        f.write(data)
        totalRecv = len(data)
        while totalRecv < int(fileSize):
            data = sock.recv(1024)
            f.write(data)
            totalRecv +=len(data)
    f.close()
    sock.send(bytes('Upload Completed!','UTF-8'))

def clientHandler(name,sock):
    validUser = checkUser(sock)
    if validUser == 1:
        sock.send(bytes('Valid','utf-8'))
        while True:
            cmd = str(sock.recv(1024).decode('UTF-8'))
            if(cmd[:3]) == 'get':
                fileName = cmd[4:]
                retrFile(fileName,sock)
            elif(cmd[:3]) == 'put':
                cmd = cmd[4:].split(',')
                fileName = cmd[0]
                fileSize = cmd[1]
                if fileName == '':
                    sock.send(bytes('ERR','UTF-8'))
                else:
                    storFile(fileName,fileSize,sock)
            elif cmd[:3]=='ext':
                sock.send(bytes('Goodbye!','UTF-8'))
                sock.close()
                return
            else:
                sock.send(bytes('ERR','UTF-8'))
    else:
        sock.send(bytes('Invalid','UTF-8'))
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
        t = threading.Thread(target=clientHandler, args=("retrThread",c))
        t.start()
    s.close()
        
if __name__ == '__main__':
    Main()

