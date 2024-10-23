# Write your Python migration here

import os
import psycopg2
import pandas as pd
from nba_api.stats.endpoints import LeagueGameLog
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv('../../.env.dev')

# Fetch game logs for the 2024-25 season from the NBA API
def fetch_league_game_log():
    # Define parameters for the 2024-25 season
    season = "2024-25"
    season_type = "Regular Season"  # Options: Regular Season, Pre Season, Playoffs, etc.
    league_id = "00"  # NBA league ID
    player_or_team = "T"  # Team-based data
    direction = "ASC"  # Ascending order by date
    sorter = "DATE"  # Sort by game date
    counter = 0  # Used to start from the beginning of the log

    # Fetch league game logs for the 2024-25 season
    league_game_log_data = LeagueGameLog(
        counter=counter,
        direction=direction,
        league_id=league_id,
        player_or_team_abbreviation=player_or_team,
        season=season,
        season_type_all_star=season_type,
        sorter=sorter
    )

    # Get the data as a DataFrame
    df = league_game_log_data.get_data_frames()[0]

    # Rename columns to match your PostgreSQL table column names
    df.rename(columns={
        'SEASON_ID': 'season_year',
        'TEAM_ID': 'team_id',
        'TEAM_ABBREVIATION': 'team_abbreviation',
        'TEAM_NAME': 'team_name',
        'GAME_ID': 'game_id',
        'GAME_DATE': 'game_date',
        'MATCHUP': 'matchup',
        'WL': 'wl',
        'MIN': 'min',
        'FGM': 'fgm',
        'FGA': 'fga',
        'FG_PCT': 'fg_pct',
        'FG3M': 'fg3m',
        'FG3A': 'fg3a',
        'FG3_PCT': 'fg3_pct',
        'FTM': 'ftm',
        'FTA': 'fta',
        'FT_PCT': 'ft_pct',
        'OREB': 'oreb',
        'DREB': 'dreb',
        'REB': 'reb',
        'AST': 'ast',
        'STL': 'stl',
        'BLK': 'blk',
        'TOV': 'tov',
        'PF': 'pf',
        'PTS': 'pts',
        'PLUS_MINUS': 'plus_minus',
        'VIDEO_AVAILABLE': 'video_available'
    }, inplace=True)

    # Add the season_type column to the DataFrame
    df['season_type'] = season_type

    return df

# Function to delete the current season's records (full refresh behavior)
def delete_current_season_data(cursor, season_year, season_type):
    try:
        cursor.execute("DELETE FROM nba_api.league_game_log WHERE season_year = %s AND season_type = %s", (season_year, season_type))
        deleted_count = cursor.rowcount  # Get the number of deleted rows
        print(f"Deleted {deleted_count} records for season {season_year} and season type {season_type}.")
    except Exception as e:
        print(f"Error deleting current season data: {e}")

# Function to insert data into the PostgreSQL database
def insert_league_game_log_to_db(df):
    # Fetch database connection details from environment variables
    db_config = {
        'host': os.getenv('DB_HOST'),
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT')
    }

    # Establish connection to the PostgreSQL database
    connection = psycopg2.connect(
        host=db_config['host'],
        database=db_config['dbname'],
        user=db_config['user'],
        password=db_config['password'],
        port=db_config['port']
    )
    cursor = connection.cursor()

    # Full refresh: Delete existing records for the 2024-25 season and season type
    season_year = "2024-25"
    season_type = "Regular Season"
    
    # Log to ensure deletion happens before insert
    delete_current_season_data(cursor, season_year, season_type)

    # Prepare the insert statement (no UPSERT, just insert)
    insert_query = """
        INSERT INTO nba_api.league_game_log (
            season_year, season_type, team_id, team_abbreviation, team_name, game_id, game_date, matchup, wl, min,
            fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, tov, stl, blk, pf, pts, plus_minus, video_available,
            created_at, modified_at
        ) VALUES (
            %(season_year)s, %(season_type)s, %(team_id)s, %(team_abbreviation)s, %(team_name)s, %(game_id)s, %(game_date)s, %(matchup)s, %(wl)s, %(min)s,
            %(fgm)s, %(fga)s, %(fg_pct)s, %(fg3m)s, %(fg3a)s, %(fg3_pct)s, %(ftm)s, %(fta)s, %(ft_pct)s, %(oreb)s, %(dreb)s, %(reb)s,
            %(ast)s, %(tov)s, %(stl)s, %(blk)s, %(pf)s, %(pts)s, %(plus_minus)s, %(video_available)s,
            NOW(), NOW()
        )
    """

    # Insert rows into the database
    for _, row in df.iterrows():
        row_data = row.to_dict()

        # Ensure the season_year and season_type fields are correctly mapped
        row_data['season_year'] = "2024-25"
        row_data['season_type'] = "Regular Season"  # Explicitly set the season_type to ensure it's not NULL

        # Cast video_available to boolean, assuming 1 means True and 0 means False
        row_data['video_available'] = bool(row_data['video_available'])

        # Insert data
        cursor.execute(insert_query, row_data)

    # Commit the transaction and close the connection
    connection.commit()
    cursor.close()
    connection.close()
    print(f"Inserted {len(df)} records into the database.")

# Main script
if __name__ == "__main__":
    # Fetch the league game log data
    game_log_df = fetch_league_game_log()

    # Display the DataFrame columns to check for correct mapping
    print(game_log_df.columns)

    # Write the game log data to the PostgreSQL database
    insert_league_game_log_to_db(game_log_df)
