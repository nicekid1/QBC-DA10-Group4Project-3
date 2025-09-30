import pandas as pd
import mysql.connector
import json
import os

absolute_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(absolute_path, 'data')

def query_to_pd(query, columns):
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    return df.reset_index(drop=True)


with open(os.path.join(absolute_path, 'database_init.json')) as file:
    db_config = json.load(file)
db_name = "NBA_DB"

try:
    temp_config = db_config.copy()
    cnxn = mysql.connector.connect(**temp_config)
    cnxn.database = db_name
    cursor = cnxn.cursor()
    query = """
            SELECT PLAYERS_DETAIL.FULL_NAME,
                   PLAYERS_DETAIL.HEIGHT
            FROM AWARDS
                     JOIN PLAYERS_DETAIL ON AWARDS.player_id = PLAYERS_DETAIL.player_id
            WHERE AWARDS.SEASON IN (2019, 2020, 2021, 2022, 2023, 2024);
            """
    query_to_pd(query, ['full_name', 'height']).to_csv(os.path.join(data_path, 'csv1_1.csv'), index=False)
    query = """
            SELECT FULL_NAME,
                   HEIGHT,
                   SEASON
            FROM TOP_PLAYERS
                     JOIN PLAYERS_DETAIL ON TOP_PLAYERS.player_id = PLAYERS_DETAIL.player_id
            WHERE TOP_PLAYERS.season IN (2019, 2020, 2021, 2022, 2023, 2024)
            GROUP BY FULL_NAME, HEIGHT, SEASON;
            """
    query_to_pd(query, ['full_name', 'height', 'season']).to_csv(os.path.join(data_path, 'csv1_2.csv'), index=False)
    query = """
            SELECT FULL_NAME,
                HEIGHT,
                EXPERIENCE,
                SEASON
            FROM WINNER_TEAMS
                    JOIN PLAYERS_DETAIL ON WINNER_TEAMS.player_id = PLAYERS_DETAIL.player_id
            WHERE WINNER_TEAMS.SEASON IN (2023, 2024)
            GROUP BY FULL_NAME, HEIGHT, EXPERIENCE, SEASON;
            """
    query_to_pd(query, ['full_name', 'height', 'experience', 'season']).to_csv(os.path.join(data_path, 'csv2_1.csv'), index=False)
    query = """
            SELECT FULL_NAME,
                HEIGHT,
                (SEASON - YEAR_MIN) AS EXPERIENCE,
                SEASON
            FROM TOP_PLAYERS
                    JOIN PLAYERS_DETAIL ON TOP_PLAYERS.player_id = PLAYERS_DETAIL.player_id
            WHERE TOP_PLAYERS.SEASON IN (2023, 2024)
            AND TOP_PLAYERS.Rk <= 15
            GROUP BY FULL_NAME, HEIGHT, (SEASON - YEAR_MIN), SEASON;
            """
    query_to_pd(query, ['full_name', 'height', 'experience', 'season']).to_csv(os.path.join(data_path, 'csv2_2.csv'), index=False)
    query = """
            WITH MVP_PG AS (SELECT DISTINCTROW PLAYERS_DETAIL.FULL_NAME, TOP_PLAYERS.POS,
                                   AWARDS.SEASON
                            FROM AWARDS
                                     JOIN PLAYERS_DETAIL
                                          ON AWARDS.player_id = PLAYERS_DETAIL.player_id
                                     JOIN TOP_PLAYERS
                                          ON TOP_PLAYERS.player_id = AWARDS.player_id
                            WHERE AWARDS.SEASON IN (2019, 2020, 2021, 2022, 2023, 2024)
                              AND TOP_PLAYERS.POS = 'PG'
                            ORDER BY AWARDS.SEASON)
            SELECT FULL_NAME,
                   POS,
                   count(*) AS NOMINATED
            FROM MVP_PG
            GROUP BY FULL_NAME, POS
            ORDER BY NOMINATED DESC, FULL_NAME LIMIT 3;
            """
    query_to_pd(query, ['full_name', 'position', 'number_of_nomination']).to_csv(os.path.join(data_path, 'csv3.csv'), index=False)
    query = """
            WITH TOP_AGILITY
                     AS (SELECT DISTINCTROW PLAYERS_DETAIL.FULL_NAME, (PLAYERS_DETAIL.HEIGHT / PLAYERS_DETAIL.WEIGHT) AS AGILITY,
                                TOP_PLAYERS.SEASON
                         FROM TOP_PLAYERS
                                  JOIN PLAYERS_DETAIL
                                       ON TOP_PLAYERS.player_id = PLAYERS_DETAIL.player_id
                         WHERE TOP_PLAYERS.Rk <= 20
                           AND SEASON IN (2023, 2024))
            SELECT FULL_NAME,
                   AGILITY
            FROM TOP_AGILITY;
            """
    query_to_pd(query, ['full_name', 'agility']).to_csv(os.path.join(data_path, 'csv_h1_1.csv'), index=False)
    query = """
            WITH TOP_AGILITY
                     AS (SELECT DISTINCTROW PLAYERS_DETAIL.FULL_NAME, (PLAYERS_DETAIL.HEIGHT / PLAYERS_DETAIL.WEIGHT) AS AGILITY,
                                TOP_PLAYERS.SEASON
                         FROM TOP_PLAYERS
                                  JOIN PLAYERS_DETAIL
                                       ON TOP_PLAYERS.player_id = PLAYERS_DETAIL.player_id
                         WHERE TOP_PLAYERS.Rk <= 20
                           AND SEASON IN (2021, 2022))
            SELECT FULL_NAME,
                   AGILITY
            FROM TOP_AGILITY; \
            """
    query_to_pd(query, ['full_name', 'agility']).to_csv(os.path.join(data_path, 'csv_h1_2.csv'), index=False)
    query = """
            WITH WINNERS AS (SELECT DISTINCTROW PLAYERS_DETAIL.FULL_NAME,
                                                WINNER_TEAMS.EXPERIENCE,
                                                (SEASON - BIRTH_YEAR) AS AGE,
                                                WINNER_TEAMS.SEASON
                            FROM WINNER_TEAMS
                                    JOIN PLAYERS_DETAIL
                                        ON WINNER_TEAMS.player_id = PLAYERS_DETAIL.player_id
                            WHERE SEASON IN (2023, 2024)),
                WINNERS_POTENTIAL AS (SELECT FULL_NAME,
                                            (EXPERIENCE / AGE) AS POTENTIAL,
                                            SEASON
                                    FROM WINNERS)

            SELECT FULL_NAME,
                POTENTIAL,
                SEASON
            FROM WINNERS_POTENTIAL;

            """
    query_to_pd(query, ['full_name', 'potential', 'season']).to_csv(os.path.join(data_path, 'csv_h2_1.csv'), index=False)
    query = """
            WITH WINNERS AS (SELECT DISTINCTROW PLAYERS_DETAIL.FULL_NAME,
                                                WINNER_TEAMS.EXPERIENCE,
                                                (SEASON - BIRTH_YEAR) AS AGE,
                                                WINNER_TEAMS.SEASON
                            FROM WINNER_TEAMS
                                    JOIN PLAYERS_DETAIL
                                        ON WINNER_TEAMS.player_id = PLAYERS_DETAIL.player_id
                            WHERE SEASON IN (2021, 2022)),
                WINNERS_POTENTIAL AS (SELECT FULL_NAME,
                                            (EXPERIENCE / AGE) AS POTENTIAL,
                                            SEASON
                                    FROM WINNERS)

            SELECT FULL_NAME,
                POTENTIAL,
                SEASON
            FROM WINNERS_POTENTIAL;
            """
    query_to_pd(query, ['full_name', 'potential', 'season']).to_csv(os.path.join(data_path, 'csv_h2_2.csv'), index=False)
    print('All is good!!')
except Exception as e:
    print(e)
finally:
    if 'cnxn' in locals() and cnxn.is_connected():
        cursor.close()
        cnxn.close()
        print("Connection Closed.")