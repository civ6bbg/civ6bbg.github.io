from pages.bbg_expanded import *
from pages.buildings import *
from pages.changelog import *
from pages.city_states import *
from pages.governor import *
from pages.great_people import *
from pages.leaders import *
from pages.misc import *
from pages.names import *
from pages.natural_wonder import *
from pages.policies import *
from pages.religion import *
from pages.units import *
from pages.world_wonder import *

pages_list = [
    {
        'name': 'leaders',
        'func': get_leader_html_file,
        'title': 'Leaders Description',
        'main_menu_title': 'LOC_PEDIA_LEADERS_TITLE'
    },
    {
        'name': 'bbg_expanded',
        'func': get_bbg_expanded_html_file,
        'title': 'BBG Expanded Leaders Description',
        'main_menu_title': 'LOC_MAIN_MENU_BBG_EXPANDED'
    },
    {
        'name': 'city_states',
        'func': get_city_state_html_file,
        'title': 'City States Description',
        'main_menu_title': 'LOC_CITY_STATES_CITY_STATES'
    },
    {
        'name': 'religion',
        'func': get_religion_html_file,
        'title': 'Religion Description',
        'main_menu_title': 'LOC_CATEGORY_RELIGION_NAME'
    },
    {
        'name': 'governor',
        'func': get_governor_html_file,
        'title': 'Governors Description',
        'main_menu_title': 'LOC_PEDIA_GOVERNORS_TITLE'
    },
    {
        'name': 'great_people',
        'func': get_great_people_html_file,
        'title': 'Great People Description',
        'main_menu_title': 'LOC_PEDIA_GREATPEOPLE_TITLE'
    },
    {
        'name': 'natural_wonder',
        'func': get_natural_wonder_html_file,
        'title': 'Natural Wonders Description',
        'main_menu_title': 'LOC_PEDIA_FEATURES_PAGEGROUP_NATURAL_WONDERS_NAME'
    },
    {
       'name': 'world_wonder',
       'func': get_world_wonder_html_file,
       'title': 'World Wonders Bonuses Description',
       'main_menu_title': 'LOC_MAIN_MENU_WORLD_WONDERS'
    },
    {
        'name': 'buildings',
        'func': get_buildings_html_file,
        'title': 'Buildings Description',
        'main_menu_title': 'LOC_PEDIA_BUILDINGS_TITLE'
    },
    {
        'name': 'units',
        'func': get_units_html_file,
        'title': 'Units Description',
        'main_menu_title': 'LOC_PEDIA_UNITS_TITLE'
    },
    {
        'name': 'names',
        'func': get_names_html_file,
        'title': 'Names List',
        'main_menu_title': 'LOC_MAIN_MENU_NAMES'
    },
    {
        'name': 'policies',
        'func': get_policy_html_file,
        'title': 'Policies',
        'main_menu_title': 'LOC_PEDIA_CONCEPTS_PAGE_GOVT_2_CHAPTER_CONTENT_TITLE'
    },
    {
        'name': 'misc',
        'func': get_misc_html_file,
        'title': 'Miscellaneous Description',
        'main_menu_title': 'LOC_MAIN_MENU_MISC'
    },
    {
        'name': 'changelog',
        'func': get_changelog_html_file,
        'title': 'Changelog',
        'main_menu_title': 'LOC_MAIN_MENU_CHANGELOG'
    }
]