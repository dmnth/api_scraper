#! /usr/bin/env python3
import itertools
import requests
import threading
import json
import sys
import os
from time import perf_counter
from threading import Thread
from gen_mmsi import panama_mids
from queue import Queue 
from dataclasses import dataclass
from threads import StoppableThread

# Forgot to shut burp's proxy down :(

URL = 'https://www.vesselfinder.com/api/pub/click/'
HEADERS = {'User-Agent': "Mozilla/5.0"}
FILTER = {
        'types': [
            'unknown',
            'unknown type',
            'other type',
            ],
        'year': [2003],
        }

jobs = Queue()
found_vessels = []
data_file_path= 'scraped_ships/test_2.json'

# TODO: Find proper way to stop threaded script
# Capture disconnect exception
# Find way to store progress if exception arised
# Capture network exceptions and write stuff on disconnect

def make_requests(url, q):
    with open(data_file_path, 'w') as outfile:
        while not q.empty() or len(found_vessels) != 12: 
             digits = q.get()
             response = requests.get(f'{URL}{digits}000', headers=HEADERS)
             if response:
                 vessel = response.json()
                 if vessel['type'].lower() not in FILTER['types']: 
                     # Adding mmsi to vessel info
                     vessel['mmsi'] = int(digits) 
                     vessels_object = json.dumps(vessel)
                     found_vessels.append(vessels_object)
                     print(vessel['name'])
             else:
                print("bad request")
                break




def create_jobs(mid_list):
    for mid in mid_list:
        for job in itertools.product(range(0, 10), repeat=3):
            jobs.put(mid + ''.join(map(str, job)))

        print(mid, jobs.unfinished_tasks)

    print(f'there are {jobs.unfinished_tasks} vessels awaiting to be stored in database')

def get_shit_done():
    for i in range(8):
        worker = StoppableThread(target=make_requests, args=(URL, jobs)) 
        worker.start()
    for i in range(8):
        worker.join()

def read_json(vessel_file):
    with open(vessel_file, 'r') as data:
        vessels = json.load(data)
    return vessels

def write_json(vessel_data):
    vessels_object = json.dumps(found_vessels, indent=4)
    with open('panama_vessels.json', 'w') as outfile:
        outfile.write(vessels_object)

if __name__ == "__main__":
    create_jobs(panama_mids)
    start = perf_counter()
    try:
        print('Starting')
        get_shit_done()
    except KeyboardInterrupt:
        print("writing stuff")
        with open(data_file_path, 'w') as out:
            vessels_object = json.dumps(found_vessels, indent=4)
            out.write(vessels_object)
    end = perf_counter()
    print(f'Today i wasted {end-start:.2f} seconds on MMSI {len(found_vessels)}')
