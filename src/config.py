#! /usr/bin/env python3

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    URL = 'https://www.vesselfinder.com/api/pub/click/'
    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    THREADS = 10
    FILTER = {
            'blacklist': [
                'unknown',
                'unknown type',
                'other type',
                'pleasure craft',
                'sailing vessel',
                'military ops',
                'tug',
                ],
            }
    COMMON_TYPES = {}
    STORAGE_PATH = basedir + '/data'
    WORDLISTS_COUNTRY = basedir + '/mmsi_lists/by_country/'
    WORDLISTS_MASTER = basedir + '/mmsi_lists/master_list/'

config = {'default': Config}
