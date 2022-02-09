#! /usr/bin/env python3

import requests

# will need a pool of identifiers

base_url = 'https://www.equasis.org/'
updated_headers = {
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        } 

landing_page = base_url + \
'EquasisWeb/public/HomePage?fs=HomePage&P_ACTION=NEW_CONNECTION'
login_page = base_url + 'EquasisWeb/authen/HomePage?fs=HomePage'
login_data = {'j_email': 'kborodin1@gmail.com',
        'j_password': 'S00p@d00p@p00p@'}

search_page = base_url + 'EquasisWeb/restricted/Search?fs=HomePage'
search_data = {
        'P_PAGE': '1', 
        'P_PAGE_COMP': '1', 
        'P_PAGE_SHIP': '1',
        'P_ENTREE_HOME': None,
        'P_ENTREE_HOME_HIDDEN': None,
        'checkbox-shop': 'Ship',
        'AdvancedSearch': '',
        'fs': 'HomePage',
        }
detailed_search_page = base_url + \
'EquasisWeb/restricted/ShipInfo?fs=Search'
detailed_search_data = {'P_IMO': None }

def make_request(imo):
    with requests.Session() as session:
        session.headers.update(updated_headers)
        test_response = session.get(landing_page)
        session_cookie = test_response.headers.get('Set-Cookie')
        session_id = session_cookie.split(';')[0].split('=')[1]
        login_data.update({'JSESSIONID': session_id})
        test_login = session.post(login_page, data=login_data) 
        search_data['P_ENTREE_HOME'] = imo
        search_data['P_ENTREE_HOME_HIDDEN'] = imo
        test_search = session.post(search_page, data=search_data)
        detailed_search_data['P_IMO'] = imo
        detailed_search = session.post(detailed_search_page, data=detailed_search_data)
        result = detailed_search.content.decode()
        return result



if __name__ == "__main__":
    wall_of_text = make_request('9850874')
    with open('wall_of_html', 'w') as out:
        out.write(wall_of_text)
    print('Registered owner' in wall_of_text)
