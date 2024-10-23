-- Write your SQL migration here

-- Alter table to remove the length limits by changing to TEXT type
ALTER TABLE nba_api.playergamelogs__player_game_log
    ALTER COLUMN season_year TYPE TEXT,
    ALTER COLUMN player_name TYPE TEXT,
    ALTER COLUMN team_name TYPE TEXT,
    ALTER COLUMN game_id TYPE TEXT,
    ALTER COLUMN game_date TYPE DATE,  -- Keep as DATE for proper date handling
    ALTER COLUMN matchup TYPE TEXT;
    ALTER COLUMN min TYPE TEXT;
    
