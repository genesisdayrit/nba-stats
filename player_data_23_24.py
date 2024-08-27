from nba_api.stats.endpoints import commonallplayers, playergamelog
import pandas as pd

# Define the season for which you want to fetch data
season = '2023-24'

# Fetch all players
players = commonallplayers.CommonAllPlayers(is_only_current_season=1, league_id='00', season=season)
players_df = players.get_data_frames()[0]

# List to store all player game logs
all_player_game_logs = []

# Loop through each player and get their game logs
for player_id in players_df['PERSON_ID']:
    # Fetch game logs for the current player
    player_logs = playergamelog.PlayerGameLog(season=season, player_id=player_id)
    
    # Get the results as a pandas DataFrame
    player_games_df = player_logs.get_data_frames()[0]
    
    # Append to the list
    all_player_game_logs.append(player_games_df)

# Combine all DataFrames into one
all_games_df = pd.concat(all_player_game_logs, ignore_index=True)

# Preview the data to ensure it's loaded correctly
print(all_games_df.head())

# Define the output file path
output_file_path = 'nba_player_game_data_2023_24.csv'

# Save the DataFrame to a CSV file
all_games_df.to_csv(output_file_path, index=False)

print(f"Data saved to {output_file_path}")
