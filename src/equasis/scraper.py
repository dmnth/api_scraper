#! /usr/bin/env python3

# So this script should parse the
# content of response we got back from
# equasis. Should return all possible data.

#####################################

# Needs more resoucef that track company by imo
# gisis.imo.org

###########################
import os
import re
from requests_html import HTMLSession

__PATH__ = os.path.abspath(os.path.dirname(__file__))

'''
session = HTMLSession()
response = session.get('http://localhost:3000')
'''


def parse_equasis(url):
    
    data = {}
    
    #######Regex#########################o

    # (?<=Registered owner)\n[A-Z]+\s[A-Z]+
    owner_re = re.compile('(?<=Registered owner\n)([A-Z]+\s[A-Z]+)')
    ism_manager_re = re.compile('(?<=Manager\n)[A-Z]+\s[A-Z]+')
    commercial_manager_re = re.compile('(?<=Commercial manager\n)[A-Z]+\s[A-Z]+')
    imo_number = re.compile('(?<=number\n)[0-9]+')
    last_renewal = re.compile('(?<=Last renewal survey\s\s)([0-9]+-[0-9]+-[0-9]+)')
    next_renewal = re.compile('(?<=Next renewal survey\s\s)([0-9]+-[0-9]+-[0-9]+)')
    classification_society = re.compile('(?<=Status\n)\w.*')

    #####################################

    management_details_string = url.html.find('#collapse3', first=True)
    classification_info = url.html.find('#collapse4', first=True)
    
    imo = imo_number.search(management_details_string.text)

    data['owner'] = owner_re.search(management_details_string.text).group()
    data['ism_manager'] = ism_manager_re.search(management_details_string.text).group()
    data['commercial_manager'] = commercial_manager_re.search(management_details_string.text).group()
    data['last_renewal'] = last_renewal.search(classification_info.text).group() 
    data['next_renewal'] = next_renewal.search(classification_info.text).group()
    # Needs to be checked for multiple results, since could be changed by owner
    data['class_soc'] = classification_society.search(classification_info.text).group()

    return data 

if __name__ == "__main__":
    url = 'http://localhost:3000'
    result = parse_equasis(url)
    print(result)

