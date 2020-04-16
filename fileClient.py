import socket
import os

def Main():
    host = input("Enter server's IP address: ")
    port = 5000

    s = socket.socket()
    s.connect((host,port))

    fileName = input("Enter filename ->")
    if fileName != 'q':
        s.send(bytes(fileName,'UTF-8'))
        data = (s.recv(1024))
        data = data.decode('UTF-8')
        if data[:6]=="EXISTS":
            fileSize = data[6:]
            message = input('File exists,'+fileSize+' B, download? (Y/N)-> ')
            if message == 'Y':
                s.send(bytes('OK','UTF-8'))
                newFileName = 'new_'+fileName
                f = open(newFileName, 'wb')
                data = s.recv(1024)
                totalReceive = len(data)
                f.write(data)
                while totalReceive < int(fileSize):
                    data = s.recv(1024)
                    f.write(data)
                    totalReceive +=len(data)
                    print ("{0:.2f}".format((totalReceive/int(fileSize))*100)+ "% Done")
                print("Download Complete!")
                f.close()
        else:
            print("File does not exists!")
    s.close()

if __name__ == "__main__":
    Main()


