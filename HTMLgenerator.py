from bs4 import BeautifulSoup
import sqlite3
import re

import dominate
from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

replacements = [
    '[ICON_AMENITIES]',
    '[ICON_ANTIAIR_LARGE]',
    '[ICON_ARMY]',
    '[ICON_BARBARIAN]',
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
    '[ICON_INFLUENCEPERTURN]',
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
    '[ICON_GREATWRITER]',
    '[ICON_HOUSING]',
    '[ICON_MOVEMENT]',
    '[ICON_FORTIFIED]',
    '[ICON_NUCLEAR]',
    '[ICON_PILLAGED]',
    # '[ICON_POPULATION]',
    '[ICON_POWER]',
    '[ICON_PRODUCTION]',
    '[ICON_PROMOTION]',
    '[ICON_RANGE]',
    '[ICON_RANGED]',
    '[ICON_RELIGION]',
    '[ICON_RESOURCE_COAL]',
    '[ICON_RESOURCE_IRON]',
    '[ICON_RESOURCE_HORSES]',
    '[ICON_RESOURCE_NITER]',
    '[ICON_RESOURCE_BANANAS]',
    '[ICON_RESOURCE_DEER]',
    '[ICON_RESOURCE_CATTLE]',
    '[ICON_RESOURCE_CINNAMON]',
    '[ICON_RESOURCE_CLOVES]',
    '[ICON_RESOURCE_MAIZE]',
    '[ICON_RESOURCE_SHEEP]',
    '[ICON_RESOURCE_RICE]',
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
    '[ICON_VISLIMITED]'
]

civ_leaders_items = get_civs_tables("sqlFiles/DebugConfiguration.sqlite")
city_states = get_city_states("sqlFiles/DebugConfiguration.sqlite")
pantheons = get_beliefs("sqlFiles/DebugGameplay.sqlite", 'BELIEF_CLASS_PANTHEON')
religion_founder = get_beliefs("sqlFiles/DebugGameplay.sqlite", 'BELIEF_CLASS_FOUNDER')
religion_follower = get_beliefs("sqlFiles/DebugGameplay.sqlite", 'BELIEF_CLASS_FOLLOWER')
religion_enhancer = get_beliefs("sqlFiles/DebugGameplay.sqlite", 'BELIEF_CLASS_ENHANCER')
religion_worship = get_beliefs("sqlFiles/DebugGameplay.sqlite", 'BELIEF_CLASS_WORSHIP')
governors = get_governors_list("sqlFiles/DebugGameplay.sqlite")
governor_promotion_set_dict = get_governors_promotion_sets_dict("sqlFiles/DebugGameplay.sqlite", governors)
governor_promotion_dict = get_governors_promotion_dict("sqlFiles/DebugGameplay.sqlite", governor_promotion_set_dict)
# for item in governor_promotion_dict:
#     print(item, governor_promotion_dict[item])
# print(governor_promotion_dict)
# exit(-1)

def refactorCivSpecialSyntax(bbg_version, lang, docStr):
    docStr = docStr.replace('[NEWLINE]', '<br>')

    for replace in replacements:
        reg = re.compile(re.escape(replace), re.IGNORECASE)
        docStr = reg.sub(f'<img src="/images/{replace[1:-1]}.webp" style="height:1em"/>', docStr)
    reg = re.compile(re.escape('[ICON_BULLET]'), re.IGNORECASE)
    docStr = reg.sub(f'<span>&#8226;</span> ', docStr)
    docStr = docStr.replace('[ICON_THEMEBONUS_ACTIVE]', '')
    docStr = docStr.replace('[ICON_PRESSUREUP]', '')
    docStr = docStr.replace('[ICON_PRESSUREDOWN]', '')
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

bbg_versions = [None, '6.4', '6.3', '6.2', '6.1', '6.0', '5.8', '5.7', '5.6']
# bbg_versions = ['6.4']

def get_version_name(bbg_version):
    return bbg_version if bbg_version != None else 'base_game'

def add_lang(text_name, link_name, bbg_version, flag, leader_page, cs_page, pantheon_page, religion_page, governor_page):
    with li():
        if leader_page:
            with a(href=f"/{link_name}/leaders_{get_version_name(bbg_version)}.html", style="align-content: center;"):
                img(src=f"/assets/flags/4x3/{flag}.svg", style="height:20px")
        elif cs_page:
            with a(href=f"/{link_name}/city_states_{get_version_name(bbg_version)}.html", style="align-content: center;"):
                img(src=f"/assets/flags/4x3/{flag}.svg", style="height:20px")
        elif pantheon_page:
            with a(href=f"/{link_name}/pantheons_{get_version_name(bbg_version)}.html", style="align-content: center;"):
                img(src=f"/assets/flags/4x3/{flag}.svg", style="height:20px")
        elif religion_page:
            with a(href=f"/{link_name}/religion_{get_version_name(bbg_version)}.html", style="align-content: center;"):
                img(src=f"/assets/flags/4x3/{flag}.svg", style="height:20px")
        elif governor_page:
            with a(href=f"/{link_name}/governor_{get_version_name(bbg_version)}.html", style="align-content: center;"):
                img(src=f"/assets/flags/4x3/{flag}.svg", style="height:20px")

def add_header(bbg_version, lang, leader_page = False, cs_page = False, pantheon_page = False, religion_page = False, governor_page = False):
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
                            with div(cls="flex center col-xl-2 col-lg-2 col-md-2 col-2"):
                                with a(href="/index.html", style="align-content: center;"):
                                    img(src="/images/BBGLogo.webp", style="width:50px; border-radius:10%", alt="#")
                                div(cls="mobile-nav")
                            with div(cls="flex col-xl-7 col-lg-7 col-md-7 col-5"):
                                with div(cls="main-menu"):
                                    with nav(cls="navigation"):
                                        with ul(cls="nav menu"):
                                            with li(cls="active" if leader_page else ""):
                                                a('Leaders', href=f"/{lang}/leaders_{get_version_name(bbg_version)}.html", onclick=f'civClicked(null)')
                                            with li(cls="active" if cs_page else ""):
                                                a('City States', href=f"/{lang}/city_states_{get_version_name(bbg_version)}.html", onclick=f'civClicked(null)')
                                            with li(cls="active" if pantheon_page else ""):
                                                a('Pantheons', href=f"/{lang}/pantheons_{get_version_name(bbg_version)}.html", onclick=f'civClicked(null)')
                                            with li(cls="active" if religion_page else ""):
                                                a('Religion', href=f"/{lang}/religion_{get_version_name(bbg_version)}.html", onclick=f'civClicked(null)')
                                            with li(cls="active" if governor_page else ""):
                                                a('Governors', href=f"/{lang}/governor_{get_version_name(bbg_version)}.html", onclick=f'civClicked(null)')
                                            with li():
                                                with a('BBG Version'):
                                                    i(cls="icofont-rounded-down")
                                                with ul(cls="dropdown"):
                                                    for v in bbg_versions:
                                                        with li():
                                                            if leader_page:
                                                                if v is None:
                                                                    a(f"Base Game", href=f"/{lang}/leaders_base_game.html")
                                                                else:
                                                                    a(f"BBG v{v}", href=f"/{lang}/leaders_{v}.html")
                                                            elif cs_page:
                                                                if v is None:
                                                                    a(f"Base Game", href=f"/{lang}/city_states_base_game.html")
                                                                else:
                                                                    a(f"BBG v{v}", href=f"/{lang}/city_states_{v}.html")
                                                            elif pantheon_page:
                                                                if v is None:
                                                                    a(f"Base Game", href=f"/{lang}/pantheons_base_game.html")
                                                                else:
                                                                    a(f"BBG v{v}", href=f"/{lang}/pantheons_{v}.html")
                                                            elif religion_page:
                                                                if v is None:
                                                                    a(f"Base Game", href=f"/{lang}/religion_base_game.html")
                                                                else:
                                                                    a(f"BBG v{v}", href=f"/{lang}/religion_{v}.html")
                                                            elif governor_page:
                                                                if v is None:
                                                                    a(f"Base Game", href=f"/{lang}/governor_base_game.html")
                                                                else:
                                                                    a(f"BBG v{v}", href=f"/{lang}/governor_{v}.html")
                            with div(cls="flex center col-xl-1 col-lg-1 col-md-1 col-2"):
                                with div(cls="main-menu"):
                                    with nav(cls="navigation"):
                                        with ul(cls="nav menu"):
                                            with li():
                                                i(cls="lang-icon fa fa-language", style="font-size:50px; padding-top:7px")

                                                with ul(cls="dropdown", style="width:80px"):
                                                    add_lang('English  ', 'en_US', bbg_version, 'us', leader_page, cs_page, pantheon_page, religion_page, governor_page)
                                                    add_lang('French  ', 'fr_FR', bbg_version, 'fr', leader_page, cs_page, pantheon_page, religion_page, governor_page)
                                                    add_lang('Russian  ', 'ru_RU', bbg_version, 'ru', leader_page, cs_page, pantheon_page, religion_page, governor_page)
                                                    add_lang('German  ', 'de_DE', bbg_version, 'de', leader_page, cs_page, pantheon_page, religion_page, governor_page)
                                                    add_lang('Chinese  ', 'zh_Hans_CN', bbg_version, 'cn', leader_page, cs_page, pantheon_page, religion_page, governor_page)
                                                    add_lang('Korean  ', 'ko_KR', bbg_version, 'kr', leader_page, cs_page, pantheon_page, religion_page, governor_page)
                            with div(cls="flex center col-xl-1 col-lg-1 col-md-1 col-2"):
                                with div(cls="theme-switcher-wrapper"):
                                    with button(cls="theme-switcher gray-circle-btn", type="button", title="Switch theme"):
                                        span("Switch theme", cls="sr-only")
                                        i(cls="sun-icon", data_feather="sun", aria_hidden="true")
                                        i(cls="moon-icon", data_feather="moon", aria_hidden="true")
    
def add_sidebar(menu_items, menu_icons, images_dir):
    with aside(cls="sidebar"):
        with div(cls="sidebar-start"):
            with div(cls="sidebar-body"):
                with ul(cls="sidebar-body-menu"):
                    for i, item in enumerate(menu_items):
                        with li():
                            with a(href=f'#{item}', onclick=f'civClicked("{item}")'):
                                with span(cls="icon", aria_hidden="true"):
                                    img(src=f'/{images_dir}/{menu_icons[i]}.webp')
                                p(item)

def add_final_scripts():
    script(src="/js/jquery.min.js")
    script(src="/js/script.js")
    script(src="/plugins/feather.min.js")
    script(src="/plugins/chart.min.js")
    script(src="https://kit.fontawesome.com/bd91c323e3.js", crossorigin="anonymous")
    
def get_loc(locs_data, s):
    try:
        res = locs_data[s]
        if res.find('|') == -1:
            return res
        else:
            return res[:res.find('|')]
    except KeyError:
        print(f'KeyError: {s} not found in locs_data')
        return s
    
def get_html_lang(lang):
    if lang == 'de_DE':
        return 'de'
    if lang == 'en_US':
        return 'en'
    if lang == 'es_ES':
        return 'es'
    if lang == 'fr_FR':
        return 'fr'
    if lang == 'it_IT':
        return 'it'
    if lang == 'ja_JP':
        return 'ja'
    if lang == 'ko_KR':
        return 'ko'
    if lang == 'pl_PL':
        return 'pl'
    if lang == 'pt_BR':
        return 'pt'
    if lang == 'ru_RU':
        return 'ru'
    if lang == 'zh_Hans_CN':
        return 'zh-Hans'
    
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
        link(rel='icon', href=f'/images/civVI.webp', type='image/x-icon')
        link(rel='stylesheet', href="https://fonts.googleapis.com/css?family=Poppins:200i,300,300i,400,400i,500,500i,600,600i,700,700i,800,800i,900,900i&display=swap")
        link(rel='stylesheet', href=f"/css/style.min.css")
        link(rel='stylesheet', href=f"/css/preloader.css")
        link(rel='stylesheet', href=f"/css/animate.min.css")
        link(rel='stylesheet', href=f"/css/header.css")
        
def add_scroll_up():
    with a(id="scrollUp", cls="scroll-up displayNone", href="#top", onclick=f'civClicked(null)', style="position: fixed; z-index: 2147483647;"):
        with span():
            i(cls='fa fa-angle-up')

def get_leader_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, 'en_US')
    locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, lang)

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    if bbg_version != None:
        add_html_header(doc, f'BBG {bbg_version} Leader Description')
    else :
        add_html_header(doc, f'Civ VI GS RF Leaders Description')

    menu_items = []
    menu_icons = []
    for leader in civ_leaders_items:
        menu_items.append(get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5]))
        menu_icons.append(get_loc(en_US_locs_data, leader[2]) + ' ' + get_loc(en_US_locs_data, leader[5]))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, leader_page=True)
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/leaders')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                for leader in civ_leaders_items:
                                    with div(cls="row", id=get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5])):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                with h2(get_loc(locs_data, leader[2]) + ' ' + get_loc(locs_data, leader[5]), cls='civ-name'):
                                                    img(src=f'/images/leaders/{get_loc(en_US_locs_data, leader[2]) + ' ' + get_loc(en_US_locs_data, leader[5])}.webp', style="vertical-align: middle")
                                                h3(get_loc(locs_data, leader[3]), style="text-align:left", cls='civ-ability-name')
                                                br()
                                                p(get_loc(locs_data, leader[4]), style="text-align:left", cls='civ-ability-desc')
                                                br()
                                                h3(get_loc(locs_data, leader[6]), style="text-align:left", cls='civ-ability-name')
                                                br()
                                                p(f'{get_loc(locs_data, leader[7])}', style="text-align:left", cls='civ-ability-desc')
                                                br()
                                                for item in civ_leaders_items[leader]:
                                                    with h3(f'{get_loc(locs_data, item[4])}', style="text-align:left", cls='civ-ability-name'):
                                                        img(src=f'/images/items/{get_loc(en_US_locs_data, item[4])}.webp', style="vertical-align: middle; width:2em; text-align:left")
                                                    p(f'{get_loc(locs_data, item[5])}', style="text-align:left", cls='civ-ability-desc')
                                                    br()

        add_final_scripts()
        add_scroll_up()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_city_state_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, 'en_US')
    locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, lang)

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    if bbg_version != None:
        add_html_header(doc, f'BBG {bbg_version} City State Description')
    else :
        add_html_header(doc, f'Civ VI GS RF City State Description')

    menu_items = []
    menu_icons = []
    for cs in city_states:
        menu_items.append(get_loc(locs_data, cs[2]))
        menu_icons.append(get_loc(en_US_locs_data, cs[2]))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, cs_page=True)
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/city_states')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                for cs in city_states:
                                    with div(cls="row", id=get_loc(locs_data, cs[2])):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                with h2(get_loc(locs_data, cs[2]), cls='civ-name'):
                                                    img(src=f'/images/city_states/{get_loc(en_US_locs_data, cs[2])}.webp', style="vertical-align: middle")
                                                p(get_loc(locs_data, cs[5]), style="text-align:left", cls='civ-ability-desc')

        add_final_scripts()
        add_scroll_up()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_pantheon_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, 'en_US')
    locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, lang)

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    if bbg_version != None:
        add_html_header(doc, f'BBG {bbg_version} Pantheons Description')
    else :
        add_html_header(doc, f'Civ VI GS RF Pantheons Description')

    menu_items = []
    menu_icons = []
    for pan in pantheons:
        menu_items.append(get_loc(locs_data, pan[1]))
        menu_icons.append(get_loc(en_US_locs_data, pan[1]))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, pantheon_page=True)
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/pantheons')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                for pan in pantheons:
                                    with div(cls="row", id=get_loc(locs_data, pan[1])):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                with h2(get_loc(locs_data, pan[1]), cls='civ-name'):
                                                    img(src=f'/images/pantheons/{get_loc(en_US_locs_data, pan[1])}.webp', style="vertical-align: middle; height:5em")
                                                p(get_loc(locs_data, pan[2]), style="text-align:left", cls='civ-ability-desc')

        add_final_scripts()
        add_scroll_up()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_religion_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, 'en_US')
    locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, lang)

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    if bbg_version != None:
        add_html_header(doc, f'BBG {bbg_version} Religion Description')
    else :
        add_html_header(doc, f'Civ VI GS RF Religion Description')

    types = [
        'LOC_BELIEF_CLASS_FOLLOWER_NAME',
        'LOC_BELIEF_CLASS_FOUNDER_NAME',
        'LOC_BELIEF_CLASS_ENHANCER_NAME',
        'LOC_BELIEF_CLASS_WORSHIP_NAME',
    ]
    menu_items = []
    menu_icons = []
    for t in types:
        menu_items.append(get_loc(locs_data, t))
        menu_icons.append(get_loc(en_US_locs_data, t))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, religion_page=True)
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/religion')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                with div(cls="row", id=menu_items[0]):
                                    with div(cls="col-lg-12"):
                                        with div(cls="chart"):
                                            h1(menu_items[0], cls='civ-name')
                                    for belief in religion_follower:
                                        with div(cls="col-lg-6"):
                                            with div(cls="chart"):
                                                h2(get_loc(locs_data, belief[1]), cls='civ-name')
                                                p(get_loc(locs_data, belief[2]), style="text-align:left", cls='civ-ability-desc')
                                with div(cls="row", id=menu_items[1]):
                                    with div(cls="col-lg-12"):
                                        with div(cls="chart"):
                                            h1(menu_items[1], cls='civ-name')
                                    for belief in religion_founder:
                                        with div(cls="col-lg-6"):
                                            with div(cls="chart"):
                                                h2(get_loc(locs_data, belief[1]), cls='civ-name')
                                                p(get_loc(locs_data, belief[2]), style="text-align:left", cls='civ-ability-desc')
                                with div(cls="row", id=menu_items[2]):
                                    with div(cls="col-lg-12"):
                                        with div(cls="chart"):
                                            h1(menu_items[2], cls='civ-name')
                                    for belief in religion_enhancer:
                                        with div(cls="col-lg-6"):
                                            with div(cls="chart"):
                                                h2(get_loc(locs_data, belief[1]), cls='civ-name')
                                                p(get_loc(locs_data, belief[2]), style="text-align:left", cls='civ-ability-desc')
                                with div(cls="row", id=menu_items[3]):
                                    with div(cls="col-lg-12"):
                                        with div(cls="chart"):
                                            h1(menu_items[3], cls='civ-name')
                                    for belief in religion_worship:
                                        with div(cls="col-lg-6"):
                                            with div(cls="chart"):
                                                h2(get_loc(locs_data, belief[1]), cls='civ-name')
                                                p(get_loc(locs_data, belief[2]), style="text-align:left", cls='civ-ability-desc')

        add_final_scripts()
        add_scroll_up()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)

def get_governor_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, 'en_US')
    locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, lang)

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    if bbg_version != None:
        add_html_header(doc, f'BBG {bbg_version} Governors')
    else :
        add_html_header(doc, f'Civ VI GS RF Governors')

    menu_items = []
    menu_icons = []
    for gov in governors:
        menu_items.append(get_loc(locs_data, gov[1]))
        menu_icons.append(get_loc(en_US_locs_data, gov[1]))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, governor_page=True)
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/governors')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                for gov in governors:
                                    with div(cls="row", id=get_loc(locs_data, gov[1])):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                with h2(get_loc(locs_data, gov[1]), cls='civ-name'):
                                                    img(src=f'/images/governors/{get_loc(en_US_locs_data, gov[1])}.webp', style="vertical-align: middle")
                                                for promotion in governor_promotion_set_dict[gov[0]]:
                                                    promotion_name = governor_promotion_dict[promotion][1]
                                                    # print(promotion, promotion_name)
                                                    with h3(f'{get_loc(locs_data, promotion_name)}', style="text-align:left", cls='civ-ability-name'):
                                                        br()
                                                        br()
                                                        promotion_desc = governor_promotion_dict[promotion][2]
                                                        p(f'{get_loc(locs_data, promotion_desc)}', style="text-align:left", cls='civ-ability-desc')
                                                        br()

        add_final_scripts()
        add_scroll_up()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)