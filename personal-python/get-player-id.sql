SELECT DISTINCT 
CASE 
    WHEN player_platform = 'xbox' THEN 'xbl' 
    WHEN player_platform = 'ps4' THEN 'psn'
    ELSE player_platform 
END player_platform
,CASE WHEN player_platform in ('xbox','epic') THEN player_name ELSE player_platform_id END player_platform_id
FROM mnrl-269717.prod_stats.player_games
where player_platform_id is not null
