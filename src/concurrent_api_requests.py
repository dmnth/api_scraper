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

# It is easyer to update small separate files 
# than huge-ass dict-styled-json abomination mf
# Countries with small or non-commercial fleet 
# will be filtered out.

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

data_file_path= 'panama_vessels.json'
vessels_by_country = {
                        'country_nam':[
                                        {
                                        'imo': 234223,
                                        'name': 'vesselname',
                                        'year': 1993
                                            },
                                        {
                                            'imo': 123121,
                                            'name': 'namesone',
                                            'year': 1923
                                            }
                                        ],
                        'seconde country name': [
                            {
                                'imo': 324234223,
                                'name': 'asdada'
                                },
                            ]
                        }


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
found_vessels = []

def make_requests(url, q):
    # sleep is here to prevent ConnectionResetError
    # for server is sometimes not ready to respond
    time.sleep(0.01)
    try:
         digits = q.get()
         sys.stdout.write('\r\t{1}/{0}'.format(q.unfinished_tasks, q.unfinished_tasks-q.qsize()))
         sys.stdout.flush()
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
            print("\nBad request")
    except ConnectionResetError as err:
        print(f'well fuck, reset on {len(vessels)} vessel')



def vessel_type_counter(queue):
    # Curses(front-end comes later) module stuff goes here 
    for vessel in make_requests(URL, queue):
        t = vessel['type'].lower()
        if t in common_types.keys():
            common_types[t] += 1
        else:
            common_types[t] = 1


def create_jobs(queue, mid_list, repeats=3):
    for mid in mid_list:
        for job in itertools.product(range(0, 10), repeat=repeats):
            queue.put(mid + ''.join(map(str, job)))

def set_vessel_types():
    with open('common_vessel_types.json', 'r') as smth:
        data = smth.loads()


def start_threads(queue):
    for i in range(10):
        # Setting daemon to true for prettyer output ^_^
        worker = StoppableThread(target=vessel_type_counter, args=(queue,), daemon=True) 
        worker.start()
    for i in range(10):
        worker.join()

def write_data(out_file, vessel_object):
    with open(out_file, 'w') as out:
        out.write(vessel_object)
        out.close()

def write_vessel_types(common_types_object):
    with open('common_vessel_types.json', 'w') as out_1:
        out_1.write(common_types_object)
        out_1.close()


def get_vessel_data(country_ids, out_file, repeats=3):
    jobs_q = Queue()
    create_jobs(jobs_q, country_ids, repeats)
    start = perf_counter()
    print(f'[+] Total possible inmarsat carriers: {jobs_q.unfinished_tasks}')
    common_types_object = json.dumps(common_types, indent=4)
    # This is considered a bad practice
    # Consider refactoring this mess to a separate class
    # later. 
    # Global variable is used to set list to empty
    # after every iteration, so contents wont get written
    # to json all at once every time.
    global found_vessels
    vessels_found = len(found_vessels) 
    
    try:
        print('[+] Sending requests:')
        while not jobs_q.empty():
            start_threads(jobs_q)
        if found_vessels:
            vessels_object = json.dumps(found_vessels, indent=4)
            write_data(out_file, vessels_object)
            vessels_found = len(found_vessels)
            found_vessels = []
        write_vessel_types(common_types_object)

    except KeyboardInterrupt:
        write_vessel_types(common_types_object)
        if found_vessels:
            vessels_object = json.dumps(found_vessels, indent=4)
            write_data(out_file, vessels_object)

    end = perf_counter()
    print(f'\n\n Found {vessels_found} vessels in {end-start:.2f} seconds\n\n#############################################\n')


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
