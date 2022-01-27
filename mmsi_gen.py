#! /usr/bin/env python3

import itertools
import requests
import aiohttp
import asyncio


class VesselFinder():
    
    unwanted_types = ['unknown type', 'Unknown']

    allowed_vessel_types = [
            'general cargo ship',
            'passenger ship',
            'cargo ship',
            'bulk Carrier',
            'tanker',
            'fishing vessel',
            'diving ops',
            'pleasure craft',
            ]

    def __init__(self):
        self.mid = None
        self.headers = None
        self.url = None 

    def set_url(self, url):
        self.url = url

    def get_mid(self):
        if self.mid is not None:
            return self.mid

    def set_mid(self, mid):
        if not self.mid:
            self.mid = mid

    def set_headers(self, custom_headers=None):
        self.headers = requests.utils.default_headers()
        if custom_headers is None:
            self.headers.update({'User-Agent': 'Mozilla/5.0'})
        else:
            self.headers.update(custom_headers)


    def add_unwanted_type(self, vessel_type):
        if vessel_type not in VesselFinder.allowed_vessel_types:
            raise ValueError('type not allowed')
        else:
            VesselFinder.unwanted_types.append(vessel_type[0].capitalize() + vessel_type[1:])
            VesselFinder.unwanted_types.append(vessel_type.title())

    def remove_type_from_unwanted(self, vessel_type):
        if vessel_type not in VesselFinder.unwanted_types:
            raise ValueError('vessel type not on list')
        VesselFinder.unwanted_types.remove(vessel_type)

    def gen_mmsi(self, mid):
        for comb in itertools.product(range(0, 10), repeat=6):
            yield mid + ''.join(map(str, comb))

    async def print_mmsi(self, mid):
        connector = aiohttp.TCPConnector(force_close=True)
        async with aiohttp.ClientSession(connector=connector) as session:
            for el in self.gen_mmsi(mid):
                async with session.get(f'{url}{el}', headers=self.headers) as result:
                    vessel = await result.json()
                    if vessel['type'] not in VesselFinder.unwanted_types:
                        print(vessel)

    def run(self):
        if self.mid is not None:
            asyncio.run(self.print_mmsi(self.mid))
        else:
            raise ValueError('mid not set')

    def write_json(self):
        pass

if __name__ == "__main__":

    url = "https://www.vesselfinder.com/api/pub/click/"
    finder = VesselFinder()
    finder.set_url(url)
    finder.set_headers()
    finder.set_mid('371')
    finder.add_unwanted_type('fishing vessel')
    finder.add_unwanted_type('pleasure craft')
    finder.run()
