#! /usr/bin/env python3
import itertools
import requests
import threading
from time import perf_counter
from threading import Thread
from gen_mmsi import panama_mids
from queue import Queue 

URL = 'https://www.vesselfinder.com/api/pub/click/'
HEADERS = {'User-Agent': "Mozilla/5.0"}

jobs = Queue()
found_vessels = []

def make_requests(url, q):
    counter = 0
    while not q.empty():
         response = requests.get(f'{URL}{q.get()}000', headers=HEADERS)
         found_vessels.append(response.content)
         counter += 1
         if counter == 34:
             return 

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


if __name__ == "__main__":
    create_jobs(panama_mids)
    start = perf_counter()
    res = get_shit_done()
    print(res)
    end = perf_counter()
    print(f'Today i wasted {end-start:.2f} seconds on MMSI {len(found_vessels)}')

