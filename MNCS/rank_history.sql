DECLARE weeknum INT64;

CREATE TEMP TABLE rank_history (
    league_name string,
    season_name string,
    team_name string,
    league_id string,
    season_id string,
    team_id string,
    week int64,
    rank_delta float64,
    rank_total float64);

--insert week 0 values
INSERT INTO rank_history
SELECT DISTINCT
  league_name
  ,season_name
  ,team_name
  ,league_id
  ,season_id
  ,team_id
  ,0 week
  ,CASE 
		WHEN league_name = 'mncs' THEN 1333 
		WHEN league_name = 'clmn 1' THEN 1000
		WHEN league_name = 'clmn' THEN 1000
		WHEN league_name = 'clmn 2' THEN 667
		WHEN league_name = 'mnrs' THEN 667		
		ELSE NULL 
	END rank_delta
  ,CASE 
		WHEN league_name = 'mncs' THEN 1333 
		WHEN league_name = 'clmn 1' THEN 1000 
		WHEN league_name = 'clmn 2' THEN 667
		WHEN league_name = 'mnrs' THEN 667
		ELSE NULL 
	END rank_total
FROM
  `mnrl-269717.prod_stats.match_results`
WHERE season_name = '4';

SELECT * FROM rank_history;


--eventually loop through weeks starting with week 1 going to max week
--insert row into rank_history for each week and then move to next week


SET weeknum = 1;
--loop through weeks, inserting rank_history values
WHILE weeknum<=(SELECT MAX(week) FROM `mnrl-269717.prod_stats.match_results` WHERE season_name = '4') DO

INSERT INTO rank_history
SELECT 
    league_name
    ,season_name
    ,team_name
    ,league_id
    ,season_id
    ,team_id
    ,week
    ,rank_delta
    ,prev_rank_total + rank_delta as rank_total
FROM(
    SELECT o.*
    ,(SELECT rank_total FROM rank_history as prev WHERE week = weeknum-1 AND prev.team_id = o.team_id_loss)
    ,25 * (o.game_wins - o.game_losses) * (1 - (1/(POW(10,-((SELECT rank_total FROM rank_history as prev WHERE week = weeknum-1 AND prev.team_id = o.team_id_win)-(SELECT rank_total FROM rank_history as prev WHERE week = weeknum-1 AND prev.team_id = o.team_id_loss))/600)+1))) rank_delta
    ,rh.rank_total as prev_rank_total
    FROM `mnrl-269717.prod_stats.match_results` as o
    LEFT JOIN rank_history as rh 
        ON o.league_id = rh.league_id
        AND o.season_id = rh.season_id
        AND o.team_id = rh.team_id
        AND rh.week = weeknum-1
    WHERE o.season_name = '4'
    AND o.week = weeknum
);
SET weeknum = weeknum+1;
END WHILE;

CREATE OR REPLACE TABLE `mnrl-269717.prod_stats.rank_history`
(
    league_name string,
    season_name string,
    team_name string,
    league_id string,
    season_id string,
    team_id string,
    week int64,
    rank_delta float64,
    rank_total float64
);

INSERT INTO `mnrl-269717.prod_stats.rank_history`
SELECT * FROM rank_history
--SELECT * FROM `mnrl-269717.prod_stats.rank_history`