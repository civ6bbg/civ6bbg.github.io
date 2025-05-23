from bs4 import BeautifulSoup
import sqlite3
import re
import numpy as np
import csv

import dominate
from dominate.tags import *

def get_locs_data(db_path, bbg_version, lang):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute(f'SELECT * FROM LocalizedText_{lang}')
    rows = crsr.fetchall()
    
    locs = dict()
    for r in rows:
        locs[r[1]] = r[2]
        
    if bbg_version == None:
        return locs
    
    # Reading BBM XML files
    with open(f'bbm_xml/{lang}.xml', 'r') as f:
        data = f.read()

    Bs_data = BeautifulSoup(data, "xml")

    b_unique = Bs_data.find_all('Replace')
    for x in b_unique:
        if hasattr(x, 'Text') and hasattr(x.Text, 'contents'):
            # print(x)
            if len(x.Text.contents) > 0:
                locs[x['Tag']] = x.Text.contents[0]
        elif hasattr(x, 'text') and hasattr(x.text, 'contents'):
            if len(x.text.contents) > 0:
                locs[x['Tag']] = x.text.contents[0]
        else:
            print(f'unsual element in xml file for BBM lang {lang}!!')
            print(x)
    
    #Reading BBG XML files
    with open(f'bbg_xml/{bbg_version}/{lang}.xml', 'r') as f:
        data = f.read()

    Bs_data = BeautifulSoup(data, "xml")

    b_unique = Bs_data.find_all('Replace')
    for x in b_unique:
        if hasattr(x, 'Text') and hasattr(x.Text, 'contents'):
            # print(x)
            if len(x.Text.contents) > 0:
                locs[x['Tag']] = x.Text.contents[0]
        elif hasattr(x, 'text') and hasattr(x.text, 'contents'):
            if len(x.text.contents) > 0:
                locs[x['Tag']] = x.text.contents[0]
        else:
            print(f'unsual element in xml file for {bbg_version} lang {lang}!!')
            print(x)
    b_unique = Bs_data.find_all('Row')
    for x in b_unique:
        if hasattr(x, 'Text') and hasattr(x.Text, 'contents'):
            # print(x)
            if len(x.Text.contents) > 0:
                locs[x['Tag']] = x.Text.contents[0]
        elif hasattr(x, 'text') and hasattr(x.text, 'contents'):
            if len(x.text.contents) > 0:
                locs[x['Tag']] = x.text.contents[0]
        else:
            print(f'unsual element in xml file for {bbg_version} lang {lang}!!')
            print(x)
    
    return locs

def get_civs_tables(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT CivilizationType, LeaderType, CivilizationName, CivilizationAbilityName, CivilizationAbilityDescription, LeaderName, LeaderAbilityName, LeaderAbilityDescription FROM Players WHERE Domain = 'Players:Expansion2_Players'")
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

def get_city_states(db_path):
    connection = sqlite3.connect(db_path)

    crsr = connection.cursor()
    crsr.execute("SELECT * FROM CityStates WHERE Domain = 'Expansion2CityStates' ORDER BY CityStateCategory, CivilizationType")
    rows = crsr.fetchall()
    
    cityStates = []
    uniques = []

    for val in rows:
        # print(val)
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
        sorted_rows = sorted(rows, key=lambda x: (governor_promotion_dict[x[1]][3], governor_promotion_dict[x[1]][4]))
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
    crsr.execute(f"SELECT * FROM GovernorPromotions")
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
    crsr.execute("SELECT BuildingType,Name,Description FROM Buildings WHERE IsWonder=1 ORDER BY Cost")
    rows = crsr.fetchall()
    connection.close()
    return rows

def get_start_biases(db_path):
    writer = csv.writer()
    writer.writerow(['CivilizationType', 'BiasType', 'TerrainType', 'FeatureType', 'ResourceType', 'Tier', 'Extra', 'CustomPlacement'])

    connection = sqlite3.connect(db_path)
    crsr = connection.cursor()
    
    startBiasCustomQuery = "SELECT CivilizationType, 'Custom', Null AS TerrainType, Null AS FeatureType, Null AS ResourceType, Null AS Tier, Null AS Extra, CustomPlacement FROM StartBiasCustom"
    startBiasFeaturesQuery = "SELECT CivilizationType, 'Feature', Null AS TerrainType, FeatureType, Null AS ResourceType, Tier, Null AS Extra, Null AS CustomPlacement FROM StartBiasFeatures"
    startBiasNegativesQuery = "SELECT CivilizationType, 'Negative', TerrainType, FeatureType, ResourceType, Tier, Extra, Null AS CustomPlacement FROM StartBiasNegatives"
    startBiasResourcesQuery = "SELECT CivilizationType, 'Resources', Null AS TerrainType, Null AS FeatureType, ResourceType, Tier, Null AS Extra, Null AS CustomPlacement FROM StartBiasResources"
    startBiasRiversQuery = "SELECT CivilizationType, 'Rivers', Null AS TerrainType, Null AS FeatureType, NULL AS ResourceType, Tier, Null AS Extra, Null AS CustomPlacement FROM StartBiasRivers"
    startBiasTerrainsQuery = "SELECT CivilizationType, 'Terrains', TerrainType, Null AS FeatureType, Null AS ResourceType, Tier, Null AS Extra, Null AS CustomPlacement FROM StartBiasTerrains"
    
    crsr.execute(f'{startBiasCustomQuery} UNION {startBiasFeaturesQuery} UNION {startBiasNegativesQuery} UNION {startBiasResourcesQuery} UNION {startBiasRiversQuery} UNION {startBiasTerrainsQuery}')
    # crsr.execute(f'{startBiasCustomQuery}')s
    rows = crsr.fetchall()
    writer.writerows(rows)
    connection.close()