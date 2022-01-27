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
    imo: int
    mmsi: int
    built: datetime.date() 

    def _post__init__(self):
        super().__init__('sort_index', self.gross_tonnage)

    def __str__(self):
        return f'{self.name} {self.type} {self.imo}'

@dataclass
class CargoVessel(Vessel):
    dead_weight: int
    gross_tonnage: int

@dataclass
class FishingVessel(Vessel):
    pass

@dataclass
class Refrigerator(CargoVessel):
    pass

@dataclass
class CruiseVessel(Vessel):
    pass



if __name__ == "__main__":

    vessel = CargoVessel('DYING_MARY', 'Cuprus', 'crude oil tanker', 122334, 65534, 'Russian Federation', 314141241, 342342424)

