from bs4 import BeautifulSoup
import sqlite3
import re
from concurrent.futures import ThreadPoolExecutor
import os

import dominate
from dominate.tags import *

from HTMLgenerator import *

langs = ['de_DE', 'es_ES', 'it_IT', 'ko_KR', 'pt_BR', 'zh_Hans_CN', 'en_US', 'fr_FR', 'ja_JP', 'pl_PL', 'ru_RU']

def generate_leader_html_file(bbg_ver, l):
    docStr = get_leader_html_file(bbg_ver, l)
    if bbg_ver == None:
        with open(f'{l}/leaders_base_game.html', 'w') as f:
            f.write(docStr)
    else:
        with open(f'{l}/leaders_{bbg_ver}.html', 'w') as f:
            f.write(docStr)

def generate_city_state_html_file(bbg_ver, l):
    docStr = get_city_state_html_file(bbg_ver, l)
    if bbg_ver == None:
        with open(f'{l}/city_states_base_game.html', 'w') as f:
            f.write(docStr)
    else:
        with open(f'{l}/city_states_{bbg_ver}.html', 'w') as f:
            f.write(docStr)

def generate_pantheon_html_file(bbg_ver, l):
    docStr = get_pantheon_html_file(bbg_ver, l)
    if bbg_ver == None:
        with open(f'{l}/pantheons_base_game.html', 'w') as f:
            f.write(docStr)
    else:
        with open(f'{l}/pantheons_{bbg_ver}.html', 'w') as f:
            f.write(docStr)

def generate_religion_html_file(bbg_ver, l):
    docStr = get_religion_html_file(bbg_ver, l)
    if bbg_ver == None:
        with open(f'{l}/religion_base_game.html', 'w') as f:
            f.write(docStr)
    else:
        with open(f'{l}/religion_{bbg_ver}.html', 'w') as f:
            f.write(docStr)

def generate_governor_html_file(bbg_ver, l):
    docStr = get_governor_html_file(bbg_ver, l)
    if bbg_ver == None:
        with open(f'{l}/governor_base_game.html', 'w') as f:
            f.write(docStr)
    else:
        with open(f'{l}/governor_{bbg_ver}.html', 'w') as f:
            f.write(docStr)
            
def generate_natural_wonder_html_file(bbg_ver, l):
    docStr = get_natural_wonder_html_file(bbg_ver, l)
    if bbg_ver == None:
        with open(f'{l}/natural_wonder_base_game.html', 'w') as f:
            f.write(docStr)
    else:
        with open(f'{l}/natural_wonder_{bbg_ver}.html', 'w') as f:
            f.write(docStr)
            
def generate_world_wonder_html_file(bbg_ver, l):
    docStr = get_world_wonder_html_file(bbg_ver, l)
    if bbg_ver == None:
        with open(f'{l}/world_wonder_base_game.html', 'w') as f:
            f.write(docStr)
    else:
        with open(f'{l}/world_wonder_{bbg_ver}.html', 'w') as f:
            f.write(docStr)
            
def generate_misc_html_file(bbg_ver, l):
    docStr = get_misc_html_file(bbg_ver, l)
    if bbg_ver == None:
        with open(f'{l}/misc_base_game.html', 'w') as f:
            f.write(docStr)
    else:
        with open(f'{l}/misc_{bbg_ver}.html', 'w') as f:
            f.write(docStr)
            
for l in langs:
    # Create directory if it does not exist
    os.makedirs(l, exist_ok=True)
for bbg_ver in bbg_versions:
    print(f'Generating HTML files for BBG version {bbg_ver}')
    for l in langs:
        generate_leader_html_file(bbg_ver, l)
        generate_city_state_html_file(bbg_ver, l)
        generate_religion_html_file(bbg_ver, l)
        generate_governor_html_file(bbg_ver, l)
        generate_natural_wonder_html_file(bbg_ver, l)
        generate_world_wonder_html_file(bbg_ver, l)
        generate_misc_html_file(bbg_ver, l)
# Uncomment the following lines to generate HTML files for the beta version
# print('Generating HTML files for beta version')
# generate_leader_html_file('Beta', 'en_US')
# generate_city_state_html_file('Beta', 'en_US')
# generate_pantheon_html_file('Beta', 'en_US')
# generate_religion_html_file('Beta', 'en_US')
# generate_governor_html_file('Beta', 'en_US')