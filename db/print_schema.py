import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Function to load environment variables
def load_env(env_file):
    # Clear any existing environment variables that might be cached
    os.environ.clear()
    load_dotenv(dotenv_path=env_file)

# Function to get database connection
def get_db_connection():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")

    connection = psycopg2.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=dbname
    )
    return connection

# Function to fetch and write schema information to a file
def print_schema_to_file(env, output_file):
    env_file = f".env.{env}"
    load_env(env_file)

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT table_schema, table_name, column_name, data_type 
    FROM information_schema.columns 
    WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
    ORDER BY table_schema, table_name, ordinal_position;
    """

    cursor.execute(query)
    results = cursor.fetchall()

    with open(output_file, 'w') as file:
        current_schema = ""
        current_table = ""
        for row in results:
            schema, table, column, data_type = row
            if schema != current_schema:
                current_schema = schema
                file.write(f"\nSchema: {schema}\n")
            if table != current_table:
                current_table = table
                file.write(f"  Table: {table}\n")
            file.write(f"    Column: {column} ({data_type})\n")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    env = input("Which environment (dev, staging, prod)?: ").strip()
    
    timestamp = datetime.now().strftime('%Y_%m_%d_%H%M%S')
    info_schema_dir = os.path.join(env, "info_schema")
    os.makedirs(info_schema_dir, exist_ok=True)
    
    output_file = os.path.join(info_schema_dir, f"{timestamp}_{env}_schema.txt")
    
    print_schema_to_file(env, output_file)
    print(f"Schema information has been written to {output_file}")
