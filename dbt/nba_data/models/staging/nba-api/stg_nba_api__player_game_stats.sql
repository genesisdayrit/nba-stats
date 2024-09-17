with source as (
    select
        season_id,
        player_id,
        game_id,
        game_date,
        matchup,
        wl,
        min as player_game_minutes,
        fgm as player_game_field_goals_made,
        fga as player_game_field_goals_attempted,
        fg_pct as player_game_field_goal_percentage,
        fg3m as player_game_three_pointers_made,
        fg3a as player_game_three_pointers_attempted,
        fg3_pct as player_game_three_point_percentage,
        ftm as player_game_free_throws_made,
        fta as player_game_free_throws_attempted,
        ft_pct as player_game_free_throw_percentage,
        oreb as player_game_offensive_rebounds,
        dreb as player_game_defensive_rebounds,
        reb as player_game_total_rebounds,
        ast as player_game_assists,
        stl as player_game_steals,
        blk as player_game_blocks,
        tov as player_game_turnovers,
        pf as player_game_personal_fouls,
        pts as player_game_points,
        plus_minus as player_game_plus_minus,
        video_available as player_game_video_available
    from {{ source('nba_api', 'player_game_stats') }}
)

select * from source

