#! /usr/bin/env python3

import json
import os
import asyncio
from threading import Thread
import itertools
import aiohttp

# Handle multiple MID values at once in list format
# Pop while list not empty
# list of lenght 1 is still a list and can be popped

path_to_file = os.path.abspath('MIDs') + '/mids.json'
print(path_to_file)
'''
fucking_dict = {
        'Panama': {
            'shortcuts': ['PA', 'PAN'],
            'mid': [351, 352, 353],
            },
        'Venesuella': {
            'shortcuts': ['VE', 'VEN'],
            'mid': [445],
            },
        }
'''

def read_json(file):
    f = open(file)
    result =json.load(f)
    return result

def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()

def generate_mmsi_bcm(mid):
    for dec in itertools.product(0, 10), repeat=3):
        yield mid + ''.join(map(str, dec)) + '000'

def create_list_o_countries(mid_file):
    legal_country_names = []
    for value in mid_file.values():
        legal_country_names.append(value[-1])
    return legal_country_names

def get_mid_list(country, mid_file):
    country_mid_list = []
    legal_names = create_list_o_countries(mid_file)
    has_fleet = True
    if country not in legal_names:
        has_fleet = False
        return (f'{country} has no fleet')
    for key, value in mid_file.items():
        if country in value:
            country_mid_list.append(key)
    return country_mid_list

def send_async_requests(url, mid):
    connector = aiohttp.TCPConnector(force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        for mmsi in generate_mmsi_bcm(mid_list)


if __name__ == "__main__":
    mid_file= read_json(path_to_file) 
    print('Iran' in create_list_o_countries(mid_file))
    panama_mids = get_mid_list('Panama', mid_file) 
    georgia_mids = get_mid_list('Georgia', mid_file)
    dickland_mids = get_mid_list('Dickland', mid_file)
    print(panama_mids)
    print(dickland_mids)
    print(georgia_mids)

