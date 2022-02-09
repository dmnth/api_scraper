#! /usr/bin/env python3

# So this script should parse the
# content of response we got back from
# equasis. Should return all possible data.
import os
import re
from requests_html import HTMLSession

__PATH__ = os.path.abspath(os.path.dirname(__file__))

session = HTMLSession()
response = session.get('http://localhost:3000')
management_details = response.html.find('#collapse3', first=True).find('td')
for elem in management_details:
    print(elem.text)

classification_info = response.html.find('#collapse4')
print(classification_info)
for el in classification_info:
    print(el.text)


# Todo: parse values with regex



