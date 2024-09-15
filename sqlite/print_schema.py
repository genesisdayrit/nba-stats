import sqlite3

def get_tables_and_views(cursor):
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Get all views
    cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
    views = cursor.fetchall()

    return tables, views

def get_table_schema(cursor, table_name):
    cursor.execute(f"PRAGMA table_info('{table_name}');")
    return cursor.fetchall()

def write_schema_to_file(file, name, schema):
    file.write(f"Schema for {name}:\n")
    file.write("Column Name | Data Type | Not Null | Primary Key\n")
    file.write("-" * 50 + "\n")
    for column in schema:
        file.write(f"{column[1]} | {column[2]} | {column[3]} | {column[5]}\n")
    file.write("\n")

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('nba-data.db')
    cursor = conn.cursor()

    # Get all tables and views
    tables, views = get_tables_and_views(cursor)

    # Open the file to write the schema
    with open("database_schema.txt", "w") as file:
        # Process tables
        file.write("Tables:\n")
        file.write("=" * 50 + "\n")
        for table in tables:
            table_name = table[0]
            schema = get_table_schema(cursor, table_name)
            write_schema_to_file(file, table_name, schema)

        # Process views
        file.write("Views:\n")
        file.write("=" * 50 + "\n")
        for view in views:
            view_name = view[0]
            schema = get_table_schema(cursor, view_name)
            write_schema_to_file(file, view_name, schema)

    # Close the database connection
    conn.close()
    print("Database schema has been written to 'database_schema.txt'.")

if __name__ == "__main__":
    main()

