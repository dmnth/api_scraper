#! /usr/bin/env python3

import itertools
import os
import json
from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

countries = json.load(open('MIDs/n_mids.json', 'r'))

def generate_mmsi(mid_list, repeats, n):
    mid_counter = 0
    for mid in mid_list:
        for mmsi in itertools.product(range(0,10), repeat=repeats):
            yield mid + ''.join(map(str,mmsi))+ '0' * n

for key,value in countries.items():
    with open(f'mmsi_lists/{key}_3_000.txt', 'w') as mmsi:
        lines = generate_mmsi(value, 3, 3)
        for line in lines:
            mmsi.write(line+'\n')

