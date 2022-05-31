from socket import *

HOST = ''
PORT = 8080
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

def loop():
    while True:
        print 'Waiting for connection...'
        tcpCliSock, addr = tcpSerSock.accept()
        print '...connected from :', addr
        while True:
            data = tcpCliSock.recv(BUFSIZ)
            if not data:
                break
            else:
                print 'data: ',data
        tcpSerSock.close()

try:
    loop()
except KeyboardInterrupt:
    tcpSerSock.close()
