#! /usr/bin/env python3
import itertools
import requests
import threading
import json
import sys
from time import perf_counter
from threading import Thread
from gen_mmsi import panama_mids
from queue import Queue 
from dataclasses import dataclass

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
outfile = 'scraped_ships/test.json'

# TODO: Find proper way to stop threaded script
# Capture disconnect exception
# Find way to store progress if exception arised

def make_requests(url, q):
    counter = 0
    with open(outfile, 'w') as file:
            while not q.empty() and is_running == True:
                try:
                     digits = q.get()
                     print(digits)
                     response = requests.get(f'{URL}{digits}000', headers=HEADERS)
                     if response:
                         vessel = response.json()
                     if vessel['type'].lower() not in FILTER['types']: 
                         # Adding mmsi to vessel info
                         vessel['mmsi'] = int(digits) 
                         found_vessels.append(vessel)
                         # print(vessel['type'], vessel['name'])
                except KeyboardInterrupt:
                    break


def create_jobs(mid_list):
    for mid in mid_list:
        for job in itertools.product(range(0, 10), repeat=3):
            jobs.put(mid + ''.join(map(str, job)))

        print(mid, jobs.unfinished_tasks)

    print(f'there are {jobs.unfinished_tasks} vessels awaiting to be stored in database')

def get_shit_done():
    if stop_threads == True:
        return
    for i in range(3):
        print(jobs)
        worker = threading.Thread(target=make_requests, args=(URL, jobs)) 
        worker.start()
    for i in range(3):
        worker.join()

def read_json(vessel_file):
    with open(vessel_file, 'r') as data:
        vessels = json.load(data)
    return vessels

def write_json(vessel_data):
    with open('panama_vessels.json', 'w') as outfile:
        outfile.write(vessel_data)



if __name__ == "__main__":
    create_jobs(panama_mids)
    start = perf_counter()
    stop_threads = False
    try:
        print('Starting')
        get_shit_done()
    except KeyboardInterrupt:
        stop_threads = True
        print("writing stuff")
        with open(outfile, 'w') as file:
            vessels_object = json.dumps(found_vessels, indent=4)
            file.write(vessels_object)
        
        
    end = perf_counter()
    print(f'Today i wasted {end-start:.2f} seconds on MMSI {len(found_vessels)}')
