CREATE VIEW int_player_game_stats AS
SELECT 
    pg.season_id,
    pg.player_id,
    pi.display_first_last,
    pi.team_name,
    pg.game_id,
    pg.game_date,
    pg.matchup,
    pg.wl,
    pg.min,
    pg.fgm,
    pg.fga,
    pg.fg_pct,
    pg.fg3m,
    pg.fg3a,
    pg.fg3_pct,
    pg.ftm,
    pg.fta,
    pg.ft_pct,
    pg.oreb,
    pg.dreb,
    pg.reb,
    pg.ast,
    pg.stl,
    pg.blk,
    pg.tov,
    pg.pf,
    pg.pts,
    pg.plus_minus,
    pg.video_available
FROM player_game_stats pg
JOIN player_info pi ON pg.player_id = pi.person_id;

