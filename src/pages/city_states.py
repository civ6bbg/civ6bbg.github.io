from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_city_state_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'

    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} City States Bonuses Description'

    menu_items = []
    menu_icons = []
    city_states = get_city_states(f"sqlFiles/{version_name}/DebugConfiguration.sqlite")
    cs_by_type = {}
    for cs in city_states:
        cs_type = cs[4]
        cs_by_type.setdefault(cs_type, [])
        cs_by_type[cs_type].append(cs)
    for cs_type in cs_by_type:
        cs_by_type[cs_type].sort(key=lambda x: get_loc(locs_data, x[2], en_US_locs_data))
    category_icon_map = {
        "CULTURAL": 'ICON_DISTRICT_THEATER',
        "INDUSTRIAL": 'ICON_DISTRICT_INDUSTRIAL_ZONE',
        'MILITARISTIC': 'ICON_DISTRICT_ENCAMPMENT',
        'RELIGIOUS': 'ICON_DISTRICT_HOLY_SITE',
        'SCIENTIFIC': 'ICON_DISTRICT_CAMPUS',
        'TRADE': 'ICON_DISTRICT_COMMERCIAL_HUB',
    }
    for cs_type in cs_by_type:
        menu_items.append(get_loc(locs_data, f'LOC_CITY_STATES_TYPE_{cs_type}', en_US_locs_data))
        menu_icons.append(category_icon_map[cs_type])

    def create_city_state_page():
        for cs_type in cs_by_type:
            with div(cls='col-lg-12', id=get_loc(locs_data, f'LOC_CITY_STATES_TYPE_{cs_type}', en_US_locs_data)), div(cls="chart"):
                comment(cs_type)
                h2(get_loc(locs_data, f'LOC_CITY_STATES_TYPE_{cs_type}', en_US_locs_data), cls='civ-name')
            with div(cls="row"):
                for cs in cs_by_type[cs_type]:
                    with div(cls="col-lg-6 col-md-12"), div(cls="chart"):
                        comment(cs[2])
                        with h2(get_loc(locs_data, cs[2], en_US_locs_data), cls='civ-name'):
                            img(src=f'/images/city_states/{get_loc(en_US_locs_data, cs[2], en_US_locs_data)}.webp',
                                style="vertical-align: middle; width:5em",
                                onerror=image_onerror)
                        cs_desc = cs[7] if cs[7] != None else (cs[6] if cs[6] != None else cs[5])
                        show_element_with_base_option(cs_desc, lang, locs_data, en_US_locs_data)
                        br()
    return create_page(bbg_version, lang, title, 'city_states', menu_items, menu_icons, 'images', pages_list, create_city_state_page, locs_data, en_US_locs_data)