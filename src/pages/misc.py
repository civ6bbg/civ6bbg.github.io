from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_misc_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else get_loc(locs_data, "LOC_BASE_GAME_TITLE", en_US_locs_data)} {get_loc(locs_data, "LOC_PAGE_TITLE_MISC", en_US_locs_data)}'

    menu_items = []
    menu_icons = []

    dedication_list_per_era = get_dedication_list_per_era(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    for era in dedication_list_per_era.keys():
        menu_items.append(get_loc(locs_data, era, en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, era, en_US_locs_data))

    alliance_list = get_alliance_list(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    for alliance in alliance_list:
        menu_items.append(get_loc(locs_data, alliance[1], en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, alliance[1], en_US_locs_data))

    dark_age_policy = get_dark_age_card_list(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    dark_age_policy_era = get_dark_age_card_list_eras(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
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

    def create_misc_page():
        for era in dedication_list_per_era.keys():
            with div(cls="row", id=get_loc(locs_data, era, en_US_locs_data)), div(cls="col-lg-12"), div(cls="chart"):
                comment(era)
                h2(get_loc(locs_data, era, en_US_locs_data), cls='civ-name')
            with div(cls="row"), div(cls="chart"), div(cls="row"):
                for dedication in dedication_list_per_era[era]:
                    with div(cls="col-lg-3"):
                        comment(dedication[0])
                        img(src=f'/images/ICON_{dedication[0]}.webp',
                            style="vertical-align: middle; width:5em",
                            onerror=image_onerror)
                        comment(dedication[2])
                        p(get_loc(locs_data, dedication[2], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')
                        br()
                br()
            with div(cls="row"):
                for policy in dark_age_policy_per_era[eras_reverse_map[era]]:
                    with div(cls="col-lg-3"), div(cls="chart"):
                        comment(policy[4])
                        h2(get_loc(locs_data, policy[4], en_US_locs_data), cls='civ-name')
                        br()
                        comment(policy[1])
                        p(get_loc(locs_data, policy[1], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')
                        br()
        for alliance in alliance_list:
            with div(cls="row", id=get_loc(locs_data, alliance[1], en_US_locs_data)), div(cls="col-lg-12"):
                comment(alliance[1])
                h2(get_loc(locs_data, alliance[1], en_US_locs_data), cls='civ-name')
                br()
                alliance_effect = get_alliance_effects(f"sqlFiles/{version_name}/DebugGameplay.sqlite", alliance[0])
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
    return create_page(bbg_version, lang, title, 'misc', menu_items, menu_icons, 'images', pages_list, create_misc_page, locs_data, en_US_locs_data) 