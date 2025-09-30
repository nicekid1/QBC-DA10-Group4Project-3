-- section 1 table 1
SELECT PLAYERS_DETAIL.FULL_NAME,
       PLAYERS_DETAIL.HEIGHT
FROM AWARDS
         JOIN PLAYERS_DETAIL ON AWARDS.player_id = PLAYERS_DETAIL.player_id
WHERE AWARDS.SEASON IN (2019, 2020, 2021, 2022, 2023, 2024);

-- section 1 table 2
SELECT FULL_NAME,
       HEIGHT,
       SEASON
FROM TOP_PLAYERS
         JOIN PLAYERS_DETAIL ON TOP_PLAYERS.player_id = PLAYERS_DETAIL.player_id
WHERE TOP_PLAYERS.season IN (2019, 2020, 2021, 2022, 2023, 2024)
GROUP BY FULL_NAME, HEIGHT, SEASON;
-- -------------------------------------------------------------------------------------------------
-- section 2 table 1
SELECT FULL_NAME,
       HEIGHT,
       EXPERIENCE,
       SEASON
FROM WINNER_TEAMS
         JOIN PLAYERS_DETAIL ON WINNER_TEAMS.player_id = PLAYERS_DETAIL.player_id
WHERE WINNER_TEAMS.SEASON IN (2023, 2024)
GROUP BY FULL_NAME, HEIGHT, EXPERIENCE, SEASON;

-- section 2 table 2
SELECT FULL_NAME,
       HEIGHT,
       (SEASON - YEAR_MIN) AS EXPERIENCE,
       SEASON
FROM TOP_PLAYERS
         JOIN PLAYERS_DETAIL ON TOP_PLAYERS.player_id = PLAYERS_DETAIL.player_id
WHERE TOP_PLAYERS.SEASON IN (2023, 2024)
  AND TOP_PLAYERS.Rk <= 15
GROUP BY FULL_NAME, HEIGHT, (SEASON - YEAR_MIN), SEASON;

-- -------------------------------------------------------------------------------------------------
-- section 3
WITH MVP_PG AS (SELECT DISTINCTROW PLAYERS_DETAIL.FULL_NAME,
                                   TOP_PLAYERS.POS,
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
ORDER BY NOMINATED DESC, FULL_NAME
LIMIT 3;
-- -------------------------------------------------------------------------------------------------
-- Hypothesis 1
WITH TOP_AGILITY AS (SELECT DISTINCTROW PLAYERS_DETAIL.FULL_NAME,
                                        (PLAYERS_DETAIL.HEIGHT / PLAYERS_DETAIL.WEIGHT) AS AGILITY,
                                        TOP_PLAYERS.SEASON
                     FROM TOP_PLAYERS
                              JOIN PLAYERS_DETAIL
                                   ON TOP_PLAYERS.player_id = PLAYERS_DETAIL.player_id
                     WHERE TOP_PLAYERS.Rk <= 20
                       AND SEASON IN (2023, 2024))
SELECT FULL_NAME,
       AGILITY
FROM TOP_AGILITY;

WITH TOP_AGILITY AS (SELECT DISTINCTROW PLAYERS_DETAIL.FULL_NAME,
                                        (PLAYERS_DETAIL.HEIGHT / PLAYERS_DETAIL.WEIGHT) AS AGILITY,
                                        TOP_PLAYERS.SEASON
                     FROM TOP_PLAYERS
                              JOIN PLAYERS_DETAIL
                                   ON TOP_PLAYERS.player_id = PLAYERS_DETAIL.player_id
                     WHERE TOP_PLAYERS.Rk <= 20
                       AND SEASON IN (2021, 2022))
SELECT FULL_NAME,
       AGILITY
FROM TOP_AGILITY;
-- -------------------------------------------------------------------------------------------------
-- Hypothesis 2
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



