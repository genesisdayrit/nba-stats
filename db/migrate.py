import os
import psycopg2
from dotenv import load_dotenv, dotenv_values

# Load the general environment variables from the main .env file
load_dotenv()

# Get the base directory for migration files from the environment variable
base_dir = os.getenv('DB_BASE_DIR')

if not base_dir:
    print("DB_BASE_DIR environment variable is not set.")
    exit(1)

def load_env(env):
    dotenv_path = os.path.join(base_dir, f".env.{env}")
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
migration_dir = os.path.join(base_dir, env, 'migrations')

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
