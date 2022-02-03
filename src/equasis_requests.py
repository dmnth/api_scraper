#! /usr/bin/env python3

import requests

# will need a pool of identifiers
from data import DefaultConfig
config = DefaultConfig()

payload = {
        'j_email': 'kborodin1@gmail.com',
        'j_password': 'S00p@d00p@p00p@',
        }
search_req = {
            'P_ENTREE_ENTETE_HIDDEN': '9839167',
            }
url = "https://www.equasis.org/EquasisWeb/public/HomePage?fs=HomePage&P_ACTION=NEW_CONNECTION" 
restricted = "https://www.equasis.com/EquasisWeb/restricted/" + "ShipInfo?fs=Search"
restricted_2 = restricted + "SurveyList?fs=HomePage"

def make_request(url, payload):
    with requests.Session() as session:
        response = session.get(url, headers=config.headers, data=payload)
        response_3 = session.get(restricted, headers=config.headers, data=search_req)
        print(response_3.content)
        print(response_3.headers)


if __name__ == "__main__":
    make_request(url, payload)
