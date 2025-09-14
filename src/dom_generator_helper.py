from bs4 import BeautifulSoup
import sqlite3
import re
import math

import dominate
from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

image_onerror = "this.onerror=null; this.src='/images/civVI.webp';"

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
    '[ICON_HEAL_CHARGES]',
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
    '[ICON_RELIGIOUS_STRENGTH]',
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
    '[ICON_SIGHT]',
    '[ICON_SPREAD_CHARGES]',
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
    '[ICON_POWERRight]',
    'ICON_LOYALTY'
]

base_game_locs_data = {}
base_game_units_dict = get_units_dict(f"sqlFiles/baseGame/DebugGameplay.sqlite")

def refactorCivSpecialSyntax(bbg_version, lang, docStr):
    docStr = docStr.replace('[NEWLINE]', '<br>')
    
    reg = re.compile(r'\[b\](.*?)\[/b\]', re.IGNORECASE)
    docStr = reg.sub(r'<b>\1</b>', docStr)
    
    reg = re.compile(r'\[u\](.*?)\[/u\]', re.IGNORECASE)
    docStr = reg.sub(r'<u>\1</u>', docStr)
    
    reg = re.compile(r'\[i\](.*?)\[/i\]', re.IGNORECASE)
    docStr = reg.sub(r'<i>\1</i>', docStr)
    
    reg = re.compile(r'\[/t\]', re.IGNORECASE)
    docStr = reg.sub(r'&nbsp;&nbsp;&nbsp;&nbsp;', docStr)

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
    with div(cls="preloader"), div(cls="loader"):
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

def add_header(bbg_version, lang, page_type, pages_list, locs_data, en_US_locs_data):
    with nav(cls="main-nav--bg"), div(cls="main-nav"):
        with div(cls="header"), div(cls="header-inner"), div(cls="inner"):
            with div(cls="row"):
                with div(cls="flex center sidebar-toggle col-xl-1 col-lg-1 col-md-1 col-1"):
                    with button(cls="transparent-btn", title="Menu", type="button"):
                        span("Toggle menu", cls="sr-only")
                        span(cls="icon menu-toggle", aria_hidden="true")
                with div(cls="flex center col-xl-1 col-lg-1 col-md-1 col-2"):
                    with a(href="/index.html", style="align-content: center;"):
                        img(src="/images/BBGLogo.webp", style="width:3em; border-radius:10%", alt="#")
                    div(cls="mobile-nav")
                with div(cls="flex col-xl-8 col-lg-8 col-md-8 col-8"), div(cls="main-menu"), nav(cls="navigation"):
                    with ul(cls="nav menu"):
                        for page in pages_list:
                            page_name = get_loc(locs_data, page['main_menu_title'])
                            t = page['name']
                            with li(cls="active" if t == page_type else ""):
                                a(page_name, href=f"/{lang}/{t}_{get_version_name(bbg_version)}.html", onclick=f'civClicked(null)')
                        with li():
                            with a('BBG Version'):
                                i(cls="icofont-rounded-down")
                            with ul(cls="dropdown bbg-version-dropdown"):
                                for v in bbg_versions:
                                    with li():
                                        a(f"Base" if v is None else f"{v}", href=f"/{lang}/{page_type}_{'base_game' if v is None else v}.html")
                with div(cls="flex center col-xl-2 col-lg-2 col-md-2 col-1"), div(cls='flex row justify-content-around'):
                    with div(cls="col-xl-4 col-lg-4 col-md-6 col-4"), div(cls="main-menu"), nav(cls="navigation"):
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
                    with div(cls="col-xl-4 col-lg-4 col-md-4 col-4"), div(cls="base-game-switcher-wrapper"):
                        with button(cls="base-game-switcher gray-circle-btn", type="button", title=get_loc(locs_data, "LOC_MAIN_MENU_SHOW_BASE_GAME")):
                            i(cls="enable-icon", data_feather="toggle-left", aria_hidden="true")
                            i(cls="disable-icon", data_feather="toggle-right", aria_hidden="true")
                    div(cls="w-100")
                    with div(cls="col-xl-4 col-lg-4 col-md-6 col-4"), div(cls="theme-switcher-wrapper"):
                        with button(cls="theme-switcher gray-circle-btn", type="button", title="Switch theme"):
                            span("Switch theme", cls="sr-only")
                            i(cls="sun-icon", data_feather="sun", aria_hidden="true")
                            i(cls="moon-icon", data_feather="moon", aria_hidden="true")
    add_footer()

def add_sidebar(menu_items, menu_icons, images_dir):
    with aside(cls="sidebar"), div(cls="sidebar-start"), div(cls="sidebar-body"), ul(cls="sidebar-body-menu"):
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

def get_loc(locs_data, s):
    try:
        res = locs_data[s]
        if res.find('|') == -1:
            return res
        else:
            return res[:res.find('|')]
    except KeyError:
        print(f'KeyError: {s} not found in locs_data')
        return f'Not found: {s}'

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
        script(_async=True, src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9556735523664127", crossorigin="anonymous")

def show_element_with_base_option(element, lang, locs_data, en_US_locs_data, data_append = '', base_game_data_append = '', alignment = 'left', add_base_game = True):
    if add_base_game:
        comment(element)
        p(get_loc(locs_data, element) + f'{data_append}', style=f"text-align:{alignment}", cls='civ-ability-desc actual-text')
        with div(cls="base-game-text row"):
            with div(cls='col-lg-6 col-md-6'):
                with div(cls="chart", style="box-shadow:none"):
                    p(get_loc(locs_data, element) + f'{data_append}', style=f"text-align:{alignment}", cls='civ-ability-desc')
            with div(cls='col-lg-6 col-md-6'):
                with div(cls="chart", style="box-shadow:none"):
                    p(get_loc(base_game_locs_data[lang], element) + f'\n{base_game_data_append}', style=f"text-align:{alignment}", cls='civ-ability-desc')
    else:
        comment(element)
        p(get_loc(locs_data, element) + f'{data_append}', style=f"text-align:{alignment}", cls='civ-ability-desc')

def get_unlock_tech_civic_dialog(unlock_tech, unlock_civic, locs_data, en_US_locs_data, tech_to_loc_dict, civic_to_loc_dict, include_tech_civic_word = True):
    if unlock_tech:
        return f'{get_loc(locs_data, tech_to_loc_dict[unlock_tech])}{f' {get_loc(locs_data, "LOC_TECHNOLOGY_NAME")}' if include_tech_civic_word else ""}'
    if unlock_civic:
        return f'{get_loc(locs_data, civic_to_loc_dict[unlock_civic])}{f' {get_loc(locs_data, "LOC_CIVIC_NAME")}' if include_tech_civic_word else ""}'

def add_footer():
    with div(cls="scroll-up footer-popup", id="footer-popup"), div(cls="footer-popup-inner"):
        with div(cls="row"):
            with div(cls="col-sm-8 col-1 footer-popup-body"):
                p("If you like this project, any donation would be extremely helpful for me in maintaining the website.", id="donateText")
            with div(cls="col-sm-2 col-6 footer-popup-donate"):
                a("Donate", href="https://ko-fi.com/calcalciffer", target="_blank", cls="btn btn-primary")
            with div(cls="col-sm-2 col-6 footer-popup-scroll-up"):
                with a(id="scrollUp", cls="displayNone", href="#top", onclick=f'civClicked(null)'):
                    i(cls='fa-solid fa-up-long')

def create_page(bbg_version, lang, title, header, menu_items, menu_icons, images_dir, pages_list, page_content_func, locs_data, en_US_locs_data, *args, **kwargs):
    doc = dominate.document(title=None, lang=get_html_lang(lang))
    add_html_header(doc, title)

    with doc:
        add_preloader()
        div(cls="layer")
        with div(cls="page-flex"), div(cls="main-wrapper"):
            add_header(bbg_version, lang, header, pages_list, locs_data, en_US_locs_data)
            with div(cls=""):
                with div(cls="fixed left-0 right-auto h-screen bg-white border-r border-neutral-300 overflow-scroll", style="z-index: 5;"):
                    add_sidebar(menu_items, menu_icons, images_dir)
                with div(cls="leaders-data min-w-full main-pl"), main(cls="main users chart-page"), div(cls="container"):
                    h1(title, cls='civ-name')
                    br()
                    page_content_func(*args, **kwargs)
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