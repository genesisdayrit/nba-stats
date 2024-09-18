-- models/int__player_game_stats.sql

with player_game_stats as (
    select *
    from {{ ref('stg_nba_api__player_game_stats') }}
),

player_info as (
    select *
    from {{ ref('stg_nba_api__player_info') }}
)

select
    player_game_stats.*,
    player_info.*
from player_game_stats
left join player_info
    on player_game_stats.player_id = player_info.player_id

