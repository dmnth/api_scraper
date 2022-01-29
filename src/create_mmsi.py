#! /usr/bin/env python3

import json
import os
import itertools

class Service:

    #Generate for services B, C, M 
    @classmethod
    def gen_bcm(self, mid):
        for comb in itertools.product(range(0, 10), repeat=3):
            yield mid + ''.join(map(str, comb)) + '000'

    # Service C
    @classmethod
    def gen_c(self, mid):
        for comb in itertools.product(range(0, 10), repeat=5):
            yield mid + ''.join(map(str, comb)) + '0'
    
    # Service A or no service 
    @classmethod
    def gen_a(self, mid):
        for comb in itertools.product(range(0, 10), repeat=6):
            yield mid + ''.join(map(str, comb))


# MID - maritime identification digits, first three digits of
# every MMSI, are unique identifiers of country

class MID:
    
    mids_db = json.load(open(os.path.abspath('MIDs') + '/mids.json')) 

    def __init__(self):
        self.country_mids = [] 
    
    @classmethod
    def get_mid_by_country(self, country):
        gathered_mids = []
        for key, value in MID.mids_db.items():
            for el in value:
                if el == country:
                    gathered_mids.append(key) 
        return gathered_mids

    @classmethod 
    def get_country_by_mid(self, mid_num):
        for mid in MID.mids_db.keys():
            if mid_num == mid:
                return MID.mids_db[mid_num]

class MMSI:

    available_services = ['B', 'C', 'A', 'M']    

    def __init__(self, country, service=None):
        self.country = country
        self.mid = MID.get_mid_by_country(self.country)
        self.service = service

    def __repr__(self):
        return f'{self.country} {_self.mid} {self.service}'

    def set_mid(self):
        if not hasattr(self, '_mid'):
            self._mid = MID.get_mid_by_country(self.country)

    def gen_mmsi(self):

        # What if MID returns list instead of string
        # Need to check all combinations of mid's
        if self.service in ['B', 'C', 'M']:
            # run itertools for repeat = 3
            return Service.gen_bcm(self.mid[0])


        if self.service  == 'C':
            # run itertools for repeat = 5
            return Service.gen_c(self.mid[0])

        else:
            # run itertools for repeat = 6
            return Service.gen_a(self.mid[0])
    
    

if __name__ == "__main__":
    mmsi = MMSI('Panama', 'C')
    mmsi.set_mid()
