from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_great_people_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'

    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Great People Abilities Description'

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
    great_people = get_great_people_list(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    great_people_modifier_dict = get_great_people_modifier_dict(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    great_people_works = get_great_people_great_works(f"sqlFiles/{version_name}/DebugGameplay.sqlite")

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
    def create_great_people_page():
        for gp_type in great_people_list:
            with div(
                    cls="row",
                    id=get_loc(locs_data, gp_type, en_US_locs_data)
                ), div(cls="col-lg-12"), div(cls="chart"):
                comment(gp_type)
                with h2(get_loc(locs_data, gp_type, en_US_locs_data), cls='civ-name'):
                    img(src=f'/images/{get_loc(en_US_locs_data, gp_type, en_US_locs_data)}.webp',
                        style="vertical-align: middle; width:5em", 
                        onerror=image_onerror)
                    br()
            for era in eras_loc:
                if era not in great_people[gp_type].keys():
                    continue
                if len(great_people[gp_type]) > 1:
                    with div(
                      cls="row", 
                      id=get_loc(locs_data, gp_type, en_US_locs_data)
                    ), div(cls="col-lg-12"), div(cls="chart"):
                        comment(era)
                        h3(get_loc(locs_data, era, en_US_locs_data), cls='civ-name')
                with div(cls='row'):
                    cls_len = max(3, math.ceil(12 / len(great_people[gp_type][era])))
                    div_cls = f'col-md-{cls_len} col-lg-{cls_len}'
                    for gp in great_people[gp_type][era]:
                        with div(cls=div_cls), div(cls="chart"):
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
                                    processed = loc_amount_parameter(
                                      get_loc(locs_data, mod, en_US_locs_data), amount)
                                    p(processed, style="text-align:left", cls='civ-ability-desc')
                                    br()
                            if gp[0] in great_people_works.keys():
                                for work in great_people_works[gp[0]]:
                                    comment(work[1])
                                    p(img(
                                            src=f'/images/{work[2]}.webp',
                                            style="vertical-align: middle; width:2em",
                                            onerror=image_onerror
                                        ),
                                        f' {get_loc(locs_data, work[1], en_US_locs_data)}',
                                        style="text-align:left",
                                        cls='civ-ability-desc')
                                        
    return create_page(bbg_version, lang, title, 'great_people', menu_items, menu_icons, 'images', create_great_people_page)