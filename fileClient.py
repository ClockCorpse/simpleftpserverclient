import socket
import json
from getpass import getpass
import os

def getUserCred():
    name = input('Enter user name: ')
    password = getpass('Enter user password: ')

    credential = {'name':name, 'password':password}

    credentialJson = json.dumps(credential)
    return credentialJson

def login(s,cred):
    s.send(bytes(cred,'UTF-8'))
    data = s.recv(1024)
    data = data.decode('UTF-8')
    if data == 'Valid':
        return True
    if data == 'Invalid':
        return False

def printMenu():
    print('0. Exit the program.')
    print('1. Download a file')
    print('2. Upload a file')

def chooseMenu():
    option = 0
    while True:
        option = int(input('Choose an option: '))
        if 0 <= option and option <= 2:
            break
    return option

def action(sock):
    while True:
        printMenu()
        option = chooseMenu()
        if option == 0:
            sock.close()
            break
        elif option == 1:
            retr(sock) 
        elif option == 2:
            store(sock)


def retr(sock):
    fileName = input('Enter file name ->')
    if fileName !='q':
        sock.send(bytes('get '+fileName,'UTF-8'))
        data = sock.recv(1024).decode('UTF-8')
        if data[:6] == 'EXISTS':
            fileSize = data[6:]
            message = input('File exists '+fileSize+' B, download?(Y/N)-> ')
            if message == 'Y':
                sock.send(bytes('OK','UTF-8'))
                with open(fileName,'wb') as f:
                    data = sock.recv(1024)
                    f.write(data)
                    totalRecv = len(data)
                    while totalRecv < int(fileSize):
                        data = sock.recv(1024)
                        f.write(data)
                        totalRecv +=len(data)
                    print('Download Complete!')
                f.close()
        else:
            print('File does not exists!')

def store(sock):
    fileName = input('Enter file name ->')
    curDir = os.path.dirname(os.path.abspath(__file__))
    fileLocation = curDir+'/'+fileName
    if fileName != 'q':
        if os.path.isfile(fileLocation):
            sock.send(bytes('put '+fileName+','+str(os.path.getsize(fileLocation)),'UTF-8'))
            response = sock.recv(1024).decode('UTF-8')
            if response[:2] == 'OK':
                print('Uploading')
                with open(fileName,'rb') as f:
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
                    while bytesToSend != b'':
                        bytesToSend = f.read(1024)
                        sock.send(bytesToSend)
                print('Upload complete!')
                f.close()
        else:
            print('File does not exists!')




def Main():
    host = input("Enter server's IP address: ")
    port = 5000

    s = socket.socket()
    s.connect((host,port))

    cred = getUserCred()
    if login(s,cred) == True:
        print('Login success!')
        action(s)
    else:
        print('Invalid username or password!')
    s.close()

if __name__ == "__main__":
    Main()


