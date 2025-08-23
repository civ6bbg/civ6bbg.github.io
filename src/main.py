from bs4 import BeautifulSoup
import sqlite3
import re
from concurrent.futures import ThreadPoolExecutor
import os

import dominate
from dominate.tags import *
import lxml.etree
import lxml.builder 
import datetime

from pages.bbg_expanded import *
from pages.buildings import *
from pages.changelog import *
from pages.city_states import *
from pages.governor import *
from pages.great_people import *
from pages.leaders import *
from pages.misc import *
from pages.names import *
from pages.natural_wonder import *
from pages.religion import *
from pages.units import *
from pages.world_wonder import *

langs = ['en_US', 'de_DE', 'es_ES', 'it_IT', 'ko_KR', 'pt_BR', 'zh_Hans_CN', 'fr_FR', 'ja_JP', 'pl_PL', 'ru_RU']
langs_tmp = ['en_US']
bbg_versions_tmp = [None, '7.1']
latest_bbg = '7.1'

sitemap = {bbg_ver: {l: [] for l in langs} for bbg_ver in bbg_versions}

bbg_version_last_timestamp = {bbg_ver: None for bbg_ver in bbg_versions}
bbg_version_last_timestamp[None] = datetime.date(2025, 8, 21)
bbg_version_last_timestamp['7.1'] = datetime.date(2025, 8, 21)
bbg_version_last_timestamp['6.5'] = datetime.date(2025, 8, 21)
bbg_version_last_timestamp['6.4'] = datetime.date(2025, 8, 21)
bbg_version_last_timestamp['6.3'] = datetime.date(2025, 8, 21)
bbg_version_last_timestamp['6.2'] = datetime.date(2025, 8, 21)
bbg_version_last_timestamp['6.1'] = datetime.date(2025, 8, 21)
bbg_version_last_timestamp['6.0'] = datetime.date(2025, 8, 21)
bbg_version_last_timestamp['5.8'] = datetime.date(2025, 8, 21)
bbg_version_last_timestamp['5.7'] = datetime.date(2025, 8, 21)
bbg_version_last_timestamp['5.6'] = datetime.date(2025, 8, 21)

pages_functions_to_file = {
    get_leader_html_file: 'leaders',
    get_city_state_html_file: 'city_states',
    get_religion_html_file: 'religion',
    get_governor_html_file: 'governor',
    get_natural_wonder_html_file: 'natural_wonder',
    get_world_wonder_html_file: 'world_wonder',
    get_misc_html_file: 'misc',
    get_names_html_file: 'names',
    get_great_people_html_file: 'great_people',
    get_buildings_html_file: 'buildings',
    get_expanded_html_file: 'bbg_expanded',
    get_units_html_file: 'units'
}

def generate_html_file(bbg_ver, l, get_page_function, page_name):
    docStr = get_page_function(bbg_ver, l)
    file_path = f'{l}/{page_name}_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)
    if bbg_ver == latest_bbg and l == 'en_US' and page_name == 'bbg_expanded':
        with open('index.html', 'w') as f:
            f.write(docStr)

def generate_sitemap():
    E = lxml.builder.ElementMaker()
    URLSET = E.urlset
    URL = E.url
    LOC = E.loc
    LASTMOD = E.lastmod

    the_doc = URLSET(xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for bbg_ver in sitemap:
        formatted_dt = bbg_version_last_timestamp[bbg_ver].strftime("%Y-%m-%d")
        for lang in sitemap[bbg_ver]:
            for file_path in sitemap[bbg_ver][lang]:
                the_doc.append(
                    URL(
                        LOC(f'https://civ6bbg.github.io/{file_path}'),
                        LASTMOD(formatted_dt),
                    )
                )

    with open('sitemap.xml', 'wb') as f:
        f.write(lxml.etree.tostring(the_doc, pretty_print=True, xml_declaration=True, encoding='UTF-8'))

for l in langs:
    os.makedirs(l, exist_ok=True)
for bbg_ver in bbg_versions:
    print(f'Generating HTML files for BBG version {bbg_ver}')
    for l in langs:
        print(f'language: {l}')
        for get_page_function, page_name in pages_functions_to_file.items():
            print(f'  page: {page_name}')
            generate_html_file(bbg_ver, l, get_page_function, page_name)

generate_sitemap()