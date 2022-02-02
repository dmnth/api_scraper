#! /usr/bin/env python3

from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Vessel:
    sort_index: int = field(init=False, repr=False)
    name: str
    country: str
    type: str
    dest: str
    dead_weight: int
    gross_tonnage: int
    imo: int
    mmsi: int
    date_built: datetime.date() 

    def _post__init__(self):
        super().__init__('sort_index', self.date_built)

    def __str__(self):
        return f'{self.name} {self.type} {self.imo}'

if __name__ == "__main__":

    vessel = CargoVessel('DYING_MARY', 'Cuprus', 'crude oil tanker', 122334, 65534, 'Russian Federation', 314141241, 342342424)

