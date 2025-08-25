from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_bbg_expanded_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else get_loc(locs_data, "LOC_BASE_GAME_TITLE", en_US_locs_data)} {get_loc(locs_data, "LOC_PAGE_TITLE_BBG_EXPANDED", en_US_locs_data)}'

    menu_items = []
    menu_icons = []
    civ_leaders_items = get_expanded_civs_tables(f"sqlFiles/{version_name}/DebugConfiguration.sqlite")
    governors = get_expanded_governors_list(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    governor_promotion_dict = get_governors_promotion_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    governor_promotion_set_dict = get_governors_promotion_sets_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite", governors, governor_promotion_dict)
    units_dict = get_units_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    tech_to_loc_dict = get_tech_to_loc_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    civic_to_loc_dict = get_civic_to_loc_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    for leader in civ_leaders_items:
        menu_items.append(
          get_loc(locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(locs_data, leader[5], en_US_locs_data))
        menu_icons.append(
          f'leaders/{get_loc(en_US_locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(en_US_locs_data, leader[5], en_US_locs_data)}')
    for gov in governors:
        menu_items.append(
          get_loc(locs_data, gov[1], en_US_locs_data))
        menu_icons.append(
          f'governors/{get_loc(en_US_locs_data, gov[1], en_US_locs_data)}')
    
    def create_expanded_page():
        for leader in civ_leaders_items:
            with div(cls="row", 
                     id=get_loc(locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(locs_data, leader[5], en_US_locs_data)
                    ), div(cls="col-lg-12"), div(cls="chart"):
                comment(f'{leader[2]} {leader[5]}')
                with h2(get_loc(locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(locs_data, leader[5], en_US_locs_data), cls='civ-name'):
                    img(src=f'/images/leaders/{get_loc(en_US_locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(en_US_locs_data, leader[5], en_US_locs_data)}.webp',
                        style="vertical-align: middle; width:7em",
                        onerror=image_onerror)
                comment(leader[3])
                h3(get_loc(locs_data, leader[3], en_US_locs_data),
                   style="text-align:left",
                   cls='civ-ability-name')
                br()
                show_element_with_base_option(leader[4], lang, locs_data, en_US_locs_data, add_base_game = False)
                br()
                comment(leader[6])
                h3(get_loc(locs_data, leader[6], en_US_locs_data),
                   style="text-align:left",
                   cls='civ-ability-name')
                br()
                show_element_with_base_option(leader[7], lang, locs_data, en_US_locs_data, add_base_game = False)
                br()
                for item in civ_leaders_items[leader]:
                    comment(item[4])
                    with h3(f'{get_loc(locs_data, item[4], en_US_locs_data)}',
                            style="text-align:left",
                            cls='civ-ability-name'):
                        img(src=f'/images/items/{get_loc(en_US_locs_data, item[4], en_US_locs_data)}.webp',
                            style="vertical-align: middle; width:2em; text-align:left",
                            onerror=image_onerror)

                    if item[3].startswith('UNIT_'):
                        unlock_tech = units_dict[item[3]][35]
                        unlock_civic = units_dict[item[3]][36]
                        tech_civic_dialog = get_unlock_tech_civic_dialog(unlock_tech, unlock_civic, locs_data, en_US_locs_data, tech_to_loc_dict, civic_to_loc_dict)
                        base_game_tech_civic_dialog = ''
                        if item[3] in base_game_units_dict:
                            unlock_tech = base_game_units_dict[item[3]][35]
                            unlock_civic = base_game_units_dict[item[3]][36]
                            base_game_tech_civic_dialog = get_unlock_tech_civic_dialog(unlock_tech, unlock_civic, locs_data, en_US_locs_data, tech_to_loc_dict, civic_to_loc_dict)
                        show_element_with_base_option(item[5], lang, locs_data, en_US_locs_data, 
                            data_append = (f'[NEWLINE][NEWLINE]{tech_civic_dialog}' if tech_civic_dialog != None else ''), 
                            base_game_data_append = (f'[NEWLINE][NEWLINE]{base_game_tech_civic_dialog}' if tech_civic_dialog != None else ''),
                            add_base_game = False)
                    else:
                        show_element_with_base_option(item[5], lang, locs_data, en_US_locs_data, add_base_game = False)
                    br()
        for gov in governors:
            with div(cls="row",
                     id=get_loc(locs_data, gov[1], en_US_locs_data)
                    ), div(cls="col-lg-12"), div(cls="chart"):
                comment(gov[1])
                with h2(get_loc(locs_data, gov[1], en_US_locs_data),
                        cls='civ-name'):
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
                                with h3(f'{get_loc(locs_data, promotion_name, en_US_locs_data)}',
                                        style=f"text-align:{alignment}",
                                        cls='civ-ability-name'):
                                    br()
                                    br()
                                    promotion_desc = governor_promotion_dict[promotion][2]
                                    comment(promotion_desc)
                                    p(f'{get_loc(locs_data, promotion_desc, en_US_locs_data)}',
                                      style=f"text-align:{alignment}",
                                      cls='civ-ability-desc')
                                    br()

    return create_page(bbg_version, lang, title, 'bbg_expanded', menu_items, menu_icons, 'images', pages_list, create_expanded_page, locs_data, en_US_locs_data)