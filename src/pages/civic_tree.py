from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_improvement_buff_text(improvement_buff, locs_data):
    improvement_name = improvement_buff[5]
    yield_type = improvement_buff[1]
    yield_amount = improvement_buff[2]
    return f'{get_loc(locs_data, improvement_name)}: +{yield_amount} {get_loc(locs_data, f"LOC_{yield_type}_NAME")}'

def get_civic_tree_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data_with_fallback(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else get_loc(locs_data, "LOC_BASE_GAME_TITLE")} {get_loc(locs_data, "LOC_PAGE_TITLE_CIVIC_TREE")}'

    menu_items = []
    menu_icons = []
    civic_per_era = get_civics_per_era(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    civic_prereqs = get_civic_prereqs(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    policies = get_civic_policies(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    boosts = get_techcivic_boosts(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    units_techcivic = get_units_per_techcivic(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    improvements_techcivic = get_improvements_per_techcivic(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    improvements_buffs_techcivic = get_improvement_buffs_per_techcivic(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    buildings_techcivic = get_buildings_per_techcivic(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    wonders_techcivic = get_wonders_per_techcivic(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    districts_techcivic = get_districts_per_techcivic(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    eras_list = [
        'ERA_ANCIENT',
        'ERA_CLASSICAL',
        'ERA_MEDIEVAL',
        'ERA_RENAISSANCE',
        'ERA_INDUSTRIAL',
        'ERA_MODERN',
        'ERA_ATOMIC',
        'ERA_INFORMATION',
        'ERA_FUTURE',
    ]
    for era in eras_list:
        menu_items.append(
          get_loc(locs_data, f'LOC_{era}_NAME'))
        menu_icons.append(
          f'{get_loc(en_US_locs_data, f'LOC_{era}_NAME')}')
    
    def create_civic_tree_page():
        for era in eras_list:
            with div(cls="row", 
                     id=get_loc(locs_data, f'LOC_{era}_NAME')
                    ), div(cls="col-lg-12"), div(cls="chart"):
                comment(f'{era}')
                with h2(get_loc(locs_data, f'LOC_{era}_NAME'), cls='civ-name'):
                    img(src=f'/images/{get_loc(en_US_locs_data, f'LOC_{era}_NAME')}.webp',
                        style="vertical-align: middle; width:3em",
                        onerror=image_onerror)
            with div(cls="row"):
                for civic in civic_per_era[era]:
                    with div(cls="col-sm-6 col-12"), div(cls="chart"):
                        comment(civic[1])
                        flag = False
                        with h3(f'{get_loc(locs_data, civic[1])}',
                                style="text-align:left",
                                cls='civ-ability-name'):
                            img(src=f'/images/civic/{get_loc(en_US_locs_data, civic[1]).replace(' ', '_')}.webp',
                                style="vertical-align: middle; width:2em; text-align:left",
                                onerror=image_onerror)
                        if civic[0] in units_techcivic:
                            for unit in units_techcivic[civic[0]]:
                                img(src=f'/images/units/{get_loc(en_US_locs_data, unit[3]).replace(' ', '_')}.webp',
                                    style="vertical-align: middle; width:2em",
                                    title = get_loc(locs_data, unit[3]),
                                    onerror=image_onerror)
                                flag = True
                        if civic[0] in improvements_techcivic:
                            for improvement in improvements_techcivic[civic[0]]:
                                img(src=f'/images/improvements/{get_loc(en_US_locs_data, improvement[3])}.webp',
                                    style="vertical-align: middle; width:2em",
                                    title = get_loc(locs_data, improvement[3]),
                                    onerror=image_onerror)
                                flag = True
                        if civic[0] in buildings_techcivic:
                            for building in buildings_techcivic[civic[0]]:
                                img(src=f'/images/buildings/{get_loc(en_US_locs_data, building[3])}.webp',
                                    style="vertical-align: middle; width:2em",
                                    title = get_loc(locs_data, building[3]),
                                    onerror=image_onerror)
                                flag = True
                        if civic[0] in wonders_techcivic:
                            for wonder in wonders_techcivic[civic[0]]:
                                img(src=f'/images/world_wonders/{get_loc(en_US_locs_data, wonder[3])}.webp',
                                    style="vertical-align: middle; width:2em",
                                    title = get_loc(locs_data, wonder[3]),
                                    onerror=image_onerror)
                                flag = True
                        if civic[0] in districts_techcivic:
                            for district in districts_techcivic[civic[0]]:
                                img(src=f'/images/districts/{get_loc(en_US_locs_data, district[3])}.webp',
                                    style="vertical-align: middle; width:2em",
                                    title = get_loc(locs_data, district[3]),
                                    onerror=image_onerror)
                                flag = True
                        if civic[0] in improvements_buffs_techcivic:
                            for improvement_buff in improvements_buffs_techcivic[civic[0]]:
                                img(src=f'/images/improvements/{get_loc(en_US_locs_data, improvement_buff[5])}.webp',
                                    style="vertical-align: middle; width:2em",
                                    title = get_improvement_buff_text(improvement_buff, locs_data),
                                    onerror=image_onerror)
                                flag = True
                        if flag:
                            br()
                            flag = False
                        if civic[0] in boosts:
                            p(f'{get_loc(locs_data, "LOC_BOOST_TO_BOOST")} {get_loc(locs_data, boosts[civic[0]][2])}', 
                                style="text-align:left",
                                cls='civ-ability-desc')
                            br()
                        # Policy Cards:
                        if civic[0] in policies:
                            for policy in policies[civic[0]]:
                                with p(get_loc(locs_data, policy[1]),
                                    style="text-align:left",
                                    cls='civ-ability-desc'):
                                    img(src=f'/images/policies/{policy[3]}.webp',
                                        style="vertical-align: middle; width:1.5em; display: inline-block",
                                        onerror=image_onerror)
                                div(get_loc(locs_data, policy[2]),
                                    style="text-align:left",
                                    cls='civ-ability-desc')
                        if civic[0] in civic_prereqs:
                            prereq_civics = civic_prereqs[civic[0]]
                            prereq_civics_locs = [get_loc(locs_data, prereq_civics[i][2]) for i in range(len(prereq_civics))]
                            prereq_civic_requires = f'{get_loc(locs_data, "LOC_HUD_RESEARCH_REQUIRES")} {", ".join(prereq_civics_locs)}'
                            p(prereq_civic_requires,
                                style="text-align:left",
                                cls='civ-ability-desc')

    return create_page(bbg_version, lang, title, 'civic_tree', menu_items, menu_icons, 'images', pages_list, create_civic_tree_page, locs_data, en_US_locs_data)