from bs4 import BeautifulSoup
import sqlite3
import re
import math

import dominate
from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

image_onerror = "this.onerror=null; this.src='/images/civVI.webp';"

def get_leader_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Leaders and their Abilities Description'
    add_html_header(doc, title)

    menu_items = []
    menu_icons = []
    civ_leaders_items = get_civs_tables(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugConfiguration.sqlite")
    units_dict = get_units_dict(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    tech_to_loc_dict = get_tech_to_loc_dict(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    civic_to_loc_dict = get_civic_to_loc_dict(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    for leader in civ_leaders_items:
        menu_items.append(get_loc(locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(locs_data, leader[5], en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(en_US_locs_data, leader[5], en_US_locs_data))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, 'leaders')
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/leaders')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                h1(title, cls='civ-name')
                                br()
                                for leader in civ_leaders_items:
                                    with div(cls="row", id=get_loc(locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(locs_data, leader[5], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                comment(f'{leader[2]} {leader[5]}')
                                                with h2(get_loc(locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(locs_data, leader[5], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/leaders/{get_loc(en_US_locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(en_US_locs_data, leader[5], en_US_locs_data)}.webp', style="vertical-align: middle; width:7em", onerror=image_onerror)
                                                comment(leader[3])
                                                h3(get_loc(locs_data, leader[3], en_US_locs_data), style="text-align:left", cls='civ-ability-name')
                                                br()
                                                show_element_with_base_option(leader[4], lang, locs_data, en_US_locs_data)
                                                br()
                                                comment(leader[6])
                                                h3(get_loc(locs_data, leader[6], en_US_locs_data), style="text-align:left", cls='civ-ability-name')
                                                br()
                                                show_element_with_base_option(leader[7], lang, locs_data, en_US_locs_data)
                                                br()
                                                for item in civ_leaders_items[leader]:
                                                    comment(item[4])
                                                    with h3(f'{get_loc(locs_data, item[4], en_US_locs_data)}', style="text-align:left", cls='civ-ability-name'):
                                                        img(src=f'/images/items/{get_loc(en_US_locs_data, item[4], en_US_locs_data)}.webp', style="vertical-align: middle; width:2em; text-align:left", onerror=image_onerror)

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
                                                            base_game_data_append = (f'[NEWLINE][NEWLINE]{base_game_tech_civic_dialog}' if tech_civic_dialog != None else ''))
                                                    else:
                                                        show_element_with_base_option(item[5], lang, locs_data, en_US_locs_data)
                                                    br()

        add_final_scripts()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_city_state_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} City States Bonuses Description'
    add_html_header(doc, title)

    menu_items = []
    menu_icons = []
    city_states = get_city_states(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugConfiguration.sqlite")
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

    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, 'city_states')
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                h1(title, cls='civ-name')
                                br()
                                for cs_type in cs_by_type:
                                    with div(cls='col-lg-12', id=get_loc(locs_data, f'LOC_CITY_STATES_TYPE_{cs_type}', en_US_locs_data)), div(cls="chart"):
                                        comment(cs_type)
                                        h2(get_loc(locs_data, f'LOC_CITY_STATES_TYPE_{cs_type}', en_US_locs_data), cls='civ-name')
                                    with div(cls="row"):
                                        for cs in cs_by_type[cs_type]:
                                            with div(cls="col-lg-6 col-md-12"), div(cls="chart"):
                                                comment(cs[2])
                                                with h2(get_loc(locs_data, cs[2], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/city_states/{get_loc(en_US_locs_data, cs[2], en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=image_onerror)
                                                cs_desc = cs[7] if cs[7] != None else (cs[6] if cs[6] != None else cs[5])
                                                show_element_with_base_option(cs_desc, lang, locs_data, en_US_locs_data)
                                                br()

        add_final_scripts()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_religion_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Religions Beliefs Description'
    add_html_header(doc, title)

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
        religion_cls_elements[t] = get_beliefs(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", t[4:-5])

    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, 'religion')
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/religion')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                h1(title, cls='civ-name')
                                br()
                                for religion_cls in religion_cls_elements.keys():
                                    with div(cls="row", id=get_loc(locs_data, religion_cls, en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                with h1(get_loc(locs_data, religion_cls, en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/religion/{get_loc(en_US_locs_data, religion_cls, en_US_locs_data)}.webp', style="vertical-align: middle; height:4em", onerror=image_onerror)
                                        for elem in religion_cls_elements[religion_cls]:
                                            with div(cls="col-lg-6"):
                                                with div(cls="chart"):
                                                    if religion_cls == 'LOC_BELIEF_CLASS_PANTHEON_NAME':
                                                        comment(elem[1])
                                                        with h2(get_loc(locs_data, elem[1], en_US_locs_data), cls='civ-name'):
                                                            img(src=f'/images/religion/{get_loc(en_US_locs_data, elem[1], en_US_locs_data)}.webp', style="vertical-align: middle; height:3em", onerror=image_onerror)
                                                    else:
                                                        comment(elem[1])
                                                        h2(get_loc(locs_data, elem[1], en_US_locs_data), cls='civ-name')
                                                    show_element_with_base_option(elem[2], lang, locs_data, en_US_locs_data)

        add_final_scripts()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_governor_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Governors and their Promotions Description'
    add_html_header(doc, title)

    menu_items = []
    menu_icons = []
    governors = get_governors_list(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    governor_promotion_dict = get_governors_promotion_dict(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    governor_promotion_set_dict = get_governors_promotion_sets_dict(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", governors, governor_promotion_dict)
    for gov in governors:
        menu_items.append(get_loc(locs_data, gov[1], en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, gov[1], en_US_locs_data))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, 'governor')
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/governors')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                h1(title, cls='civ-name')
                                br()
                                for gov in governors:
                                    with div(cls="row", id=get_loc(locs_data, gov[1], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                comment(gov[1])
                                                with h2(get_loc(locs_data, gov[1], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/governors/{get_loc(en_US_locs_data, gov[1], en_US_locs_data)}.webp', style="vertical-align: middle; width:7em", onerror=image_onerror)
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
                                                                    # show_element_with_base_option(promotion_desc, lang, locs_data, en_US_locs_data, alignment = alignment)
                                                                    br()

        add_final_scripts()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_natural_wonder_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Natural Wonders Bonuses Description'
    add_html_header(doc, title)

    menu_items = []
    menu_icons = []
    natural_wonders = get_natural_wonders_list(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugConfiguration.sqlite")
    for wonder in natural_wonders:
        menu_items.append(get_loc(locs_data, wonder[1], en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, wonder[1], en_US_locs_data))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, 'natural_wonder')
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/natural_wonders')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                h1(title, cls='civ-name')
                                br()
                                for wonder in natural_wonders:
                                    with div(cls="row", id=get_loc(locs_data, wonder[1], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                comment(wonder[1])
                                                with h2(get_loc(locs_data, wonder[1], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/natural_wonders/{get_loc(en_US_locs_data, wonder[1], en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=image_onerror)
                                                br()
                                                show_element_with_base_option(wonder[2], lang, locs_data, en_US_locs_data)
                                                br()
        add_final_scripts()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_world_wonder_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} World Wonders Bonuses Description'
    add_html_header(doc, title)

    menu_items = []
    menu_icons = []
    world_wonders = get_world_wonders_list(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    for era in world_wonders.keys():
        menu_items.append(get_loc(locs_data, era, en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, era, en_US_locs_data))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, 'world_wonder')
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/world_wonders')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                h1(title, cls='civ-name')
                                br()
                                for era in world_wonders.keys():
                                    with div(cls='col-lg-12', id=get_loc(locs_data, era, en_US_locs_data)):
                                        with div(cls="chart"):
                                            comment(era)
                                            h2(get_loc(locs_data, era, en_US_locs_data), cls='civ-name')
                                    with div(cls="row"):
                                        for wonder_name in world_wonders[era]:
                                            wonder = world_wonders[era][wonder_name]
                                            with div(cls="col-lg-6 col-md-12"):
                                                with div(cls="chart"):
                                                    comment(wonder[0][1])
                                                    with h2(get_loc(locs_data, wonder[0][1], en_US_locs_data), cls='civ-name'):
                                                        img(src=f'/images/world_wonders/{get_loc(en_US_locs_data, wonder[0][1], en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=image_onerror)
                                                    br()
                                                    show_building_yields(wonder, locs_data, en_US_locs_data)
                                                    br()
        add_final_scripts()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_misc_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Miscellaneous Details on Eras and Alliances'
    add_html_header(doc, title)

    menu_items = []
    menu_icons = []

    dedication_list_per_era = get_dedication_list_per_era(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    for era in dedication_list_per_era.keys():
        menu_items.append(get_loc(locs_data, era, en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, era, en_US_locs_data))

    alliance_list = get_alliance_list(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    for alliance in alliance_list:
        menu_items.append(get_loc(locs_data, alliance[1], en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, alliance[1], en_US_locs_data))

    dark_age_policy = get_dark_age_card_list(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    dark_age_policy_era = get_dark_age_card_list_eras(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    dark_age_policy_per_era = get_dark_age_card_list_per_era(dark_age_policy, dark_age_policy_era)

    eras_reverse_map = {
        'LOC_ERA_CLASSICAL_NAME':'ERA_CLASSICAL',
        'LOC_ERA_MEDIEVAL_NAME':'ERA_MEDIEVAL',
        'LOC_ERA_RENAISSANCE_NAME':'ERA_RENAISSANCE',
        'LOC_ERA_INDUSTRIAL_NAME':'ERA_INDUSTRIAL',
        'LOC_ERA_MODERN_NAME':'ERA_MODERN',
        'LOC_ERA_ATOMIC_NAME':'ERA_ATOMIC',
        'LOC_ERA_INFORMATION_NAME':'ERA_INFORMATION',
        'LOC_ERA_FUTURE_NAME':'ERA_FUTURE'
    }

    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, 'misc')
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                h1(title, cls='civ-name')
                                br()
                                for era in dedication_list_per_era.keys():
                                    with div(cls="row", id=get_loc(locs_data, era, en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                comment(era)
                                                h2(get_loc(locs_data, era, en_US_locs_data), cls='civ-name')
                                    with div(cls="row"):
                                        with div(cls="chart"):
                                            with div(cls="row"):
                                                for dedication in dedication_list_per_era[era]:
                                                    # print(dedication[0])
                                                    with div(cls="col-lg-3"):
                                                        comment(dedication[0])
                                                        img(src=f'/images/ICON_{dedication[0]}.webp', style="vertical-align: middle; width:5em", onerror=image_onerror)
                                                        comment(dedication[2])
                                                        p(get_loc(locs_data, dedication[2], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')
                                                        br()
                                                br()
                                    with div(cls="row"):
                                        for policy in dark_age_policy_per_era[eras_reverse_map[era]]:
                                            with div(cls="col-lg-3"):
                                                with div(cls="chart"):
                                                    comment(policy[4])
                                                    h2(get_loc(locs_data, policy[4], en_US_locs_data), cls='civ-name')
                                                    br()
                                                    comment(policy[1])
                                                    p(get_loc(locs_data, policy[1], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')
                                                    br()
                                for alliance in alliance_list:
                                    with div(cls="row", id=get_loc(locs_data, alliance[1], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            comment(alliance[1])
                                            h2(get_loc(locs_data, alliance[1], en_US_locs_data), cls='civ-name')
                                            br()
                                            alliance_effect = get_alliance_effects(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", alliance[0])
                                            for lvl in alliance_effect.keys():
                                                with h3(f'Level {lvl}', style="text-align:left", cls='civ-ability-name'):
                                                    br()
                                                    br()
                                                    with div(cls="row"):
                                                        div_cls_sz = math.floor(12 / len(alliance_effect[lvl]))
                                                        div_cls = f'col-md-{div_cls_sz} col-lg-{div_cls_sz}'
                                                        for effect in alliance_effect[lvl]:
                                                            with div(cls=div_cls):
                                                                with div(cls="chart"):
                                                                    comment(effect)
                                                                    p(get_loc(locs_data, effect, en_US_locs_data), style="text-align:left", cls='civ-ability-desc')
                                            br()
 
        add_final_scripts()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_names_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Map Elements Naming Information'
    add_html_header(doc, title)

    menu_items = []
    menu_icons = []
    desert_names = get_property_names(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", 'Desert', 'Deserts')
    lakes_names = get_property_names(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", 'Lake', 'Lakes')
    mountain_names = get_property_names(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", 'Mountain', 'Mountains')
    river_names = get_property_names(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", 'River', 'Rivers')
    sea_names = get_property_names(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", 'Sea', 'Seas')
    volcano_names = get_property_names(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", 'Volcano', 'Volcanoes')

    menu_items.append('Desert')
    menu_icons.append('Desert')
    menu_items.append('Lake')
    menu_icons.append('Lake')
    menu_items.append('Mountain')
    menu_icons.append('Mountain')
    menu_items.append('River')
    menu_icons.append('River')
    menu_items.append('Sea')
    menu_icons.append('Sea')
    menu_items.append('Volcano')
    menu_icons.append('Volcano')

    name_classes = {
        'Desert': desert_names,
        'Lakes': lakes_names,
        'Mountain': mountain_names,
        'River': river_names,
        'Sea': sea_names,
        'Volcano': volcano_names
    }

    # for name_cls in name_classes.keys():
    #     print(name_classes[name_cls])

    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, 'names')
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                h1(title, cls='civ-name')
                                br()
                                for name_cls in name_classes.keys():
                                    with div(cls="row", id=name_cls):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                h2(name_cls, cls='civ-name')
                                    with div(cls="row"):
                                        # with div(cls="chart"):
                                        with div(cls="row"):
                                            for property_name in name_classes[name_cls]:
                                                if len(name_classes[name_cls][property_name]) <= 1:
                                                    div_cls = 'col-md-3 col-lg-3'
                                                elif len(name_classes[name_cls][property_name]) <= 3:
                                                    div_cls = 'col-md-6 col-lg-6'
                                                else:
                                                    div_cls = 'col-md-12 col-lg-12'
                                                with div(cls=div_cls):
                                                    with div(cls="chart"):
                                                        comment(property_name)
                                                        h2(get_loc(locs_data, f'{property_name}', en_US_locs_data), style="text-align:center", cls='civ-ability-desc')
                                                        with div(cls='row'):
                                                            cls_len = math.floor(12 / (1 if len(name_classes[name_cls][property_name]) == 0 else len(name_classes[name_cls][property_name])))
                                                            curr_div_cls = f'col-md-{cls_len} col-lg-{cls_len}'
                                                            for name in name_classes[name_cls][property_name]:
                                                                with div(cls=curr_div_cls):
                                                                    comment(name)
                                                                    p(get_loc(locs_data, f'{name}', en_US_locs_data), style="text-align:center", cls='civ-ability-desc')
                                                                # br()
                                            br()
        add_final_scripts()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_great_people_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Great People Abilities Description'
    add_html_header(doc, title)

    eras_loc = [
        'LOC_ERA_ANCIENT_NAME',
        'LOC_ERA_CLASSICAL_NAME',
        'LOC_ERA_MEDIEVAL_NAME',
        'LOC_ERA_RENAISSANCE_NAME',
        'LOC_ERA_INDUSTRIAL_NAME',
        'LOC_ERA_MODERN_NAME',
        'LOC_ERA_ATOMIC_NAME',
        'LOC_ERA_INFORMATION_NAME',
        'LOC_ERA_FUTURE_NAME'
    ]

    menu_items = []
    menu_icons = []
    great_people = get_great_people_list(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    great_people_modifier_dict = get_great_people_modifier_dict(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    great_people_works = get_great_people_great_works(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")

    great_people_list = [
        'LOC_GREAT_PERSON_CLASS_GENERAL_NAME',
        'LOC_GREAT_PERSON_CLASS_ADMIRAL_NAME',
        'LOC_GREAT_PERSON_CLASS_ENGINEER_NAME',
        'LOC_GREAT_PERSON_CLASS_MERCHANT_NAME',
        'LOC_GREAT_PERSON_CLASS_PROPHET_NAME',
        'LOC_GREAT_PERSON_CLASS_SCIENTIST_NAME',
        'LOC_GREAT_PERSON_CLASS_WRITER_NAME',
        'LOC_GREAT_PERSON_CLASS_ARTIST_NAME',
        'LOC_GREAT_PERSON_CLASS_MUSICIAN_NAME',
        'LOC_GREAT_PERSON_CLASS_COMANDANTE_GENERAL_NAME',
    ]

    for gp_type in great_people_list:
        menu_items.append(get_loc(locs_data, gp_type, en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, gp_type, en_US_locs_data))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, 'great_people')
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                h1(title, cls='civ-name')
                                br()
                                for gp_type in great_people_list:
                                    with div(cls="row", id=get_loc(locs_data, gp_type, en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                comment(gp_type)
                                                with h2(get_loc(locs_data, gp_type, en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/{get_loc(en_US_locs_data, gp_type, en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=image_onerror)
                                                    br()
                                    for era in eras_loc:
                                        if era not in great_people[gp_type].keys():
                                            continue
                                        if len(great_people[gp_type]) > 1:
                                            with div(cls="row", id=get_loc(locs_data, gp_type, en_US_locs_data)):
                                                with div(cls="col-lg-12"):
                                                    with div(cls="chart"):
                                                        comment(era)
                                                        h3(get_loc(locs_data, era, en_US_locs_data), cls='civ-name')
                                        with div(cls='row'):
                                            cls_len = max(3, math.ceil(12 / len(great_people[gp_type][era])))
                                            div_cls = f'col-md-{cls_len} col-lg-{cls_len}'
                                            for gp in great_people[gp_type][era]:
                                                with div(cls=div_cls):
                                                    with div(cls="chart"):
                                                        comment(gp[1])
                                                        p(get_loc(locs_data, gp[1], en_US_locs_data), cls='civ-ability-name')
                                                        br()
                                                        if gp[4] > 0:
                                                            with p(gp[4], cls='civ-ability-name'):
                                                                img(src=f'/images/ICON_CHARGES.webp', style="height:1em")
                                                        br()
                                                        if gp[0] in great_people_modifier_dict.keys():
                                                            for mod, amount in great_people_modifier_dict[gp[0]]:
                                                                comment(mod)
                                                                processed = loc_amount_parameter(get_loc(locs_data, mod, en_US_locs_data), amount)
                                                                p(processed, style="text-align:left", cls='civ-ability-desc')
                                                                br()
                                                        if gp[0] in great_people_works.keys():
                                                            for work in great_people_works[gp[0]]:
                                                                comment(work[1])
                                                                p(img(src=f'/images/{work[2]}.webp', style="vertical-align: middle; width:2em", onerror=image_onerror), f' {get_loc(locs_data, work[1], en_US_locs_data)}', style="text-align:left", cls='civ-ability-desc')
        add_final_scripts()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def show_building_yields(yields, locs_data, en_US_locs_data):
    yield_dict = {}
    for element in yields:
        if element[10] != None:
            if element[10] not in yield_dict:
                yield_loc = f'LOC_{element[10]}_NAME'
                yield_type = element[10][6:]
                p(f'+{element[11]} [ICON_{yield_type}] {get_loc(locs_data, yield_loc, en_US_locs_data)}', style="text-align:left", cls='civ-ability-desc')
                yield_dict[element[10]] = 1


    tmp_yields = yields[0]
    if tmp_yields[6] > 0:
        p(f'+{tmp_yields[6]} [ICON_HOUSING] {get_loc(locs_data, 'LOC_HUD_CITY_HOUSING', en_US_locs_data)}', style="text-align:left", cls='civ-ability-desc')
    if tmp_yields[7] > 0:
        p(f'+{tmp_yields[7]} [ICON_AMENITIES] {get_loc(locs_data, 'LOC_HUD_CITY_AMENITIES', en_US_locs_data)}', style="text-align:left", cls='civ-ability-desc')
    if tmp_yields[9] != None:
        processed = loc_amount_parameter(get_loc(locs_data, 'LOC_TYPE_TRAIT_CITIZENS', en_US_locs_data), tmp_yields[9])
        p(f'{processed}', style="text-align:left", cls='civ-ability-desc')

    for element in yields:
        if element[14] != None:
            gp_type = get_loc(locs_data, element[14], en_US_locs_data)
            if gp_type not in yield_dict:
                gp_icon = f'[ICON_GREAT{element[14][23:-5]}]'
                gpp_turn = element[15]
                loc = get_loc(locs_data, 'LOC_TYPE_TRAIT_GREAT_PERSON_POINTS', en_US_locs_data)
                loc = loc.replace('{2_Icon}', f'{gp_icon}')
                loc = loc.replace('{3_GreatPersonClassName}', gp_type)
                processed = loc_amount_parameter(loc, gpp_turn)
                p(f'{processed}', style="text-align:left", cls='civ-ability-desc')
                yield_dict[gp_type] = 1
        if element[16] != None:
            slot_type = element[16]
            if slot_type not in yield_dict:
                num_slots = element[17]
                loc = get_loc(locs_data, f'LOC_TYPE_TRAIT_GREAT_WORKS_{slot_type[14:]}_SLOTS', en_US_locs_data)
                processed = loc_amount_parameter(loc, num_slots)
                p(f'{processed}', style="text-align:left", cls='civ-ability-desc')
                # p(f'{num_slots} [ICON_{slot_type}] {get_loc(locs_data, slot_type, en_US_locs_data)}', style="text-align:left", cls='civ-ability-desc')
                yield_dict[slot_type] = 1
        if element[18] != None:
            key = f'{element[18]}->{element[19]}'
            if key not in yield_dict:
                from_yield_type = element[18][6:]
                to_yield_type = element[19][6:]
                loc = get_loc(locs_data, f'LOC_TYPE_TRAIT_BUILDING_DISTRICT_COPY', en_US_locs_data)
                loc = loc.replace('{1_ToYieldIcon}', f'[ICON_{to_yield_type}]')
                loc = loc.replace('{2_ToYieldName}', get_loc(locs_data, f'LOC_YIELD_{to_yield_type}_NAME', en_US_locs_data))
                loc = loc.replace('{3_FromYieldIcon}', f'[ICON_{from_yield_type}]')
                loc = loc.replace('{4_FromYieldName}', get_loc(locs_data, f'LOC_YIELD_{from_yield_type}_NAME', en_US_locs_data))

                p(f'{loc}', style="text-align:left", cls='civ-ability-desc')
                yield_dict[key] = 1
        if element[20] != None:
            key = f'Power{element[20]}'
            if key not in yield_dict:
                yield_loc = f'LOC_{element[20]}_NAME'
                yield_type = element[20][6:]
                loc = get_loc(locs_data, f'LOC_TYPE_TRAIT_YIELD_POWER_ENHANCEMENT', en_US_locs_data)
                loc = loc.replace('{2_Icon}', f'[ICON_{yield_type}]')
                loc = loc.replace('{3_Name}', get_loc(locs_data, yield_loc, en_US_locs_data))
                processed = loc_amount_parameter(loc, element[21])
                p(f'{processed}', style="text-align:left", cls='civ-ability-desc')
                yield_dict[key] = 1
        if element[22] != None and element[22] > 0:
            key = f'Entertainment'
            if key not in yield_dict:
                loc = get_loc(locs_data, f'LOC_TYPE_TRAIT_AMENITY_ENTERTAINMENT_POWER_ENHANCEMENT', en_US_locs_data)
                processed = loc_amount_parameter(loc, element[22])
                p(f'{processed}', style="text-align:left", cls='civ-ability-desc')
                yield_dict[key] = 1
        if element[12] != None:
            key = f'citizen_{element[12]}'
            if key not in yield_dict:
                yield_loc = f'LOC_{element[12]}_NAME'
                yield_type = element[12][6:]
                p(f'{get_loc(locs_data, "LOC_TOOLTIP_BUILDING_CITIZEN_YIELDS_HEADER", en_US_locs_data)}[NEWLINE][ICON_BULLET]+{element[13]} [ICON_{yield_type}] {get_loc(locs_data, yield_loc, en_US_locs_data)}', style="text-align:left", cls='civ-ability-desc')
                yield_dict[key] = 1

    if tmp_yields[5] != None:
        p(f'{get_loc(locs_data, tmp_yields[5], en_US_locs_data)}', style="text-align:left", cls='civ-ability-desc')

    building_cost = int(int(tmp_yields[2]) / 2)
    if building_cost > 0:
        with p(f'{get_loc(locs_data, 'LOC_UI_PEDIA_PRODUCTION_COST', en_US_locs_data)} = {building_cost}', style="text-align:left", cls='civ-ability-desc'):
            img(src=f'/images/ICON_PRODUCTION.webp', style="vertical-align: middle", onerror=image_onerror)
    building_maintenance = int(tmp_yields[8])
    if building_maintenance > 0:
        maintenance_loc = get_loc(locs_data, 'LOC_TOOLTIP_MAINTENANCE', en_US_locs_data)
        processed = loc_amount_parameter(maintenance_loc, building_maintenance)
        processed = processed.replace('{2_YieldIcon}', '[ICON_GOLD]')
        processed = processed.replace('{3_YieldName}', get_loc(locs_data, 'LOC_YIELD_GOLD_NAME', en_US_locs_data))
        processed = processed.replace('{3_YieldName[2]}', get_loc(locs_data, 'LOC_YIELD_GOLD_NAME', en_US_locs_data))
        processed = processed.replace('{3_YieldName[8]}', get_loc(locs_data, 'LOC_YIELD_GOLD_NAME', en_US_locs_data))
        p(processed, style="text-align:left", cls='civ-ability-desc')
        # img(src=f'/images/ICON_PRODUCTION.webp', style="vertical-align: middle", onerror=image_onerror)

def get_buildings_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Buildings Details per District'
    add_html_header(doc, title)

    menu_items = []
    menu_icons = []
    buildings_per_district = get_buildings_per_district_list(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    for district in buildings_per_district.keys():
        menu_items.append(get_loc(locs_data, district, en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, district, en_US_locs_data))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, 'buildings')
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/buildings')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                h1(title, cls='civ-name')
                                br()
                                for district in buildings_per_district.keys():
                                    with div(cls='col-lg-12', id=get_loc(locs_data, district, en_US_locs_data)):
                                        with div(cls="chart"):
                                            comment(district)
                                            h2(get_loc(locs_data, district, en_US_locs_data), cls='civ-name')
                                    with div(cls="row"):
                                        for building in buildings_per_district[district].keys():
                                            with div(cls="col-lg-6 col-md-12"):
                                                with div(cls="chart"):
                                                    comment(building)
                                                    with h2(get_loc(locs_data, building, en_US_locs_data), cls='civ-name'):
                                                        img(src=f'/images/buildings/{get_loc(en_US_locs_data, building, en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=image_onerror)
                                                    br()
                                                    show_building_yields(buildings_per_district[district][building], locs_data, en_US_locs_data)
        add_final_scripts()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_expanded_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Expanded Leaders Description'
    add_html_header(doc, title)

    menu_items = []
    menu_icons = []
    civ_leaders_items = get_expanded_civs_tables(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugConfiguration.sqlite")
    governors = get_expanded_governors_list(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    governor_promotion_dict = get_governors_promotion_dict(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    governor_promotion_set_dict = get_governors_promotion_sets_dict(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", governors, governor_promotion_dict)
    units_dict = get_units_dict(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    tech_to_loc_dict = get_tech_to_loc_dict(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    civic_to_loc_dict = get_civic_to_loc_dict(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    for leader in civ_leaders_items:
        menu_items.append(get_loc(locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(locs_data, leader[5], en_US_locs_data))
        menu_icons.append(f'leaders/{get_loc(en_US_locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(en_US_locs_data, leader[5], en_US_locs_data)}')
    for gov in governors:
        menu_items.append(get_loc(locs_data, gov[1], en_US_locs_data))
        menu_icons.append(f'governors/{get_loc(en_US_locs_data, gov[1], en_US_locs_data)}')
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, 'bbg_expanded')
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                h1(title, cls='civ-name')
                                br()
                                for leader in civ_leaders_items:
                                    with div(cls="row", id=get_loc(locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(locs_data, leader[5], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                comment(f'{leader[2]} {leader[5]}')
                                                with h2(get_loc(locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(locs_data, leader[5], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/leaders/{get_loc(en_US_locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(en_US_locs_data, leader[5], en_US_locs_data)}.webp', style="vertical-align: middle; width:7em", onerror=image_onerror)
                                                comment(leader[3])
                                                h3(get_loc(locs_data, leader[3], en_US_locs_data), style="text-align:left", cls='civ-ability-name')
                                                br()
                                                show_element_with_base_option(leader[4], lang, locs_data, en_US_locs_data, add_base_game = False)
                                                br()
                                                comment(leader[6])
                                                h3(get_loc(locs_data, leader[6], en_US_locs_data), style="text-align:left", cls='civ-ability-name')
                                                br()
                                                show_element_with_base_option(leader[7], lang, locs_data, en_US_locs_data, add_base_game = False)
                                                br()
                                                for item in civ_leaders_items[leader]:
                                                    comment(item[4])
                                                    with h3(f'{get_loc(locs_data, item[4], en_US_locs_data)}', style="text-align:left", cls='civ-ability-name'):
                                                        img(src=f'/images/items/{get_loc(en_US_locs_data, item[4], en_US_locs_data)}.webp', style="vertical-align: middle; width:2em; text-align:left", onerror=image_onerror)

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
                                    with div(cls="row", id=get_loc(locs_data, gov[1], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                comment(gov[1])
                                                with h2(get_loc(locs_data, gov[1], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/governors/{get_loc(en_US_locs_data, gov[1], en_US_locs_data)}.webp', style="vertical-align: middle; width:7em", onerror=image_onerror)
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
                                                                    # show_element_with_base_option(promotion_desc, lang, locs_data, en_US_locs_data, alignment = alignment)
                                                                    br()

        add_final_scripts()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)


def loc_amount_parameter(localized_text: str, amount: float) -> str:
    def fix_scaling_factor(matchobj):
        return matchobj.group(0)
    def fix_amount(matchobj):
        return matchobj.group(2) if amount > 1 else matchobj.group(1)
    localized_text = re.sub(r'{Amount ?: ?plural 1\?(.*?); ?other\?(.*?);}', fix_amount, localized_text)
    localized_text = localized_text.replace('{Amount}', f'{amount}').replace('{Amount : number #}', f'{amount}')

    localized_text = re.sub(r'{1_Amount ?: ?plural 1\?(.*?); ?other\?(.*?);}', fix_amount, localized_text)
    localized_text = localized_text.replace('{Amount}', f'{amount}').replace('{Amount : number #}', f'{amount}')

    # 1_Amount: number +#,###;-#,###}
    localized_text = re.sub(r'{1_Amount: number +#,###;-#,###}', fix_amount, localized_text)
    localized_text = localized_text.replace('{1_Amount}', f'{amount}').replace('{1_Amount: number +#,###;-#,###}', f'{amount}')

    localized_text = re.sub(r'{ScalingFactor}', fix_scaling_factor, localized_text)
    localized_text = localized_text.replace('{ScalingFactor}', f'{amount}')

    return localized_text

def get_units_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data

    def create_units_page():
        for promo_cls in unit_stats.keys():
            loc_promo_cls = f'LOC_{promo_cls}_NAME'
            with div(cls='col-lg-12', id=get_loc(locs_data, loc_promo_cls, en_US_locs_data)), div(cls="chart"):
                comment(loc_promo_cls)
                h2(get_loc(locs_data, loc_promo_cls, en_US_locs_data), cls='civ-name')
            with div(cls="row"):
                for unit_type in unit_stats[promo_cls].keys():
                    process_unit_stats(unit_type, promo_cls)

    def process_unit_stats(unit_type, promo_cls):
        with div(cls="col-lg-6 col-md-12"), div(cls="chart"):
            comment(unit_type)
            (
                unit_name_loc, sight, movement, cs, ranged_cs, attack_range, bombard_cs, prod, desc,
                maint, strategic_type, strategic_amt, strategic_maint_type, strategic_maint_amt, antiair_cs
            ) = unit_stats[promo_cls][unit_type]
            with h2(get_loc(locs_data, unit_name_loc, en_US_locs_data), cls='civ-name'):
                img(src=f'/images/units/{get_loc(en_US_locs_data, unit_name_loc, en_US_locs_data).replace(' ', '_')}_icon_(Civ6).webp', style="vertical-align: middle; width:5em", onerror=image_onerror)
            br()
            p(f'{get_loc(locs_data, 'LOC_UI_PEDIA_PRODUCTION_COST', en_US_locs_data)}: {prod// 2} [ICON_PRODUCTION]', style="display:inline-block;text-align:left", cls='civ-ability-desc')
            br()
            if strategic_amt and strategic_type:
                p(f'{max(strategic_amt // 2, 1)} [ICON_{strategic_type}]', style="display:inline-block;text-align:left", cls='civ-ability-desc')
                br()
            strategic_maint_text = get_loc(locs_data, 'LOC_HUD_REPORTS_PER_TURN', en_US_locs_data).replace('{1_Yield}', '')
            if strategic_maint_amt:
                strategic_maint_text = f', {strategic_maint_amt} [ICON_{strategic_maint_type}]{strategic_maint_text}'
            # BTW yes this typo "MAITENANCE" is part of the game lol
            p(f'{get_loc(locs_data, 'LOC_UI_PEDIA_MAITENANCE_COST', en_US_locs_data)}: {maint} [ICON_GOLD]{strategic_maint_text}', style="display:inline-block;text-align:left", cls='civ-ability-desc')
            br()                
            icon_to_stats = {
                'ICON_MOVEMENT': ('LOC_UI_PEDIA_MOVEMENT_POINTS', movement),
                'ICON_STRENGTH': ('LOC_UI_PEDIA_MELEE_STRENGTH', cs),
                'ICON_RANGE': ('LOC_UI_PEDIA_RANGE', attack_range),
                'ICON_RANGED': ('LOC_UI_PEDIA_RANGED_STRENGTH', ranged_cs),
                'ICON_BOMBARD': ('LOC_UI_PEDIA_BOMBARD_STRENGTH', bombard_cs),
                'ICON_ANTIAIR_LARGE': ('LOC_UI_PEDIA_ANTIAIR_STRENGTH', antiair_cs)
            }
            for icon in icon_to_stats:
                name, val = icon_to_stats[icon]
                if val <= 0:
                    continue
                p(f'{val} [{icon}] {get_loc(locs_data, name, en_US_locs_data)}', style="display:inline-block;text-align:left", cls='civ-ability-desc')
                br()
            p(f'{sight} Sight', style="display:inline-block;text-align:left", cls='civ-ability-desc')
            br()
            p(get_loc(locs_data, desc, en_US_locs_data), style="display:inline-block;text-align:left", cls='civ-ability-desc')


    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version else "Base Game"} Unit Details'
    unit_stats = get_unit_stats(f"sqlFiles/{bbg_version if bbg_version else 'baseGame'}/DebugGameplay.sqlite")
    return create_page(bbg_version, lang, title, 'units', [], [], 'images', create_units_page)
    doc = dominate.document(title=None, lang=get_html_lang(lang))
    add_html_header(doc, title)
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"), div(cls="main-wrapper"):
            add_header(bbg_version, lang, 'units')
            with div(cls=""):
                with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                    pass # implement some related icons to make this work
                with div(cls="leaders-data min-w-full main-pl"), main(cls="main users chart-page"), div(cls="container"):
                    h1(title, cls='civ-name')
                    br()
                    create_units_page()
        add_final_scripts()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)
