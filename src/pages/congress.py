from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_congress_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data_with_fallback(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else get_loc(locs_data, "LOC_BASE_GAME_TITLE")} {get_loc(locs_data, "LOC_PEDIA_CONCEPTS_PAGE_WORLD_CONGRESS_CHAPTER_CONGRESS_TITLE")}'

    menu_items = []
    menu_icons = []
    congress_options = get_congress_options(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    for opt in congress_options:
        menu_items.append(get_loc(locs_data, opt[2]))
        menu_icons.append(f'/images/resolutions/{opt[0]}.webp')

    def create_congress_page():
        for opt in congress_options:
            with div(cls="row"):
                with div(cls="col-lg-12"), div(cls="chart"):
                    comment(opt[2])
                    with h2(get_loc(locs_data, opt[2]), cls='civ-name'):
                        img(src=f'/images/resolutions/{opt[0]}.webp',
                            style="vertical-align: middle; width:5em",
                            onerror=image_onerror)
                    p(f'{get_loc(locs_data, opt[3])}', style=f"text-align:left", cls='civ-ability-desc')
                    p(f'{get_loc(locs_data, opt[4])}', style=f"text-align:right", cls='civ-ability-desc')
                    if opt[9]:
                        era_name = f'LOC_{opt[9]}_NAME'
                        p(f'Earliest Era: {get_loc(locs_data, era_name)}', style=f"text-align:left", cls='civ-ability-desc')
                    if opt[10]:
                        era_name = f'LOC_{opt[10]}_NAME'
                        p(f'Latest Era: {get_loc(locs_data, era_name)}', style=f"text-align:left", cls='civ-ability-desc')
                    br()
                    
    return create_page(bbg_version, lang, title, 'congress', menu_items, menu_icons, 'images', pages_list, create_congress_page, locs_data, en_US_locs_data)