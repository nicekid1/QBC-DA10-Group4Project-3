 -- Question1
select name,height from players_datails
 join top_players on top_players.player_id = players_Details.player_id
where top_players.season in (2019,2020,2021,2022,2023,2024);
 group by name,height, limit(50)

select name,height from players_datails
 join awards on awards.player_id = players_Details.player_id
where awards.season in (2019,2020,2021,2022,2023,2024);
 group by name,height;




 -- Question2
 select name,height,experience from players_datails
 join top_players on top_players.player_id = players_Details.player_id
where top_players.season=2023 or top_players.season=2024
 group by name,height,experience, limit(15);

select name,height,experience from player_details
join winner_teams on winner_teams.player_id = players_details.player_id,
where top_players.season in (2023,2024)
group by name,height,experience,

 -- Question3

select players_datails.name,awards.season,count(awards.player_id) as total_presence from players_details
       join awards on awards.player_id = players_details.player_id
where player_details.pos="Point Guard" and awards.season in(2019,2020,2021,2022,2023);
group by name,total_presence, order by total_presence desc , limit(3)

 


