#!/usr/bin/env python3

#
# (C) 2025 Heinlein Support GmbH - License: GNU General Public License v2
# Robert Sander <r.sander@heinlein-support.de>
#

import sys
from bs4 import BeautifulSoup

from pprint import pprint

with open(sys.argv[1]) as htmlfile:
    html_doc = htmlfile.read()

soup = BeautifulSoup(html_doc, 'html.parser')

def get_tag_by_attr_value(tag, name, attr, value):
    return tag.name == name and tag.get(attr) == value

print("Title;HREF;Downloads;Views;Stars")

for li in soup.find_all("li"):    
    for header in li.find_all("header"):
        title = header.a.string
        href = header.a["href"]
        
    downloads = ""
    views = ""
    stars = ""
        
    for span in li.find_all(lambda x: get_tag_by_attr_value(x, "span", "data-testid", "downloads")):
        downloads = int(list(span.strings)[0])
    for span in li.find_all(lambda x: get_tag_by_attr_value(x, "span", "data-testid", "views")):
        views = int(list(span.strings)[0])
    for span in li.find_all(lambda x: get_tag_by_attr_value(x, "span", "data-testid", "rating")):
        stars = float(list(span.strings)[0])
        
    print(f'"{title}";"{href}";{downloads};{views};{stars}')
