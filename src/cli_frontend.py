#! /usr/bin/env python3

import sys
import time
import json

with open('estonia.json', 'r') as out:
    data = json.load(out)

types = {}


for el in data:
    if el['type'] not in types.keys():
        types[el['type']] = 1
    else:
        types[el['type']] += 1        
    if 'Fishing Vessel' in types.keys():
        sys.stdout.write("\r[+] Fishing vessels: {0}".format(types['Fishing Vessel']))
        sys.stdout.flush()
        time.sleep(0.5)
       



'''
for i in range(10):
    sys.stdout.write("\r{0}>".format("="*i))
    sys.stdout.flush()
    time.sleep(1)
print(data)
'''
