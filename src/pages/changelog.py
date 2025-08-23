from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_changelog_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'

    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Changelog'

    menu_items = []
    menu_icons = []

    def create_changelog_page():
        with div(cls='col-lg-12'), div(cls="chart"):
            h2("Changelog", cls='civ-name')
    return create_page(bbg_version, lang, title, 'changelog', menu_items, menu_icons, 'images', pages_list, create_changelog_page)