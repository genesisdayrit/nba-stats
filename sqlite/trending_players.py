import sqlite3
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Connect to the SQLite database and fetch data from 'int_player_game_stats'
def load_data():
    logging.info('Connecting to SQLite database...')
    conn = sqlite3.connect('nba-data.db')  # Updated to query from nba-data.db

    logging.info('Querying data from int_player_game_stats...')
    query = "SELECT * FROM int_player_game_stats"
    data = pd.read_sql_query(query, conn)

    logging.info('Closing database connection...')
    conn.close()

    logging.info(f'Data loaded successfully. Number of rows fetched: {len(data)}')
    return data

# Step 2: Calculate rolling averages for performance metrics and minutes
def calculate_rolling_avg(df, window=5):
    logging.info(f'Calculating rolling averages (window={window}) for player {df["display_first_last"].iloc[0]}...')
    df['Rolling Minutes'] = df['min'].rolling(window).mean()
    df['Rolling Points'] = df['pts'].rolling(window).mean()
    df['Rolling Assists'] = df['ast'].rolling(window).mean()
    df['Rolling Rebounds'] = df['reb'].rolling(window).mean()
    return df

# Step 3: Calculate growth rates for minutes and performance metrics
def calculate_growth_rate(df):
    logging.info(f'Calculating growth rates for player {df["display_first_last"].iloc[0]}...')

    # Calculate percentage change with a cap on extreme values (-200% to +200%)
    df['Minutes Growth'] = df['min'].pct_change().clip(-2, 2)
    df['Points Growth'] = df['pts'].pct_change().clip(-2, 2)
    df['Assists Growth'] = df['ast'].pct_change().clip(-2, 2)
    df['Rebounds Growth'] = df['reb'].pct_change().clip(-2, 2)

    # Replace inf and -inf with NaN for proper handling
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    return df

# Step 4: Create a composite improvement score based on growth rates
def calculate_improvement_score(df):
    logging.info(f'Calculating improvement score for player {df["display_first_last"].iloc[0]}...')
    
    # Weighted improvement score focusing more on points, assists, and rebounds
    df['Improvement Score'] = (
        0.4 * df['Points Growth'] + 
        0.2 * df['Assists Growth'] + 
        0.2 * df['Rebounds Growth'] + 
        0.2 * df['Minutes Growth']
    )
    return df

# Step 5: Rank players based on improvement score, with a filter for minimum games played
def rank_players(data):
    logging.info('Dropping rows with NaN values...')
    data_clean = data.dropna()

    logging.info('Filtering out players with fewer than 10 games played...')
    game_counts = data_clean.groupby('display_first_last').size()
    filtered_players = game_counts[game_counts >= 10].index
    data_clean = data_clean[data_clean['display_first_last'].isin(filtered_players)]

    logging.info('Grouping data by player and calculating mean improvement score...')
    ranked_players = data_clean.groupby('display_first_last').agg({'Improvement Score': 'mean'}).sort_values(by='Improvement Score', ascending=False)

    logging.info(f'Ranking completed. Number of players ranked: {len(ranked_players)}')
    return ranked_players

# Main function to execute all steps
def main():
    logging.info('Starting the analysis process...')

    # Load the data from SQLite database
    data = load_data()

    # Apply rolling averages
    logging.info('Applying rolling averages for all players...')
    data = data.groupby('display_first_last').apply(calculate_rolling_avg).reset_index(drop=True)

    # Calculate growth rates for each player
    logging.info('Calculating growth rates for all players...')
    data = data.groupby('display_first_last').apply(calculate_growth_rate).reset_index(drop=True)

    # Calculate improvement scores
    logging.info('Calculating improvement scores for all players...')
    data = calculate_improvement_score(data)

    # Rank players by improvement score
    logging.info('Ranking players by improvement score...')
    ranked_players = rank_players(data)

    # Display the top 10 players
    logging.info('Displaying top 10 players by improvement score:')
    print(ranked_players.head(10))

# Run the script
if __name__ == "__main__":
    main()

