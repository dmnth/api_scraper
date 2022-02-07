#! /usr/bin/env python3

import threading

class StoppableThread(threading.Thread):
    # Thread class with stop method,
    # Checks regularly for stopped condition

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


if __name__ == "__main__":
    stoppie = StoppableThread()
