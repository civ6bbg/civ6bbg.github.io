from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_natural_wonder_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'

    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Natural Wonders Bonuses Description'

    menu_items = []
    menu_icons = []
    natural_wonders = get_natural_wonders_list(f"sqlFiles/{version_name}/DebugConfiguration.sqlite")
    for wonder in natural_wonders:
        menu_items.append(get_loc(locs_data, wonder[1], en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, wonder[1], en_US_locs_data))
    def create_natural_wonder_page():
        for wonder in natural_wonders:
            with div(cls="row", id=get_loc(locs_data, wonder[1], en_US_locs_data)), div(cls="col-lg-12"), div(cls="chart"):
                comment(wonder[1])
                with h2(get_loc(locs_data, wonder[1], en_US_locs_data), cls='civ-name'):
                    img(src=f'/images/natural_wonders/{get_loc(en_US_locs_data, wonder[1], en_US_locs_data)}.webp',
                        style="vertical-align: middle; width:5em",
                        onerror=image_onerror)
                br()
                show_element_with_base_option(wonder[2], lang, locs_data, en_US_locs_data)
                br()
    return create_page(bbg_version, lang, title, 'natural_wonder', menu_items, menu_icons, 'images/natural_wonders', create_natural_wonder_page)