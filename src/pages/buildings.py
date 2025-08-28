from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_buildings_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data_with_fallback(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else get_loc(locs_data, "LOC_BASE_GAME_TITLE")} {get_loc(locs_data, "LOC_PAGE_TITLE_BUILDINGS")}'

    menu_items = []
    menu_icons = []
    buildings_per_district = get_buildings_per_district_list(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    for district in buildings_per_district.keys():
        menu_items.append(get_loc(locs_data, district))
        menu_icons.append(get_loc(en_US_locs_data, district))

    def create_buildings_page():
        for district in buildings_per_district.keys():
            with div(cls='col-lg-12', id=get_loc(locs_data, district)), div(cls="chart"):
                comment(district)
                h2(get_loc(locs_data, district),
                   cls='civ-name')
            with div(cls="row"):
                for building in buildings_per_district[district].keys():
                    with div(cls="col-lg-6 col-md-12"), div(cls="chart"):
                        comment(building)
                        with h2(get_loc(locs_data, building), 
                                cls='civ-name'):
                            img(src=f'/images/buildings/{get_loc(en_US_locs_data, building)}.webp',
                                style="vertical-align: middle; width:5em",
                                onerror=image_onerror)
                        br()
                        show_building_yields(
                          buildings_per_district[district][building],
                          locs_data,
                          en_US_locs_data)

    return create_page(bbg_version, lang, title, 'buildings', menu_items, menu_icons, 'images/buildings', pages_list, create_buildings_page, locs_data, en_US_locs_data)

def show_building_yields(yields, locs_data, en_US_locs_data):
    yield_dict = {}
    for element in yields:
        if element[10] != None:
            if element[10] not in yield_dict:
                yield_loc = f'LOC_{element[10]}_NAME'
                yield_type = element[10][6:]
                p(f'+{element[11]} [ICON_{yield_type}] {get_loc(locs_data, yield_loc)}',
                  style="text-align:left",
                  cls='civ-ability-desc')
                yield_dict[element[10]] = 1


    tmp_yields = yields[0]
    if tmp_yields[6] > 0:
        p(f'+{tmp_yields[6]} [ICON_HOUSING] {get_loc(locs_data, 'LOC_HUD_CITY_HOUSING')}',
          style="text-align:left",
          cls='civ-ability-desc')
    if tmp_yields[7] > 0:
        p(f'+{tmp_yields[7]} [ICON_AMENITIES] {get_loc(locs_data, 'LOC_HUD_CITY_AMENITIES')}',
          style="text-align:left",
          cls='civ-ability-desc')
    if tmp_yields[9] != None:
        processed = loc_amount_parameter(
            get_loc(locs_data, 'LOC_TYPE_TRAIT_CITIZENS'),
            tmp_yields[9])
        p(f'{processed}', style="text-align:left", cls='civ-ability-desc')

    for element in yields:
        if element[14] != None:
            gp_type = get_loc(locs_data, element[14])
            if gp_type not in yield_dict:
                gp_icon = f'[ICON_GREAT{element[14][23:-5]}]'
                gpp_turn = element[15]
                loc = get_loc(locs_data, 'LOC_TYPE_TRAIT_GREAT_PERSON_POINTS')
                loc = loc.replace('{2_Icon}', f'{gp_icon}')
                loc = loc.replace('{3_GreatPersonClassName}', gp_type)
                processed = loc_amount_parameter(loc, gpp_turn)
                p(f'{processed}', style="text-align:left", cls='civ-ability-desc')
                yield_dict[gp_type] = 1
        if element[16] != None:
            slot_type = element[16]
            if slot_type not in yield_dict:
                num_slots = element[17]
                loc = get_loc(locs_data, f'LOC_TYPE_TRAIT_GREAT_WORKS_{slot_type[14:]}_SLOTS')
                processed = loc_amount_parameter(loc, num_slots)
                p(f'{processed}', style="text-align:left", cls='civ-ability-desc')
                yield_dict[slot_type] = 1
        if element[18] != None:
            key = f'{element[18]}->{element[19]}'
            if key not in yield_dict:
                from_yield_type = element[18][6:]
                to_yield_type = element[19][6:]
                loc = get_loc(locs_data, f'LOC_TYPE_TRAIT_BUILDING_DISTRICT_COPY')
                loc = loc.replace('{1_ToYieldIcon}', f'[ICON_{to_yield_type}]')
                loc = loc.replace('{2_ToYieldName}', get_loc(locs_data, f'LOC_YIELD_{to_yield_type}_NAME'))
                loc = loc.replace('{3_FromYieldIcon}', f'[ICON_{from_yield_type}]')
                loc = loc.replace('{4_FromYieldName}', get_loc(locs_data, f'LOC_YIELD_{from_yield_type}_NAME'))

                p(f'{loc}', style="text-align:left", cls='civ-ability-desc')
                yield_dict[key] = 1
        if element[20] != None:
            key = f'Power{element[20]}'
            if key not in yield_dict:
                yield_loc = f'LOC_{element[20]}_NAME'
                yield_type = element[20][6:]
                loc = get_loc(locs_data, f'LOC_TYPE_TRAIT_YIELD_POWER_ENHANCEMENT')
                loc = loc.replace('{2_Icon}', f'[ICON_{yield_type}]')
                loc = loc.replace('{3_Name}', get_loc(locs_data, yield_loc))
                processed = loc_amount_parameter(loc, element[21])
                p(f'{processed}', style="text-align:left", cls='civ-ability-desc')
                yield_dict[key] = 1
        if element[22] != None and element[22] > 0:
            key = f'Entertainment'
            if key not in yield_dict:
                loc = get_loc(locs_data, f'LOC_TYPE_TRAIT_AMENITY_ENTERTAINMENT_POWER_ENHANCEMENT')
                processed = loc_amount_parameter(loc, element[22])
                p(f'{processed}', style="text-align:left", cls='civ-ability-desc')
                yield_dict[key] = 1
        if element[12] != None:
            key = f'citizen_{element[12]}'
            if key not in yield_dict:
                yield_loc = f'LOC_{element[12]}_NAME'
                yield_type = element[12][6:]
                p(f'{get_loc(locs_data, "LOC_TOOLTIP_BUILDING_CITIZEN_YIELDS_HEADER")}[NEWLINE][ICON_BULLET]+{element[13]} [ICON_{yield_type}] {get_loc(locs_data, yield_loc)}',
                  style="text-align:left",
                  cls='civ-ability-desc')
                yield_dict[key] = 1

    if tmp_yields[5] != None:
        p(f'{get_loc(locs_data, tmp_yields[5])}',
          style="text-align:left",
          cls='civ-ability-desc')

    building_cost = int(int(tmp_yields[2]) / 2)
    if building_cost > 0:
        with p(f'{get_loc(locs_data, 'LOC_UI_PEDIA_PRODUCTION_COST')} = {building_cost}', style="text-align:left", cls='civ-ability-desc'):
            img(src=f'/images/ICON_PRODUCTION.webp', style="vertical-align: middle", onerror=image_onerror)
    building_maintenance = int(tmp_yields[8])
    if building_maintenance > 0:
        maintenance_loc = get_loc(locs_data, 'LOC_TOOLTIP_MAINTENANCE')
        processed = loc_amount_parameter(maintenance_loc, building_maintenance)
        processed = processed.replace('{2_YieldIcon}', '[ICON_GOLD]')
        processed = processed.replace('{3_YieldName}', get_loc(locs_data, 'LOC_YIELD_GOLD_NAME'))
        processed = processed.replace('{3_YieldName[2]}', get_loc(locs_data, 'LOC_YIELD_GOLD_NAME'))
        processed = processed.replace('{3_YieldName[8]}', get_loc(locs_data, 'LOC_YIELD_GOLD_NAME'))
        p(processed, style="text-align:left", cls='civ-ability-desc')