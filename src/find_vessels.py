#! /usr/bin/env python3

import os
import sys
import time
import json
from queue import Queue
from config import config
from time import perf_counter
from threads import ResponseGenerator, RequestsThread 


# Class for requests, pops url from queue, generates response
# Create function inside vf class that captures generator object,
# set it as target for threaded req ??? profit (DOCUMENTATION)

class ApiRequests:

    def __init__(self, base_url, *args):
        super().__init__()
        self.base_url = base_url
        self.wordlists = list(args) 
        self.jobs = Queue()
        self.vessels_found = 0

    def get_jobs_done(self):

        if len(self.wordlists) >= 1:
            for wl in self.wordlists:
                with open(wl, 'r') as wordlist:
                    for word in wordlist:
                        job = self.base_url + word.rstrip()
                        self.jobs.put(job)
                        if self.jobs.unfinished_tasks == 20:
                            self.save_results_json('test.json')

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
        while not self.jobs.empty():
            try:
                response = ResponseGenerator(20, RequestsThread, self.jobs)
                yield list(response)
            except Exception as err:
                print(err, err.args)
                sys.exit()

    def sanitize_results(self):
        filtered_result = []
        for result in self.gather_results():
            for element in result:
                try:
                    if element['type'].lower() not in config.FILTER['blacklist'] \
                            and element['imo'] != 0 and element != None:
                                filtered_result.append(element)
                except TypeError as err:
                    print('Because of connection reset/(502 error) NoneType got into list')
        if len(filtered_result) != 0:
            self.vessels_found += len(result)
            print(f'Vessels found: {self.vessels_found}')
            yield filtered_result
                            

    def save_results_json(self, filepath):
        with open(filepath, 'a') as out:
            for result in self.sanitize_results():
                vessels = json.dumps(result, indent=4)
                out.write(vessels)
        out.close()
    
    def save_results_txt(self, path):
        pass

    def save_results_csv(self, path):
        pass




if __name__ == "__main__":
    country = 'Tuvalu'
    country_2 = 'Spain'
    config = config['default']
    url = config.URL
    print(url)
    tuvalu_mmsi_list = config.WORDLISTS_COUNTRY + country + '_3_000.txt'
    spain_mmsi_list = config.WORDLISTS_COUNTRY + country_2 + '_3_000.txt'
    huge_list = config.WORDLISTS_MASTER + 'longlist_3_000.txt'
    write_file = 'test.json'

    miner = ApiRequests(url, huge_list)
    miner.parse_args()
    while True:
        miner.get_jobs_done()
