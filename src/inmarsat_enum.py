#! /usr/bin/env python3

from enum_mmsi import MID
from concurrent_api_requests import get_vessel_data, write_json

# This scripts gathers data of all
# that have or will install in nearest
# future Inmarsat earth-station 

class InmarsatEnum:

    def __init__(self, country):
        self.country = country
        self.service_type = None

    def set_country(self, country):
        self.country = country

    def get_country(self):
        return self.country
    
    # First we want to generate mmsi numbers,
    # they rely on value from country id list witch is dict
    # of {country_name: [mid, mid, mid]}
    def get_country_codes(self):
        if not hasattr(self, '_country_id_list'):
            self._country_id_list = MID.get_mid_by_country_name(self.country)

    # number_of_repeats:
    # for service type 'B, C, M' - 3
    # just 'C' - 5
    # "A" like any other - 6
    # Should be a seprate option for (A), (C), [B, C, M]
    def generate_output(self, number_of_repeats):
        if not hasattr(self, '_out_file'):
            self._out_file = f'{self.country.lower()}.json'
        if not hasattr(self, '_country_id_list'):
            raise ValueError('no country id list provided')
        get_vessel_data(self._country_id_list, self._out_file, 3)



    # And all done - fire up requests

if __name__ == "__main__":
    enumerator = InmarsatEnum('estonia')
    enumerator.get_country_codes()
    enumerator.generate_output(3)
