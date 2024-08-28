from nba_api.stats.endpoints import playergamelog
import pandas as pd

# Define the season for which you want to fetch data
season = '2023-24'

# Define a specific player ID (Stephen Curry's ID is used here as an example)
player_id = '201939'

# Fetch game logs for the selected player
try:
    player_logs = playergamelog.PlayerGameLog(season=season, player_id=player_id)
    player_games_df = player_logs.get_data_frames()[0]

    # Preview the data to ensure it's loaded correctly
    print(player_games_df.head())

    # Define the output file path
    output_file_path = 'nba_player_game_data_curry_2023_24.csv'

    # Save the DataFrame to a CSV file
    player_games_df.to_csv(output_file_path, index=False)

    print(f"Data saved to {output_file_path}")
except Exception as e:
    print(f"Error fetching data: {e}")
