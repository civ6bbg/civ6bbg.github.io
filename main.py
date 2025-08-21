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

from HTMLgenerator import *

langs = ['en_US', 'de_DE', 'es_ES', 'it_IT', 'ko_KR', 'pt_BR', 'zh_Hans_CN', 'fr_FR', 'ja_JP', 'pl_PL', 'ru_RU']
langs_tmp = ['en_US']
bbg_versions_tmp = [None, '7.1']
latest_bbg = '7.1'

sitemap = {bbg_ver: {l: [] for l in langs} for bbg_ver in bbg_versions}

bbg_version_last_timestamp = {bbg_ver: None for bbg_ver in bbg_versions}
bbg_version_last_timestamp[None] = datetime.date(2025, 8, 12)
bbg_version_last_timestamp['7.1'] = datetime.date(2025, 8, 20)
bbg_version_last_timestamp['6.5'] = datetime.date(2025, 8, 12)
bbg_version_last_timestamp['6.4'] = datetime.date(2025, 8, 12)
bbg_version_last_timestamp['6.3'] = datetime.date(2025, 8, 12)
bbg_version_last_timestamp['6.2'] = datetime.date(2025, 8, 12)
bbg_version_last_timestamp['6.1'] = datetime.date(2025, 8, 12)
bbg_version_last_timestamp['6.0'] = datetime.date(2025, 8, 12)
bbg_version_last_timestamp['5.8'] = datetime.date(2025, 8, 12)
bbg_version_last_timestamp['5.7'] = datetime.date(2025, 8, 12)
bbg_version_last_timestamp['5.6'] = datetime.date(2025, 8, 12)

def generate_leader_html_file(bbg_ver, l):
    docStr = get_leader_html_file(bbg_ver, l)
    file_path = f'{l}/leaders_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)
    # if bbg_ver == latest_bbg and l == 'en_US':
    #     with open('index.html', 'w') as f:
    #         f.write(docStr)

def generate_city_state_html_file(bbg_ver, l):
    docStr = get_city_state_html_file(bbg_ver, l)
    file_path = f'{l}/city_states_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)

def generate_religion_html_file(bbg_ver, l):
    docStr = get_religion_html_file(bbg_ver, l)
    file_path = f'{l}/religion_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)

def generate_governor_html_file(bbg_ver, l):
    docStr = get_governor_html_file(bbg_ver, l)
    file_path = f'{l}/governor_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)

def generate_natural_wonder_html_file(bbg_ver, l):
    docStr = get_natural_wonder_html_file(bbg_ver, l)
    file_path = f'{l}/natural_wonder_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)

def generate_world_wonder_html_file(bbg_ver, l):
    docStr = get_world_wonder_html_file(bbg_ver, l)
    file_path = f'{l}/world_wonder_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)

def generate_misc_html_file(bbg_ver, l):
    docStr = get_misc_html_file(bbg_ver, l)
    file_path = f'{l}/misc_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)

def generate_names_html_file(bbg_ver, l):
    docStr = get_names_html_file(bbg_ver, l)
    file_path = f'{l}/names_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)

def generate_great_people_html_file(bbg_ver, l):
    docStr = get_great_people_html_file(bbg_ver, l)
    file_path = f'{l}/great_people_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)

def generate_buildings_html_file(bbg_ver, l):
    docStr = get_buildings_html_file(bbg_ver, l)
    file_path = f'{l}/buildings_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)

def generate_expanded_html_file(bbg_ver, l):
    docStr = get_expanded_html_file(bbg_ver, l)
    file_path = f'{l}/bbg_expanded_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)
    if bbg_ver == latest_bbg and l == 'en_US':
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


def generate_units_html_file(bbg_ver, l):
    docStr = get_units_html_file(bbg_ver, l)
    file_path = f'{l}/units_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
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
        generate_units_html_file(bbg_ver, l)

generate_sitemap()