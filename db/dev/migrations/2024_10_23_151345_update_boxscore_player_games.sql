-- Write your SQL migration here

-- Create a new schema if not exists
CREATE SCHEMA IF NOT EXISTS nba_api;

-- Drop the old table if it exists
DROP TABLE IF EXISTS nba_api.boxscoretraditionalv2__player_stats;

-- Create the helper function to set the modified_at timestamp
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the new table with the updated schema
CREATE TABLE nba_api.boxscoretraditionalv2__player_stats (
    GAME_ID VARCHAR(15),                         -- Game ID
    TEAM_ID INTEGER,                             -- Team ID
    TEAM_ABBREVIATION VARCHAR(5),                -- Team abbreviation
    TEAM_CITY VARCHAR(50),                       -- Team city
    PLAYER_ID INTEGER,                           -- Player ID
    PLAYER_NAME VARCHAR(100),                    -- Player name
    START_POSITION VARCHAR(2),                   -- Start position
    COMMENT TEXT,                                -- Comments about the player
    MIN VARCHAR(5),                              -- Minutes played
    FGM INTEGER,                                 -- Field goals made
    FGA INTEGER,                                 -- Field goals attempted
    FG_PCT NUMERIC(5, 2),                        -- Field goal percentage
    FG3M INTEGER,                                -- 3-point field goals made
    FG3A INTEGER,                                -- 3-point field goals attempted
    FG3_PCT NUMERIC(5, 2),                       -- 3-point field goal percentage
    FTM INTEGER,                                 -- Free throws made
    FTA INTEGER,                                 -- Free throws attempted
    FT_PCT NUMERIC(5, 2),                        -- Free throw percentage
    OREB INTEGER,                                -- Offensive rebounds
    DREB INTEGER,                                -- Defensive rebounds
    REB INTEGER,                                 -- Total rebounds
    AST INTEGER,                                 -- Assists
    STL INTEGER,                                 -- Steals
    BLK INTEGER,                                 -- Blocks
    TOV INTEGER,                                 -- Turnovers (renamed from TO)
    PF INTEGER,                                  -- Personal fouls
    PTS INTEGER,                                 -- Points
    PLUS_MINUS NUMERIC(5, 2),                    -- Plus/Minus
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Record creation timestamp
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Record last modification timestamp
    PRIMARY KEY (GAME_ID, PLAYER_ID)             -- Primary key on GAME_ID and PLAYER_ID
);

-- Create the trigger to automatically update modified_at on row update
CREATE TRIGGER update_modified_at
BEFORE UPDATE ON nba_api.boxscoretraditionalv2__player_stats
FOR EACH ROW
EXECUTE PROCEDURE trigger_set_timestamp();
