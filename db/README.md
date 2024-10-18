Project Documentation
Overview
This repository is designed to manage database migrations for different environments (dev, staging, and prod). It includes scripts for creating new migrations and applying them to the database. The project structure and script functionalities are detailed below. This setup attempts to simulate the Laravel framework for database migrations.

Project Structure
php
Copy code
<DB_BASE_DIR>/
├── .env.dev
├── .env.prod
├── .env.staging
├── create_migration.py
├── dev
│   └── migrations
│       ├── 2024_07_02_205342_create_test_table.sql
│       └── 2024_07_02_211504_add_auth_and_tally_schemas.sql
├── migrate.py
├── prod
│   └── migrations
├── requirements.txt
├── rollback.py
├── staging
│   └── migrations
└── test_connection.py
Environment Setup
Each environment (dev, staging, prod) has its own .env file to store environment-specific variables:

.env.dev
.env.prod
.env.staging
These files should include the following variables:

makefile
Copy code
DB_NAME=<database_name>
DB_USER=<database_user>
DB_PASSWORD=<database_password>
DB_HOST=<database_host>
DB_PORT=<database_port>
Additionally, you need to set the DB_BASE_DIR environment variable in your main .env file:

javascript
Copy code
DB_BASE_DIR=/path/to/your/db/directory
Scripts
1. create_migration.py
This script creates a new SQL migration file with a timestamp and a specified name.

How to Use:
Navigate to the project directory:
sh
Copy code
cd <DB_BASE_DIR>
Run the script:
sh
Copy code
python create_migration.py
Enter the environment when prompted (dev, staging, or prod).
Enter the migration name when prompted.
A new migration file will be created in the specified environment's migrations directory with a template for SQL commands.

Script Content:
python
Copy code
import os
from datetime import datetime

# Base directory for migration files
base_dir = os.getenv('DB_BASE_DIR')

# Prompt the user for the environment
env = input("Enter the environment (dev/staging/prod): ").strip()

# Validate the environment input
if env not in ['dev', 'staging', 'prod']:
    print("Invalid environment. Please enter one of 'dev', 'staging', or 'prod'.")
    exit(1)

# Directory to store migration files for the specified environment
migration_dir = os.path.join(base_dir, env, 'migrations')

# Ensure the migrations directory exists
if not os.path.exists(migration_dir):
    os.makedirs(migration_dir)

# Prompt the user for the migration name
migration_name = input("Enter the migration name: ").strip()

# Generate the timestamp in the format YYYY_MM_DD_HHMMSS
timestamp = datetime.now().strftime('%Y_%m_%d_%H%M%S')

# Create the migration filename
filename = f"{timestamp}_{migration_name}.sql"

# Path to the new migration file
filepath = os.path.join(migration_dir, filename)

# Create an empty migration file
with open(filepath, 'w') as file:
    file.write("-- Write your SQL migration here\n")

print(f"Created migration file: {filepath}")
2. migrate.py
This script applies all pending migrations to the database.

How to Use:
Navigate to the project directory:
sh
Copy code
cd <DB_BASE_DIR>
Run the script:
sh
Copy code
python migrate.py
Enter the environment when prompted (dev, staging, or prod).
The script will connect to the specified database, check for already applied migrations, and apply any new migrations in the correct order.

Script Content:
python
Copy code
import os
import psycopg2
from dotenv import load_dotenv, dotenv_values

def load_env(env):
    dotenv_path = os.path.join(os.getenv('DB_BASE_DIR'), f".env.{env}")
    if os.path.exists(dotenv_path):
        # Clear existing environment variables set by dotenv
        for key in dotenv_values(dotenv_path).keys():
            os.environ.pop(key, None)
        
        # Load the new .env file
        load_dotenv(dotenv_path)
    else:
        print(f"Environment file {dotenv_path} not found.")
        exit(1)

def connect_to_db():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )

def ensure_migrations_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS migrations (
        id SERIAL PRIMARY KEY,
        filename VARCHAR(255) UNIQUE NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    ''')

def get_applied_migrations(cursor):
    cursor.execute('SELECT filename FROM migrations')
    return [row[0] for row in cursor.fetchall()]

def apply_migrations(cursor, migration_files):
    for migration_file in migration_files:
        if migration_file not in applied_migrations:
            print(f'Applying {migration_file}...')
            with open(migration_file, 'r') as file:
                sql_commands = file.read()
                cursor.execute(sql_commands)
                cursor.execute('INSERT INTO migrations (filename) VALUES (%s)', (migration_file,))
                connection.commit()
            print(f'Applied {migration_file}')
        else:
            print(f'Skipping {migration_file} (already applied)')

# Prompt for environment
env = input("Enter the environment (dev/staging/prod): ").strip()

# Load environment variables
load_env(env)

# Directory to store migration files for the specified environment
migration_dir = os.path.join(os.getenv('DB_BASE_DIR'), env, 'migrations')

# Connect to the PostgreSQL database
connection = connect_to_db()
cursor = connection.cursor()

# Ensure migrations table exists to track applied migrations
ensure_migrations_table(cursor)
connection.commit()

# Get the list of already applied migrations
applied_migrations = get_applied_migrations(cursor)

# Get the list of all migration files
migration_files = sorted(
    os.path.join(migration_dir, f) for f in os.listdir(migration_dir) if f.endswith('.sql')
)

# Apply each migration in order if it hasn't been applied yet
apply_migrations(cursor, migration_files)

# Close the cursor and connection
cursor.close()
connection.close()
Additional Scripts
rollback.py
This script can be used to roll back the last applied migration. Ensure you modify it according to your specific needs.

print_schema.py
This script connects to the specified AWS RDS Postgres database and prints out the information schema to a text file, excluding the information_schema and pg_catalog schemas. The output is saved in the info_schema directory, organized by environment (dev, staging, prod), and prefixed with a timestamp.

How to Use:
Navigate to the project directory:
sh
Copy code
cd <DB_BASE_DIR>
Run the script:
sh
Copy code
python print_schema.py
Enter the environment when prompted (dev, staging, or prod).
The script will:

Load the corresponding environment variables.
Connect to the database.
Retrieve the schema information (excluding information_schema and pg_catalog).
Write the schema information to a text file in the info_schema directory with the format {timestamp}_{env}_schema.txt.
Script Content:
python
Copy code
import os
import psycopg2
from dotenv import load_dotenv
from datetime import datetime

# Function to load environment variables
def load_env(env_file):
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
    env_file = os.path.join(os.getenv('DB_BASE_DIR'), f".env.{env}")
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
    info_schema_dir = os.path.join("info_schema", env)
    os.makedirs(info_schema_dir, exist_ok=True)
    
    output_file = os.path.join(info_schema_dir, f"{timestamp}_{env}_schema.txt")
    
    print_schema_to_file(env, output_file)
    print(f"Schema information has been written to {output_file}")
This updated README.md now uses <DB_BASE_DIR> as a placeholder for the base directory path, making it clear where the environment variable is used.