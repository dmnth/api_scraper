#! /usr/bin/env python3

import itertools
import os
import json
from config import config

basedir = os.path.abspath(os.path.dirname(__file__))


class MMSIgen:

    def generate_mmsi(mid_list, repeats, n):
        for mid in mid_list:
            for mmsi in itertools.product(range(0,10), repeat=repeats):
                yield mid + ''.join(map(str,mmsi))+ '0' * n
    
    def write_separate_files(self, repeats, n):
        if os.path.exists():
            return
        for key,value in countries.items():
            with open(f'mmsi_lists/by_country/{key}_{repeats}_{"0" * n}.txt', 'w') as m:
                for mid in value:
                    for mmsi in itertools.product(range(0,10), repeat=repeats):
                        line = mid + ''.join(map(str,mmsi))+ '0' * n
                        m.write(line+'\n')
            m.close()

    def write_master_file(self, repeats, n):
        if os.path.exists():
            return
        with open(f'mmsi_lists/by_country/{key}_{repeats}_{"0" * n}.txt', 'w') as m:
            for key,value in countries.items():
                for mid in value:
                    for mmsi in itertools.product(range(0,10), repeat=repeats):
                        line = mid + ''.join(map(str,mmsi))+ '0' * n
                        m.write(line+'\n')
        m.close()

if __name__ == "__main__":
    countries = json.load(open('MIDs/n_mids.json', 'r'))
    gen = MMSIgen()
    gen.write_separate_files(5, 1)

