import socket

name = 'Datuluna Ali Dilangalen'
sn = '2015-04685'
section = 'MYZ-XCLNCE'

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(("127.0.0.1", 58913))
clientsocket.send('%s, %s, CS 145 %s'%(name, sn, section))
