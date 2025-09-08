from dominate.svg import *
from dominate.tags import *

from parseBBGFiles import *

from dom_generator_helper import *


def get_policy_html_file(bbg_version, lang, pages_list):
    en_US_locs_data = get_locs_data(bbg_version, "en_US")
    locs_data = get_locs_data_with_fallback(bbg_version, lang)
    if bbg_version == None and lang not in base_game_locs_data:
        base_game_locs_data[lang] = locs_data
    version_name = bbg_version if bbg_version != None else "baseGame"
    title = f'Civ VI {f"BBG {bbg_version}" if bbg_version != None else get_loc(locs_data, "LOC_BASE_GAME_TITLE")} {get_loc(locs_data, "LOC_PEDIA_CONCEPTS_PAGE_GOVT_2_CHAPTER_CONTENT_TITLE")}'
    civic_to_loc = get_civic_to_loc_dict(
        f"sqlFiles/{version_name}/DebugGameplay.sqlite"
    )

    menu_items = []
    menu_icons = []
    age_name = {}
    policies = get_policies(f"sqlFiles/{version_name}/DebugGameplay.sqlite")
    for policy_type in policies:
        # damn firaxis typos
        policy_page_str = "POLICES" if policy_type == "ECONOMIC" else "POLICIES"
        age_name[policy_type] = get_loc(
            locs_data,
            f"LOC_PEDIA_GOVERNMENTS_PAGEGROUP_{policy_type}_{policy_page_str}_NAME",
        )
        menu_items.append(age_name[policy_type])
        menu_icons.append(f"{policy_type}_CARD")

    def create_policy_page():
        for policy_type in policies:
            with div(cls="col-lg-12", id=age_name[policy_type]), div(cls="chart"):
                comment(policy_type)
                h2(age_name[policy_type], cls="civ-name")
            with div(cls="row"):
                for policy_name in policies[policy_type]:
                    policy = policies[policy_type][policy_name]
                    with div(cls="col-lg-6 col-md-12"), div(cls="chart"):
                        comment(policy_name)
                        with h2(get_loc(locs_data, policy[2]), cls="civ-name"):
                            img(
                                src=f"/images/policies/{policy_type}_CARD.webp",
                                style="vertical-align: middle; width:2em",
                                onerror=image_onerror,
                            )
                        p(
                            get_loc(locs_data, policy[1]),
                            style="display:inline-block;text-align:left",
                            cls="civ-ability-desc",
                        )
                        br()
                        if policy[0]:
                            p(
                                get_loc(locs_data, "LOC_UI_PEDIA_UNLOCKED_BY")
                                + " "
                                + get_unlock_tech_civic_dialog(
                                    None,
                                    policy[0],
                                    locs_data,
                                    en_US_locs_data,
                                    None,
                                    civic_to_loc,
                                ),
                                style="display:inline-block;text-align:left",
                                cls="civ-ability-desc",
                            )
                        if policy[3]:
                            br()
                            obsolete_civics = []
                            for obsolete_policy in policy[3]:
                                # unfortunately due to the design, we need to find
                                # the obsolete policies by searching every card type
                                # since craftsmen card etc is obsoleted by
                                # different type
                                for policy_type2 in policies:
                                    if obsolete_policy not in policies[policy_type2]:
                                        continue
                                    obsolete_civics.append(
                                        policies[policy_type2][obsolete_policy][0]
                                    )
                                    break
                            p(
                                get_loc(locs_data, "LOC_UI_PEDIA_MADE_OBSOLETE_BY")
                                + " "
                                + ", ".join(
                                    [
                                        get_unlock_tech_civic_dialog(
                                            None,
                                            obsolete_civic,
                                            locs_data,
                                            en_US_locs_data,
                                            None,
                                            civic_to_loc,
                                        )
                                        for obsolete_civic in obsolete_civics
                                    ]
                                ),
                                style="display:inline-block;text-align:left",
                                cls="civ-ability-desc",
                            )

    return create_page(
        bbg_version,
        lang,
        title,
        "city_states",
        menu_items,
        menu_icons,
        "images/policies",
        pages_list,
        create_policy_page,
        locs_data,
        en_US_locs_data,
    )
