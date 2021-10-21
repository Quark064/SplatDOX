import pyshark
import netCore, config

log = netCore.log
compIP = netCore.compIP

if config.useFile:
    log("[•] Using File For Packet Capture")
    cap = pyshark.FileCapture(config.fileName)
    log("[•] Loading File Into Memory...")
    cap.load_packets()
    log("[•] Imported (P)CAP File!")
else:
    log('[+] Starting Capture...')
    capture = pyshark.LiveCapture(interface=config.interfaceName)
    PacketRecieved = capture.apply_on_packets

try:
    playersInMatch = int(input("[?] How Many Players Are In The Match: "))
except ValueError:
    print("[-] Invalid Input, Defaulting to 8...")
    playersInMatch = 8

finished = False



ipList = {}
canidateList = []

def findUsers():
    x = 0
    global finished
    sortedList = dict(sorted(ipList.items(), key=lambda item: item[1], reverse=True))
    log("[•] User Dictionary Count Reads: {}".format(str(sortedList)))
    sortedList = list(sortedList.keys())
    while x < playersInMatch-1:
        canidateList.append(sortedList[x])
        x += 1
    finished = True

def feedbackLoop(packet):
    if packet.highest_layer in config.acceptedProtocols:
        
        if packet.ip.src != config.switchIP:
            return
        
        try:
            dstAddr = packet.ip.dst
            dstPort = packet[packet.transport_layer].dstport
        except AttributeError:
            return

        compress = compIP(dstAddr, dstPort)
        
        if compress not in ipList:
            ipList[compress] = 0
            log('[•] Located New Entity At {}'.format(compress))
        else:
            if ipList[compress] >= config.packetThreshold:
                log("[+] Packet Threshold Reached! ({} With {} Packets)".format(compress, ipList[compress]))
                findUsers()
                return
            ipList[compress] += 1

# PacketRecieved(feedbackLoop)
for x in range(0, len(cap)):
    if finished:
        break
    feedbackLoop(cap[x])

print("[+] Located Players!")
print("[•] Attempting to GeoLocate...")
netCore.printPlayers(canidateList)