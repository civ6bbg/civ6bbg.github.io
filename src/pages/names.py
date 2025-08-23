from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_names_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'

    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Map Elements Naming Information'

    menu_items = []
    menu_icons = []
    desert_names = get_property_names(f"sqlFiles/{version_name}/DebugGameplay.sqlite", 'Desert', 'Deserts')
    lakes_names = get_property_names(f"sqlFiles/{version_name}/DebugGameplay.sqlite", 'Lake', 'Lakes')
    mountain_names = get_property_names(f"sqlFiles/{version_name}/DebugGameplay.sqlite", 'Mountain', 'Mountains')
    river_names = get_property_names(f"sqlFiles/{version_name}/DebugGameplay.sqlite", 'River', 'Rivers')
    sea_names = get_property_names(f"sqlFiles/{version_name}/DebugGameplay.sqlite", 'Sea', 'Seas')
    volcano_names = get_property_names(f"sqlFiles/{version_name}/DebugGameplay.sqlite", 'Volcano', 'Volcanoes')

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

    def create_names_page():
        for name_cls in name_classes.keys():
            with div(cls="row", id=name_cls):
                with div(cls="col-lg-12"):
                    with div(cls="chart"):
                        h2(name_cls, cls='civ-name')
            with div(cls="row"), div(cls="row"):
                for property_name in name_classes[name_cls]:
                    if len(name_classes[name_cls][property_name]) <= 1:
                        div_cls = 'col-md-3 col-lg-3'
                    elif len(name_classes[name_cls][property_name]) <= 3:
                        div_cls = 'col-md-6 col-lg-6'
                    else:
                        div_cls = 'col-md-12 col-lg-12'
                    with div(cls=div_cls), div(cls="chart"):
                        comment(property_name)
                        h2(get_loc(locs_data, f'{property_name}', en_US_locs_data),
                           style="text-align:center",
                           cls='civ-ability-desc')
                        with div(cls='row'):
                            cls_len = math.floor(12 / 
                                (1 if len(name_classes[name_cls][property_name]) == 0 
                                 else len(name_classes[name_cls][property_name])))
                            curr_div_cls = f'col-md-{cls_len} col-lg-{cls_len}'
                            for name in name_classes[name_cls][property_name]:
                                with div(cls=curr_div_cls):
                                    comment(name)
                                    p(get_loc(locs_data, f'{name}', en_US_locs_data),
                                      style="text-align:center",
                                      cls='civ-ability-desc')
                br()
    return create_page(bbg_version, lang, title, 'names', menu_items, menu_icons, 'images', create_names_page)