#! /usr/bin/env python3

import itertools
import time
import requests
import os
from queue import Queue
from threading import Thread
from threads import ResponseGenerator 
from config import config


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

    def create_jobs_all(self):
        with open(self.wordlist, 'r') as wl:
            for word in wl:
                job = self.base_url + word.rstrip()
                self.jobs.put(job)

    def gather_results(self):
        while not self.jobs.empty():
            responses = ResponseGenerator(10, self.jobs)


if __name__ == "__main__":
    country = 'Tuvalu'
    config = config['default']
    url = config.URL
    print(url)
    wordlist_dir = config.WORDLISTS_COUNTRY
    tuvalu_mmsi = wordlist_dir + country + '_3_000.txt'
    api = ApiRequests(url, tuvalu_mmsi)
    api.create_jobs_all()
    api.gather_results()
