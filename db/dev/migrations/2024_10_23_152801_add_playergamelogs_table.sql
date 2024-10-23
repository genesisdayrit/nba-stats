-- Write your SQL migration here

-- Drop the existing table if it exists
DROP TABLE IF EXISTS nba_api.playergamelogs__player_game_log;

-- Ensure the schema exists before creating the table
CREATE SCHEMA IF NOT EXISTS nba_api;

-- Create the new table within the schema
CREATE TABLE nba_api.playergamelogs__player_game_log (
    SEASON_YEAR VARCHAR(9),                     -- Example: '2024-25'
    PLAYER_ID INTEGER,                          -- Player ID
    PLAYER_NAME VARCHAR(100),                   -- Player Name
    TEAM_ID INTEGER,                            -- Team ID
    TEAM_ABBREVIATION VARCHAR(10),              -- Team Abbreviation
    TEAM_NAME VARCHAR(50),                      -- Team Name
    GAME_ID VARCHAR(15),                        -- Game ID
    GAME_DATE DATE,                             -- Game Date
    MATCHUP VARCHAR(50),                        -- Matchup info (e.g., "LAL vs GSW")
    WL CHAR(1),                                 -- Win/Loss ('W' or 'L')
    MIN VARCHAR(5),                             -- Minutes Played
    FGM INTEGER,                                -- Field Goals Made
    FGA INTEGER,                                -- Field Goals Attempted
    FG_PCT DECIMAL(4, 3),                       -- Field Goal Percentage
    FG3M INTEGER,                               -- 3-Point Field Goals Made
    FG3A INTEGER,                               -- 3-Point Field Goals Attempted
    FG3_PCT DECIMAL(4, 3),                      -- 3-Point Field Goal Percentage
    FTM INTEGER,                                -- Free Throws Made
    FTA INTEGER,                                -- Free Throws Attempted
    FT_PCT DECIMAL(4, 3),                       -- Free Throw Percentage
    OREB INTEGER,                               -- Offensive Rebounds
    DREB INTEGER,                               -- Defensive Rebounds
    REB INTEGER,                                -- Total Rebounds
    AST INTEGER,                                -- Assists
    TOV INTEGER,                                -- Turnovers
    STL INTEGER,                                -- Steals
    BLK INTEGER,                                -- Blocks
    BLKA INTEGER,                               -- Blocked Attempts
    PF INTEGER,                                 -- Personal Fouls
    PFD INTEGER,                                -- Personal Fouls Drawn
    PTS INTEGER,                                -- Points
    PLUS_MINUS INTEGER,                         -- Plus/Minus
    NBA_FANTASY_PTS DECIMAL(5, 2),              -- NBA Fantasy Points
    DD2 INTEGER,                                -- Double-Doubles
    TD3 INTEGER,                                -- Triple-Doubles
    GP_RANK INTEGER,                            -- Games Played Rank
    W_RANK INTEGER,                             -- Wins Rank
    L_RANK INTEGER,                             -- Losses Rank
    W_PCT_RANK INTEGER,                         -- Win Percentage Rank
    MIN_RANK INTEGER,                           -- Minutes Played Rank
    FGM_RANK INTEGER,                           -- Field Goals Made Rank
    FGA_RANK INTEGER,                           -- Field Goals Attempted Rank
    FG_PCT_RANK INTEGER,                        -- Field Goal Percentage Rank
    FG3M_RANK INTEGER,                          -- 3-Point Field Goals Made Rank
    FG3A_RANK INTEGER,                          -- 3-Point Field Goals Attempted Rank
    FG3_PCT_RANK INTEGER,                       -- 3-Point Field Goal Percentage Rank
    FTM_RANK INTEGER,                           -- Free Throws Made Rank
    FTA_RANK INTEGER,                           -- Free Throws Attempted Rank
    FT_PCT_RANK INTEGER,                        -- Free Throw Percentage Rank
    OREB_RANK INTEGER,                          -- Offensive Rebounds Rank
    DREB_RANK INTEGER,                          -- Defensive Rebounds Rank
    REB_RANK INTEGER,                           -- Total Rebounds Rank
    AST_RANK INTEGER,                           -- Assists Rank
    TOV_RANK INTEGER,                           -- Turnovers Rank
    STL_RANK INTEGER,                           -- Steals Rank
    BLK_RANK INTEGER,                           -- Blocks Rank
    BLKA_RANK INTEGER,                          -- Blocked Attempts Rank
    PF_RANK INTEGER,                            -- Personal Fouls Rank
    PFD_RANK INTEGER,                           -- Personal Fouls Drawn Rank
    PTS_RANK INTEGER,                           -- Points Rank
    PLUS_MINUS_RANK INTEGER,                    -- Plus/Minus Rank
    NBA_FANTASY_PTS_RANK INTEGER,               -- NBA Fantasy Points Rank
    DD2_RANK INTEGER,                           -- Double-Doubles Rank
    TD3_RANK INTEGER,                           -- Triple-Doubles Rank
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Record creation timestamp
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Record last modification timestamp
    PRIMARY KEY (GAME_ID, PLAYER_ID)            -- Primary key on GAME_ID and PLAYER_ID
);

-- Create the trigger to automatically update modified_at on row update
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add the trigger to the new table
CREATE TRIGGER update_modified_at
BEFORE UPDATE ON nba_api.playergamelogs__player_game_log
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();
