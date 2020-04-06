import sys
import os
import requests
import time
import datetime
import random
import json
import psutil
# from pylab import imread

old_tx = 0
old_rx = 0

def get_bandwidth():     
    global old_tx, old_rx

    new_tx = psutil.net_io_counters().bytes_sent
    new_rx = psutil.net_io_counters().bytes_recv
    
    tx_rate = (new_tx - old_tx)/1024.*8 #kbps
    rx_rate = (new_rx - old_rx)/1024.*8 #kbps    

    if old_tx + old_rx == 0:
        return_val = (0, 0)
    else:
        return_val = (tx_rate, rx_rate)

    old_rx = new_rx
    old_tx = new_tx
    
    return return_val
    
geolocations = {
    "0": "50.087320, 14.414246",
    "1": "50.087320, 14.414246",
    "2": "50.082192, 14.413627",
    "3": "50.077846, 14.414858",
    "4": "50.073822, 14.414350",
    "5": "50.108863, 8.769267"
}

hostname = sys.argv[1]
pi_id = sys.argv[2]

def main():

    while True:
        send()
        time.sleep(1)
        
def send():    
    url = 'http://%s:9200/rpi-%s/log' % (hostname, pi_id)
    tx_rate, rx_rate = get_bandwidth()
    data = {
        "tx": tx_rate,
        "rx": rx_rate,
        "cpu": psutil.cpu_percent(),
        "location": geolocations[pi_id],       
        "@timestamp": (datetime.datetime.utcnow()).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "name": "PI-"+pi_id
    }
    # print(data)    
    payload = json.dumps(data)
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=payload, headers=headers)
    # print(r.text)

if __name__=="__main__":    
    main()
