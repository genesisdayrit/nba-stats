import sqlite3

conn = sqlite3.connect('nba-data.db')

cursor = conn.cursor()

cursor.execute("SELECT * FROM int_player_game_stats limit 10;")

results = cursor.fetchall()

for row in results:
    print(row)

conn.close
