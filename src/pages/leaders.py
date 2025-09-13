import dominate
from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_leader_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data_with_fallback(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else get_loc(locs_data, "LOC_BASE_GAME_TITLE")} {get_loc(locs_data, "LOC_PAGE_TITLE_LEADERS")}'

    menu_items = []
    menu_icons = []
    civ_leaders_items = get_civs_tables(f"sqlFiles/{version_name}/DebugConfiguration.sqlite")
    units_dict = get_units_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    tech_to_loc_dict = get_tech_to_loc_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    civic_to_loc_dict = get_civic_to_loc_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    for leader in civ_leaders_items:
        menu_items.append(get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5]))
        menu_icons.append(get_loc(en_US_locs_data, leader[2]) + ' ' + get_loc(en_US_locs_data, leader[5]))
    def create_leader_page():
        for leader in civ_leaders_items:
            with div(cls="row",
                     id=get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5])
                ), div(cls="col-lg-12"), div(cls="chart"):
                comment(f'{leader[2]} {leader[5]}')
                with h2(get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5]), cls='civ-name'):
                    img(src=f'/images/leaders/{get_loc(en_US_locs_data, leader[2]) + ' ' + get_loc(en_US_locs_data, leader[5])}.webp',
                        style="vertical-align: middle; width:7em",
                        onerror=image_onerror)
                comment(leader[3])
                h3(get_loc(locs_data, leader[3]), style="text-align:left", cls='civ-ability-name')
                br()
                show_element_with_base_option(leader[4], lang, locs_data, en_US_locs_data)
                br()
                comment(leader[6])
                h3(get_loc(locs_data, leader[6]), style="text-align:left", cls='civ-ability-name')
                br()
                show_element_with_base_option(leader[7], lang, locs_data, en_US_locs_data)
                br()
                for item in civ_leaders_items[leader]:
                    comment(item[4])
                    with h3(f'{get_loc(locs_data, item[4])}', style="text-align:left", cls='civ-ability-name'):
                        img(src=f'/images/items/{get_loc(en_US_locs_data, item[4])}.webp',
                            style="vertical-align: middle; width:2em; text-align:left",
                            onerror=image_onerror)

                    if item[3].startswith('UNIT_'):
                        unlocked_by = get_loc(locs_data, "LOC_UI_PEDIA_UNLOCKED_BY")
                        unlock_tech = units_dict[item[3]][35]
                        unlock_civic = units_dict[item[3]][36]
                        tech_civic_dialog = get_unlock_tech_civic_dialog(unlock_tech, unlock_civic, locs_data, en_US_locs_data, tech_to_loc_dict, civic_to_loc_dict)
                        base_game_tech_civic_dialog = None
                        if item[3] in base_game_units_dict:
                            unlock_tech = base_game_units_dict[item[3]][35]
                            unlock_civic = base_game_units_dict[item[3]][36]
                            base_game_tech_civic_dialog = get_unlock_tech_civic_dialog(
                                unlock_tech, unlock_civic, locs_data, en_US_locs_data, tech_to_loc_dict, civic_to_loc_dict)
                        show_element_with_base_option(item[5], lang, locs_data, en_US_locs_data, 
                            data_append = (f'[NEWLINE][NEWLINE]{unlocked_by} {tech_civic_dialog}' if tech_civic_dialog != None else ''), 
                            base_game_data_append = (f'[NEWLINE][NEWLINE]{unlocked_by} {base_game_tech_civic_dialog}' if base_game_tech_civic_dialog != None else ''))
                    else:
                        show_element_with_base_option(item[5], lang, locs_data, en_US_locs_data)
                    br()
    return create_page(bbg_version, lang, title, 'leaders', menu_items, menu_icons, 'images/leaders', pages_list, create_leader_page, locs_data, en_US_locs_data)