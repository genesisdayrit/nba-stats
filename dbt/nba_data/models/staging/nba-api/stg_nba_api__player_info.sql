with source as (
    select
        person_id as player_id,
        display_last_comma_first,
        display_first_last,
        rosterstatus as player_roster_status,
        from_year as player_from_year,
        to_year as player_to_year,
        playercode,
        player_slug,
        team_id,
        team_city,
        team_name,
        team_abbreviation,
        team_slug,
        team_code,
        games_played_flag as player_games_played_flag,
        otherleague_experience_ch as player_other_league_experience
    from {{ source('nba_api', 'player_info') }}
)

select * from source

