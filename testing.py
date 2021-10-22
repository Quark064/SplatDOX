import socket, random

test = "10.0.0.1"
test2 = 7778
test3 = (test, test2)

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creates a socket
bytes=random._urandom(1024)

sock.sendto(bytes,(test3))