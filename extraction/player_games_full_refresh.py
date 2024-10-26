# Write your Python migration here

import os
import psycopg2
import pandas as pd
from nba_api.stats.endpoints import PlayerGameLogs
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env
load_dotenv('.env')

# Fetch player game logs for the 2024-25 season from the NBA API
def fetch_player_game_logs():
    # Define parameters for the 2024-25 Regular Season
    season = "2024-25"
    season_type = "Regular Season"  # Options: Regular Season, Pre Season, Playoffs, etc.
    league_id = "00"  # NBA league ID

    logging.info(f"Fetching player game logs for season: {season}, season type: {season_type}")

    # Fetch player game logs for the 2024-25 season
    player_game_log_data = PlayerGameLogs(
        season_nullable=season,
        season_type_nullable=season_type,
        league_id_nullable=league_id
    )

    # Get the data as a DataFrame
    df = player_game_log_data.get_data_frames()[0]

    # Rename columns to match your PostgreSQL table column names
    df.rename(columns={
        'SEASON_YEAR': 'season_year',
        'PLAYER_ID': 'player_id',
        'PLAYER_NAME': 'player_name',
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
        'TOV': 'tov',
        'STL': 'stl',
        'BLK': 'blk',
        'BLKA': 'blka',
        'PF': 'pf',
        'PFD': 'pfd',
        'PTS': 'pts',
        'PLUS_MINUS': 'plus_minus',
        'NBA_FANTASY_PTS': 'nba_fantasy_pts',
        'DD2': 'dd2',
        'TD3': 'td3',
        'GP_RANK': 'gp_rank',
        'W_RANK': 'w_rank',
        'L_RANK': 'l_rank',
        'W_PCT_RANK': 'w_pct_rank',
        'MIN_RANK': 'min_rank',
        'FGM_RANK': 'fgm_rank',
        'FGA_RANK': 'fga_rank',
        'FG_PCT_RANK': 'fg_pct_rank',
        'FG3M_RANK': 'fg3m_rank',
        'FG3A_RANK': 'fg3a_rank',
        'FG3_PCT_RANK': 'fg3_pct_rank',
        'FTM_RANK': 'ftm_rank',
        'FTA_RANK': 'fta_rank',
        'FT_PCT_RANK': 'ft_pct_rank',
        'OREB_RANK': 'oreb_rank',
        'DREB_RANK': 'dreb_rank',
        'REB_RANK': 'reb_rank',
        'AST_RANK': 'ast_rank',
        'TOV_RANK': 'tov_rank',
        'STL_RANK': 'stl_rank',
        'BLK_RANK': 'blk_rank',
        'BLKA_RANK': 'blka_rank',
        'PF_RANK': 'pf_rank',
        'PFD_RANK': 'pfd_rank',
        'PTS_RANK': 'pts_rank',
        'PLUS_MINUS_RANK': 'plus_minus_rank',
        'NBA_FANTASY_PTS_RANK': 'nba_fantasy_pts_rank',
        'DD2_RANK': 'dd2_rank',
        'TD3_RANK': 'td3_rank'
    }, inplace=True)

    # Drop unnecessary columns not present in your PostgreSQL schema
    columns_to_drop = ['NICKNAME', 'WNBA_FANTASY_PTS', 'WNBA_FANTASY_PTS_RANK', 'AVAILABLE_FLAG', 'MIN_SEC']
    df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

    return df

# Function to delete the current season's records (full refresh behavior)
def delete_current_season_data(cursor, season_year):
    try:
        cursor.execute("DELETE FROM nba_api.playergamelogs__player_game_log WHERE season_year = %s", (season_year,))
        deleted_count = cursor.rowcount  # Get the number of deleted rows
        logging.info(f"Deleted {deleted_count} records for season {season_year}.")
    except Exception as e:
        logging.error(f"Error deleting current season data: {e}")

# Function to insert data into the PostgreSQL database
def insert_player_game_logs_to_db(df):
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

    # Full refresh: Delete existing records for the 2024-25 season
    season_year = "2024-25"
    
    # Delete the existing data
    delete_current_season_data(cursor, season_year)

    # Prepare the insert statement
    insert_query = """
        INSERT INTO nba_api.playergamelogs__player_game_log (
            season_year, player_id, player_name, team_id, team_abbreviation, team_name, game_id, game_date, matchup, wl, min,
            fgm, fga, fg_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct, oreb, dreb, reb, ast, tov, stl, blk, blka, pf, pfd, pts, 
            plus_minus, nba_fantasy_pts, dd2, td3, gp_rank, w_rank, l_rank, w_pct_rank, min_rank, fgm_rank, fga_rank, fg_pct_rank,
            fg3m_rank, fg3a_rank, fg3_pct_rank, ftm_rank, fta_rank, ft_pct_rank, oreb_rank, dreb_rank, reb_rank, ast_rank, 
            tov_rank, stl_rank, blk_rank, blka_rank, pf_rank, pfd_rank, pts_rank, plus_minus_rank, nba_fantasy_pts_rank, dd2_rank, td3_rank,
            created_at, modified_at
        ) VALUES (
            %(season_year)s, %(player_id)s, %(player_name)s, %(team_id)s, %(team_abbreviation)s, %(team_name)s, %(game_id)s, %(game_date)s, %(matchup)s, %(wl)s, %(min)s,
            %(fgm)s, %(fga)s, %(fg_pct)s, %(fg3m)s, %(fg3a)s, %(fg3_pct)s, %(ftm)s, %(fta)s, %(ft_pct)s, %(oreb)s, %(dreb)s, %(reb)s, %(ast)s, %(tov)s, %(stl)s, %(blk)s, 
            %(blka)s, %(pf)s, %(pfd)s, %(pts)s, %(plus_minus)s, %(nba_fantasy_pts)s, %(dd2)s, %(td3)s, %(gp_rank)s, %(w_rank)s, %(l_rank)s, %(w_pct_rank)s, 
            %(min_rank)s, %(fgm_rank)s, %(fga_rank)s, %(fg_pct_rank)s, %(fg3m_rank)s, %(fg3a_rank)s, %(fg3_pct_rank)s, %(ftm_rank)s, %(fta_rank)s, %(ft_pct_rank)s,
            %(oreb_rank)s, %(dreb_rank)s, %(reb_rank)s, %(ast_rank)s, %(tov_rank)s, %(stl_rank)s, %(blk_rank)s, %(blka_rank)s, %(pf_rank)s, %(pfd_rank)s, 
            %(pts_rank)s, %(plus_minus_rank)s, %(nba_fantasy_pts_rank)s, %(dd2_rank)s, %(td3_rank)s, NOW(), NOW()
        )
    """

    # Insert rows into the database
    for _, row in df.iterrows():
        row_data = row.to_dict()

        try:
            # Insert data
            cursor.execute(insert_query, row_data)
        except Exception as e:
            logging.error(f"Error inserting row: {row_data['player_name']}, game ID: {row_data['game_id']}, Error: {e}")

    # Commit the transaction and close the connection
    connection.commit()
    cursor.close()
    connection.close()
    logging.info(f"Inserted {len(df)} records into the database.")

# Main script
if __name__ == "__main__":
    # Fetch the player game log data
    game_log_df = fetch_player_game_logs()

    # Display the DataFrame columns to check for correct mapping
    logging.info(f"Columns in DataFrame: {game_log_df.columns}")

    # Write the game log data to the PostgreSQL database
    insert_player_game_logs_to_db(game_log_df)
