#! /usr/bin/env python3

import requests
import aiohttp
import asyncio
from .create_mmsi import MMSI

# add response json filter for unwanter vessel types
# create a db to frite stuff to
class VesselScraper:

    banned_items = []
    allowd_vessels = []

    # Country and service are needed to degenerate
    # proper MMSI format

    def __init__(self, country, service):
        self.country = country
        self.service = service

    def set_url(self, url):
        if not hasattr(self, '__url'):
            self.__url = url

    def set_headers(self, headers):
        if not hasattr(self, '__headers'):
            self.__headers = headers


    async def make_requests(self):
        connector = aiohttp.TCPConnector(force_close=True)
        async with aiohttp.ClientSession(connector=connector) as session:
            for mmsi in self._mmsi:
                async with session.get(f'{self.__url}{mmsi}', headers=self.__headers) as result:
                    print(result.status)
                    vessel = await result.json()
                    if vessel['type'] not in ['Unknown', 'Unknown type', 'Fishing vessel', 'Pleasure craft']:
                        print(vessel)

    def run(self):
        asyncio.run(self.make_requests())

    def write_to_db(self, data):
        pass

    def create_mmsi_pool(self):
        if not hasattr(self, '_mmsi'):
            mmsi = MMSI(self.country, self.service)
            mmsi.set_mid()
            self._mmsi = mmsi.gen_mmsi()


if __name__ == "__main__":
    scraper = VesselScraper('Panama', 'C')
    scraper.create_mmsi_pool()
    scraper.set_headers()
    scraper.run()
