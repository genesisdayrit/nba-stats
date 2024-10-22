import pandas as pd
from nba_api.stats.endpoints import playergamelogs

# Define parameters for the 2023-24 season
season = "2023-24"
season_type = "Regular Season"  # Options: Regular Season, Playoffs, Pre Season, etc.

# Fetch player game logs for the 2023-24 season
player_game_logs_data = playergamelogs.PlayerGameLogs(season_nullable=season, season_type_nullable=season_type)

# Get the data as a DataFrame
player_game_logs_df = player_game_logs_data.get_data_frames()[0]  # The first DataFrame in the response

# Display the DataFrame (optional)
print(player_game_logs_df)

# Save the DataFrame to a CSV file
player_game_logs_df.to_csv('nba_player_game_logs_2023_24.csv', index=False)

print("Player game logs have been successfully saved to 'nba_player_game_logs_2023_24.csv'.")
