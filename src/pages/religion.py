from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_religion_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'

    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Religions Beliefs Description'

    types = [
        'LOC_BELIEF_CLASS_PANTHEON_NAME',
        'LOC_BELIEF_CLASS_FOLLOWER_NAME',
        'LOC_BELIEF_CLASS_FOUNDER_NAME',
        'LOC_BELIEF_CLASS_ENHANCER_NAME',
        'LOC_BELIEF_CLASS_WORSHIP_NAME',
    ]
    menu_items = []
    menu_icons = []

    religion_cls_elements = {}
    for t in types:
        menu_items.append(get_loc(locs_data, t, en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, t, en_US_locs_data))
        religion_cls_elements[t] = get_beliefs(f"sqlFiles/{version_name}/DebugGameplay.sqlite", t[4:-5])

    def create_religion_page():
        for religion_cls in religion_cls_elements.keys():
            with div(cls="row", id=get_loc(locs_data, religion_cls, en_US_locs_data)):
                with div(cls="col-lg-12"), div(cls="chart"):
                    with h1(get_loc(locs_data, religion_cls, en_US_locs_data), cls='civ-name'):
                        img(src=f'/images/religion/{get_loc(en_US_locs_data, religion_cls, en_US_locs_data)}.webp',
                            style="vertical-align: middle; height:4em",
                            onerror=image_onerror)
                for elem in religion_cls_elements[religion_cls]:
                    with div(cls="col-lg-6"), div(cls="chart"):
                        if religion_cls == 'LOC_BELIEF_CLASS_PANTHEON_NAME':
                            comment(elem[1])
                            with h2(get_loc(locs_data, elem[1], en_US_locs_data), cls='civ-name'):
                                img(src=f'/images/religion/{get_loc(en_US_locs_data, elem[1], en_US_locs_data)}.webp',
                                    style="vertical-align: middle; height:3em",
                                    onerror=image_onerror)
                        else:
                            comment(elem[1])
                            h2(get_loc(locs_data, elem[1], en_US_locs_data), cls='civ-name')
                        show_element_with_base_option(elem[2], lang, locs_data, en_US_locs_data)
    return create_page(bbg_version, lang, title, 'religion', menu_items, menu_icons, 'images/religion', pages_list, create_religion_page, locs_data, en_US_locs_data)