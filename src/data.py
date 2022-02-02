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

