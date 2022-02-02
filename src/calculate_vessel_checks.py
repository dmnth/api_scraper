#! /usr/bin/env python3

import json
from datetime import datetime
from concurrent_api_requests import read_json

vessels_json = 'panama_vessels.json'
current_year = datetime.today().year
print(current_year)

class Vessel:

    def __init__(self, name, imo, country, type, year_build):
        self.name = name
        self.imo = imo
        self.type = type
        self.year_build = year_build
        self.age = current_year - self.year_build


if __name__ == "__main__":
    vessels = read_json(vessels_json)
    year = vessels[1]['y']
    print(vessels[1].keys())
