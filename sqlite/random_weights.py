import sqlite3
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Connect to the SQLite database and fetch data from 'int_player_game_stats'
def load_data():
    logging.info('Connecting to SQLite database...')
    conn = sqlite3.connect('nba-data.db')  # Change to your database path

    logging.info('Querying data from int_player_game_stats...')
    query = "SELECT * FROM int_player_game_stats"
    data = pd.read_sql_query(query, conn)

    logging.info('Closing database connection...')
    conn.close()

    logging.info(f'Data loaded successfully. Number of rows fetched: {len(data)}')
    return data

# Step 2: Filter players by minimum average minutes per game (at least 12 minutes)
def filter_min_minutes(data, min_minutes=12):
    logging.info(f'Filtering players with at least {min_minutes} minutes per game on average...')
    avg_minutes_per_player = data.groupby('display_first_last')['min'].mean()
    
    # Filter out players who played fewer than `min_minutes` on average
    valid_players = avg_minutes_per_player[avg_minutes_per_player >= min_minutes].index
    filtered_data = data[data['display_first_last'].isin(valid_players)]
    
    logging.info(f'Players remaining after filtering: {len(valid_players)}')
    return filtered_data

# Step 3: Calculate rolling averages for performance metrics and minutes
def calculate_rolling_avg(df, window=5):
    logging.info(f'Calculating rolling averages (window={window}) for player {df["display_first_last"].iloc[0]}...')
    df['Rolling Minutes'] = df['min'].rolling(window).mean()
    df['Rolling Points'] = df['pts'].rolling(window).mean()
    df['Rolling Assists'] = df['ast'].rolling(window).mean()
    df['Rolling Rebounds'] = df['reb'].rolling(window).mean()
    return df

# Step 4: Calculate growth rates for minutes and performance metrics
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

# Function to evaluate a set of weights and return a "score" based on ranking performance
def evaluate_weights(data, weights):
    # weights = [weight_points, weight_assists, weight_rebounds, weight_minutes]
    logging.info(f'Evaluating weights: {weights}')
    
    data['Improvement Score'] = (
        weights[0] * data['Points Growth'] + 
        weights[1] * data['Assists Growth'] + 
        weights[2] * data['Rebounds Growth'] + 
        weights[3] * data['Minutes Growth']
    )
    
    # Rank players based on the weighted scores
    ranked_players = data.groupby('display_first_last').agg({'Improvement Score': 'mean'}).sort_values(by='Improvement Score', ascending=False)
    
    # Evaluate the performance of this ranking (you can change this logic to fit your evaluation needs)
    # For example, return the ranking of a known player such as LeBron James
    target_player = 'LeBron James'
    rank = ranked_players.index.get_loc(target_player) if target_player in ranked_players.index else len(ranked_players)
    
    # The score is better when the player ranks higher (lower rank = better)
    return 1 / (rank + 1)

# Perform random search over different weight combinations
def random_search(data, num_iterations=100):
    best_score = -np.inf
    best_weights = None

    for i in range(num_iterations):
        # Generate random weights for Points, Assists, Rebounds, and Minutes (sum to 1)
        weights = np.random.dirichlet(np.ones(4), size=1).flatten()

        # Evaluate this set of weights
        score = evaluate_weights(data, weights)
        
        # Keep track of the best set of weights
        if score > best_score:
            best_score = score
            best_weights = weights

        logging.info(f'Iteration {i+1}/{num_iterations} - Score: {score} - Weights: {weights}')

    logging.info(f'Best score: {best_score} achieved with weights: {best_weights}')
    return best_weights

# Main function to execute all steps
def main():
    logging.info('Starting the analysis process...')
    
    # Load the data from SQLite database
    data = load_data()

    # Filter players by minimum average minutes played (at least 12 minutes per game)
    data = filter_min_minutes(data)

    # Apply rolling averages and growth rates
    logging.info('Applying rolling averages for all players...')
    data = data.groupby('display_first_last').apply(calculate_rolling_avg).reset_index(drop=True)
    
    logging.info('Calculating growth rates for all players...')
    data = data.groupby('display_first_last').apply(calculate_growth_rate).reset_index(drop=True)

    # Use random search to find the best set of weights
    best_weights = random_search(data)

    # Apply the best weights to calculate the final improvement score
    data['Improvement Score'] = (
        best_weights[0] * data['Points Growth'] +
        best_weights[1] * data['Assists Growth'] +
        best_weights[2] * data['Rebounds Growth'] +
        best_weights[3] * data['Minutes Growth']
    )

    # Rank players based on the final improvement score
    logging.info('Ranking players by improvement score...')
    ranked_players = data.groupby('display_first_last').agg({'Improvement Score': 'mean'}).sort_values(by='Improvement Score', ascending=False)

    # Display the top 10 players
    logging.info('Displaying top 10 players by improvement score:')
    print(ranked_players.head(10))

# Run the script
if __name__ == "__main__":
    main()

