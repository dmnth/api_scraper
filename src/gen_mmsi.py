#! /usr/bin/env python3

import json
import os
import asyncio
from threading import Thread
import itertools
import aiohttp
from time import perf_counter
import asyncio
import concurrent.futures
# RTFM for this:
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


# Rework this mess into a helper functions - class thingy
# Handle multiple MID values at once in list format
# Pop while list not empty
# list of lenght 1 is still a list and can be popped

path_to_file = os.path.abspath('MIDs') + '/mids.json'
print(path_to_file)
# Thread MMSI gen

url = 'https://www.vesselfinder.com/api/pub/click/'
headers = {'User-Agent': "Mozilla/5.0"}

THREAD_POOL = 16
mmsi_numbers = []
def read_json(file):
    f = open(file)
    result =json.load(f)
    return result

def simple_iterations(mid_list):
    counter = 0
    for mid in mid_list:
        for dec in itertools.product(range(0, 10), repeat=3):
            response = requests.get(f'{url}{mid}{dec}000', headers=headers)
            counter += 1
            if counter == 79:
                print('11 seconds')
                return
            print(response)



vessels = []
async def generate_mmsi_bcm(mid):
    connector = aiohttp.TCPConnector(force_close=True)
    responses = 0
    start = perf_counter()
    try:
        async with aiohttp.ClientSession(connector=connector) as session:
            for dec in itertools.product(range(0, 10), repeat=3):
                responses += 1
                mmsi = mid + ''.join(map(str, dec)) + '000'
                mmsi_numbers.append(mmsi)
                print(f'Processing mmsi {mmsi} {responses}')
                print(mmsi)
                async with session.get(f'{url}{mmsi}', headers=headers) as result:
                    print(result.status)
                    vessel = await result.json()
                    vessels.append(vessel)
                    print(vessels)
    except KeyboardInterrupt:
        end = perf_counter()
        print(f' waster {end - start:.2f} on {vessels}')

out = []
def make_threaded_requests(mid_list):
    CONNECTIONS = 100
    TIMEOUT = 5
    start =  perf_counter()
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
            future_to_mmsi = (executor.submit(asyncio.run(generate_mmsi_bcm(mid))) for mid in mid_list)
            for future in concurrent.futures.as_completed(future_to_mmsi):
                try:
                    data = future.result()
                except Exception as exc:
                    data = str(type(exc))
                finally:
                    out.append(data)
    except KeyboardInterrupt:
        end = perf_counter()
        print(f'took {end-start:.2f} seconds')


###############################################################
def make_single_request(mmsi):
    result = requests.get(f'{url}{mmsi}', headers=headers)
    print(result)

def s_generate_mmsi_bcm(mid):
    start = perf_counter()
    try:
        for dec in itertools.product(range(0, 10), repeat=3):
            mmsi = mid + ''.join(map(str, dec)) + '000'
            mmsi_numbers.append(mmsi)
            print(f'Processing mmsi {mmsi}')
            print(mmsi)
            make_single_request(mmsi)
    except KeyboardInterrupt:
        end = perf_counter()
        print(f' waster {end - start:.2f} on {vessels}')

def make_threaded_single_requests(mid_list):
    CONNECTIONS = 100
    TIMEOUT = 5
    start =  perf_counter()
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
            future_to_mmsi = (executor.submit(s_generate_mmsi_bcm(mid)) for mid in mid_list)
            for future in concurrent.futures.as_completed(future_to_mmsi):
                try:
                    data = future.result()
                except Exception as exc:
                    data = str(type(exc))
                finally:
                    out.append(data)
    except KeyboardInterrupt:
        end = perf_counter()
        print(f'took {end-start:.2f} seconds')

################################################################################################        
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

mid_file= read_json(path_to_file) 
panama_mids = get_mid_list('Panama', mid_file)

if __name__ == "__main__":
    start = perf_counter()
    panama_mids = get_mid_list('Panama', mid_file) 
    print(panama_mids)
    end = perf_counter()
    print(f'wasted {end-start: .2f} seconds of my life on {len(mmsi_numbers)} MMSI"s')
