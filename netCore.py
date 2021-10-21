import config
import requests
import time

def compIP(addr, port):
    comp = "{}:{}".format(addr, port)
    return comp

def decompIP(comp):
    addr, port= comp.split(":")
    return addr, port

def log(msg):
    if config.debugMode:
        print(msg)

def printPlayers(playerList):
    for x in range(0, len(playerList)):
        addr= decompIP(playerList[x])[0]
        r = requests.get('https://api.freegeoip.app/json/{}?apikey={}'.format(addr, config.geoLocateAPI))
        data = r.json()
        lat, long = data['latitude'], data['longitude']
        final = requests.get('http://api.positionstack.com/v1/reverse?access_key={}&query={},{}'.format(config.latLongAPI, lat, long))
        data = final.json()
        print("    [•] Player {}: {} -> {} ({}% Confidence)".format(x+1, playerList[x], data['data'][0]['label'], int(float(data['data'][0]['confidence'])*100)))
        
        if x < len(playerList)-1:
            time.sleep(1)