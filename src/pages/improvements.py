from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_improvements_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data_with_fallback(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else get_loc(locs_data, "LOC_BASE_GAME_TITLE")} {get_loc(locs_data, "LOC_TECH_FILTER_IMPROVEMENTS")}'
    tech_to_loc_dict = get_tech_to_loc_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    civic_to_loc_dict = get_civic_to_loc_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    menu_items = []
    menu_icons = []

    def create_improvements_page():
        with div(cls="row"):
            for imp in improvements:
                improvement_name = imp['Name']
                with div(cls='col-md-6 col-12',
                        id=get_loc(locs_data, improvement_name)
                        ), div(cls="chart"):
                    comment(improvement_name)
                    with h2(get_loc(locs_data, improvement_name),
                    cls='civ-name'):
                        img(src=f'/images/improvements/{get_loc(en_US_locs_data, improvement_name)}.webp',
                            style="vertical-align: middle; width:5em",
                            onerror=image_onerror)
                    if imp['PlunderType'] != 'NO_PLUNDER' and imp['PlunderType'] != 'PLUNDER_NONE':
                        pillage_text = get_loc(locs_data, 'LOC_TYPE_TRAIT_PILLAGE_AWARD')
                        if imp['PlunderType'] == 'PLUNDER_HEAL':
                            pillage_text = pillage_text.replace('{1_AwardIcon}', get_loc(locs_data, 'LOC_TYPE_TRAIT_PILLAGE_AWARD_HEALING'))
                            pillage_text = pillage_text.replace('{2_AwardText}', str(imp['PlunderAmount']))
                        else:
                            pillage_text = pillage_text.replace('{1_AwardIcon}', f'[ICON_{imp["PlunderType"][8:]}]')
                            pillage_text = pillage_text.replace('{2_AwardText}', str(imp['PlunderAmount']))
                        p(pillage_text, style="text-align:left", cls='civ-ability-desc')
                    if imp['Housing'] > 0:
                        p(f'+{imp["Housing"]} [ICON_HOUSING] {get_loc(locs_data, "LOC_HUD_CITY_HOUSING")}',
                          style="text-align:left",
                          cls='civ-ability-desc')
                    # if imp['SameAdjacentValid'] == 0:
                    #     p(get_loc(locs_data, 'LOC_PEDIA_TRAIT_NO_SAME_ADJACENT'),
                    #       style="text-align:left",
                    #       cls='civ-ability-desc')
                    if imp['DefenseModifier'] != 0:
                        def_modifier_text = get_loc(locs_data, 'LOC_TOOLTIP_DEFENSE_MODIFIER')
                        def_modifier_text = def_modifier_text.replace('{1_Amount}', str(imp['DefenseModifier']))
                        p(def_modifier_text,
                          style="text-align:left",
                          cls='civ-ability-desc')
                    if imp['GrantFortification'] != 0:
                        fortification_text = get_loc(locs_data, 'LOC_OPERATION_BUILD_IMPROVEMENT_GRANT_FORTIFICATION')
                        p(fortification_text,
                          style="text-align:left",
                          cls='civ-ability-desc')
                    if imp['MinimumAppeal'] != None:
                        appeal_text = f'{get_loc(locs_data, 'LOC_HUD_APPEAL_LENS')} >= {imp["MinimumAppeal"]}'
                        required_appeal = get_loc(locs_data, 'LOC_UI_PEDIA_REQUIRES').replace('{1_Name}', appeal_text)
                        p(required_appeal,
                          style="text-align:left",
                          cls='civ-ability-desc')
                    if imp['YieldFromAppeal'] != None:
                        appeal_yield_text = f'{get_loc(locs_data, f"LOC_DISTRICT_APPEAL_{imp['YieldFromAppeal'][6:]}")}'
                        appeal_yield_text = appeal_yield_text.replace('{1_num}', str(imp['YieldFromAppealPercent']) + '%')
                        p(appeal_yield_text,
                          style="text-align:left",
                          cls='civ-ability-desc')
                    appeal_text = get_loc(locs_data, 'LOC_TYPE_TRAIT_APPEAL')
                    appeal_text = loc_amount_parameter(appeal_text, imp['Appeal'])
                    p(appeal_text,
                      style="text-align:left",
                      cls='civ-ability-desc')
                    for yc in imp['YieldChanges']:
                        yield_type = yc['YieldType']
                        yield_change = yc['YieldChange']
                        if yield_change > 0:
                            yield_text = f'+{yield_change} [ICON_{yield_type[6:]}] {get_loc(locs_data, f"LOC_{yield_type}_NAME")}'
                            p(yield_text,
                                style="text-align:left",
                                cls='civ-ability-desc')
                    for byc in imp['BonusYieldChanges']:
                        bonus_yield_type = byc['YieldType']
                        bonus_yield_change = byc['BonusYieldChange']
                        bonus_yield_prereq_tech = byc['PrereqTech']
                        bonus_yield_prereq_civic = byc['PrereqCivic']
                        if bonus_yield_change > 0:
                            bonus_yield_text = f'+{bonus_yield_change} [ICON_{bonus_yield_type[6:]}] {get_loc(locs_data, f"LOC_{bonus_yield_type}_NAME")}'
                            if bonus_yield_prereq_tech != None or bonus_yield_prereq_civic != None:
                                unlocked_by = get_loc(locs_data, "LOC_UI_PEDIA_UNLOCKED_BY")
                                tech_civic_dialog = get_unlock_tech_civic_dialog(bonus_yield_prereq_tech, bonus_yield_prereq_civic, locs_data, en_US_locs_data, tech_to_loc_dict, civic_to_loc_dict)
                                if tech_civic_dialog != None:
                                    bonus_yield_text += f' ({unlocked_by} {tech_civic_dialog})'
                            p(bonus_yield_text,
                                style="text-align:left",
                                cls='civ-ability-desc')
                    for tour in imp['Tourism']:
                        tourism_source = tour['TourismSource']
                        tourism_prereq_tech = tour['PrereqTech']
                        tourism_scaling_factor = tour['ScalingFactor']
                        if tourism_prereq_tech == None:
                            tourism_text = f'{get_loc(locs_data, 'LOC_TYPE_TRAIT_TOURISM_BONUS_YIELD_NO_REQUIREMENT')}'
                        else:
                            tourism_text = f'{get_loc(locs_data, 'LOC_TYPE_TRAIT_TOURISM_BONUS_YIELD')}'
                        tourism_text = loc_amount_parameter(tourism_text, tourism_scaling_factor)
                        if tourism_source == 'TOURISMSOURCE_APPEAL':
                            tourism_text = tourism_text.replace('{2_YieldIcon}', '')
                            tourism_text = tourism_text.replace('{3_YieldName}', get_loc(locs_data, 'LOC_HUD_APPEAL_LENS'))
                        else:
                            tourism_text = tourism_text.replace('{2_YieldIcon}', f'[ICON_{tourism_source[14:]}]')
                            tourism_text = tourism_text.replace('{3_YieldName}', get_loc(locs_data, f'LOC_YIELD_{tourism_source[14:]}_NAME'))
                        if tourism_prereq_tech != None:
                            tech_civic_dialog = get_unlock_tech_civic_dialog(tourism_prereq_tech, None, locs_data, en_US_locs_data, tech_to_loc_dict, civic_to_loc_dict)
                            if tech_civic_dialog != None:
                                tourism_text = tourism_text.replace('{4_TechOrCivicName}', tech_civic_dialog)
                        p(tourism_text,
                          style="text-align:left",
                          cls='civ-ability-desc')
                    valid_build_unit_text = get_loc(locs_data, 'LOC_UI_PEDIA_BUILT_BY')
                    valid_build_unit_text += f' {get_loc(locs_data, "LOC_WORLD_CONGRESS_OR")} '.join(f' {get_loc(locs_data, f'LOC_{ivb["UnitType"]}_NAME')}' for ivb in imp['ValidBuildUnits'])
                    p(valid_build_unit_text,
                        style="text-align:left",
                        cls='civ-ability-desc')
                    
                    if len(imp['ValidTerrains']) > 0:
                        valid_terrains_text = get_loc(locs_data, 'LOC_VALID_TERRAIN_TYPE')
                        valid_terrains_text += f', '.join(f' {get_loc(locs_data, f"LOC_{ivt["TerrainType"]}_NAME")}{'' if ivt['PrereqCivic'] == None else f" ({get_loc(locs_data, 'LOC_HUD_RESEARCH_REQUIRES')} {get_loc(locs_data, civic_to_loc_dict[ivt['PrereqCivic']])})"}' for ivt in imp['ValidTerrains'])
                        p(valid_terrains_text,
                            style="text-align:left",
                            cls='civ-ability-desc')
                    if len(imp['ValidFeatures']) > 0:
                        valid_features_text = get_loc(locs_data, 'LOC_VALID_FEATURE_TYPE')
                        valid_features_text += f', '.join(f' {get_loc(locs_data, f"LOC_{ivf["FeatureType"]}_NAME")}{'' if ivf['PrereqCivic'] == None else f" ({get_loc(locs_data, 'LOC_HUD_RESEARCH_REQUIRES')} {get_loc(locs_data, civic_to_loc_dict[ivf['PrereqCivic']])})"}' for ivf in imp['ValidFeatures'])
                        p(valid_features_text,
                            style="text-align:left",
                            cls='civ-ability-desc')
                    prereq_tech = imp['PrereqTech']
                    prereq_civic = imp['PrereqCivic']
                    if prereq_tech != None or prereq_civic != None:
                        unlocked_by = get_loc(locs_data, "LOC_UI_PEDIA_UNLOCKED_BY")
                        tech_civic_dialog = get_unlock_tech_civic_dialog(prereq_tech, prereq_civic, locs_data, en_US_locs_data, tech_to_loc_dict, civic_to_loc_dict)
                        p(f'{unlocked_by} {tech_civic_dialog}' if tech_civic_dialog != None else '',
                            style="text-align:left",
                            cls='civ-ability-desc')
                    p('------------------------------', style="text-align:left", cls='civ-ability-desc')
                    p(get_loc(locs_data, imp['Description']),
                      style="text-align:left",
                      cls='civ-ability-desc')

    improvements = get_improvements(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    improvements = sorted(improvements, key=lambda x: get_loc(locs_data, x['Name']))
    return create_page(bbg_version, lang, title, 'improvements', menu_items, menu_icons, 'images/improvements', pages_list, create_improvements_page, locs_data, en_US_locs_data)