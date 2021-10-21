import requests
import config

playerList= ["172.217.164.4:443"]

def decompIP(comp):
    addr, port= comp.split(":")
    return addr, port

for x in range(0, len(playerList)):
    addr= decompIP(playerList[x])[0]
    print('https://api.freegeoip.app/json/{}?apikey={}'.format(addr, config.geoLocateAPI))
    r = requests.get('https://api.freegeoip.app/json/{}?apikey={}'.format(addr, config.geoLocateAPI))
    data = r.json()
        
    print(r)