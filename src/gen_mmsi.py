#! /usr/bin/env python3

import json
import os
import asyncio
from threading import Thread
import itertools
import aiohttp
from time import perf_counter
import asyncio
# RTFM for this:
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

# Handle multiple MID values at once in list format
# Pop while list not empty
# list of lenght 1 is still a list and can be popped

path_to_file = os.path.abspath('MIDs') + '/mids.json'
print(path_to_file)
# Thread MMSI gen
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

url = 'https://www.vesselfinder.com/api/pub/click/'
headers = {'User-Agent': "Mozilla/5.0"}

THREAD_POOL = 16
mmsi_numbers = []
def read_json(file):
    f = open(file)
    result =json.load(f)
    return result


def generate_mmsi_bcm(mid):
    for dec in itertools.product(range(0, 10), repeat=3):
        mmsi = mid + ''.join(map(str, dec)) + '000'
        mmsi_numbers.append(mmsi)
        print(f'Processing mmsi {mmsi}')
        if len(mmsi_numbers) == 34:
            raise ValueError()
        yield mmsi

async def make_requests(mid):
    connector = aiohttp.TCPConnector(force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        for mmsi in generate_mmsi_bcm(mid):
            async with session.get(f'{url}{mmsi}', headers=headers) as result:
                print(result.status)
                vessel = await result.json()

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

# Generate all possible mmsi for every mid assigned to Panama

def gen_panama_vessels(mid_list):
    try:
        threads = [Thread(target=asyncio.run(make_requests(mid))) for mid in mid_list]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
    except:
        ValueError(f'Thats all Folks')

def make_requests(mmsi):
    response = requests.get(f'{url}{mmsi}', headers=headers)

session = requests.Session()
session.mount(requests.adapters.HTTPAdapter(pool_maxsize=THREAD_POOL, max_retries==3, pool_block=True))
def gen_panama_vessels_v2(mid_list):
    with ThreadPoolExecutor(max_workers=THREAD_POOL) as executor:


if __name__ == "__main__":
    mid_file= read_json(path_to_file) 
    print('Iran' in create_list_o_countries(mid_file))
    panama_mids = get_mid_list('Panama', mid_file) 
    georgia_mids = get_mid_list('Georgia', mid_file)
    dickland_mids = get_mid_list('Dickland', mid_file)
    start = perf_counter()
    gen_panama_vessels(panama_mids)
    end = perf_counter()
    print(f'wasted {end-start: .2f} seconds of my life on {len(mmsi_numbers)} MMSI"s')
    print(panama_mids)
