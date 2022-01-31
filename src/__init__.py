#! /usr/bin/enb python3

from .vessel_scraper import VesselScraper
import os
import sys
from config import config

# Setters should be cared in other manner
# Headers should be in config file, same goes for url and mid
# everything should be passed to class instance upon creation

def create_scraper(config):
    scraper = VesselScraper('Panama', 'M')
    scraper.set_url(config.url)
    scraper.create_mmsi_pool()
    scraper.set_headers(config.headers)
    return scraper 

scraper = create_scraper(config['default']())
