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
    '[ICON_GREATWRITER]',
    '[ICON_HOUSING]',
    '[ICON_INFLUENCEPERTURN]',
    '[ICON_LIFESPAN]',
    '[ICON_MOVEMENT]',
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
    '[ICON_RESOURCE_STONE]',
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

def add_lang(text_name, link_name, bbg_version, flag, leader_page, cs_page, pantheon_page, religion_page, governor_page, natural_wonder_page, world_wonder_page):
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
        elif natural_wonder_page:
            with a(href=f"/{link_name}/natural_wonder_{get_version_name(bbg_version)}.html", style="align-content: center;"):
                img(src=f"/assets/flags/4x3/{flag}.svg", style="height:20px")
        elif world_wonder_page:
            with a(href=f"/{link_name}/world_wonder_{get_version_name(bbg_version)}.html", style="align-content: center;"):
                img(src=f"/assets/flags/4x3/{flag}.svg", style="height:20px")

def add_header(bbg_version, lang, leader_page = False, cs_page = False, pantheon_page = False, religion_page = False, governor_page = False, natural_wonder_page = False, world_wonder_page = False):
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
                            with div(cls="flex center col-xl-1 col-lg-1 col-md-1 col-1"):
                                with a(href="/index.html", style="align-content: center;"):
                                    img(src="/images/BBGLogo.webp", style="width:3em; border-radius:10%", alt="#")
                                div(cls="mobile-nav")
                            with div(cls="flex col-xl-8 col-lg-8 col-md-8 col-8"):
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
                                            with li(cls="active" if natural_wonder_page else ""):
                                                a('Natural Wonders', href=f"/{lang}/natural_wonder_{get_version_name(bbg_version)}.html", onclick=f'civClicked(null)')
                                            with li(cls="active" if world_wonder_page else ""):
                                                a('World Wonders', href=f"/{lang}/world_wonder_{get_version_name(bbg_version)}.html", onclick=f'civClicked(null)')
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
                                                            elif natural_wonder_page:
                                                                if v is None:
                                                                    a(f"Base Game", href=f"/{lang}/natural_wonder_base_game.html")
                                                                else:
                                                                    a(f"BBG v{v}", href=f"/{lang}/natural_wonder_{v}.html")
                                                            elif world_wonder_page:
                                                                if v is None:
                                                                    a(f"Base Game", href=f"/{lang}/world_wonder_base_game.html")
                                                                else:
                                                                    a(f"BBG v{v}", href=f"/{lang}/world_wonder_{v}.html")
                                            with li(cls=""):
                                                a('Donate!', href=f"https://ko-fi.com/calcalciffer", target="_blank")
                            with div(cls="flex center col-xl-2 col-lg-2 col-md-2 col-2"):
                                with div(cls='flex row justify-content-around'):
                                    with div(cls="col-xl-6 col-lg-6 col-md-6 col-6"):
                                        with div(cls="main-menu"):
                                            with nav(cls="navigation"):
                                                with ul(cls="nav menu"):
                                                    with li():
                                                        i(cls="fa fa-language lang-icon")

                                                        with ul(cls="dropdown", style="width:80px"):
                                                            add_lang('English  ', 'en_US', bbg_version, 'us', leader_page, cs_page, pantheon_page, religion_page, governor_page, natural_wonder_page, world_wonder_page)
                                                            add_lang('French  ', 'fr_FR', bbg_version, 'fr', leader_page, cs_page, pantheon_page, religion_page, governor_page, natural_wonder_page, world_wonder_page)
                                                            add_lang('Russian  ', 'ru_RU', bbg_version, 'ru', leader_page, cs_page, pantheon_page, religion_page, governor_page, natural_wonder_page, world_wonder_page)
                                                            add_lang('German  ', 'de_DE', bbg_version, 'de', leader_page, cs_page, pantheon_page, religion_page, governor_page, natural_wonder_page, world_wonder_page)
                                                            add_lang('Chinese  ', 'zh_Hans_CN', bbg_version, 'cn', leader_page, cs_page, pantheon_page, religion_page, governor_page, natural_wonder_page, world_wonder_page)
                                                            add_lang('Korean  ', 'ko_KR', bbg_version, 'kr', leader_page, cs_page, pantheon_page, religion_page, governor_page, natural_wonder_page, world_wonder_page)
                                    div(cls="w-100")
                                    with div(cls="col-xl-6 col-lg-6 col-md-6 col-6"):
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
                                    img(src=f'/{images_dir}/{menu_icons[i]}.webp', onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
                                p(item)

def add_final_scripts():
    script(src="/js/jquery.min.js")
    script(src="/js/script.js")
    script(src="/plugins/feather.min.js")
    script(src="/plugins/chart.min.js")
    script(src="https://kit.fontawesome.com/bd91c323e3.js", crossorigin="anonymous")
    
def get_loc(locs_data, s, en_US_locs_data):
    try:
        res = locs_data[s]
        if res.find('|') == -1:
            return res
        else:
            return res[:res.find('|')]
    except KeyError:
        print(f'KeyError: {s} not found in locs_data')
        return get_loc(en_US_locs_data, s, en_US_locs_data)
    
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
    civ_leaders_items = get_civs_tables(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugConfiguration.sqlite")
    for leader in civ_leaders_items:
        menu_items.append(get_loc(locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(locs_data, leader[5], en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(en_US_locs_data, leader[5], en_US_locs_data))
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
                                    with div(cls="row", id=get_loc(locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(locs_data, leader[5], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                with h2(get_loc(locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(locs_data, leader[5], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/leaders/{get_loc(en_US_locs_data, leader[2], en_US_locs_data) + ' ' + get_loc(en_US_locs_data, leader[5], en_US_locs_data)}.webp', style="vertical-align: middle; width:7em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
                                                h3(get_loc(locs_data, leader[3], en_US_locs_data), style="text-align:left", cls='civ-ability-name')
                                                br()
                                                p(get_loc(locs_data, leader[4], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')
                                                br()
                                                h3(get_loc(locs_data, leader[6], en_US_locs_data), style="text-align:left", cls='civ-ability-name')
                                                br()
                                                p(f'{get_loc(locs_data, leader[7], en_US_locs_data)}', style="text-align:left", cls='civ-ability-desc')
                                                br()
                                                for item in civ_leaders_items[leader]:
                                                    with h3(f'{get_loc(locs_data, item[4], en_US_locs_data)}', style="text-align:left", cls='civ-ability-name'):
                                                        img(src=f'/images/items/{get_loc(en_US_locs_data, item[4], en_US_locs_data)}.webp', style="vertical-align: middle; width:2em; text-align:left", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
                                                    p(f'{get_loc(locs_data, item[5], en_US_locs_data)}', style="text-align:left", cls='civ-ability-desc')
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
    city_states = get_city_states(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugConfiguration.sqlite")
    for cs in city_states:
        menu_items.append(get_loc(locs_data, cs[2], en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, cs[2], en_US_locs_data))
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
                                    with div(cls="row", id=get_loc(locs_data, cs[2], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                with h2(get_loc(locs_data, cs[2], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/city_states/{get_loc(en_US_locs_data, cs[2], en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
                                                p(get_loc(locs_data, cs[5], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')

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
    pantheons = get_beliefs(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", 'BELIEF_CLASS_PANTHEON')
    for pan in pantheons:
        menu_items.append(get_loc(locs_data, pan[1], en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, pan[1], en_US_locs_data))
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
                                    with div(cls="row", id=get_loc(locs_data, pan[1], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                with h2(get_loc(locs_data, pan[1], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/pantheons/{get_loc(en_US_locs_data, pan[1], en_US_locs_data)}.webp', style="vertical-align: middle; height:5em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
                                                p(get_loc(locs_data, pan[2], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')

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
        menu_items.append(get_loc(locs_data, t, en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, t, en_US_locs_data))
    religion_founder = get_beliefs(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", 'BELIEF_CLASS_FOUNDER')
    religion_follower = get_beliefs(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", 'BELIEF_CLASS_FOLLOWER')
    religion_enhancer = get_beliefs(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", 'BELIEF_CLASS_ENHANCER')
    religion_worship = get_beliefs(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite", 'BELIEF_CLASS_WORSHIP')

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
                                                h2(get_loc(locs_data, belief[1], en_US_locs_data), cls='civ-name')
                                                p(get_loc(locs_data, belief[2], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')
                                with div(cls="row", id=menu_items[1]):
                                    with div(cls="col-lg-12"):
                                        with div(cls="chart"):
                                            h1(menu_items[1], cls='civ-name')
                                    for belief in religion_founder:
                                        with div(cls="col-lg-6"):
                                            with div(cls="chart"):
                                                h2(get_loc(locs_data, belief[1], en_US_locs_data), cls='civ-name')
                                                p(get_loc(locs_data, belief[2], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')
                                with div(cls="row", id=menu_items[2]):
                                    with div(cls="col-lg-12"):
                                        with div(cls="chart"):
                                            h1(menu_items[2], cls='civ-name')
                                    for belief in religion_enhancer:
                                        with div(cls="col-lg-6"):
                                            with div(cls="chart"):
                                                h2(get_loc(locs_data, belief[1], en_US_locs_data), cls='civ-name')
                                                p(get_loc(locs_data, belief[2], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')
                                with div(cls="row", id=menu_items[3]):
                                    with div(cls="col-lg-12"):
                                        with div(cls="chart"):
                                            h1(menu_items[3], cls='civ-name')
                                    for belief in religion_worship:
                                        with div(cls="col-lg-6"):
                                            with div(cls="chart"):
                                                h2(get_loc(locs_data, belief[1], en_US_locs_data), cls='civ-name')
                                                p(get_loc(locs_data, belief[2], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')

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
                add_header(bbg_version, lang, governor_page=True)
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/governors')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                for gov in governors:
                                    with div(cls="row", id=get_loc(locs_data, gov[1], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                with h2(get_loc(locs_data, gov[1], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/governors/{get_loc(en_US_locs_data, gov[1], en_US_locs_data)}.webp', style="vertical-align: middle; width:7em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
                                                br()
                                                for level in governor_promotion_set_dict[gov[0]]:
                                                    column_count = len(governor_promotion_set_dict[gov[0]][level])
                                                    if column_count == 1:
                                                        div_cls = "col-lg-12"
                                                    else:
                                                        div_cls = "col-lg-6"
                                                    with div(cls='row'):
                                                        for column in governor_promotion_set_dict[gov[0]][level]:
                                                            has_border = 'gov-promotion-border' if column < column_count - 1 else ''
                                                            with div(cls=f'{div_cls} gov-promotion {has_border}'):
                                                                promotion = governor_promotion_set_dict[gov[0]][level][column][0]
                                                                promotion_name = governor_promotion_dict[promotion][1]
                                                                alignment = 'left' if column == 0 else 'center' if column == 1 else 'right'
                                                                with h3(f'{get_loc(locs_data, promotion_name, en_US_locs_data)}', style=f"text-align:{alignment}", cls='civ-ability-name'):
                                                                    br()
                                                                    br()
                                                                    promotion_desc = governor_promotion_dict[promotion][2]
                                                                    p(f'{get_loc(locs_data, promotion_desc, en_US_locs_data)}', style=f"text-align:{alignment}", cls='civ-ability-desc')
                                                                    br()

        add_final_scripts()
        add_scroll_up()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)
    
def get_natural_wonder_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, 'en_US')
    locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, lang)

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    if bbg_version != None:
        add_html_header(doc, f'BBG {bbg_version} Natural Wonders')
    else :
        add_html_header(doc, f'Civ VI GS RF Natural Wonders')

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
                add_header(bbg_version, lang, natural_wonder_page=True)
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/natural_wonders')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                for wonder in natural_wonders:
                                    with div(cls="row", id=get_loc(locs_data, wonder[1], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                with h2(get_loc(locs_data, wonder[1], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/natural_wonders/{get_loc(en_US_locs_data, wonder[1], en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
                                                br()
                                                p(get_loc(locs_data, wonder[2], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')
                                                br()
        add_final_scripts()
        add_scroll_up()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)
    
def get_world_wonder_html_file(bbg_version, lang):
    en_US_locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, 'en_US')
    locs_data = get_locs_data("sqlFiles/CivVILocalization.sqlite", bbg_version, lang)

    doc = dominate.document(title=None, lang=get_html_lang(lang))
    if bbg_version != None:
        add_html_header(doc, f'BBG {bbg_version} World Wonders')
    else :
        add_html_header(doc, f'Civ VI GS RF World Wonders')

    menu_items = []
    menu_icons = []
    world_wonders = get_world_wonders_list(f"sqlFiles/{bbg_version if bbg_version != None else 'baseGame'}/DebugGameplay.sqlite")
    for wonder in world_wonders:
        menu_items.append(get_loc(locs_data, wonder[1], en_US_locs_data))
        menu_icons.append(get_loc(en_US_locs_data, wonder[1], en_US_locs_data))
    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"):
            with div(cls="main-wrapper"):
                add_header(bbg_version, lang, world_wonder_page=True)
                with div(cls=""):
                    with div(cls="fixed left-0 right-auto h-screen w-[253px] bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                        add_sidebar(menu_items, menu_icons, 'images/world_wonders')
                    with div(cls="leaders-data min-w-full main-pl"):
                        with main(cls="main users chart-page"):
                            with div(cls="container"):
                                for wonder in world_wonders:
                                    with div(cls="row", id=get_loc(locs_data, wonder[1], en_US_locs_data)):
                                        with div(cls="col-lg-12"):
                                            with div(cls="chart"):
                                                with h2(get_loc(locs_data, wonder[1], en_US_locs_data), cls='civ-name'):
                                                    img(src=f'/images/world_wonders/{get_loc(en_US_locs_data, wonder[1], en_US_locs_data)}.webp', style="vertical-align: middle; width:5em", onerror=f"this.onerror=null; this.src='/images/civVI.webp';")
                                                br()
                                                p(get_loc(locs_data, wonder[2], en_US_locs_data), style="text-align:left", cls='civ-ability-desc')
                                                br()
        add_final_scripts()
        add_scroll_up()

    docStr = str(doc)
    return refactorCivSpecialSyntax(bbg_version, lang, docStr)