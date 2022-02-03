#! /usr/bin/env python3

import requests

# will need a pool of identifiers
from data import DefaultConfig, EquasisConfig
config = DefaultConfig()
eq_config =EquasisConfig()

updated_headers = {
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        } 

landing_page = eq_config.base_url + 'EquasisWeb/public/HomePage'
landing_data = {'fs': 'HomePage', 'P_ACTION': 'NEW_CONNECTION'}
login_data = {'fs': 'HomePage', 'j_email': 'kborodin1@gmail.com',
        'j_password': 'S00p@d00p@p00p@'}

def make_request(config, imo):
    with requests.Session() as session:
        session.headers.update(updated_headers)
        test_response = session.get(landing_page, data=landing_data)
        session_cookie = test_response.headers.get('Set-Cookie')
        session_id = session_cookie.split(';')[0].split('=')[1]
        # login_data.update({'JSESSIONID': session_id})
        print(session_id)
        test_login = session.post(landing_page, data=login_data) 
        print(test_login.text)



if __name__ == "__main__":
    make_request(eq_config, {'P_IMO': '9836048'})
