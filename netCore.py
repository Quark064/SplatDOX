import config
import requests
import time

# Compresses IP address and port into a single string.
def compIP(addr, port):
    comp = "{}:{}".format(addr, port)
    return comp

# Decompresses ip address and port from a single string.
# Returns two variables: IP address and port.
def decompIP(comp):
    addr, port= comp.split(":")
    return addr, int(port)

# Prints messages to console. Messages printed by this function can be hidden by the config file.
def log(msg):
    if config.debugMode:
        print(msg)

# Recieves the sorted player list and gathers the IP location.
def printPlayers(playerList):
    for x in range(0, len(playerList)):
        
        # Gets the lat/long of a specified IP address.
        addr = decompIP(playerList[x])[0]
        r = requests.get('https://api.freegeoip.app/json/{}?apikey={}'.format(addr, config.geoLocateAPI))
        data = r.json()
        lat, long = data['latitude'], data['longitude']
        
        # Returns the physical location of a specified lat/long.
        final = requests.get('http://api.positionstack.com/v1/reverse?access_key={}&query={},{}'.format(config.latLongAPI, lat, long))
        data = final.json()
        ipaddr, port = decompIP(playerList[x])
        
        # Prints gathered information to the console with padding.
        print("    [•] Player {}: {:18s}{} -> {} ({}% Confidence)".format(x+1, ipaddr, port, data['data'][0]['label'], int(float(data['data'][0]['confidence'])*100)))
        
        # Sleeps for a specified amount of time to prevent API rate limiting.
        if x < len(playerList)-1:
            time.sleep(1)
