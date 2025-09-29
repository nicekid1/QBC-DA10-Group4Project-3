import json
import pandas as pd
import numpy as np
import mysql.connector
import os

def feet_inch_to_cm(x):
    feet = int(x[0])
    inch = int(x[2:])
    return round(feet * 30.48 + inch * 2.54)


player_id_regex = r'/./(.*)\.html'

# Getting the users data from database_init.json (add it to .gitignore)
with open('database_init.json') as file:
    db_config = json.load(file)

# Dataframe containing all the top players in each season
lst = []
for i in {2019, 2020, 2021, 2022, 2023, 2024, 2025}:
    path = os.path.join('top 50 player of mjt list', f'nba_top50_players_{i}.csv')
    tmp = pd.read_csv(path)
    tmp['Season'] = i
    lst.append(tmp)
players = pd.concat(lst, axis=0, ignore_index=True)
# Cleaning some data.
players['player_id'] = players['Player_Link'].str.extract(player_id_regex)
players.drop(columns='Player_Link', inplace=True)
players['MVP ranking'] = players['Awards'].str.extract(r'MVP-([0-9]*)').astype('Int64')

# Dataframe for players in MVP Award ranking
mvp_players = pd.read_csv(os.path.join('data', 'mvp_players.csv'))
mvp_players['id'] = mvp_players['id'].str.extract(player_id_regex)
mvp_players['rank'] = mvp_players['rank'].str.replace(r'[a-zA-Z]', '', regex=True).astype('Int64')

# Dataframe for all the top players
top_players = players[['player_id', 'Rk', 'Age', 'Team', 'Pos', 'PTS', 'Season']].copy()

# Dataframe for the players details
players_list = pd.read_csv(os.path.join('data', 'all_players.csv'))
players_list['player'] = players_list['player'].str.replace('*', '')
players_list['id'] = players_list['id'].str.extract(player_id_regex)
players_list['height'] = players_list['height'].map(feet_inch_to_cm)
players_list['birth_date'] = pd.to_datetime(players_list['birth_date'])
players_list['birth_date'] = players_list['birth_date'].dt.year.astype('Int64')
players_list['weight'] = np.floor(players_list['weight'] * 0.45359237 ).astype('Int64')# from lbs to kg


# Dataframe for champion teams.
file_names = os.listdir('champ team')
lst = []
for file in file_names:
    if file[-2:] != "py":   # escaping python files
        path = os.path.join('champ team', file)
        tmp = pd.read_csv(path)
        lst.append(tmp)

winners = pd.concat(lst, axis=0, ignore_index=True)
winners['player_id'] = winners['player_link'].str.extract(r'/./(.*)\.html')
winners['Exp'] = winners['Exp'].str.replace('R', '0').astype('Int64')

# Dataframe for Team details
teams_list = pd.read_csv(os.path.join('team stat', 'nba_teams.csv'))



db_name = "NBA_DB"
try:

    temp_config = db_config.copy()
    cnxn = mysql.connector.connect(**temp_config)
    cursor = cnxn.cursor()

    # first remove the old data
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")

    # creating NBA_DB if it is not already exists.
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} COLLATE utf8mb4_unicode_ci")
    print(f"Database '{db_name}' created or already exists.")
    cnxn.database = db_name
#######################################################################################################################
    # Adding Awards table to the database
    tbl_name = "AWARDS"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tbl_name} ("
                   f"player_id VARCHAR(255) NOT NULL,"
                   f"Ranking INT NOT NULL,"
                   f"SEASON INT NOT NULL);")
    print(f"Table '{tbl_name}' created or already exists.")
    # Insert Dataframe into SQL Server:
    for index, row in mvp_players.iterrows():
        # print(f"inserting player {row['player_id']} year {row['Season']}")
        query = f"INSERT INTO {tbl_name} (player_id, Ranking, SEASON) VALUES (%s, %s, %s)"
        cursor.execute(query, (row['id'], row['rank'], row['year']))
#######################################################################################################################
    # Adding Top players table
    tbl_name = "TOP_PLAYERS"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tbl_name} ("
                   f"player_id VARCHAR(255) NOT NULL,"
                   f"Rk INT NOT NULL,"
                   f"AGE INT NOT NULL,"
                   f"team_id VARCHAR(20) NOT NULL,"
                   f"POS VARCHAR(20) NOT NULL,"
                   f"PTS INT NOT NULL,"
                   f"SEASON INT NOT NULL);")
    print(f"Table '{tbl_name}' created or already exists.")
    # Insert Dataframe into SQL Server:
    for index, row in top_players.iterrows():
        query = f"INSERT INTO {tbl_name} (player_id, Rk, AGE, team_id, POS, PTS, SEASON) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query,(
            row['player_id'],
            row['Rk'],
            row['Age'],
            row['Team'],
            row['Pos'],
            row['PTS'],
            row['Season']))
#######################################################################################################################
    # Adding players information
    tbl_name = "PLAYERS_DETAIL"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tbl_name} ("
                   f"player_id VARCHAR(255) NOT NULL PRIMARY KEY,"
                   f"FULL_NAME VARCHAR(255) NOT NULL,"
                   f"POS VARCHAR(31) NOT NULL,"
                   f"YEAR_MIN INT NOT NULL,"
                   f"YEAR_MAX INT NOT NULL,"
                   f"HEIGHT INT,"
                   f"WEIGHT INT,"
                   f"BIRTH_YEAR INT,"
                   f"COLLEGE VARCHAR(255),"
                   f"ACTIVE BOOLEAN NOT NULL);")
    print(f"Table '{tbl_name}' created or already exists.")
    # Insert Dataframe into SQL Server:
    for index, row in players_list.iterrows():
        query = f"INSERT INTO {tbl_name} (player_id, FULL_NAME, POS, YEAR_MIN, YEAR_MAX,  HEIGHT, WEIGHT, BIRTH_YEAR, COLLEGE, ACTIVE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (
            row['id'],
            row['player'],
            row['pos'],
            row['year_min'],
            row['year_max'],
            row['height'],
            row['weight'] if pd.notna(row['weight']) else None,
            row['birth_date'] if pd.notna(row['birth_date']) else None,
            row['colleges'] if pd.notna(row['colleges']) else None,
            row['is_active']))
    #######################################################################################################################
    # Adding Winner team for each year.
    tbl_name = "WINNER_TEAMS"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tbl_name} ("
                   f"team_id VARCHAR(20) NOT NULL,"
                   f"player_id VARCHAR(255) NOT NULL,"
                   f"POS VARCHAR(20) NOT NULL,"
                   f"EXPERIENCE INT,"
                   f"YEAR INT NOT NULL);")
    print(f"Table '{tbl_name}' created or already exists.")
    # Insert Dataframe into SQL Server:
    for index, row in winners.iterrows():
        query = f"INSERT INTO {tbl_name} (team_id, player_id, POS, EXPERIENCE, YEAR) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (
            row['team_id'],
            row['player_id'],
            row['Pos'],
            row['Exp'],
            row['year']))
    #######################################################################################################################
    # Adding Teams Informations
    tbl_name = "TEAMS_DETAILS"
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tbl_name} ("
                   f"id VARCHAR(20) NOT NULL PRIMARY KEY,"
                   f"NAME VARCHAR(255) NOT NULL,"
                   f"LOCATION VARCHAR(255) NOT NULL);")
    print(f"Table '{tbl_name}' created or already exists.")
    # Insert Dataframe into SQL Server:
    for index, row in teams_list.iterrows():
        query = f"INSERT INTO {tbl_name} (id, NAME, LOCATION) VALUES (%s, %s, %s)"
        cursor.execute(query,(
            row['id'],
            row['Team'],
            row['Location']))
    print('All is fine Committing')
    cnxn.commit()

except mysql.connector.Error as err:
    print(f"Error!!: {err}")
finally:
    if 'cnxn' in locals() and cnxn.is_connected():
        cursor.close()
        cnxn.close()
        print("Connection Closed.")