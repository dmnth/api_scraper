#! /usr/bin/env python3

from enum_mmsi import MID
from concurrent_api_requests import get_vessel_data, write_json
import json
import sys

# This scripts gathers data of all
# that have or will install in nearest
# future Inmarsat earth-station 

class InmarsatEnum:

    def __init__(self, json_obj):
        self.country: str  
        self.json_obj = json_obj

    def read_data(self):
        with open(self.json_obj, 'r') as db:
            self._data = json.load(db) 

    def set_country(self, country):
        self.country = country

    def get_country(self):
        return self.country
    
    # First we want to generate mmsi numbers,
    # they rely on value from country id list witch is dict
    # of {country_name: [mid, mid, mid]}
    def get_country_codes(self):
        self._country_id_list = MID.get_mid_by_country_name(self.country)

    # number_of_repeats:
    # for service type 'B, C, M' - 3
    # just 'C' - 5
    # "A" like any other - 6
    # Should be a seprate option for (A), (C), [B, C, M]
    def generate_output(self, number_of_repeats):
        self._out_file = 'vessels_by_country/' + f'{self.country.lower()}.json'
        if not hasattr(self, '_country_id_list'):
            raise ValueError('no country id list provided')
        get_vessel_data(self._country_id_list, self._out_file, number_of_repeats)
    
    def get_all_tha_vessels(self):
        for country in self._data.keys():
            try:
                sys.stdout.write('\r Current country: {0}\n'.format(country))
                sys.stdout.flush()
                self.country = country
                self.get_country_codes()
                self.generate_output(3)
            except KeyboardInterrupt as done:
                print(done)

if __name__ == "__main__":
    path_to_json = 'MIDs/n_mids.json'
    enumerator = InmarsatEnum(path_to_json)
    enumerator.read_data()
    enumerator.get_all_tha_vessels()
