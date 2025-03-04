-- Write your SQL migration here

DROP TABLE IF EXISTS nba_api.player_game_stats;

-- Ensure the schema exists before creating the table
CREATE SCHEMA IF NOT EXISTS nba_api_scoreboard_v2;

-- Create the table within the schema
CREATE TABLE nba_api_scoreboard_v2.player_game_stats (
    GAME_ID VARCHAR(15),
    TEAM_ID INTEGER,
    TEAM_ABBREVIATION VARCHAR(5),
    TEAM_CITY VARCHAR(50),
    PLAYER_ID INTEGER,
    PLAYER_NAME VARCHAR(100),
    START_POSITION VARCHAR(2),
    COMMENT TEXT,
    MIN VARCHAR(5),
    FGM INTEGER,
    FGA INTEGER,
    FG_PCT NUMERIC(5, 2),
    FG3M INTEGER,
    FG3A INTEGER,
    FG3_PCT NUMERIC(5, 2),
    FTM INTEGER,
    FTA INTEGER,
    FT_PCT NUMERIC(5, 2),
    OREB INTEGER,
    DREB INTEGER,
    REB INTEGER,
    AST INTEGER,
    STL INTEGER,
    BLK INTEGER,
    "TO" INTEGER,  -- Escape the 'TO' column
    PF INTEGER,
    PTS INTEGER,
    PLUS_MINUS NUMERIC(5, 2),
    record_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_last_modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
