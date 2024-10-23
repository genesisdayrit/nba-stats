-- Write your SQL migration here

CREATE SCHEMA IF NOT EXISTS nba_api;

CREATE TABLE IF NOT EXISTS nba_api.leaguegamelog (
    season_year VARCHAR(9),               -- Example: '2024-25'
    team_id INTEGER,                      -- Example: Team ID
    team_abbreviation VARCHAR(5),         -- Example: 'LAL'
    team_name VARCHAR(50),                -- Example: 'Los Angeles Lakers'
    game_id VARCHAR(15),                  -- Example: '0022100001'
    game_date DATE,                       -- Example: '2024-10-18'
    matchup VARCHAR(20),                  -- Example: 'LAL vs GSW'
    wl CHAR(1),                           -- Win or Loss ('W' or 'L')
    min INTEGER,                          -- Minutes played
    fgm INTEGER,                          -- Field Goals Made
    fga INTEGER,                          -- Field Goals Attempted
    fg_pct DECIMAL(4, 3),                 -- Field Goal Percentage
    fg3m INTEGER,                         -- 3-Point Field Goals Made
    fg3a INTEGER,                         -- 3-Point Field Goals Attempted
    fg3_pct DECIMAL(4, 3),                -- 3-Point Field Goal Percentage
    ftm INTEGER,                          -- Free Throws Made
    fta INTEGER,                          -- Free Throws Attempted
    ft_pct DECIMAL(4, 3),                 -- Free Throw Percentage
    oreb INTEGER,                         -- Offensive Rebounds
    dreb INTEGER,                         -- Defensive Rebounds
    reb INTEGER,                          -- Total Rebounds
    ast INTEGER,                          -- Assists
    tov INTEGER,                          -- Turnovers
    stl INTEGER,                          -- Steals
    blk INTEGER,                          -- Blocks
    blka INTEGER,                         -- Block Attempts Against
    pf INTEGER,                           -- Personal Fouls
    pfd INTEGER,                          -- Personal Fouls Drawn
    pts INTEGER,                          -- Points
    plus_minus INTEGER,                   -- Plus/Minus
    gp_rank INTEGER,                      -- Games Played Rank
    w_rank INTEGER,                       -- Wins Rank
    l_rank INTEGER,                       -- Losses Rank
    w_pct_rank INTEGER,                   -- Win Percentage Rank
    min_rank INTEGER,                     -- Minutes Rank
    fgm_rank INTEGER,                     -- Field Goals Made Rank
    fga_rank INTEGER,                     -- Field Goals Attempted Rank
    fg_pct_rank INTEGER,                  -- Field Goal Percentage Rank
    fg3m_rank INTEGER,                    -- 3-Point Field Goals Made Rank
    fg3a_rank INTEGER,                    -- 3-Point Field Goals Attempted Rank
    fg3_pct_rank INTEGER,                 -- 3-Point Field Goal Percentage Rank
    ftm_rank INTEGER,                     -- Free Throws Made Rank
    fta_rank INTEGER,                     -- Free Throws Attempted Rank
    ft_pct_rank INTEGER,                  -- Free Throw Percentage Rank
    oreb_rank INTEGER,                    -- Offensive Rebounds Rank
    dreb_rank INTEGER,                    -- Defensive Rebounds Rank
    reb_rank INTEGER,                     -- Total Rebounds Rank
    ast_rank INTEGER,                     -- Assists Rank
    tov_rank INTEGER,                     -- Turnovers Rank
    stl_rank INTEGER,                     -- Steals Rank
    blk_rank INTEGER,                     -- Blocks Rank
    blka_rank INTEGER,                    -- Block Attempts Rank
    pf_rank INTEGER,                      -- Personal Fouls Rank
    pfd_rank INTEGER,                     -- Personal Fouls Drawn Rank
    pts_rank INTEGER,                     -- Points Rank
    plus_minus_rank INTEGER,              -- Plus/Minus Rank
    available_flag INTEGER                -- Availability Flag (1 if available, 0 otherwise)
);

