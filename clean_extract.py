import json
import pandas as pd
import numpy as np
import mysql.connector
import os

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
players['player_id'] = players['Player_Link'].str.extract(r'/./(.*)\.html')
players.drop(columns='Player_Link', inplace=True)
players['MVP ranking'] = players['Awards'].str.extract(r'MVP-([0-9]*)').astype('Int64')

# Dataframe for players in MVP Award ranking
mvp_players = players[['player_id', 'MVP ranking', 'Season', 'Pos']].copy()
mvp_players.dropna(inplace=True)

# Dataframe for all the top players
top_players = players[['player_id', 'Rk', 'Age', 'Team', 'Pos', 'PTS', 'Season']].copy()

# Dataframe for the players details
players_list = pd.read_csv(os.path.join('player stat', 'nba_players_stat.csv'))
players_list['id'] = players_list['link'].str.extract(r'/./(.*)\.html')
players_list['Height'] = players_list['Height_Weight'].str.extract(r'([0-9]*)cm').astype('Int64')
players_list['Weight'] = players_list['Height_Weight'].str.extract(r'([0-9]*)kg').astype('Int64')
players_list.drop(columns=['Born', 'link', 'Height_Weight'], inplace=True)
players_list.drop_duplicates(inplace=True)




db_name = "NBA_DB"
try:

    temp_config = db_config.copy()
    cnxn = mysql.connector.connect(**temp_config)
    cursor = cnxn.cursor()

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
                   f"POS VARCHAR(255) NOT NULL,"
                   f"SEASON INT NOT NULL);")
    print(f"Table '{tbl_name}' created or already exists.")
    # Insert Dataframe into SQL Server:
    for index, row in mvp_players.iterrows():
        # print(f"inserting player {row['player_id']} year {row['Season']}")
        query = f"INSERT INTO {tbl_name} (player_id, Ranking, POS, SEASON) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (row['player_id'], row['MVP ranking'], row['Pos'], row['Season']))
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
                   f"NAME VARCHAR(255) NOT NULL,"
                   f"POS VARCHAR(255) NOT NULL,"
                   f"SHOOTS VARCHAR(10) NOT NULL,"
                   f"HEIGHT INT NOT NULL,"
                   f"WEIGHT INT NOT NULL);")
    print(f"Table '{tbl_name}' created or already exists.")
    # Insert Dataframe into SQL Server:
    for index, row in players_list.iterrows():
        query = f"INSERT INTO {tbl_name} (player_id, NAME, POS, SHOOTS,  HEIGHT, WEIGHT) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query,(
            row['id'],
            row['Name'],
            row['Position'],
            row['Shoots'],
            row['Height'],
            row['Weight']))
    print('All is fine Committing')
    cnxn.commit()

except mysql.connector.Error as err:
    print(f"Error!!: {err}")
finally:
    if 'cnxn' in locals() and cnxn.is_connected():
        cursor.close()
        cnxn.close()
        print("Connection Closed.")