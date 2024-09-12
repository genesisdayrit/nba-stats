import sqlite3

conn = sqlite3.connect('nba-data.db')

cursor = conn.cursor()

cursor.execute("SELECT name from sqlite_master WHERE type = 'table';")

cursor.execute("SELECT name from sqlite_master WHERE type = 'view';")

tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    print(table[0])

# Close the connection
conn.close()

