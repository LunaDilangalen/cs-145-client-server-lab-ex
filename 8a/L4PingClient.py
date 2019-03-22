import socket
from time import time

UDP_IP_ADDRESS = "127.0.0.1" # server IP address
UDP_PORT_NO = 6790  # server port number

Message = "rasenshuriken"

clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSock.bind(('', 6780))

for i in range(3):
    start = 0
    end = 0
    clientSock.sendto('%d'%(i+1), (UDP_IP_ADDRESS, UDP_PORT_NO))
    start = time()
    print 'PING %s:%s' %(UDP_IP_ADDRESS, UDP_PORT_NO)
    while True:
        data, addr = clientSock.recvfrom(1024) # receive message from server
        end = time()
        final = end-start
        if(data == '%d'%(i+1) and addr[0] == UDP_IP_ADDRESS):
            print '%s bytes from %s: seq=%s time=%f ms' %(str(len(data)), str(addr[0]), data, final*1000)
            break
        if(end >= start + 1):
            print "LOST | || || |_"
            break
