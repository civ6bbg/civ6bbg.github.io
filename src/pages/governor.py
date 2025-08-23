from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_governor_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'

    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Governors and their Promotions Description'

    menu_items = []
    menu_icons = []
    governors = get_governors_list(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    governor_promotion_dict = get_governors_promotion_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    governor_promotion_set_dict = get_governors_promotion_sets_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite", governors, governor_promotion_dict)
    for gov in governors:
        menu_items.append(get_loc(locs_data, gov[1], en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, gov[1], en_US_locs_data))
    def create_governor_page():
        for gov in governors:
            with div(cls="row", id=get_loc(locs_data, gov[1], en_US_locs_data)), div(cls="col-lg-12"), div(cls="chart"):
                comment(gov[1])
                with h2(get_loc(locs_data, gov[1], en_US_locs_data), cls='civ-name'):
                    img(src=f'/images/governors/{get_loc(en_US_locs_data, gov[1], en_US_locs_data)}.webp',
                        style="vertical-align: middle; width:7em",
                        onerror=image_onerror)
                br()
                for level in governor_promotion_set_dict[gov[0]]:
                    column_count = len(governor_promotion_set_dict[gov[0]][level])
                    div_cls = f'col-lg-{math.floor(12 / column_count)}'
                    with div(cls='row'):
                        for column in governor_promotion_set_dict[gov[0]][level]:
                            has_border = 'gov-promotion-border' if column < column_count - 1 else ''
                            with div(cls=f'{div_cls} gov-promotion {has_border}'):
                                promotion = governor_promotion_set_dict[gov[0]][level][column][0]
                                promotion_name = governor_promotion_dict[promotion][1]
                                alignment = 'left' if column == 0 else 'center' if column == 1 else 'right'
                                comment(promotion_name)
                                with h3(f'{get_loc(locs_data, promotion_name, en_US_locs_data)}', style=f"text-align:{alignment}", cls='civ-ability-name'):
                                    br()
                                    br()
                                    promotion_desc = governor_promotion_dict[promotion][2]
                                    comment(promotion_desc)
                                    p(f'{get_loc(locs_data, promotion_desc, en_US_locs_data)}', style=f"text-align:{alignment}", cls='civ-ability-desc')
                                    br()
    return create_page(bbg_version, lang, title, 'governor', menu_items, menu_icons, 'images/governors', create_governor_page)