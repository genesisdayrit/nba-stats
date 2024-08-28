from nba_api.stats.endpoints import commonallplayers
import pandas as pd

# Define the season for which you want to fetch player information
season = '2023-24'

# Fetch all players for the current season
players = commonallplayers.CommonAllPlayers(is_only_current_season=1, league_id='00', season=season)

# Convert the data to a pandas DataFrame
players_df = players.get_data_frames()[0]

# Preview the data to ensure it's loaded correctly
print(players_df.head())

# Define the output file path
output_file_path = 'nba_player_information_2023_24.csv'

# Save the DataFrame to a CSV file
players_df.to_csv(output_file_path, index=False)

print(f"Player information data saved to {output_file_path}")

