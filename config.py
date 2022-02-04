#! /usr/bin/env python3

from dataclasses import dataclass, field
import requests

@dataclass
class Config:

    database: str = "sqlite3:///mydb.db" 
    url: str = 'https://www.vesselfinder.com/api/pub/click/'
    headers: dict = field(init=False, compare=False, default_factory=dict)

    def __post_init__(self):
        # probably will be easier to modify later
        self.headers['User-Agent'] = "Mozilla/5.0"  

@dataclass
class TestConfig(Config):
    pass

@dataclass
class DevelopmentConfig(Config):
    pass


config = {
        'default': Config,
        }
