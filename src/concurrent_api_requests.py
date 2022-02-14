#! /usr/bin/env python3
import itertools
import requests
import json
import sys
import time
import curses
from time import perf_counter
#from gen_mmsi import panama_mids
from queue import Queue 
from threads import StoppableThread
from enum_mmsi import panama_mids

URL = 'https://www.vesselfinder.com/api/pub/click/'
HEADERS = {'User-Agent': "Mozilla/5.0"}
FILTER = {
        'types_restrict': [
            'unknown',
            'unknown type',
            'other type',
            'pleasure craft',
            'sailing vessel',
            'military ops',
            'tug',
            ],
        'types_allowed': [
            'Fishing Vessel',
            ],
        'year': [
            2003
            ],
        }

jobs = Queue()
found_vessels = []
data_file_path= 'cli_test_2.json'

# TODO: Find proper way to eaded script
# Capture disconnect exception
# Find way to store progress if exception arised
# Capture network exceptions and write stuff on disconnect

# This script generates decartian product len(3) range(0, 10) and 
# add it as part of mmsi number to a pre-made format string,
# that is same fro vessels equipped with inmarsat earth station
# that supports services B, C or M

# Returns legit mmsi number as result
common_types = {
        'crude oil tanker': 0,
        'bulk carrier': 0,
        'fishing vessel': 0,
        'container ship': 0,
        'general cargo ship': 0,
        }


vessel_types = []
def make_requests(url, q):
    while not q.empty() or len(found_vessels) != 12: 
         digits = q.get()
         response = requests.get(f'{URL}{digits}000', headers=HEADERS)
         if response:
             vessel = response.json()
             # Right now dont add length/width sorting.
             if vessel['type'].lower() not in FILTER['types_restrict'] and vessel['imo'] !=0: 
                 # Adding mmsi to vessel info
                 vessel['mmsi'] = int(digits) 
                 found_vessels.append(vessel)
                 yield vessel
         else:
            print("bad request")
            break



def vessel_type_counter():
    # Curses(front-end comes later) module stuff goes here 
    for vessel in make_requests(URL, jobs):
        t = vessel['type'].lower()
        if t in common_types.keys():
            common_types[t] += 1
        else:
            common_types[t] = 1
        yield common_types

def print_common_types():
    for taip in vessel_type_counter():
        sys.stdout.write(f"Tankers: {taip['crude oil tanker']}")
        sys.stdout.flush()




def create_jobs(mid_list, repeats=3):
    for mid in mid_list:
        for job in itertools.product(range(0, 10), repeat=repeats):
            jobs.put(mid + ''.join(map(str, job)))

def start_threads():
    for i in range(10):
        # Setting daemon to true for prettyer output ^_^
        worker = StoppableThread(target=vessel_type_counter, daemon=True) 
        worker.start()
    for i in range(10):
        worker.join()

def get_vessel_data(country_ids, out_file, repeats=3):
    create_jobs(country_ids, repeats)
    start = perf_counter()
    print(f'[+] Total possible inmarsat carriers: {jobs.unfinished_tasks}')
    print(common_types)
    try:
        print('[+] Sending requests')
        start_threads()
        print_common_types()
    except KeyboardInterrupt:
        print("\nwriting stuff")
        vessels_object = json.dumps(found_vessels, indent=4)
        common_types_object = json.dumps(common_types, indent=4)
        with open(out_file, 'w') as out:
            out.write(vessels_object)
            out.close()
        with open('common_vessel_types.txt', 'w') as out_1:
            out_1.write(common_types_object)
            out_1.close()
    end = perf_counter()
    print(f' Found {len(found_vessels)} vessels in {end-start:.2f} seconds')


def read_json(vessel_file):
    with open(vessel_file, 'r') as data:
        vessels = json.load(data)
    return vessels

def write_json(file_name, vessel_data):
    vessels_object = json.dumps(found_vessels, indent=4)
    json.dump(vessels_object, out_file)
    with open('panama_vessels.json', 'w') as outfile:
        outfile.write(vessels_object)

if __name__ == "__main__":
    get_vessel_data(panama_mids, data_file_path, 3)
