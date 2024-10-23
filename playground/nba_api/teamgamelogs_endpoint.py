import pandas as pd
from nba_api.stats.endpoints import teamgamelogs

# Define parameters for the 2024-25 preseason
season = "2024-25"
season_type = "Regular Season"  # Options: Pre Season, Regular Season, Playoffs, etc.
league_id = "00"  # NBA league ID

# Fetch team game logs for the 2024-25 preseason
team_game_logs_data = teamgamelogs.TeamGameLogs(
    season_nullable=season,
    season_type_nullable=season_type,
    league_id_nullable=league_id
)

# Get the data as a DataFrame
team_game_logs_df = team_game_logs_data.get_data_frames()[0]  # Access the first DataFrame

# Display the DataFrame (optional)
print(team_game_logs_df)

# Save the DataFrame to a CSV file
team_game_logs_df.to_csv('nba_2024_25_preseason_team_game_logs.csv', index=False)

print("Team game logs for the 2024-25 preseason have been successfully saved to 'nba_2024_25_preseason_team_game_logs.csv'.")
