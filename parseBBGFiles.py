from bs4 import BeautifulSoup
import sqlite3
import numpy as np
import csv


def get_locs_data(bbg_version, lang):
    db_path = "sqlFiles/CivVILocalization.sqlite"
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute(f"SELECT * FROM LocalizedText_{lang}")
    rows = crsr.fetchall()

    locs = dict()
    for r in rows:
        locs[r[1]] = r[2]

    if bbg_version == None:
        return locs

    # Reading BBM XML files
    with open(f"bbm_xml/{lang}.xml", "r") as f:
        data = f.read()

    Bs_data = BeautifulSoup(data, "xml")

    b_unique = Bs_data.find_all("Replace")
    for x in b_unique:
        if hasattr(x, "Text") and hasattr(x.Text, "contents"):
            if len(x.Text.contents) > 0:
                locs[x["Tag"]] = x.Text.contents[0]
        elif hasattr(x, "text") and hasattr(x.text, "contents"):
            if len(x.text.contents) > 0:
                locs[x["Tag"]] = x.text.contents[0]
        else:
            print(f"unsual element in xml file for BBM lang {lang}!!")
            print(x)

    # Reading BBG XML files
    with open(f"bbg_xml/{bbg_version}/{lang}.xml", "r") as f:
        data = f.read()

    Bs_data = BeautifulSoup(data, "xml")

    b_unique = Bs_data.find_all("Replace")
    for x in b_unique:
        if hasattr(x, "Text") and hasattr(x.Text, "contents"):
            if len(x.Text.contents) > 0:
                locs[x["Tag"]] = x.Text.contents[0]
        elif hasattr(x, "text") and hasattr(x.text, "contents"):
            if len(x.text.contents) > 0:
                locs[x["Tag"]] = x.text.contents[0]
        else:
            print(f"unsual element in xml file for {bbg_version} lang {lang}!!")
            print(x)
    b_unique = Bs_data.find_all("Row")
    for x in b_unique:
        if hasattr(x, "Text") and hasattr(x.Text, "contents"):
            if len(x.Text.contents) > 0:
                locs[x["Tag"]] = x.Text.contents[0]
        elif hasattr(x, "text") and hasattr(x.text, "contents"):
            if len(x.text.contents) > 0:
                locs[x["Tag"]] = x.text.contents[0]
        else:
            print(f"unsual element in xml file for {bbg_version} lang {lang}!!")
            print(x)

    return locs


def get_civs_tables(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute(
        """SELECT CivilizationType, LeaderType, CivilizationName, CivilizationAbilityName, CivilizationAbilityDescription, LeaderName, LeaderAbilityName, LeaderAbilityDescription
         FROM Players WHERE Domain = 'Players:Expansion2_Players'"""
    )
    rows = crsr.fetchall()

    rows = sorted(rows)
    civLeaders = []
    civLeaderItems = dict()
    uniques = []

    for val in rows:
        if val[0] + val[1] not in uniques:
            civLeaders.append(val)
            uniques.append(val[0] + val[1])

    for row in civLeaders:
        crsr.execute(f"SELECT * FROM PlayerItems WHERE CivilizationType = '{row[0]}' AND LeaderType = '{row[1]}' AND Domain = 'Players:Expansion2_Players'")
        items = crsr.fetchall()
        unique_items = []
        unique_items_names = []
        for val in items:
            if val[3] not in unique_items_names:
                unique_items.append(val)
                unique_items_names.append(val[3])
        civLeaderItems[row] = unique_items

    connection.close()
    return civLeaderItems


def get_units_dict(db_path):
    res = {}
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT * FROM Units")
    rows = crsr.fetchall()
    for r in rows:
        res[r[0]] = r
    connection.close()
    return res


def get_tech_to_loc_dict(db_path):
    res = {}
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT * FROM Technologies")
    rows = crsr.fetchall()
    for r in rows:
        res[r[0]] = r[1]
    connection.close()
    return res


def get_civic_to_loc_dict(db_path):
    res = {}
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT * FROM Civics")
    rows = crsr.fetchall()
    for r in rows:
        res[r[0]] = r[1]
    connection.close()
    return res


def get_city_states(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT * FROM CityStates WHERE Domain = 'Expansion2CityStates' ORDER BY CityStateCategory, CivilizationType")
    rows = crsr.fetchall()

    cityStates = []
    uniques = []

    for val in rows:
        if val[0] + val[1] not in uniques:
            cityStates.append(val)
            uniques.append(val[0] + val[1])

    connection.close()
    return cityStates


def get_beliefs(db_path, belief_type):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute(f"SELECT * FROM Beliefs WHERE BeliefClassType = '{belief_type}'")
    rows = crsr.fetchall()
    connection.close()
    return rows


def get_governors_list(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT GovernorType, Name, Description, Title, ShortTitle, TransitionStrength, AssignCityState FROM Governors")
    rows = crsr.fetchall()
    connection.close()
    return rows


def get_governors_promotion_sets_dict(db_path, governor_list, governor_promotion_dict):
    res = {}
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    for gov in governor_list:
        crsr.execute(f"SELECT * FROM GovernorPromotionSets WHERE GovernorType='{gov[0]}'")
        rows = crsr.fetchall()
        sorted_rows = sorted(
            rows,
            key=lambda x: (
                governor_promotion_dict[x[1]][3],
                governor_promotion_dict[x[1]][4],
            ),
        )
        sorted_rows = [governor_promotion_dict[i[1]] for i in sorted_rows]
        res[gov[0]] = {}
        for i in np.arange(4):
            res[gov[0]][i] = {}
        for item in sorted_rows:
            res[gov[0]][item[3]][item[4]] = item
    connection.close()
    return res


def get_governors_promotion_dict(db_path):
    res = {}
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT * FROM GovernorPromotions")
    rows = crsr.fetchall()
    promotion_to_row = {}
    for r in rows:
        promotion_to_row[r[0]] = r
    connection.close()
    return promotion_to_row


def get_natural_wonders_list(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT FeatureType, Name, Description FROM NaturalWonders WHERE Domain = 'Expansion2NaturalWonders'")
    rows = crsr.fetchall()
    connection.close()
    return rows


def get_world_wonders_list(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT BuildingType,Name,Description,Cost,PrereqTech,PrereqCivic FROM Buildings WHERE IsWonder=1 ORDER BY Name")
    wonder_rows = crsr.fetchall()
    crsr.execute("SELECT TechnologyType, EraType FROM Technologies")
    tech_rows = crsr.fetchall()
    tech_to_era_dict = {}
    for tech in tech_rows:
        tech_to_era_dict[tech[0]] = tech[1]
    crsr.execute("SELECT CivicType, EraType FROM Civics")
    civic_rows = crsr.fetchall()
    civic_to_era_dict = {}
    for civic in civic_rows:
        civic_to_era_dict[civic[0]] = civic[1]

    eras = [
        "ERA_ANCIENT",
        "ERA_CLASSICAL",
        "ERA_MEDIEVAL",
        "ERA_RENAISSANCE",
        "ERA_INDUSTRIAL",
        "ERA_MODERN",
        "ERA_ATOMIC",
    ]
    era_to_loc = lambda x: f"LOC_{x}_NAME"
    result = {era_to_loc(era): [] for era in eras}

    for wonder in wonder_rows:
        wonder_tech = wonder[4]
        wonder_civic = wonder[5]
        if wonder_tech is not None:
            result[era_to_loc(tech_to_era_dict[wonder_tech])].append(wonder)
        elif wonder_civic is not None:
            result[era_to_loc(civic_to_era_dict[wonder_civic])].append(wonder)
        else:
            print(f"Wonder {wonder[0]} has no tech or civic prerequisites!")
    connection.close()
    return result


def get_dark_age_card_list(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT * FROM Policies WHERE PrereqCivic is NULL AND RequiresGovernmentUnlock is NULL")
    rows = crsr.fetchall()
    connection.close()
    return rows


def get_eras_name_dict(eras, db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT EraType, Name FROM Eras")
    rows = crsr.fetchall()
    connection.close()

    eras_translation = {}
    for row in rows:
        if row[0] in eras:
            eras_translation[row[0]] = row[1]

    return eras_translation


def get_dark_age_card_list_eras(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT * FROM Policies_XP1")
    rows = crsr.fetchall()
    connection.close()

    eras = [
        "ERA_CLASSICAL",
        "ERA_MEDIEVAL",
        "ERA_RENAISSANCE",
        "ERA_INDUSTRIAL",
        "ERA_MODERN",
        "ERA_ATOMIC",
        "ERA_INFORMATION",
        "ERA_FUTURE",
    ]
    card_to_era_dict = {}
    for i in range(len(rows)):
        start = False
        end = False
        for j in range(len(eras)):
            if rows[i][1] == eras[j]:
                start = True
                card_to_era_dict[rows[i][0]] = []
            if start and not end:
                card_to_era_dict[rows[i][0]].append(eras[j])
            if rows[i][2] == eras[j]:
                end = True
                break
    return card_to_era_dict


def get_dark_age_card_list_per_era(dark_age_policy, dark_age_policy_era):
    eras = [
        "ERA_CLASSICAL",
        "ERA_MEDIEVAL",
        "ERA_RENAISSANCE",
        "ERA_INDUSTRIAL",
        "ERA_MODERN",
        "ERA_ATOMIC",
        "ERA_INFORMATION",
        "ERA_FUTURE",
    ]
    era_to_card_dict = {era: [] for era in eras}
    for card in dark_age_policy:
        for era in dark_age_policy_era[card[0]]:
            era_to_card_dict[era].append(card)
    return era_to_card_dict


def get_dedication_list_per_era(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT * FROM CommemorationTypes")
    rows = crsr.fetchall()
    connection.close()

    eras = [
        "ERA_CLASSICAL",
        "ERA_MEDIEVAL",
        "ERA_RENAISSANCE",
        "ERA_INDUSTRIAL",
        "ERA_MODERN",
        "ERA_ATOMIC",
        "ERA_INFORMATION",
        "ERA_FUTURE",
    ]
    eras_name = get_eras_name_dict(eras, db_path)

    era_to_dedication_dict = {era: [] for era in eras_name.values()}
    for i in range(len(rows)):
        start = rows[i][5]
        end = rows[i][6]
        after_start = False
        for j in range(len(eras)):
            if start == eras[j]:
                after_start = True
            if after_start:
                era_to_dedication_dict[eras_name[eras[j]]].append(rows[i])
            if end == eras[j]:
                break

    return era_to_dedication_dict


def get_start_biases(db_path):
    writer = csv.writer()
    writer.writerow(
        [
            "CivilizationType",
            "BiasType",
            "TerrainType",
            "FeatureType",
            "ResourceType",
            "Tier",
            "Extra",
            "CustomPlacement",
        ]
    )

    connection = sqlite3.connect(db_path)
    crsr = connection.cursor()

    startBiasCustomQuery = "SELECT CivilizationType, 'Custom', Null AS TerrainType, Null AS FeatureType, Null AS ResourceType, Null AS Tier, Null AS Extra, CustomPlacement FROM StartBiasCustom"
    startBiasFeaturesQuery = "SELECT CivilizationType, 'Feature', Null AS TerrainType, FeatureType, Null AS ResourceType, Tier, Null AS Extra, Null AS CustomPlacement FROM StartBiasFeatures"
    startBiasNegativesQuery = "SELECT CivilizationType, 'Negative', TerrainType, FeatureType, ResourceType, Tier, Extra, Null AS CustomPlacement FROM StartBiasNegatives"
    startBiasResourcesQuery = "SELECT CivilizationType, 'Resources', Null AS TerrainType, Null AS FeatureType, ResourceType, Tier, Null AS Extra, Null AS CustomPlacement FROM StartBiasResources"
    startBiasRiversQuery = "SELECT CivilizationType, 'Rivers', Null AS TerrainType, Null AS FeatureType, NULL AS ResourceType, Tier, Null AS Extra, Null AS CustomPlacement FROM StartBiasRivers"
    startBiasTerrainsQuery = "SELECT CivilizationType, 'Terrains', TerrainType, Null AS FeatureType, Null AS ResourceType, Tier, Null AS Extra, Null AS CustomPlacement FROM StartBiasTerrains"

    crsr.execute(
        f"{startBiasCustomQuery} UNION {startBiasFeaturesQuery} UNION {startBiasNegativesQuery} UNION {startBiasResourcesQuery} UNION {startBiasRiversQuery} UNION {startBiasTerrainsQuery}"
    )
    rows = crsr.fetchall()
    writer.writerows(rows)
    connection.close()


def get_property_names(db_path, property_type, name_db):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute(
        f"SELECT * FROM Named{property_type}Civilizations ORDER BY Named{property_type}Type"
    )
    rows = crsr.fetchall()
    crsr.execute(f"SELECT * FROM Named{name_db}")
    property_names = crsr.fetchall()
    property_to_loc_dict = {}
    property_dict = {}
    for name in property_names:
        property_to_loc_dict[name[0]] = name[1]
        property_dict[name[1]] = []

    crsr.execute("SELECT * FROM Civilizations")
    civ_names = crsr.fetchall()
    civ_to_loc_dict = {}
    for name in civ_names:
        civ_to_loc_dict[name[0]] = name[1]

    for val in rows:
        property_dict[property_to_loc_dict[val[0]]].append(civ_to_loc_dict[val[1]])

    connection.close()
    return property_dict


def get_great_people_list(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT GreatPersonIndividualType, Name, GreatPersonClassType, EraType, ActionCharges FROM GreatPersonIndividuals ORDER BY GreatPersonClassType, EraType, Name")
    rows = crsr.fetchall()

    crsr.execute("SELECT GreatPersonClassType, Name FROM GreatPersonClasses")
    gp_classes = crsr.fetchall()
    class_to_loc_dict = {}
    for row in gp_classes:
        class_to_loc_dict[row[0]] = row[1]

    eras = [
        "ERA_ANCIENT",
        "ERA_CLASSICAL",
        "ERA_MEDIEVAL",
        "ERA_RENAISSANCE",
        "ERA_INDUSTRIAL",
        "ERA_MODERN",
        "ERA_ATOMIC",
        "ERA_INFORMATION",
        "ERA_FUTURE",
    ]
    eras_name = get_eras_name_dict(eras, db_path)

    great_people_dict = {}
    for row in rows:
        gp_type_loc = class_to_loc_dict[row[2]]

        if gp_type_loc not in great_people_dict:
            great_people_dict[gp_type_loc] = {}
        gp_era = eras_name[row[3]]
        if gp_era not in great_people_dict[gp_type_loc]:
            great_people_dict[gp_type_loc][gp_era] = []
        great_people_dict[gp_type_loc][gp_era].append(row)
    connection.close()
    return great_people_dict

def get_great_people_great_works(db_path):
    res = {}
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("""SELECT ga.GreatPersonIndividualType, gw.Name, gw.GreatWorkObjectType
	    FROM GreatPersonIndividuals ga
	    LEFT JOIN GreatWorks gw Using(GreatPersonIndividualType)
	    WHERE gw.Name Not NULL""")
    great_works = crsr.fetchall()
    for row in great_works:
        if row[0] not in res:
            res[row[0]] = []
        res[row[0]].append(row)
    return res

def get_great_people_modifier_dict(db_path):
    res = {}
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute(
        """SELECT ga.GreatPersonIndividualType, ga.ModifierId, Text, ActionEffectTextOverride, Value FROM GreatPersonIndividualActionModifiers ga 
         LEFT JOIN ModifierStrings USING(ModifierId)
         LEFT JOIN GreatPersonIndividuals USING(GreatPersonIndividualType) 
         LEFT JOIN (SELECT ModifierId, Value FROM ModifierArguments where Name='Amount') USING(ModifierId)"""
    )
    rows = crsr.fetchall()
    overridden = set()
    for gp, modifier, loc, action_override, amount in rows:
        amount = float(amount) if amount else 0
        res.setdefault(gp, [])
        if action_override:
            if action_override not in overridden:
                res[gp].append((action_override, amount))
                overridden.add(action_override)
        elif loc:
            res[gp].append((loc, amount))

    connection.close()
    return res

def get_alliance_list(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("""
      SELECT * FROM Alliances
                 """)
    rows = crsr.fetchall()
    connection.close()
    return rows

def get_alliance_effects(db_path, alliance_type):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute(f"""
      SELECT AllianceType, ga.Name, LevelRequirement, Text FROM Alliances ga
		 LEFT JOIN AllianceEffects USING(AllianceType)
         LEFT JOIN (SELECT ModifierId, Value FROM ModifierArguments where Name='Amount') USING(ModifierId)
         LEFT JOIN ModifierStrings USING(ModifierId)
         WHERE ga.AllianceType = '{alliance_type}' 
         AND Text is not NULL
         AND Context = 'Summary'
         ORDER BY LevelRequirement
                 """)
    rows = crsr.fetchall()
    res = {}
    res[1] = []
    res[2] = []
    res[3] = []
    for effect in rows:
        res[effect[2]].append((effect[3]))
    connection.close()
    return res