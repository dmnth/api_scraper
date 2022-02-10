#! /usr/bin/env python3

# So this script should parse the
# content of response we got back from
# equasis. Should return all possible data.
import os
import re
from requests_html import HTMLSession

__PATH__ = os.path.abspath(os.path.dirname(__file__))

def get_equasis_data(url):
    
    data = {}
    
    session = HTMLSession()
    response = session.get('http://localhost:3000')

    #######Regex#########################o

    # (?<=Registered owner)\n[A-Z]+\s[A-Z]+
    owner_re = re.compile('(?<=Registered owner)([A-Z]+\s[A-Z]+)')
    ism_manager_re = re.compile('(?<=Manager)[A-Z]+\s[A-Z]+')
    commercial_manager_re = re.compile('(?<=Commercial manager)[A-Z]+\s[A-Z]+')

    #####################################

    re_string = ''
    management_details = response.html.find('#collapse3', first=True)
    print(management_details.text)
    for elem in management_details:
        re_string += elem.text

    data['owner'] = owner_re.search(re_string).group()
    data['ism_manager'] = ism_manager_re.search(re_string).group()
    data['commercial_manager'] = commercial_manager_re.search(re_string).group()

    classification_info = response.html.find('#collapse4')
    '''
    for el in classification_info:
        print(el.text)
    '''

    # Todo: parse values with regex
    # Create a legit vessel class 

    return data 

if __name__ == "__main__":
    url = 'http://localhost:3000'
    result = get_equasis_data(url)
    print(result)

