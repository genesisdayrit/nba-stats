import os
import psycopg2
from nba_api.stats.endpoints import scoreboardv2, boxscoretraditionalv2
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv('.env')

# Function to check if a player record exists in the database
def player_record_exists(cursor, game_id, player_id):
    cursor.execute("""
        SELECT 1 FROM nba_api_scoreboard_v2.player_game_stats 
        WHERE game_id = %(game_id)s AND player_id = %(player_id)s
    """, {'game_id': game_id, 'player_id': player_id})
    return cursor.fetchone() is not None

# Function to insert or update player stats in PostgreSQL
def insert_player_stats_to_db(game_date):
    # Fetch database connection details from environment variables
    db_config = {
        'host': os.getenv('DB_HOST'),
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'port': os.getenv('DB_PORT')
    }

    print(f"Connecting to database {db_config['dbname']} at {db_config['host']}...")

    # Establish connection to the PostgreSQL database
    try:
        connection = psycopg2.connect(
            host=db_config['host'],
            database=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password'],
            port=db_config['port']
        )
        cursor = connection.cursor()
        print("Database connection established.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return

    # Fetch scoreboard data for the provided game date
    print(f"Fetching games for date: {game_date}...")
    try:
        scoreboard = scoreboardv2.ScoreboardV2(game_date=game_date)
        games = scoreboard.get_normalized_dict()['GameHeader']
        print(f"Found {len(games)} games.")
    except Exception as e:
        print(f"Error fetching scoreboard data: {e}")
        cursor.close()
        connection.close()
        return

    # Check if there are any games from the provided date
    if len(games) > 0:
        for game in games:
            game_id = game['GAME_ID']
            print(f"Processing game ID: {game_id}...")
            try:
                boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
                player_stats = boxscore.player_stats.get_dict()
            except Exception as e:
                print(f"Error fetching box score data for game {game_id}: {e}")
                continue

            headers = player_stats['headers']
            data = player_stats['data']

            for player in data:
                player_data = dict(zip(headers, player))
                db_player_data = {
                    'game_id': player_data['GAME_ID'],
                    'team_id': player_data['TEAM_ID'],
                    'team_abbreviation': player_data['TEAM_ABBREVIATION'],
                    'team_city': player_data['TEAM_CITY'],
                    'player_id': player_data['PLAYER_ID'],
                    'player_name': player_data['PLAYER_NAME'],
                    'start_position': player_data['START_POSITION'],
                    'comment': player_data['COMMENT'],
                    'min': player_data['MIN'],
                    'fgm': player_data['FGM'],
                    'fga': player_data['FGA'],
                    'fg_pct': player_data['FG_PCT'],
                    'fg3m': player_data['FG3M'],
                    'fg3a': player_data['FG3A'],
                    'fg3_pct': player_data['FG3_PCT'],
                    'ftm': player_data['FTM'],
                    'fta': player_data['FTA'],
                    'ft_pct': player_data['FT_PCT'],
                    'oreb': player_data['OREB'],
                    'dreb': player_data['DREB'],
                    'reb': player_data['REB'],
                    'ast': player_data['AST'],
                    'stl': player_data['STL'],
                    'blk': player_data['BLK'],
                    'tos': player_data['TO'], 
                    'pf': player_data['PF'],
                    'pts': player_data['PTS'],
                    'plus_minus': player_data['PLUS_MINUS']
                }

                try:
                    # Check if the player record exists
                    if player_record_exists(cursor, db_player_data['game_id'], db_player_data['player_id']):
                        print(f"Updating stats for player: {db_player_data['player_name']} (ID: {db_player_data['player_id']})")
                        cursor.execute("""
                            UPDATE nba_api_scoreboard_v2.player_game_stats
                            SET team_id = %(team_id)s, team_abbreviation = %(team_abbreviation)s, team_city = %(team_city)s,
                                player_name = %(player_name)s, start_position = %(start_position)s, comment = %(comment)s, min = %(min)s,
                                fgm = %(fgm)s, fga = %(fga)s, fg_pct = %(fg_pct)s, fg3m = %(fg3m)s, fg3a = %(fg3a)s, fg3_pct = %(fg3_pct)s,
                                ftm = %(ftm)s, fta = %(fta)s, ft_pct = %(ft_pct)s, oreb = %(oreb)s, dreb = %(dreb)s, reb = %(reb)s,
                                ast = %(ast)s, stl = %(stl)s, blk = %(blk)s, tos = %(tos)s, pf = %(pf)s, pts = %(pts)s, plus_minus = %(plus_minus)s,
                                record_last_modified_at = CURRENT_TIMESTAMP
                            WHERE game_id = %(game_id)s AND player_id = %(player_id)s
                        """, db_player_data)
                    else:
                        print(f"Inserting new stats for player: {db_player_data['player_name']} (ID: {db_player_data['player_id']})")
                        cursor.execute("""
                            INSERT INTO nba_api_scoreboard_v2.player_game_stats (
                                game_id, team_id, team_abbreviation, team_city, player_id, player_name,
                                start_position, comment, min, fgm, fga, fg_pct, fg3m, fg3a, fg3_pct,
                                ftm, fta, ft_pct, oreb, dreb, reb, ast, stl, blk, tos, pf, pts, plus_minus,
                                record_created_at, record_last_modified_at
                            ) VALUES (%(game_id)s, %(team_id)s, %(team_abbreviation)s, %(team_city)s, %(player_id)s, %(player_name)s,
                                      %(start_position)s, %(comment)s, %(min)s, %(fgm)s, %(fga)s, %(fg_pct)s, %(fg3m)s, %(fg3a)s, %(fg3_pct)s,
                                      %(ftm)s, %(fta)s, %(ft_pct)s, %(oreb)s, %(dreb)s, %(reb)s, %(ast)s, %(stl)s, %(blk)s, %(tos)s, %(pf)s,
                                      %(pts)s, %(plus_minus)s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        """, db_player_data)

                except Exception as e:
                    connection.rollback()
                    print(f"Error inserting/updating player: {db_player_data['player_name']} for game {game_id}: {e}")

    else:
        print(f"No games found for the date: {game_date}.")

    connection.commit()
    cursor.close()
    connection.close()
    print("Database connection closed.")

# Example usage:
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
print(f"Starting data insertion for {yesterday}...")
insert_player_stats_to_db(yesterday)
print("Data insertion completed.")
