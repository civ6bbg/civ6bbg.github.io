from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *

def get_units_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, 'en_US')
    locs_data = get_locs_data_with_fallback(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else 'baseGame'
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else get_loc(locs_data, "LOC_BASE_GAME_TITLE")} {get_loc(locs_data, "LOC_PAGE_TITLE_UNITS")}'
    unit_classes = [
        'PROMOTION_CLASS_MELEE',
        'PROMOTION_CLASS_ANTI_CAVALRY',
        'PROMOTION_CLASS_RANGED',
        'PROMOTION_CLASS_SIEGE',
        'PROMOTION_CLASS_LIGHT_CAVALRY',
        'PROMOTION_CLASS_HEAVY_CAVALRY',
        'PROMOTION_CLASS_RECON',
        'PROMOTION_CLASS_SUPPORT',
        'PROMOTION_CLASS_NAVAL_MELEE',
        'PROMOTION_CLASS_NAVAL_RANGED',
        'PROMOTION_CLASS_NAVAL_RAIDER',
        'PROMOTION_CLASS_NAVAL_CARRIER',
        'PROMOTION_CLASS_NIHANG',
        'PROMOTION_CLASS_MONK',
        'PROMOTION_CLASS_AIR_FIGHTER',
        'PROMOTION_CLASS_AIR_BOMBER',
        'PROMOTION_CLASS_GIANT_DEATH_ROBOT',
    ]
    menu_items = []
    menu_icons = []
    for unit_cls in unit_classes:
        menu_items.append(get_loc(locs_data, f'LOC_{unit_cls}_NAME'))
        menu_icons.append(f'TYPE_{unit_cls[16:]}')

    def create_units_page():
        for promo_cls in unit_classes:
            loc_promo_cls = f'LOC_{promo_cls}_NAME'
            with div(cls='col-lg-12',
                     id=get_loc(locs_data, loc_promo_cls)
                    ), div(cls="chart"):
                comment(loc_promo_cls)
                h2(get_loc(locs_data, loc_promo_cls),
                   cls='civ-name')
            with div(cls="row"):
                for unit_type in unit_stats[promo_cls].keys():
                    process_unit_stats(unit_type, promo_cls)

    def process_unit_stats(unit_type, promo_cls):
        with div(cls="col-lg-6 col-md-12"), div(cls="chart"):
            (
                unit_name_loc, sight, movement, cs, ranged_cs, attack_range, bombard_cs, prod, desc,
                maint, strategic_type, strategic_amt, strategic_maint_type, strategic_maint_amt, antiair_cs
            ) = unit_stats[promo_cls][unit_type]
            comment(unit_name_loc)
            with h2(get_loc(locs_data, unit_name_loc),
                    cls='civ-name'):
                img(src=f'/images/units/{get_loc(en_US_locs_data, unit_name_loc).replace(' ', '_')}.webp',
                    style="vertical-align: middle; width:5em",
                    onerror=image_onerror)
            br()
            comment('LOC_UI_PEDIA_PRODUCTION_COST')
            p(f'{get_loc(locs_data, 'LOC_UI_PEDIA_PRODUCTION_COST')}: {prod// 2} [ICON_PRODUCTION]',
              style="display:inline-block;text-align:left",
              cls='civ-ability-desc')
            br()
            if strategic_amt and strategic_type:
                p(f'{max(strategic_amt // 2, 1)} [ICON_{strategic_type}]',
                  style="display:inline-block;text-align:left",
                  cls='civ-ability-desc')
                br()
            strategic_maint_text = get_loc(locs_data, 'LOC_HUD_REPORTS_PER_TURN').replace('{1_Yield}', '')
            if strategic_maint_amt:
                comment('LOC_HUD_REPORTS_PER_TURN')
                strategic_maint_text = f', {strategic_maint_amt} [ICON_{strategic_maint_type}]{strategic_maint_text}'
            # BTW yes this typo "MAITENANCE" is part of the game lol
            comment('LOC_UI_PEDIA_MAITENANCE_COST')
            p(f'{get_loc(locs_data, 'LOC_UI_PEDIA_MAITENANCE_COST')}: {maint} [ICON_GOLD]{strategic_maint_text}',
              style="display:inline-block;text-align:left",
              cls='civ-ability-desc')
            br()                
            icon_to_stats = {
                'ICON_MOVEMENT': ('LOC_UI_PEDIA_MOVEMENT_POINTS', movement),
                'ICON_STRENGTH': ('LOC_UI_PEDIA_MELEE_STRENGTH', cs),
                'ICON_RANGE': ('LOC_UI_PEDIA_RANGE', attack_range),
                'ICON_RANGED': ('LOC_UI_PEDIA_RANGED_STRENGTH', ranged_cs),
                'ICON_BOMBARD': ('LOC_UI_PEDIA_BOMBARD_STRENGTH', bombard_cs),
                'ICON_ANTIAIR_LARGE': ('LOC_UI_PEDIA_ANTIAIR_STRENGTH', antiair_cs)
            }
            for icon in icon_to_stats:
                name, val = icon_to_stats[icon]
                if val <= 0:
                    continue
                comment(name)
                p(f'{val} [{icon}] {get_loc(locs_data, name)}',
                  style="display:inline-block;text-align:left",
                  cls='civ-ability-desc')
                br()
            p(f'{sight} Sight',
              style="display:inline-block;text-align:left",
              cls='civ-ability-desc')
            br()
            comment(desc)
            p(get_loc(locs_data, desc),
              style="display:inline-block;text-align:left",
              cls='civ-ability-desc')
    unit_stats = get_unit_stats(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    return create_page(bbg_version, lang, title, 'units', menu_items, menu_icons, 'images/units', pages_list, create_units_page, locs_data, en_US_locs_data)