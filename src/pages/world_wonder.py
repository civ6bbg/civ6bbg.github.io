from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *
from pages.buildings import show_building_yields

def get_world_wonder_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data_with_fallback(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'
    tech_to_loc_dict = get_tech_to_loc_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    civic_to_loc_dict = get_civic_to_loc_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else get_loc(locs_data, "LOC_BASE_GAME_TITLE")} {get_loc(locs_data, "LOC_PAGE_TITLE_WORLD_WONDERS")}'

    menu_items = []
    menu_icons = []
    world_wonders = get_world_wonders_list(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    for era in world_wonders.keys():
        menu_items.append(get_loc(locs_data, era))
        menu_icons.append(get_loc(en_US_locs_data, era))

    def create_world_wonder_page():
        for era in world_wonders.keys():
            with div(cls='col-lg-12', id=get_loc(locs_data, era)), div(cls="chart"):
                comment(era)
                h2(get_loc(locs_data, era), cls='civ-name')
            with div(cls="row"):
                for wonder_name in world_wonders[era]:
                    wonder = world_wonders[era][wonder_name]
                    with div(cls="col-lg-6 col-md-12"), div(cls="chart"):
                        comment(wonder[0][1])
                        with h2(get_loc(locs_data, wonder[0][1]), cls='civ-name'):
                            img(src=f'/images/world_wonders/{get_loc(en_US_locs_data, wonder[0][1])}.webp',
                                style="vertical-align: middle; width:5em",
                                onerror=image_onerror)
                        br()
                        show_building_yields(wonder, locs_data, en_US_locs_data)
                        unlocked_by = get_loc(locs_data, "LOC_UI_PEDIA_UNLOCKED_BY")
                        unlock_tech = wonder[0][23]
                        unlock_civic = wonder[0][24]
                        tech_civic_dialog = get_unlock_tech_civic_dialog(unlock_tech, unlock_civic, locs_data, en_US_locs_data, tech_to_loc_dict, civic_to_loc_dict)
                        p(f'{unlocked_by} {tech_civic_dialog}' if tech_civic_dialog != None else '',
                            style="text-align:left",
                            cls='civ-ability-desc')
                        br()
    return create_page(bbg_version, lang, title, 'world_wonder', menu_items, menu_icons, 'images/world_wonders', pages_list, create_world_wonder_page, locs_data, en_US_locs_data)