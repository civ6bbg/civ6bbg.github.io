from bs4 import BeautifulSoup
import sqlite3
import re
import math

import dominate
from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

bbg_versions = [None, '7.0', '6.5', '6.4', '6.3', '6.2', '6.1', '6.0', '5.8', '5.7', '5.6']

replacements = [
    '[ICON_AMENITIES]',
    '[ICON_ANTIAIR_LARGE]',
    '[ICON_ARMY]',
    '[ICON_BARBARIAN]',
    '[ICON_BOMBARD]',
    '[ICON_CAPITAL]',
    '[ICON_CHARGES]',
    '[ICON_CITIZEN]',
    '[ICON_CIVICBOOSTED]',
    '[ICON_CORPS]',
    '[ICON_CULTURE]',
    '[ICON_DAMAGED]',
    '[ICON_DISTRICT]',
    '[ICON_DISTRICT_AERODROME]',
    '[ICON_DISTRICT_AQUEDUCT]',
    '[ICON_DISTRICT_CAMPUS]',
    '[ICON_DISTRICT_CANAL]',
    '[ICON_DISTRICT_CITY_CENTER]',
    '[ICON_DISTRICT_COMMERCIAL_HUB]',
    '[ICON_DISTRICT_DAM]',
    '[ICON_DISTRICT_DIPLOMATIC_QUARTER]',
    '[ICON_DISTRICT_ENCAMPMENT]',
    '[ICON_DISTRICT_ENTERTAINMENT]',
    '[ICON_DISTRICT_HARBOR]',
    '[ICON_DISTRICT_GOVERNMENT]',
    '[ICON_DISTRICT_HOLYSITE]',
    '[ICON_DISTRICT_HOLY_SITE]',
    '[ICON_DISTRICT_INDUSTRIAL_ZONE]',
    '[ICON_DISTRICT_MBANZA]',
    '[ICON_DISTRICT_NEIGHBORHOOD]',
    '[ICON_DISTRICT_LAVRA]',
    '[ICON_DISTRICT_PRESERVE]',
    '[ICON_DISTRICT_SEOWON]',
    '[ICON_DISTRICT_SPACEPORT]',
    '[ICON_DISTRICT_THEATER]',
    '[ICON_DISTRICT_WATER_ENTERTAINMENT_COMPLEX]',
    '[ICON_DISTRICT_WONDER]',
    '[ICON_ENVOY]',
    '[ICON_FAITH]',
    '[ICON_FAVOR]',
    '[ICON_FOOD]',
    '[ICON_FORMATION]',
    '[ICON_FORTIFIED]',
    '[ICON_GLORY_DARK_AGE]',
    '[ICON_GLORY_NORMAL_AGE]',
    '[ICON_GLORY_GOLDEN_AGE]',
    '[ICON_GLORY_SUPER_GOLDEN_AGE]',
    '[ICON_GOLD]',
    '[ICON_GOVERNMENT]',
    '[ICON_GOVERNOR]',
    '[ICON_GREATADMIRAL]',
    '[ICON_GREATARTIST]',
    '[ICON_GREATENGINEER]',
    '[ICON_GREATGENERAL]',
    '[ICON_GREATMERCHANT]',
    '[ICON_GREATMUSICIAN]',
    '[ICON_GREATPERSON]',
    '[ICON_GREATPROPHET]',
    '[ICON_GREATSCIENTIST]',
    '[ICON_GREATWORK_ARTIFACT]',
    '[ICON_GREATWORK_LANDSCAPE]',
    '[ICON_GREATWORK_MUSIC]',
    '[ICON_GREATWORK_RELIC]',
    '[ICON_GREATWORK_PORTRAIT]',
    '[ICON_GREATWORK_SCULPTURE]',
    '[ICON_GREATWORK_WRITING]',
    '[ICON_GREATWORK_RELIGIOUS]',
    '[ICON_GREATWORKSLOT_ART]',
    '[ICON_GREATWORKSLOT_ARTIFACT]',
    '[ICON_GREATWORKSLOT_PALACE]',
    '[ICON_GREATWORKSLOT_MUSIC]',
    '[ICON_GREATWORKSLOT_RELIC]',
    '[ICON_GREATWORKSLOT_WRITING]',
    '[ICON_GREATWRITER]',
    '[ICON_HOUSING]',
    '[ICON_INFLUENCEPERTURN]',
    '[ICON_LIFESPAN]',
    '[ICON_MOVEMENT]',
    '[ICON_NUCLEAR]',
    '[ICON_PILLAGED]',
    '[ICON_POWER]',
    '[ICON_PRODUCTION]',
    '[ICON_PROMOTION]',
    '[ICON_RANGE]',
    '[ICON_RANGED]',
    '[ICON_RELIGION]',
    '[ICON_RESOURCE_ALUMINUM]',
    '[ICON_RESOURCE_COAL]',
    '[ICON_RESOURCE_HORSES]',
    '[ICON_RESOURCE_IRON]',
    '[ICON_RESOURCE_NITER]',
    '[ICON_RESOURCE_OIL]',
    '[ICON_RESOURCE_URANIUM]',
    '[ICON_RESOURCE_AMBER]',
    '[ICON_RESOURCE_BANANAS]',
    '[ICON_RESOURCE_CATTLE]',
    '[ICON_RESOURCE_COPPER]',
    '[ICON_RESOURCE_CINNAMON]',
    '[ICON_RESOURCE_CLOVES]',
    '[ICON_RESOURCE_CITRUS]',
    '[ICON_RESOURCE_COCOA]',
    '[ICON_RESOURCE_COFFEE]',
    '[ICON_RESOURCE_COPPER]',
    '[ICON_RESOURCE_COSMETICS]',
    '[ICON_RESOURCE_COTTON]',
    '[ICON_RESOURCE_CRABS]',
    '[ICON_RESOURCE_DEER]',
    '[ICON_RESOURCE_DIAMONDS]',
    '[ICON_RESOURCE_DYES]',
    '[ICON_RESOURCE_FISH]',
    '[ICON_RESOURCE_FURS]',
    '[ICON_RESOURCE_GYPSUM]',
    '[ICON_RESOURCE_HONEY]',
    '[ICON_RESOURCE_INCENSE]',
    '[ICON_RESOURCE_IVORY]',
    '[ICON_RESOURCE_JADE]',
    '[ICON_RESOURCE_MARBLE]',
    '[ICON_RESOURCE_MERCURY]',
    '[ICON_RESOURCE_OLIVES]',
    '[ICON_RESOURCE_PEARLS]',
    '[ICON_RESOURCE_SALT]',
    '[ICON_RESOURCE_SILK]',
    '[ICON_RESOURCE_SILVER]',
    '[ICON_RESOURCE_SPICES]',
    '[ICON_RESOURCE_SUGAR]',
    '[ICON_RESOURCE_TEA]',
    '[ICON_RESOURCE_TOBACCO]',
    '[ICON_RESOURCE_TRUFFLES]',
    '[ICON_RESOURCE_TURTLES]',
    '[ICON_RESOURCE_WHALES]',
    '[ICON_RESOURCE_WINE]',
    '[ICON_RESOURCE_GYPSUM]',
    '[ICON_RESOURCE_JADE]',
    '[ICON_RESOURCE_JEANS]',
    '[ICON_RESOURCE_MAIZE]',
    '[ICON_RESOURCE_MARBLE]',
    '[ICON_RESOURCE_MERCURY]',
    '[ICON_RESOURCE_PERFUME]',
    '[ICON_RESOURCE_SALT]',
    '[ICON_RESOURCE_SHEEP]',
    '[ICON_RESOURCE_SILVER]',
    '[ICON_RESOURCE_STONE]',
    '[ICON_RESOURCE_RICE]',
    '[ICON_RESOURCE_TOYS]',
    '[ICON_RESOURCE_WHEAT]',
    '[ICON_SCIENCE]',
    '[ICON_STAT_GRIEVANCE]',
    '[ICON_STRENGTH]',
    '[ICON_TECHBOOSTED]',
    '[ICON_THERMONUCLEAR]',
    '[ICON_TOURISM]',
    '[ICON_TRADEROUTE]',
    '[ICON_TRADINGPOST]',
    '[ICON_TURN]',
    '[ICON_VISOPEN]',
    '[ICON_VISLIMITED]',
    '[ICON_VISSECRET]',
    '[ICON_VISTOPSECRET]',
]

notSupportedIcons = [
    '[ICON_THEMEBONUS_ACTIVE]',
    '[ICON_PRESSUREUP]',
    '[ICON_PRESSUREDOWN]',
    '[ICON_TEAM]',
    '[ICON_UNDERSIEGE]',
    '[ICON_UNIT]',
    '[ICON_BUILDINGS]',
    '[ICON_Fortifying]',
    '[ICON_RAZED]',
    '[ICON_Occupied]',
    '[ICON_ABILITY]',
    '[ICON_POWERRight]'
]

base_game_locs_data = {}
base_game_units_dict = get_units_dict(f"sqlFiles/baseGame/DebugGameplay.sqlite")

def refactorCivSpecialSyntax(bbg_version, lang, docStr):
    docStr = docStr.replace('[NEWLINE]', '<br>')

    for replace in replacements:
        reg = re.compile(re.escape(replace), re.IGNORECASE)
        docStr = reg.sub(f'<img src="/images/{replace[1:-1]}.webp" style="height:1em"/>', docStr)
    reg = re.compile(re.escape('[ICON_BULLET]'), re.IGNORECASE)
    docStr = reg.sub(f'<span>&#8226;</span> ', docStr)
    reg = re.compile(re.escape('[ICON_BULLETGLOW]'), re.IGNORECASE)
    docStr = reg.sub(f'<span>&#8226;</span> ', docStr)
    for icon in notSupportedIcons:
        reg = re.compile(re.escape(icon), re.IGNORECASE)
        docStr = reg.sub(f' ', docStr)
    if (docStr.find('[ICON_') != -1):
        print(f'missing ICON_ in {bbg_version} lang={lang} {docStr.find('[ICON_')}')

    return docStr

def add_preloader():
    with div(cls="preloader"):
        with div(cls="loader"):
            div(cls="loader-outter")
            div(cls="loader-inner")
            with div(cls="indicator"):
                with svg(width="16px",height="12px"):
                    polyline(id="back", points="1 6 4 6 6 11 10 1 12 6 15 6")
                    polyline(id="front", points="1 6 4 6 6 11 10 1 12 6 15 6")

def get_version_name(bbg_version):
    return bbg_version if bbg_version != None else 'base_game'

def add_lang(text_name, link_name, bbg_version, flag, page_type):
    with li():
        with a(href=f"/{link_name}/{page_type}_{get_version_name(bbg_version)}.html", style="align-content: center;"):
            img(src=f"/assets/flags/4x3/{flag}.svg", style="height:20px")

def add_header(bbg_version, lang, page_type):
    pages_list = [
        ('leaders','Leaders'),
        ('bbg_expanded','BBG Expanded'),
        ('city_states','City States'),
        ('religion','Religion'),
        ('governor','Governors'),
        ('great_people','Great People'),
        ('natural_wonder','Natural Wonders'),
        ('world_wonder','World Wonders'),
        ('buildings','Buildings'),
        ('names','Names'),
        ('misc','Misc'),
    ]
    with nav(cls="main-nav--bg"):
        with div(cls="main-nav"):
            with div(cls="header"):
                with div(cls="header-inner"):
                    with div(cls="inner"):
                        with div(cls="row"):
                            with div(cls="flex center sidebar-toggle col-xl-1 col-lg-1 col-md-1 col-1"):
                                with button(cls="transparent-btn", title="Menu", type="button"):
                                    span("Toggle menu", cls="sr-only")
                                    span(cls="icon menu-toggle", aria_hidden="true")
                            with div(cls="flex center col-xl-1 col-lg-1 col-md-1 col-2"):
                                with a(href="/index.html", style="align-content: center;"):
                                    img(src="/images/BBGLogo.webp", style="width:3em; border-radius:10%", alt="#")
                                div(cls="mobile-nav")
                            with div(cls="flex col-xl-8 col-lg-8 col-md-8 col-8"):
                                with div(cls="main-menu"):
                                    with nav(cls="navigation"):
                                        with ul(cls="nav menu"):
                                            for t, page_name in pages_list:
                                                with li(cls="active" if t == page_type else ""):
                                                    a(page_name, href=f"/{lang}/{t}_{get_version_name(bbg_version)}.html", onclick=f'civClicked(null)')
                                            with li():
                                                with a('BBG Version'):
                                                    i(cls="icofont-rounded-down")
                                                with ul(cls="dropdown bbg-version-dropdown"):
                                                    for v in bbg_versions:
                                                        with li():
                                                            a(f"Base" if v is None else f"{v}", href=f"/{lang}/{page_type}_{'base_game' if v is None else v}.html")
                            with div(cls="flex center col-xl-2 col-lg-2 col-md-2 col-1"):
                                with div(cls='flex row justify-content-around'):
                                    # with div(cls="col-xl-3 col-lg-3 col-md-3 col-3"):
                                    #     with div(cls="extended-bbg-switcher-wrapper"):
                                    #         with button(cls="extended-bbg-switcher", type="button", title="Only Expanded BBG"):
                                    #             i(cls="fa-solid fa-star extended-icon")
                                    #             # i(cls="enable-icon", data_feather="toggle-left", aria_hidden="true")
                                    #             # i(cls="disable-icon", data_feather="toggle-right", aria_hidden="true")
                                    # div(cls="w-100")
                                    with div(cls="col-xl-4 col-lg-4 col-md-6 col-4"):
                                        with div(cls="main-menu"):
                                            with nav(cls="navigation"):
                                                with ul(cls="nav menu"):
                                                    with li():
                                                        i(cls="fa-solid fa-language lang-icon")
                                                        with ul(cls="dropdown"):
                                                            add_lang('English  ', 'en_US', bbg_version, 'us', page_type)
                                                            add_lang('French  ', 'fr_FR', bbg_version, 'fr', page_type)
                                                            add_lang('Russian  ', 'ru_RU', bbg_version, 'ru', page_type)
                                                            add_lang('German  ', 'de_DE', bbg_version, 'de', page_type)
                                                            add_lang('Chinese  ', 'zh_Hans_CN', bbg_version, 'cn', page_type)
                                                            add_lang('Korean  ', 'ko_KR', bbg_version, 'kr', page_type)
                                                            add_lang('Japanese  ', 'ja_JP', bbg_version, 'jp', page_type)
                                    div(cls="w-100")
                                    with div(cls="col-xl-4 col-lg-4 col-md-4 col-4"):
                                        with div(cls="base-game-switcher-wrapper"):
                                            with button(cls="base-game-switcher gray-circle-btn", type="button", title="Show Base Game"):
                                                i(cls="enable-icon", data_feather="toggle-left", aria_hidden="true")
                                                i(cls="disable-icon", data_feather="toggle-right", aria_hidden="true")
                                    div(cls="w-100")
                                    with div(cls="col-xl-4 col-lg-4 col-md-6 col-4"):
                                        with div(cls="theme-switcher-wrapper"):
                                            with button(cls="theme-switcher gray-circle-btn", type="button", title="Switch theme"):
                                                span("Switch theme", cls="sr-only")
                                                i(cls="sun-icon", data_feather="sun", aria_hidden="true")
                                                i(cls="moon-icon", data_feather="moon", aria_hidden="true")
    add_footer()

def add_sidebar(menu_items, menu_icons, images_dir):
    with aside(cls="sidebar"):
        with div(cls="sidebar-start"):
            with div(cls="sidebar-body"):
                with ul(cls="sidebar-body-menu"):
                    for i, item in enumerate(menu_items):
                        with li():
                            with a(href=f'#{item}', onclick=f'civClicked("{item}")'):
                                with span(cls="icon", aria_hidden="true"):
                                    img(src=f'/{images_dir}/{menu_icons[i]}.webp', onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
                                p(item)

def add_final_scripts():
    script(src="/js/jquery.min.js")
    script(src="/js/script.js")
    script(src="/plugins/feather.min.js")
    script(src="/plugins/chart.min.js")

def get_loc(locs_data, s, en_US_locs_data):
    try:
        res = locs_data[s]
        if res.find('|') == -1:
            return res
        else:
            return res[:res.find('|')]
    except KeyError:
        if locs_data == en_US_locs_data:
            return f'Not found: {s}'
        print(f'KeyError: {s} not found in locs_data')
        return get_loc(en_US_locs_data, s, en_US_locs_data)

def get_html_lang(lang):
    if len(lang) == 5:
        return lang[0 : -3]
    elif lang == 'zh_Hans_CN':
        return 'zh-Hans'
    else:
        raise ValueError(f'Unknown lang: {lang}')

def add_html_header(doc, page_title):
    with doc.head:
        script(_async=True, src="https://www.googletagmanager.com/gtag/js?id=G-Z2ESCT7CR0")
        script('''
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-Z2ESCT7CR0');
    ''')
        title(page_title)
        meta(charset='utf-8')
        meta(httpequiv="X-UA-Compatible", contents="IE=edge")
        meta(name="viewport", content="width=device-width, initial-scale=1")
        link(rel='icon', href=f'/images/BBGLogo.webp', type='image/x-icon')
        link(rel='stylesheet', href="https://fonts.googleapis.com/css?family=Poppins:200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900,900i&display=swap")
        link(rel='stylesheet', href=f"/css/style.min.css")
        link(rel='stylesheet', href=f"/css/preloader.css")
        link(rel='stylesheet', href=f"/css/animate.min.css")
        link(rel='stylesheet', href=f"/css/header.css")
        link(rel='stylesheet', href=f"/css/footer.css")
        link(rel='stylesheet', href=f"/fontawesome-free-7.0.0-web/css/all.css")

def show_element_with_base_option(element, lang, locs_data, en_US_locs_data, data_append = '', base_game_data_append = '', alignment = 'left', add_base_game = True):
    if add_base_game:
        comment(element)
        p(get_loc(locs_data, element, en_US_locs_data) + f'{data_append}', style=f"text-align:{alignment}", cls='civ-ability-desc actual-text')
        with div(cls="base-game-text row"):
            with div(cls='col-lg-6 col-md-6'):
                with div(cls="chart", style="box-shadow:none"):
                    p(get_loc(locs_data, element, en_US_locs_data) + f'{data_append}', style=f"text-align:{alignment}", cls='civ-ability-desc')
            with div(cls='col-lg-6 col-md-6'):
                with div(cls="chart", style="box-shadow:none"):
                    p(get_loc(base_game_locs_data[lang], element, base_game_locs_data['en_US']) + f'\n{base_game_data_append}', style=f"text-align:{alignment}", cls='civ-ability-desc')
    else:
        comment(element)
        p(get_loc(locs_data, element, en_US_locs_data) + f'{data_append}', style=f"text-align:{alignment}", cls='civ-ability-desc')

def get_unlock_tech_civic_dialog(unlock_tech, unlock_civic, locs_data, en_US_locs_data, tech_to_loc_dict, civic_to_loc_dict):
    if unlock_tech:
        return f'{get_loc(locs_data, "LOC_UI_PEDIA_UNLOCKED_BY", en_US_locs_data)} {get_loc(locs_data, tech_to_loc_dict[unlock_tech], en_US_locs_data)} {get_loc(locs_data, "LOC_TECHNOLOGY_NAME", en_US_locs_data)}'
    if unlock_civic:
        return f'{get_loc(locs_data, "LOC_UI_PEDIA_UNLOCKED_BY", en_US_locs_data)} {get_loc(locs_data, civic_to_loc_dict[unlock_civic], en_US_locs_data)} {get_loc(locs_data, "LOC_CIVIC_NAME", en_US_locs_data)}'

def add_footer():
    with div(cls="scroll-up footer-popup", id="footer-popup"):
        with div(cls="footer-popup-inner"):
            with div(cls="row"):
                with div(cls="col-sm-8 col-1 footer-popup-body"):
                    p("If you like this project, any donation would be extremely helpful for me in maintaining the website.", id="donateText")
                    # p("Your support helps to keep the project alive and allows for further development.")
                with div(cls="col-sm-2 col-6 footer-popup-donate"):
                    a("Donate", href="https://ko-fi.com/calcalciffer", target="_blank", cls="btn btn-primary")
                with div(cls="col-sm-2 col-6 footer-popup-scroll-up"):
                    with a(id="scrollUp", cls="displayNone", href="#top", onclick=f'civClicked(null)'):
                        i(cls='fa-solid fa-up-long')

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
                                                    img(src=f'/images/leaders/{get_loc(en_US_locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(en_US_locs_data, leader[5], en_US_locs_data)}.webp', style="vertical-align: middle; width:7em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
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
                                                        img(src=f'/images/items/{get_loc(en_US_locs_data, item[4], en_US_locs_data)}.webp', style="vertical-align: middle; width:2em; text-align:left", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")

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
    for cs in city_states:
        menu_items.append(get_loc(locs_data, cs[2], en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, cs[2], en_US_locs_data))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, 'city_states')
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/city_states')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                h1(title, cls='civ-name')
                                br()
                                for cs in city_states:
                                    with div(cls="row", id=get_loc(locs_data, cs[2], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                comment(cs[2])
                                                with h2(get_loc(locs_data, cs[2], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/city_states/{get_loc(en_US_locs_data, cs[2], en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
                                                cs_desc = cs[7] if cs[7] != None else (cs[6] if cs[6] != None else cs[5])
                                                show_element_with_base_option(cs_desc, lang, locs_data, en_US_locs_data)

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
                                                    img(src=f'/images/religion/{get_loc(en_US_locs_data, religion_cls, en_US_locs_data)}.webp', style="vertical-align: middle; height:4em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
                                        for elem in religion_cls_elements[religion_cls]:
                                            with div(cls="col-lg-6"):
                                                with div(cls="chart"):
                                                    if religion_cls == 'LOC_BELIEF_CLASS_PANTHEON_NAME':
                                                        comment(elem[1])
                                                        with h2(get_loc(locs_data, elem[1], en_US_locs_data), cls='civ-name'):
                                                            img(src=f'/images/religion/{get_loc(en_US_locs_data, elem[1], en_US_locs_data)}.webp', style="vertical-align: middle; height:3em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
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
                                                    img(src=f'/images/governors/{get_loc(en_US_locs_data, gov[1], en_US_locs_data)}.webp', style="vertical-align: middle; width:7em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
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
                                                    img(src=f'/images/natural_wonders/{get_loc(en_US_locs_data, wonder[1], en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
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
                                                        img(src=f'/images/world_wonders/{get_loc(en_US_locs_data, wonder[0][1], en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
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
                                                        img(src=f'/images/ICON_{dedication[0]}.webp', style="vertical-align: middle; width:5em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
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
                                                    img(src=f'/images/{get_loc(en_US_locs_data, gp_type, en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
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
                                                                p(img(src=f'/images/{work[2]}.webp', style="vertical-align: middle; width:2em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';"), f' {get_loc(locs_data, work[1], en_US_locs_data)}', style="text-align:left", cls='civ-ability-desc')
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
            img(src=f'/images/ICON_PRODUCTION.webp', style="vertical-align: middle", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
    building_maintenance = int(tmp_yields[23])
    if building_maintenance > 0:
        maintenance_loc = get_loc(locs_data, 'LOC_TOOLTIP_MAINTENANCE', en_US_locs_data)
        processed = loc_amount_parameter(maintenance_loc, building_maintenance)
        processed = processed.replace('{2_YieldIcon}', '[ICON_GOLD]')
        processed = processed.replace('{3_YieldName}', get_loc(locs_data, 'LOC_YIELD_GOLD_NAME', en_US_locs_data))
        processed = processed.replace('{3_YieldName[2]}', get_loc(locs_data, 'LOC_YIELD_GOLD_NAME', en_US_locs_data))
        processed = processed.replace('{3_YieldName[8]}', get_loc(locs_data, 'LOC_YIELD_GOLD_NAME', en_US_locs_data))
        p(processed, style="text-align:left", cls='civ-ability-desc')
        # img(src=f'/images/ICON_PRODUCTION.webp', style="vertical-align: middle", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")

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
                                                        img(src=f'/images/buildings/{get_loc(en_US_locs_data, building, en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
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
                                                    img(src=f'/images/leaders/{get_loc(en_US_locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(en_US_locs_data, leader[5], en_US_locs_data)}.webp', style="vertical-align: middle; width:7em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
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
                                                        img(src=f'/images/items/{get_loc(en_US_locs_data, item[4], en_US_locs_data)}.webp', style="vertical-align: middle; width:2em; text-align:left", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")

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
                                                    img(src=f'/images/governors/{get_loc(en_US_locs_data, gov[1], en_US_locs_data)}.webp', style="vertical-align: middle; width:7em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
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