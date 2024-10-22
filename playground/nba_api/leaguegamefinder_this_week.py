from nba_api.stats.endpoints import LeagueGameFinder
import pandas as pd

# Function to get game-level NBA data for a specific date range
def get_game_level_data_for_week(date_from, date_to, season='2024-25'):
    # Use LeagueGameFinder to get team-game data for a specific date range
    game_finder = LeagueGameFinder(
        date_from_nullable=date_from, 
        date_to_nullable=date_to,
        season_nullable=season,
        season_type_nullable="Regular Season",  # Assuming we want regular season data
        player_or_team_abbreviation="T"  # Fetching team games
    )
    
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

    # Display the data
    print(game_data)
    return game_data

# Example usage
if __name__ == "__main__":
    # Define the current week's date range
    date_from = '2024-10-22'  # Monday, Oct 22, 2024
    date_to = '2024-10-28'    # Sunday, Oct 28, 2024

    # Get game-level data for the current week
    game_data = get_game_level_data_for_week(date_from, date_to)
    print(game_data.head())
