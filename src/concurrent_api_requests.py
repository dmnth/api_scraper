#! /usr/bin/env python3
import itertools
import requests
import threading
import json
from time import perf_counter
from threading import Thread
from gen_mmsi import panama_mids
from queue import Queue 

URL = 'https://www.vesselfinder.com/api/pub/click/'
HEADERS = {'User-Agent': "Mozilla/5.0"}
FILTER = {
        'types': [
            'unknown',
            'unknown type',
            ],
        'year': [2003],
        }

jobs = Queue()
found_vessels = []
outfile = '/media/postgres-data/vessels.json'

def make_requests(url, q):
    counter = 0
    with open(outfile, 'w') as file:
        while not q.empty():
             response = requests.get(f'{URL}{q.get()}000', headers=HEADERS)
             if response:
                 vessel = response.json()
             if vessel['type'].lower() not in FILTER['types']: 
                 found_vessels.append(vessel)
                 print(vessel['type'], vessel['name'])
        vessels_object = json.dumps(found_vessels, indent=4)
        file.write(vessels_object)

def create_jobs(mid_list):
    for mid in mid_list:
        for job in itertools.product(range(0, 10), repeat=3):
            jobs.put(mid + ''.join(map(str, job)))

        print(mid, jobs.unfinished_tasks)

    print(f'there are {jobs.unfinished_tasks} vessels awaiting to be stored in database')

def get_shit_done():
    for i in range(3):
        worker = threading.Thread(target=make_requests, args=(URL, jobs)) 
        worker.start()
    for i in range(3):
        worker.join()

def write_json(vessel_data):
    with open('panama_vessels.json', 'w') as outfile:
        outfile.write(vessel_data)




if __name__ == "__main__":
    create_jobs(panama_mids)
    start = perf_counter()
    try:
        get_shit_done()
    except:
        print("writing stuff")
        with open(outfile, 'w') as file:
            vessels_object = json.dumps(found_vessels, indent=4)
            file.write(vessels_object)
        
    end = perf_counter()
    print(found_vessels)
    print(f'Today i wasted {end-start:.2f} seconds on MMSI {len(found_vessels)}')

