-- Write your SQL migration here

-- Add primary key
ALTER TABLE nba_api.league_game_log ADD PRIMARY KEY (game_id, team_id);

-- Add indexes to speed up queries
CREATE INDEX idx_team_id ON nba_api.league_game_log (team_id);
CREATE INDEX idx_game_date ON nba_api.league_game_log (game_date);
