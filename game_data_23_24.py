# Import necessary libraries
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd

# Define the season for which you want to fetch data
season = '2023-24'

# Initialize the game finder for regular season games
gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season, season_type_nullable='Regular Season')

# Get the results as a pandas DataFrame
games_df = gamefinder.get_data_frames()[0]

# Preview the data to ensure it's loaded correctly
print(games_df.head())

# Define the output file path
output_file_path = 'nba_game_data_2023_24.csv'

# Save the DataFrame to a CSV file
games_df.to_csv(output_file_path, index=False)

print(f"Data saved to {output_file_path}")

