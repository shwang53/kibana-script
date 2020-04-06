import sys
import os
import requests
import time
import datetime
import random
import json
# from pylab import imread

import pprint
pp = pprint.PrettyPrinter(indent=4)

geolocations = {
    "0": "50.087320, 14.414246",
    "1": "50.087320, 14.414246",
    "2": "50.082192, 14.413627",
    "3": "50.077846, 14.414858",
    "4": "50.073822, 14.414350",
    "5": "50.108863, 8.769267"
}

def mapping():

    for k, v in geolocations.items():
        url = 'http://athena.cs.illinois.edu:9200/rpi-'+k
        data = \
        {
            "mappings": {
                "log": {
                    "properties": {
                        "location": {
                            "type": "geo_point"
                        }
                    }
                }        
            }
        }

        payload = json.dumps(data)    
        headers = {'content-type': 'application/json'}        
        r = requests.put(url, data=payload, headers=headers)
        print(r.text)

if __name__=="__main__":    
    mapping()        