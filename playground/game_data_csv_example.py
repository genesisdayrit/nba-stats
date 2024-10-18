from nba_api.stats.endpoints import LeagueGameFinder
import pandas as pd

# Function to get NBA game data for a specific month
def get_game_level_data_by_month(month='2024-10'):
    # Use LeagueGameFinder to get team-game data
    game_finder = LeagueGameFinder()
    
    # Convert the results into a DataFrame
    games_df = game_finder.get_data_frames()[0]
    
    # Convert GAME_DATE to a datetime format for filtering
    games_df['GAME_DATE'] = pd.to_datetime(games_df['GAME_DATE'])
    
    # Filter games for the given month (e.g., '2024-10' for October 2024)
    games_this_month = games_df[games_df['GAME_DATE'].dt.strftime('%Y-%m') == month]
    
    # Extract game-level details for each game
    game_data = games_this_month.groupby('GAME_ID').agg(
        HOME_TEAM_ID=('TEAM_ID', 'first'),
        AWAY_TEAM_ID=('TEAM_ID', 'last'),
        HOME_TEAM_ABBREVIATION=('TEAM_ABBREVIATION', 'first'),
        AWAY_TEAM_ABBREVIATION=('TEAM_ABBREVIATION', 'last'),
        GAME_DATE=('GAME_DATE', 'first'),
        MATCHUP=('MATCHUP', 'first'),
        PTS_HOME=('PTS', 'first'),
        PTS_AWAY=('PTS', 'last')
    ).reset_index()

    # Save the cleaned data to a CSV file
    csv_file_path = f"nba_game_level_{month}.csv"
    game_data.to_csv(csv_file_path, index=False)
    
    print(f"Game-level data for {month} has been saved to {csv_file_path}")
    return game_data

# Example usage
if __name__ == "__main__":
    # Get game-level data for October 2024 and save it to a CSV
    game_data_october = get_game_level_data_by_month('2024-10')
    print(game_data_october.head())

