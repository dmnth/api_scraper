#! /usr/bin/env python3

import requests
from scraper import parse_equasis
from requests_html import HTMLSession
from config import config

config = config['equasis']

headers = config.updated_headers
base_url = config.base_url
login_data = config.login_data
login_page = config.login_page
auth_page = config.auth_page
email = login_data['j_email']
password = login_data['j_password']
imo_data = config.imo
imo_search_page = config.imo_search_url

def get_session_id(url, session):
    test_response = session.get(url, headers=headers)
    if test_response.status_code == 200:
        session_cookie = test_response.headers.get('Set-Cookie')
        session_id = session_cookie.split(';')[0].split('=')[1]
        print(session_id)
        return session_id
    else:
        print('Returned: ', test_response.status_code)

def login(email, password, sid, session):
    login_data.update({'JSESSIONID': sid})
    test_login = session.post(login_page, data=login_data) 
    if test_login.status_code == 200:
        print('sucess/not really')

def search_by_imo(imo, session):
    imo_data.update({'P_IMO': imo})
    result = session.post(imo_search_page, data=imo_data)
    return result

def make_request(imo):
    with HTMLSession() as session:
        session.headers.update(headers)
        sid = get_session_id(auth_page, session)
        login(email, password, sid, session)
        result = search_by_imo(imo, session)
        r = parse_equasis(result)
        return r


if __name__ == "__main__":
    print(make_request(9473834))
