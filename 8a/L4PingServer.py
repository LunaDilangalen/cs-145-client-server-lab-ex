
import socket

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverSock.bind(('', 6790))

while True:
  data, addr = serverSock.recvfrom(1024)

  if(data):
      print data
      serverSock.sendto(data, (addr[0], 6780))
