from nba_api.stats.endpoints import LeagueGameFinder
import pandas as pd

# Function to get NBA game data for a specific season
def get_nba_game_data(season='2023-24'):
    # Use LeagueGameFinder to get game data
    game_finder = LeagueGameFinder(season_nullable=season)
    
    # Convert the results into a Pandas DataFrame
    games_df = game_finder.get_data_frames()[0]
    
    # Select the relevant columns for game-level details
    selected_columns = [
        'GAME_ID',           # Unique game ID
        'GAME_DATE',         # Game date
        'MATCHUP',           # Teams involved
        'HOME_TEAM_ID',      # Home team ID
        'VISITOR_TEAM_ID',   # Visitor team ID
        'PTS_HOME',          # Home team points
        'PTS_AWAY',          # Away team points
        'SEASON_ID',         # Season ID
    ]
    
    # Filter the dataframe to include only these columns
    games_data = games_df[selected_columns]
    
    # Save the dataframe to a CSV file
    csv_file_path = f"nba_games_{season}.csv"
    games_data.to_csv(csv_file_path, index=False)
    
    print(f"Game data for season {season} has been saved to {csv_file_path}")
    return games_data

# Example usage
if __name__ == "__main__":
    # Get game data for the 2023-24 season and save it to a CSV
    nba_game_data = get_nba_game_data('2023-24')

