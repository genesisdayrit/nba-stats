WITH WeeklyFantasyStats AS (
    SELECT 
        player_id,
        player_name,
        team_abbreviation,
        DATE_TRUNC('week', game_date) AS week_start,
        SUM(pts) AS total_points,
        SUM(reb) AS total_rebounds,
        SUM(ast) AS total_assists,
        SUM(stl) AS total_steals,
        SUM(blk) AS total_blocks,
        SUM(tov) AS total_turnovers,
        SUM(fgm) AS total_fg_made,
        SUM(fga) AS total_fg_attempted,
        SUM(ftm) AS total_ft_made,
        SUM(fta) AS total_ft_attempted,
        SUM(fg3m) AS total_3pt_made,
        SUM(nba_fantasy_pts) AS total_fantasy_pts
    FROM nba_api.playergamelogs__player_game_log
    WHERE game_date >= NOW() - INTERVAL '1 month'
    GROUP BY player_id, player_name, team_abbreviation, DATE_TRUNC('week', game_date)
),
PlayerWeeklyAverages AS (
    SELECT 
        player_id,
        player_name,
        team_abbreviation,
        ROUND(AVG(total_points), 1) AS avg_points,
        ROUND(AVG(total_rebounds), 1) AS avg_rebounds,
        ROUND(AVG(total_assists), 1) AS avg_assists,
        ROUND(AVG(total_steals), 1) AS avg_steals,
        ROUND(AVG(total_blocks), 1) AS avg_blocks,
        ROUND(AVG(total_turnovers), 1) AS avg_turnovers,
        ROUND(AVG(total_fg_made), 1) AS avg_fg_made,
        ROUND(AVG(total_fg_attempted), 1) AS avg_fg_attempted,
        ROUND(AVG(total_ft_made), 1) AS avg_ft_made,
        ROUND(AVG(total_ft_attempted), 1) AS avg_ft_attempted,
        ROUND(AVG(total_3pt_made), 1) AS avg_3pt_made,
        ROUND(AVG(total_fantasy_pts), 1) AS avg_fantasy_pts
    FROM WeeklyFantasyStats
    GROUP BY player_id, player_name, team_abbreviation
)
SELECT 
    RANK() OVER (ORDER BY avg_fantasy_pts DESC) AS Rank,
    player_id AS Player_ID,
    player_name AS Player_Name,
    team_abbreviation AS Team,
    avg_fantasy_pts AS Fantasy_Points,
    avg_points AS Points,
    avg_rebounds AS Rebounds,
    avg_assists AS Assists,
    avg_steals AS Steals,
    avg_blocks AS Blocks,
    avg_turnovers AS Turnovers,
    avg_fg_made AS FG_Made,
    avg_fg_attempted AS FG_Attempted,
    avg_ft_made AS FT_Made,
    avg_ft_attempted AS FT_Attempted,
    avg_3pt_made AS ThreePt_Made
FROM PlayerWeeklyAverages
ORDER BY Fantasy_Points DESC
LIMIT 150;

