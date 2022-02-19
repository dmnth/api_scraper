#! /usr/bin/env python3

import os
import time
import requests
import itertools
from queue import Queue
from config import config
from time import perf_counter
from threads import ResponseGenerator, RequestsThread 


# Class for requests, pops url from queue, generates resoponse
# Create function inside vf class that captures generator object,
# set it as target for threaded req ??? profit (DOCUMENTATION)

class ApiRequests:

    def __init__(self, base_url, wordlist):
        super().__init__()
        self.base_url = base_url
        self.wordlist = wordlist 
        # itertools chain multiple wordlists together
        self.jobs = Queue()

    def create_jobs(self):
        with open(self.wordlist, 'r') as wl:
            for word in wl:
                job = self.base_url + word.rstrip()
                self.jobs.put(job)

    def gather_results(self):
        results = []
        print('##########################################')
        print('Gatherting data: ')
        start = perf_counter()
        while not self.jobs.empty():
            try:
                responses1 = ResponseGenerator(10, RequestsThread, self.jobs)
                responses2 = ResponseGenerator(10, RequestsThread, self.jobs)
                responses3 = ResponseGenerator(10, RequestsThread, self.jobs)
                responses4 = ResponseGenerator(10, RequestsThread, self.jobs)
                responses5 = ResponseGenerator(10, RequestsThread, self.jobs)
                results.extend(list(itertools.chain(responses1, responses2, responses3, responses4, responses5)))
            except Exception as err:
                print(err, err.args)
            except KeyboardInterrupt as en:
                print('\n (-_-) TODO: Spawn OKAYEST amount of processes, prevent data loss')
        
        end = perf_counter()
        print(f'ehrmarhge garhered {len(results)} data in {end-start:.2f} seconds\n\n################')

        print(len(results) == 2000)
        print(results[-1])


if __name__ == "__main__":
    country = 'Tuvalu'
    config = config['default']
    url = config.URL
    print(url)
    tuvalu_mmsi_list = config.WORDLISTS_COUNTRY + country + '_3_000.txt'
    miner = ApiRequests(url, tuvalu_mmsi_list)
    miner.create_jobs()
    miner.gather_results()
