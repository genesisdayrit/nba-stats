with source as (
    select
        season_id,
        player_id,
        game_id,
        game_date,
        matchup,
        wl,
        min,
        fgm,
        fga,
        fg_pct,
        fg3m,
        fg3a,
        fg3_pct,
        ftm,
        fta,
        ft_pct,
        oreb,
        dreb,
        reb,
        ast,
        stl,
        blk,
        tov,
        pf,
        pts,
        plus_minus,
        video_available
    from {{ source('nba_api', 'player_game_stats') }}
)

select * from source

