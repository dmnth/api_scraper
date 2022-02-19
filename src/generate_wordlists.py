#! /usr/bin/env python3

import itertools
import os
import json
from config import config

basedir = os.path.abspath(os.path.dirname(__file__))
config = config['default']
wordlist_master_dir = config.WORDLISTS_MASTER


class MMSIgen:
    
    countries = json.load(open('MIDs/n_mids.json', 'r'))

    def _generate_mmsi(mid_list, repeats, n):
        for mid in mid_list:
            for mmsi in itertools.product(range(0,10), repeat=repeats):
                yield mid + ''.join(map(str,mmsi))+ '0' * n
    
    def write_separate_lists(self, repeats, n):
        if os.path.exists(config.WORDLISTS_COUNTRY):
            os.mkdir(config.WORDLISTS_COUNTRY)
        for key,value in MMSIgen.countries.items():
            with open(f'mmsi_lists/by_country/{key}_{repeats}_{"0" * n}.txt', 'w') as m:
                for mid in value:
                    for line in self._generate_mmsi(self.mid_list, self.repeats):
                        m.write(line+'\n')
            m.close()

    def write_longlist(self, repeats, n):
        if not os.path.exists(config.WORDLISTS_MASTER):
            os.mkdir(config.WORDLISTS_MASTER)
        with open(f'mmsi_lists/master_list/longlist_{repeats}_{"0" * n}.txt', 'w') as m:
            for key,value in MMSIgen.countries.items():
                for mid in value:
                    for mmsi in itertools.product(range(0,10), repeat=repeats):
                        line = mid + ''.join(map(str,mmsi))+ '0' * n
                        m.write(line+'\n')
        m.close()

if __name__ == "__main__":
    gen = MMSIgen()
    #gen.write_separate_files(5, 1)
    gen.write_longlist(3, 3)

