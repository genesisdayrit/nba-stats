from nba_api.stats.endpoints import commonallplayers, playergamelog
import pandas as pd
import time
import random
import os
import logging

# Set up logging
logging.basicConfig(
    filename='nba_data_fetch.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define the season for which you want to fetch data
season = '2023-24'

# Fetch all players
players = commonallplayers.CommonAllPlayers(is_only_current_season=1, league_id='00', season=season)
players_df = players.get_data_frames()[0]

# List to store all player game logs
all_player_game_logs = []

# Checkpoint file to keep track of processed players
checkpoint_file = 'processed_players.txt'

# Load processed players from checkpoint file
if os.path.exists(checkpoint_file):
    with open(checkpoint_file, 'r') as f:
        processed_players = set(f.read().splitlines())
else:
    processed_players = set()

# Function to safely fetch player game logs with retries
def fetch_player_logs(player_id, season, max_retries=5):
    for attempt in range(max_retries):
        try:
            start_time = time.time()
            # Fetch game logs for the current player
            player_logs = playergamelog.PlayerGameLog(season=season, player_id=player_id)
            player_games_df = player_logs.get_data_frames()[0]
            
            # Log the successful fetch and response time
            response_time = time.time() - start_time
            logging.info(f"Successfully fetched data for player {player_id} in {response_time:.2f} seconds.")
            
            return player_games_df
        except Exception as e:
            error_message = str(e)
            if 'rate limit' in error_message.lower():
                logging.warning(f"Rate limit error for player {player_id} (Attempt {attempt+1}/{max_retries}). Retrying...")
            elif 'timeout' in error_message.lower():
                logging.warning(f"Timeout error for player {player_id} (Attempt {attempt+1}/{max_retries}). Retrying...")
            else:
                logging.error(f"Error fetching data for player {player_id} (Attempt {attempt+1}/{max_retries}): {e}")
            
            # Exponential backoff for retries
            time.sleep(2 ** attempt)
    
    logging.error(f"Failed to fetch data for player {player_id} after {max_retries} attempts.")
    return pd.DataFrame()  # Return an empty DataFrame if all retries fail

# Loop through each player and get their game logs
for player_id in players_df['PERSON_ID']:
    if str(player_id) in processed_players:
        logging.info(f"Skipping already processed player {player_id}")
        continue

    player_games_df = fetch_player_logs(player_id, season)
    
    if not player_games_df.empty:
        all_player_game_logs.append(player_games_df)
    
    # Save player ID to checkpoint file
    with open(checkpoint_file, 'a') as f:
        f.write(f"{player_id}\n")

    # Random delay to avoid hitting the API rate limits
    time.sleep(random.uniform(1, 3))

# Combine all DataFrames into one
if all_player_game_logs:
    all_games_df = pd.concat(all_player_game_logs, ignore_index=True)

    # Preview the data to ensure it's loaded correctly
    print(all_games_df.head())

    # Define the output file path
    output_file_path = 'nba_player_game_data_2023_24_test.csv'

    # Save the DataFrame to a CSV file
    all_games_df.to_csv(output_file_path, index=False)

    print(f"Data saved to {output_file_path}")

# Generate a summary report
successful_requests = len(all_player_game_logs)
total_players = len(players_df)
failed_requests = total_players - successful_requests

logging.info(f"Summary Report: Total Players: {total_players}, Successful Requests: {successful_requests}, Failed Requests: {failed_requests}")
print(f"Summary Report: Total Players: {total_players}, Successful Requests: {successful_requests}, Failed Requests: {failed_requests}")

