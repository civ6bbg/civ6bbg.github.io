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
from pages.religion import *
from pages.units import *
from pages.world_wonder import *

pages_list = [
    {
        'name': 'leaders',
        'func': get_leader_html_file,
        'title': 'Leaders Description',
        'main_menu_title': 'Leaders'
    },
    {
        'name': 'bbg_expanded',
        'func': get_bbg_expanded_html_file,
        'title': 'BBG Expanded Leaders Description',
        'main_menu_title': 'BBG Expanded'
    },
    {
        'name': 'city_states',
        'func': get_city_state_html_file,
        'title': 'City States Description',
        'main_menu_title': 'City States'
    },
    {
        'name': 'religion',
        'func': get_religion_html_file,
        'title': 'Religion Description',
        'main_menu_title': 'Religion'
    },
    {
        'name': 'governor',
        'func': get_governor_html_file,
        'title': 'Governors Description',
        'main_menu_title': 'Governors'
    },
    {
        'name': 'great_people',
        'func': get_great_people_html_file,
        'title': 'Great People Description',
        'main_menu_title': 'Great People'
    },
    {
        'name': 'natural_wonder',
        'func': get_natural_wonder_html_file,
        'title': 'Natural Wonders Description',
        'main_menu_title': 'Natural Wonders'
    },
    {
       'name': 'world_wonder',
       'func': get_world_wonder_html_file,
       'title': 'World Wonders Bonuses Description',
       'main_menu_title': 'World Wonders'
    },
    {
        'name': 'buildings',
        'func': get_buildings_html_file,
        'title': 'Buildings Description',
        'main_menu_title': 'Buildings'
    },
    {
        'name': 'units',
        'func': get_units_html_file,
        'title': 'Units Description',
       'main_menu_title': 'Units'
    },
    {
        'name': 'names',
        'func': get_names_html_file,
        'title': 'Names List',
        'main_menu_title': 'Names'
    },
    {
        'name': 'misc',
        'func': get_misc_html_file,
        'title': 'Miscellaneous Description',
        'main_menu_title': 'Misc'
    },
    # {
    #     'name': 'changelog',
    #     'func': get_changelog_html_file,
    #     'title': 'Changelog',
    #     'main_menu_title': 'Changelog'
    # }
]