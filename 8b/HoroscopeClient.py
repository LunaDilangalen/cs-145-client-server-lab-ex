import socket

TCP_IP_SERVER = '127.0.0.1'
TCP_PORT_SERVER = 58900



clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect((TCP_IP_SERVER, TCP_PORT_SERVER))
# clientsocket.bind(('', 58901))
while True:
  message = raw_input()
  clientsocket.send(message)
  data = clientsocket.recv(512)
  clientsocket.close()
  if data == 'q':

    break
  else:

    print data
