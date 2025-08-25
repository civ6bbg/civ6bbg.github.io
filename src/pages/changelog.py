from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

changelog_items = {
    'LOC_CHANGELOG_GAME_MECHANICS': {
        'LOC_CHANGELOG_GAME_MECHANICS_GLOBAL': [
            'LOC_CHANGELOG_GAME_MECHANICS_GLOBAL_DESC',
        ],
        'LOC_CHANGELOG_COMBAT': [
            'LOC_CHANGELOG_COMBAT_DESC',
        ],
        'LOC_CHANGELOG_CONGRESS': [
            'LOC_CHANGELOG_CONGRESS_DESC'
        ],
        'LOC_CHANGELOG_DIPLOMATIC_FAVOR': [
            'LOC_CHANGELOG_DIPLOMATIC_FAVOR_CONQUER_CAPITAL_DESC',
        ],
        'LOC_CHANGELOG_DISASTERS': [
            'LOC_CHANGELOG_DISASTERS_DESC',
        ],
        'LOC_CHANGELOG_SPECIALISTS': [
            'LOC_CHANGELOG_SPECIALISTS_DESC',
        ],
        'LOC_CHANGELOG_SPIES': [
            'LOC_CHANGELOG_SPIES_DESC',
        ],
        'LOC_CHANGELOG_TRIBAL_HUTS': [
            'LOC_CHANGELOG_TRIBAL_HUTS_RELIC_DESC',
        ]
    },
    'LOC_CHANGELOG_TECHNOLOGIES_AND_CIVICS': {
        'LOC_CHANGELOG_TECHNOLOGIES': [
            'LOC_CHANGELOG_TECHNOLOGIES_DESC',
        ],
        'LOC_CHANGELOG_CIVICS': [
            'LOC_CHANGELOG_CIVICS_DESC',
        ]
    },
    'LOC_CHANGELOG_VICTORY_CONDITIONS': {
        'LOC_CHANGELOG_DUMMY_STR': [
            'LOC_CHANGELOG_VICTORY_CONDITIONS_DESC'
        ],
        'LOC_CHANGELOG_VICTORY_CONDITIONS_LEGACY_BBG_SETTINGS': [
            'LOC_CHANGELOG_VICTORY_CONDITIONS_LEGACY_BBG_SETTINGS_DESC',
            'LOC_CHANGELOG_VICTORY_CONDITIONS_LEGACY_BBG_SETTINGS_CULTURAL_VICTORY_DESC',
            'LOC_CHANGELOG_VICTORY_CONDITIONS_LEGACY_BBG_SETTINGS_DIPLOMATIC_VICTORY_DESC',
            'LOC_CHANGELOG_VICTORY_CONDITIONS_LEGACY_BBG_SETTINGS_SCORE_VICTORY_DESC',
        ],
        'LOC_CHANGELOG_VICTORY_CONDITIONS_CUSTOM_SETTINGS': [
            'LOC_CHANGELOG_VICTORY_CONDITIONS_CUSTOM_SETTINGS_DESC',
            'LOC_CHANGELOG_VICTORY_CONDITIONS_CUSTOM_SETTINGS_CULTURAL_VICTORY_DESC',
            'LOC_CHANGELOG_VICTORY_CONDITIONS_CUSTOM_SETTINGS_SCIENCE_VICTORY_DESC',
            'LOC_CHANGELOG_VICTORY_CONDITIONS_CUSTOM_SETTINGS_DIPLOMATIC_VICTORY_DESC',
            'LOC_CHANGELOG_VICTORY_CONDITIONS_CUSTOM_SETTINGS_DOMINATION_VICTORY_DESC',
            'LOC_CHANGELOG_VICTORY_CONDITIONS_CUSTOM_SETTINGS_TERRITORIAL_VICTORY_DESC',
            'LOC_CHANGELOG_VICTORY_CONDITIONS_CUSTOM_SETTINGS_RELIGIOUS_VICTORY_DESC',
            'LOC_CHANGELOG_VICTORY_CONDITIONS_CUSTOM_SETTINGS_SCORE_VICTORY_DESC',
        ]
    },
    'LOC_CHANGELOG_DISTRICTS': {
        'LOC_CHANGELOG_DISTRICTS_DISTRICT_COST_DISCOUNT': [
            'LOC_CHANGELOG_DISTRICTS_DISTRICT_COST_DISCOUNT_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_CITY_CENTER': [
            'LOC_CHANGELOG_DISTRICTS_CITY_CENTER_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_AERODROME': [
            'LOC_CHANGELOG_DISTRICTS_AERODROME_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_CAMPUS': [
            'LOC_CHANGELOG_DISTRICTS_CAMPUS_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_COMMERCIAL_HUB': [
            'LOC_CHANGELOG_DISTRICTS_COMMERCIAL_HUB_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_DAM_CANAL': [
            'LOC_CHANGELOG_DISTRICTS_DAM_CANAL_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_ENCAMPMENT': [
            'LOC_CHANGELOG_DISTRICTS_ENCAMPMENT_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_ENTERTAINMENT_COMPLEX': [
            'LOC_CHANGELOG_DISTRICTS_ENTERTAINMENT_COMPLEX_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_GOVERNMENT_PLAZA': [
            'LOC_CHANGELOG_DISTRICTS_GOVERNMENT_PLAZA_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_HARBOR': [
            'LOC_CHANGELOG_DISTRICTS_HARBOR_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_INDUSTRIAL_ZONE': [
            'LOC_CHANGELOG_DISTRICTS_INDUSTRIAL_ZONE_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_NEIGHBORHOOD': [
            'LOC_CHANGELOG_DISTRICTS_NEIGHBORHOOD_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_PRESERVE': [
            'LOC_CHANGELOG_DISTRICTS_PRESERVE_DESC',
        ],
        'LOC_CHANGELOG_DISTRICTS_WATER_PARK': [
            'LOC_CHANGELOG_DISTRICTS_WATER_PARK_DESC',
        ],
    },
    'LOC_CHANGELOG_IMPROVEMENTS': {
        'LOC_CHANGELOG_DUMMY_STR': [
            'LOC_CHANGELOG_IMPROVEMENTS_DESC'
        ]
    },
    'LOC_CHANGELOG_RESOURCES': {
        'LOC_CHANGELOG_DUMMY_STR': [
            'LOC_CHANGELOG_RESOURCES_DESC'
        ]
    },
    'LOC_CHANGELOG_MILITARY_UNITS': {
        'LOC_CHANGELOG_UNITS_MILITARY_PREBUILD_SYSTEM': [
            'LOC_CHANGELOG_UNITS_MILITARY_PREBUILD_SYSTEM_DESC'
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_UNIQUE_UNIT_PREBUILD_SYSTEM': [
            'LOC_CHANGELOG_UNITS_MILITARY_UNIQUE_UNIT_PREBUILD_SYSTEM_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_ANTI_CAVALRY': [
            'LOC_CHANGELOG_UNITS_MILITARY_ANTI_CAVALRY_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_LIGHT_CAVALRY': [
            'LOC_CHANGELOG_UNITS_MILITARY_LIGHT_CAVALRY_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_HEAVY_CAVALRY': [
            'LOC_CHANGELOG_UNITS_MILITARY_HEAVY_CAVALRY_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_MELEE': [
            'LOC_CHANGELOG_UNITS_MILITARY_MELEE_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_RANGED': [
            'LOC_CHANGELOG_UNITS_MILITARY_RANGED_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_RECON': [
            'LOC_CHANGELOG_UNITS_MILITARY_RECON_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_SIEGE': [
            'LOC_CHANGELOG_UNITS_MILITARY_SIEGE_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_GDR': [
            'LOC_CHANGELOG_UNITS_MILITARY_GDR_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_AIR_UNITS': [
            'LOC_CHANGELOG_UNITS_MILITARY_AIR_UNITS_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_NAVAL_MELEE': [
            'LOC_CHANGELOG_UNITS_MILITARY_NAVAL_MELEE_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_NAVAL_RANGED': [
            'LOC_CHANGELOG_UNITS_MILITARY_NAVAL_RANGED_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_NAVAL_RAIDER': [
            'LOC_CHANGELOG_UNITS_MILITARY_NAVAL_RAIDER_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_NAVAL_CARRIER': [
            'LOC_CHANGELOG_UNITS_MILITARY_NAVAL_CARRIER_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_NUCLEAR_DEVICES': [
            'LOC_CHANGELOG_UNITS_MILITARY_NUCLEAR_DEVICES_DESC',
        ],
        'LOC_CHANGELOG_UNITS_MILITARY_SUPPORT_UNITS': [
            'LOC_CHANGELOG_UNITS_MILITARY_SUPPORT_UNITS_DESC',
        ]
    },
    'LOC_CHANGELOG_GOVERNMENTS': {
        'LOC_CHANGELOG_DUMMY_STR': [
            'LOC_CHANGELOG_GOVERNMENTS_DESC'
        ]
    },
    'LOC_CHANGELOG_POLICIES': {
        'LOC_CHANGELOG_DUMMY_STR': [
            'LOC_CHANGELOG_POLICIES_DESC'
        ]
    }
}

def get_changelog_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'

    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else "Base Game"} Changelog'

    if bbg_version == None or bbg_version[0] == '5':
        menu_items = []
        menu_icons = []
    else:
        menu_items = [get_loc(locs_data, item, en_US_locs_data) for item in changelog_items.keys()]
        menu_icons = [f'ICON_{item}' for item in changelog_items.keys()]

    def create_changelog_page():
        if bbg_version == None or bbg_version[0] == '5':
            p('Changelog is only available for BBG versions 6.0 and later.', cls='civ-ability-desc')
            return
        for section in changelog_items.keys():
            with div(cls='col-lg-12'), div(cls="chart"):
                comment(section)
                h1(get_loc(locs_data, section, en_US_locs_data), cls='civ-name', id=get_loc(locs_data, section, en_US_locs_data))
                br()
                br()
                for item in changelog_items[section].keys():
                    comment(item)
                    h2(get_loc(locs_data, item, en_US_locs_data), cls='civ-name')
                    br()
                    for desc in changelog_items[section][item]:
                        comment(desc)
                        p(get_loc(locs_data, desc, en_US_locs_data), 
                        style='text-align:left', 
                        cls='civ-ability-desc')
                    br()
    return create_page(bbg_version, lang, title, 'changelog', menu_items, menu_icons, 'images', pages_list, create_changelog_page)