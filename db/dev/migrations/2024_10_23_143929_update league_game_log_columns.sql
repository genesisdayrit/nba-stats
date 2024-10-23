-- Write your SQL migration here

-- Enable the pgcrypto extension for UUID generation (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Drop the existing table
DROP TABLE IF EXISTS nba_api.league_game_log;

-- Recreate the table with columns based on the API response and a UUID primary key
CREATE TABLE nba_api.league_game_log (
    game_log_id UUID DEFAULT gen_random_uuid(),  -- UUID primary key, generated automatically
    season_year VARCHAR(9),                     -- Example: '2024-25'
    team_id INTEGER,                            -- Example: Team ID
    team_abbreviation VARCHAR(5),               -- Example: 'LAL'
    team_name VARCHAR(50),                      -- Example: 'Los Angeles Lakers'
    game_id VARCHAR(15),                        -- Example: '0022100001'
    game_date DATE,                             -- Example: '2024-10-18'
    matchup VARCHAR(50),                        -- Example: 'LAL vs GSW'
    wl CHAR(1),                                 -- Win or Loss ('W' or 'L')
    min INTEGER,                                -- Minutes played
    fgm INTEGER,                                -- Field Goals Made
    fga INTEGER,                                -- Field Goals Attempted
    fg_pct DECIMAL(4, 3),                       -- Field Goal Percentage
    fg3m INTEGER,                               -- 3-Point Field Goals Made
    fg3a INTEGER,                               -- 3-Point Field Goals Attempted
    fg3_pct DECIMAL(4, 3),                      -- 3-Point Field Goal Percentage
    ftm INTEGER,                                -- Free Throws Made
    fta INTEGER,                                -- Free Throws Attempted
    ft_pct DECIMAL(4, 3),                       -- Free Throw Percentage
    oreb INTEGER,                               -- Offensive Rebounds
    dreb INTEGER,                               -- Defensive Rebounds
    reb INTEGER,                                -- Total Rebounds
    ast INTEGER,                                -- Assists
    stl INTEGER,                                -- Steals
    blk INTEGER,                                -- Blocks
    tov INTEGER,                                -- Turnovers
    pf INTEGER,                                 -- Personal Fouls
    pts INTEGER,                                -- Points
    plus_minus INTEGER,                         -- Plus/Minus
    video_available BOOLEAN,                    -- Flag if video is available
    PRIMARY KEY (game_log_id)                   -- Use UUID as primary key
);

-- Optionally, create a unique constraint on team_id and game_id to enforce uniqueness
CREATE UNIQUE INDEX idx_unique_team_game ON nba_api.league_game_log (team_id, game_id);
