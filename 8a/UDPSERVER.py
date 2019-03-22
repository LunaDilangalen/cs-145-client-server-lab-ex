import socket

serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverSock.bind(('', 6788))

while True:
  data, addr = serverSock.recvfrom(1024)
  print data
