from nba_api.stats.endpoints import LeagueGameFinder
import pandas as pd

# Function to get game-level NBA data for a specific season
def get_game_level_data(season='2023-24'):
    # Use LeagueGameFinder to get team-game data
    game_finder = LeagueGameFinder(season_nullable=season)
    
    # Convert to a DataFrame
    games_df = game_finder.get_data_frames()[0]
    
    # Pivot the data to get game-level details
    game_data = games_df.pivot_table(
        index='GAME_ID',
        values=['TEAM_ID', 'TEAM_ABBREVIATION', 'GAME_DATE', 'MATCHUP', 'PTS'],
        aggfunc={
            'TEAM_ID': ['first', 'last'],
            'TEAM_ABBREVIATION': ['first', 'last'],
            'GAME_DATE': 'first',
            'MATCHUP': 'first',
            'PTS': ['first', 'last']
        }
    )

    # Flatten the column names for readability
    game_data.columns = ['HOME_TEAM_ID', 'AWAY_TEAM_ID', 'HOME_TEAM_ABBREVIATION', 
                         'AWAY_TEAM_ABBREVIATION', 'GAME_DATE', 'MATCHUP', 'PTS_HOME', 'PTS_AWAY']

    # Save the data to a CSV
    csv_file_path = f"nba_game_level_{season}.csv"
    game_data.to_csv(csv_file_path, index=True)
    
    print(f"Game-level data for season {season} has been saved to {csv_file_path}")
    return game_data

# Example usage
if __name__ == "__main__":
    # Get game-level data for the 2023-24 season
    game_data = get_game_level_data('2023-24')
    print(game_data.head())

