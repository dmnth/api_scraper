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
                'yacht',
                'buoy/lighthouse vessel',
                'crew boat',
                'landing craft',
                'motor hopper',
                'anchor hoy',
                'standby safety vessel',
                'fishing support vessel',
                'pontoon',
                ],
            }
    COMMON_TYPES = {}
    STORAGE_PATH = basedir + '/data'
    WORDLISTS_COUNTRY = basedir + '/mmsi_lists/by_country/'
    WORDLISTS_MASTER = basedir + '/mmsi_lists/master_list/'
    DATA_DIR = basedir + '/data'
    DB_URL = f'sqlite:////{basedir}/vessels.db'
    VESSELS_DATA_PATH = basedir + '/vessels_by_country/'

config = {'default': Config}
