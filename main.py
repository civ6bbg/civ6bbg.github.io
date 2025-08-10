from bs4 import BeautifulSoup
import sqlite3
import re
from concurrent.futures import ThreadPoolExecutor
import os

import dominate
from dominate.tags import *

from HTMLgenerator import *

langs = ['en_US', 'de_DE', 'es_ES', 'it_IT', 'ko_KR', 'pt_BR', 'zh_Hans_CN', 'fr_FR', 'ja_JP', 'pl_PL', 'ru_RU']
langs_tmp = ['en_US']
bbg_versions_tmp = [None, '6.5']

def generate_leader_html_file(bbg_ver, l):
    docStr = get_leader_html_file(bbg_ver, l)
    with open(f'{l}/leaders_{'base_game' if bbg_ver == None else bbg_ver}.html', 'w') as f:
        f.write(docStr)

def generate_city_state_html_file(bbg_ver, l):
    docStr = get_city_state_html_file(bbg_ver, l)
    with open(f'{l}/city_states_{'base_game' if bbg_ver == None else bbg_ver}.html', 'w') as f:
        f.write(docStr)

def generate_religion_html_file(bbg_ver, l):
    docStr = get_religion_html_file(bbg_ver, l)
    with open(f'{l}/religion_{'base_game' if bbg_ver == None else bbg_ver}.html', 'w') as f:
        f.write(docStr)

def generate_governor_html_file(bbg_ver, l):
    docStr = get_governor_html_file(bbg_ver, l)
    with open(f'{l}/governor_{'base_game' if bbg_ver == None else bbg_ver}.html', 'w') as f:
        f.write(docStr)

def generate_natural_wonder_html_file(bbg_ver, l):
    docStr = get_natural_wonder_html_file(bbg_ver, l)
    with open(f'{l}/natural_wonder_{'base_game' if bbg_ver == None else bbg_ver}.html', 'w') as f:
        f.write(docStr)

def generate_world_wonder_html_file(bbg_ver, l):
    docStr = get_world_wonder_html_file(bbg_ver, l)
    with open(f'{l}/world_wonder_{'base_game' if bbg_ver == None else bbg_ver}.html', 'w') as f:
        f.write(docStr)

def generate_misc_html_file(bbg_ver, l):
    docStr = get_misc_html_file(bbg_ver, l)
    with open(f'{l}/misc_{'base_game' if bbg_ver == None else bbg_ver}.html', 'w') as f:
        f.write(docStr)

def generate_names_html_file(bbg_ver, l):
    docStr = get_names_html_file(bbg_ver, l)
    with open(f'{l}/names_{'base_game' if bbg_ver == None else bbg_ver}.html', 'w') as f:
        f.write(docStr)

def generate_great_people_html_file(bbg_ver, l):
    docStr = get_great_people_html_file(bbg_ver, l)
    with open(f'{l}/great_people_{'base_game' if bbg_ver == None else bbg_ver}.html', 'w') as f:
        f.write(docStr)

def generate_buildings_html_file(bbg_ver, l):
    docStr = get_buildings_html_file(bbg_ver, l)
    with open(f'{l}/buildings_{'base_game' if bbg_ver == None else bbg_ver}.html', 'w') as f:
        f.write(docStr)

def generate_expanded_html_file(bbg_ver, l):
    docStr = get_expanded_html_file(bbg_ver, l)
    with open(f'{l}/bbg_expanded_{'base_game' if bbg_ver == None else bbg_ver}.html', 'w') as f:
        f.write(docStr)

for l in langs:
    # Create directory if it does not exist
    os.makedirs(l, exist_ok=True)
for bbg_ver in bbg_versions:
    print(f'Generating HTML files for BBG version {bbg_ver}')
    for l in langs:
        print(f'language: {l}')
        generate_leader_html_file(bbg_ver, l)
        generate_city_state_html_file(bbg_ver, l)
        generate_religion_html_file(bbg_ver, l)
        generate_governor_html_file(bbg_ver, l)
        generate_natural_wonder_html_file(bbg_ver, l)
        generate_world_wonder_html_file(bbg_ver, l)
        generate_misc_html_file(bbg_ver, l)
        generate_names_html_file(bbg_ver, l)
        generate_great_people_html_file(bbg_ver, l)
        generate_buildings_html_file(bbg_ver, l)
        generate_expanded_html_file(bbg_ver, l)