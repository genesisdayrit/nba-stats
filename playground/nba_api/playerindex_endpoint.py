import pandas as pd
from nba_api.stats.endpoints import playerindex

# Fetch player index data for the 2022-23 season
season = "2024-25"
player_index_data = playerindex.PlayerIndex(season=season, league_id="00")

# Get the player index data from the response
player_index = player_index_data.player_index.get_data_frame()

# Display the DataFrame
print(player_index)

# Optionally, save to CSV
player_index.to_csv('nba_player_index_2022_23.csv', index=False)
print("Player index data has been successfully saved to 'nba_player_index_2024_25.csv'.")
