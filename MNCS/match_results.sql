SELECT league_name,season_name,team_name,week,league_id,season_id,team_id,match_id,opponent_team_id,ROW_NUMBER() OVER(PARTITION BY league_id,season_id,team_id ORDER BY match_id) match_number
,COUNT(game_id_win_total)game_wins
,COUNT(CASE WHEN wins = 0 THEN game_id_total ELSE NULL END)game_losses
,CASE WHEN COUNT(game_id_win_total) > COUNT(CASE WHEN wins = 0 THEN game_id_total ELSE NULL END) THEN 'Win' ELSE 'Loss' END match_result
,CASE WHEN COUNT(game_id_win_total) > COUNT(CASE WHEN wins = 0 THEN game_id_total ELSE NULL END) THEN team_id ELSE opponent_team_id END team_id_win
,CASE WHEN COUNT(game_id_win_total) < COUNT(CASE WHEN wins = 0 THEN game_id_total ELSE NULL END) THEN team_id ELSE opponent_team_id END team_id_loss
FROM `mnrl-269717.prod_stats.team_games` 
--WHERE league_name = 'clmn' and season_name = '4'
GROUP BY league_name,season_name,team_name,week,league_id,season_id,team_id,match_id,opponent_team_id
ORDER BY league_name,season_name,team_name,week