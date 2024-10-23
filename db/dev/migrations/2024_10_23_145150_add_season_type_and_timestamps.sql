-- Write your SQL migration here

-- Add created_at and modified_at columns to the league_game_log table
ALTER TABLE nba_api.league_game_log
ADD COLUMN season_type TEXT,
ADD COLUMN created_at TIMESTAMPTZ DEFAULT NOW(),
ADD COLUMN modified_at TIMESTAMPTZ DEFAULT NOW();

-- Ensure modified_at is updated automatically on record update
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
   NEW.modified_at = NOW();
   RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger to automatically update modified_at
CREATE TRIGGER set_modified_at
BEFORE UPDATE ON nba_api.league_game_log
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
