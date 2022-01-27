#! /usr/bin/enb python3

from .finder import VesselFinder
import os
import sys
from config import Config

# Setters should be cared in other manner
# Headers should be in config file, same goes for url and mid
# everything should be passed to class instance upon creation

def create_finder():
    finder = VesselFinder()
    url = "https://www.vesselfinder.com/api/pub/click/"
    finder.set_headers()
    finder.set_url(url)
    finder.set_mid('210')
    print(Config.data)

    return finder

finder = create_finder()
