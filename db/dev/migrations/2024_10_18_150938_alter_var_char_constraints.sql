-- Write your SQL migration here

-- Alter the existing table to remove VARCHAR constraints
ALTER TABLE nba_api_scoreboard_v2.player_game_stats
    ALTER COLUMN team_abbreviation TYPE TEXT,
    ALTER COLUMN team_city TYPE TEXT,
    ALTER COLUMN player_name TYPE TEXT,
    ALTER COLUMN start_position TYPE TEXT,
    ALTER COLUMN min TYPE TEXT;
