#! /usr/bin/env python3

import os
import sys
import time
import json
from queue import Queue
from config import config
from time import perf_counter
from threads import ResponseGenerator, RequestsThread 


# Class for requests, pops url from queue, generates resoponse
# Create function inside vf class that captures generator object,
# set it as target for threaded req ??? profit (DOCUMENTATION)

class ApiRequests:

    def __init__(self, base_url, *args):
        super().__init__()
        self.base_url = base_url
        self.wordlists = args 
        self.jobs = Queue()
        self.jobs_q = []

    def create_jobs(self):

        if len(self.wordlists) == 1:
            with open(self.wordlists[0], 'r') as wordlist:
                for word in wordlist:
                    job = self.base_url + word.rstrip()
                    self.jobs.put(job)

        elif len(self.wordlists) > 1:
            for wl in self.wordlists:
                new_q = Queue()
                with open(wl, 'r') as wordlist:
                    for word in wordlist:
                        job = self.base_url + word.rstrip()
                        new_q.put(job)
                    self.jobs_q.append(new_q)

        else: 
            print('No wordlists provided')
            sys.exit()
    
    def parse_args(self):
        if len(self.wordlists) > 1:
            print('MULTILIST')
        elif len(self.wordlists) == 1:
            print('SINGLE FILE')
        else:
            print('NO FILE')

    def gather_results(self):
        results = []
        print('##########################################')
        print('Gatherting data: ')
        start = perf_counter()
        while not self.jobs.empty():
            try:
                response = ResponseGenerator(50, RequestsThread, self.jobs)
                results.extend(list(response))
            except Exception as err:
                print(err, err.args)
                sys.exit()
        
        end = perf_counter()
        print(f'\nEehrmarhge garhered {len(results)} objects in {end-start:.2f} seconds\n\n################')
        print(results[-1])
        yield results

    def do_stuff_with_results(self):
        # For every country in input write separate file
        for result in self.gather_results():
            print(result[-1])

    def write_json(self, results, filepath):
        vessels = json.dumps(results, indent=4)
        with open(filepath, 'w') as out:
            out.write(vessels)
            out.close()



if __name__ == "__main__":
    country = 'Tuvalu'
    country_2 = 'Spain'
    config = config['default']
    url = config.URL
    print(url)
    tuvalu_mmsi_list = config.WORDLISTS_COUNTRY + country + '_3_000.txt'
    spain_mmsi_list = config.WORDLISTS_COUNTRY + country_2 + '_3_000.txt'

    miner = ApiRequests(url, tuvalu_mmsi_list, spain_mmsi_list)
    miner.parse_args()
    miner.create_jobs()
    miner.do_stuff_with_results()
