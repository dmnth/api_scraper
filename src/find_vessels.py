#! /usr/bin/env python3

import itertools
import time
import requests
from threads import StoppableThread
from queue import Queue

# Class for requests, pops url from queue, generates resoponse
# Create function inside vf class that captures generator object,
# set it as target for threaded req ??? profit (DOCUMENTATION)
class ThreadedRequests:

    def __init__(self):
        self.threads = 1 
        self.queue= None 

    def set_jobs_queue(self, queue):
        self.queue = queue

    def set_threads_number(self, threads):
        self.threads = threads 
    
    def make_request(self):
        # Prevent connection reset by peer
        time.sleep(0.01)
        try:
            url = self.jobs.get()
            sys.stdout.write('\r\t{0}/{1}'.format(self.jobs.unfinished_tasks, \
                    self.jobs.unfinished_tasks-self.jobs.qsize()))
            sys.stdout.flush()
            response = requests.get(url)
            if response.status_code == 200:
                yield response
            else:
                msg = f'{response.status_code} occured for {url}'
                print(msg)
        except Exception as err:
            print(err.message, err.args)

    def send_threaded_requests(self, function, threads_num):
        for n in range(threads_num):
            worker = StoppableThread(target=make_request, daemon=True) )
            worker.start()
        for n in range(threads_num):
            worker.join()

class ApiRequests(ThreadedRequests):

    def __init__(self, base_url, wordlist):
        super().__init__()
        self.base_url = base_url
        self.wordlist = wordlist 

    def set_mid_list(self, mid_list):
        self.mid_list = mid_list

    def create_jobs(self, mmsi_file):
        jobs = Queue()
        with open(mmsi_file, 'r') as wl:
            for mmsi in wl:
                jobs.put(self.base_url + '/' + mmsi)
        return jobs
        # Here i will stop to generate wordlists with MMSI numbers.
if __name__ == "__main__":
    queue = Queue()
    res = ApiRequests('someurl', '[somelist]')
    print(res.jobs)
    print(res.threads)
