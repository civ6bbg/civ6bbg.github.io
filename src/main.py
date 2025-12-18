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

from pages_list import *
from dom_generator_helper import *

langs = ['en_US', 'de_DE', 'es_ES', 'it_IT', 'ko_KR', 'pt_BR', 'zh_Hans_CN', 'fr_FR', 'ja_JP', 'pl_PL', 'ru_RU']
langs_tmp = ['en_US', 'fr_FR']
bbg_versions_tmp = [None, '7.2']
latest_bbg = '7.2'

sitemap = {bbg_ver: {l: [] for l in langs} for bbg_ver in bbg_versions}

bbg_version_last_timestamp = {bbg_ver: None for bbg_ver in bbg_versions}
bbg_version_last_timestamp[None] = datetime.date(2025, 12, 15)
bbg_version_last_timestamp['7.2'] = datetime.date(2025, 12, 15)
bbg_version_last_timestamp['7.1'] = datetime.date(2025, 12, 15)
bbg_version_last_timestamp['6.5'] = datetime.date(2025, 12, 15)
bbg_version_last_timestamp['6.4'] = datetime.date(2025, 12, 15)
bbg_version_last_timestamp['6.3'] = datetime.date(2025, 12, 15)
bbg_version_last_timestamp['6.2'] = datetime.date(2025, 12, 15)
bbg_version_last_timestamp['6.1'] = datetime.date(2025, 12, 15)
bbg_version_last_timestamp['6.0'] = datetime.date(2025, 12, 15)
bbg_version_last_timestamp['5.8'] = datetime.date(2025, 12, 15)
bbg_version_last_timestamp['5.7'] = datetime.date(2025, 12, 15)
bbg_version_last_timestamp['5.6'] = datetime.date(2025, 12, 15)

def generate_html_file(bbg_ver, l, get_page_function, page_name):
    docStr = get_page_function(bbg_ver, l, pages_list)
    file_path = f'{l}/{page_name}_{'base_game' if bbg_ver == None else bbg_ver}.html'
    sitemap[bbg_ver][l].append(file_path)
    with open(file_path, 'w') as f:
        f.write(docStr)
    if bbg_ver == latest_bbg and l == 'en_US' and page_name == 'leaders':
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
        for page in pages_list:
            page_name = page['name']
            get_page_function = page['func']
            # if page_name == 'civic_tree' or page_name == 'tech_tree':
            print(f'  page: {page_name}')
            generate_html_file(bbg_ver, l, get_page_function, page_name)

generate_sitemap()