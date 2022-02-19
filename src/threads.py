#! /usr/bin/env python3

from threading import Thread
from queue import Queue
import time
import sys
import requests
from config import config

config = config['default']

class RequestsThread(Thread):

    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.response = None 

    def run(self):
        # Prevent connection reset by peer
        time.sleep(0.01)
        try:
            url = self.queue.get()
            sys.stdout.write('\r\t{0}/{1}'.format(self.queue.unfinished_tasks, \
                    self.queue.unfinished_tasks-self.queue.qsize()))
            sys.stdout.flush()
            response = requests.get(url, headers=config.HEADERS)
            if response.status_code == 200:
                self.response = response
            else:
                msg = f'{response.status_code} occured for {url}'
                print(msg)
        except Exception as err:
            print(err.args)

class ResponseGenerator(object):

    def __init__(self, num_threads, custom_thread, queue): 
        self.num_threads = num_threads
        self.threads = []
        self.position = 0
        self.custom_thread = custom_thread

        # Create some threads
        for i in range(num_threads):
            t = self.custom_thread(queue) 
            t.start()
            self.threads.append(t)

    def __iter__(self):
        return self

    def __next__(self):
        if self.position >= self.num_threads:
            raise StopIteration

        t = self.threads[self.position]
        self.position += 1

        t.join()
        return t.response

if __name__ == "__main__":
    print(config.HEADERS)
























