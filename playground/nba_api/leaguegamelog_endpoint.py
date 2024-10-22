import pandas as pd
from nba_api.stats.endpoints import LeagueGameFinder

# Define parameters for the 2024-25 season
season = "2024-25"
season_type = "Regular Season"  # Options: Regular Season, Pre Season, Playoffs, etc.
league_id = "00"  # NBA league ID
player_or_team = "T"  # Team-based data
direction = "ASC"  # Ascending order by date
sorter = "DATE"  # Sort by game date
counter = 0  # Used to start from the beginning of the log

# Fetch league game logs for the 2024-25 season
league_game_log_data = leaguegamelog.LeagueGameLog(
    counter=counter,
    direction=direction,
    league_id=league_id,
    player_or_team_abbreviation=player_or_team,
    season=season,
    season_type_all_star=season_type,
    sorter=sorter
)

# Get the data as a DataFrame
league_game_log_df = league_game_log_data.get_data_frames()[0]  # Access the first DataFrame

# Display the DataFrame (optional)
print(league_game_log_df)

# Save the DataFrame to a CSV file
league_game_log_df.to_csv('nba_2024_25_game_schedule.csv', index=False)

print("NBA 2024-25 game schedule has been successfully saved to 'nba_2024_25_game_schedule.csv'.")
