#! /usr/bin/env python3

import json
from datetime import datetime
from data import DefaultConfig, read_json

vessels_json = 'panama_vessels.json'
current_year = datetime.today().year
config = DefaultConfig()



class Vessel:

    def __init__(self, name, imo, country, type, year_build):
        self.name = name
        self.imo = imo
        self.type = type
        self.year_build = year_build
        self.age = current_year - self.year_build

    def get_next_inspection_year(self):
       next_inspection = self.year_build 
       times_served = 0
       # Quality control - annual every 5 years for first 10 years after y.b
       # After that intermidiate is added and is done every 2.5 years
       # (inbetween of annual)
       while next_inspection < current_year:
           # if vessel is less than five years - no need to iterate
           if self.age <= 5:
               next_inspection += 5
               break 
           # For first 10 years vessel goes through 2 qc routines
           if times_served < 2:
               next_inspection += 5
           # After that intermediate qc is held for every 2.5 years 
           else:
               next_inspection += 2.5
           times_served += 1
       # Type of inspection to be carried in the future 
       if times_served % 2 == 1:
           inspection_type = 'intermediate'
       else:
           # 
           inspection_type = 'annual'
       return int(next_inspection), last_check 


if __name__ == "__main__":
    vessels = read_json(vessels_json)
    my_vessels = vessels[:20]
    for vessel in my_vessels:
        current_vessel = Vessel(vessel['name'], vessel['imo'],
                vessel['country'], vessel['type'],
                vessel['y'])
        print(current_vessel.type, current_vessel.year_build, current_vessel.get_next_service_year())
