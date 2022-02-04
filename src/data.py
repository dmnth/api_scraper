#! /usr/bin/env python3

from dataclasses import dataclass, field
import json

@dataclass
class DefaultConfig:
    url: str = 'https://www.vesselfinder.com/api/pub/click/'
    headers: dict = field(init=False, compare=False, default_factory=dict)
    outfile: str = 'vessels.json'

    def __post_init__(self):
        self.headers['User-Agent'] = 'Mozilla/5.0'

def read_json(json_file):
    with open(json_file, 'r') as outfile:
        data = json.load(outfile)

    return data

@dataclass
class EquasisConfig:

    base_url: str = 'https://www.equasis.org/'
    login_url: str = base_url + 'EquasisWeb/public' \
            + '/HomePage' 
    restricted_url: str = base_url + 'EquasisWeb/restricted/ShipInfo?fs=Search'
    headers: dict = field(init=False, compare=False, default_factory=dict)
    data: dict = field(init=False, compare=False, default_factory=dict)
    credentials: dict = field(init=False, compare=False, default_factory=dict)

    def __post_init__(self):
        self.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64;' \
        + 'x64)'
        self.credentials['j_email'] = 'kborodin1@gmail.com'
        self.credentials['j_password'] = 'S00p@d00p@p00p@'
        self.credentials['submit'] = 'Login'

    def set_data(self, imo):
        self.data = {'P_IMO': imo} 

if __name__ == "__main__":
    eq_conf = EquasisConfig()
    eq_conf.set_data('2343242', 'data')
