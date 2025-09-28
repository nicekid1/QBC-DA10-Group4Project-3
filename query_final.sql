-- section 1 table 1
SELECT NAME,
       HEIGHT
FROM PLAYERS_DETAIL
 JOIN AWARDS ON AWARDS.player_id = PLAYERS_DETAIL.player_id
WHERE AWARDS.SEASON IN (2019,2020,2021,2022,2023,2024);


-- section 1 table 2
SELECT NAME,
       HEIGHT
FROM PLAYERS_DETAIL
    JOIN TOP_PLAYERS ON TOP_PLAYERS.player_id = PLAYERS_DETAIL.player_id
WHERE TOP_PLAYERS.season IN (2019,2020,2021,2022,2023,2024)
GROUP BY NAME,HEIGHT;
-- -------------------------------------------------------------------------------------------------