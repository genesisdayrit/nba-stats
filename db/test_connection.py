import psycopg2
import os
from dotenv import load_dotenv, dotenv_values
import traceback

# Load the general environment variables from the main .env file
load_dotenv()

# Get the directory containing the .env files from the environment variable
env_dir = os.getenv('DB_BASE_DIR')

if not env_dir:
    print("ENV_DIR environment variable is not set.")
    exit(1)

# Prompt user to input the environment
environment = input("Please enter the environment (dev/staging/prod): ").strip().lower()

# Map environment input to corresponding .env file
env_files = {
    'dev': '.env.dev',
    'staging': '.env.staging',
    'prod': '.env.prod'
}

# Check if the environment is valid
if environment in env_files:
    env_file_path = os.path.join(env_dir, env_files[environment])
    
    # Load the environment variables from the specified .env file
    if os.path.exists(env_file_path):
        # Clear existing environment variables set by dotenv
        for key in dotenv_values(env_file_path).keys():
            os.environ.pop(key, None)
        
        # Load the new .env file
        load_dotenv(env_file_path)
    else:
        print(f"Environment file {env_file_path} does not exist.")
        exit(1)
else:
    print("Invalid environment. Please enter 'dev', 'staging', or 'prod'.")
    exit(1)

# Get connection parameters from environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Construct the PostgreSQL URL
postgres_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
print("PostgreSQL URL:", postgres_url)

connection = None
try:
    connection = psycopg2.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name
    )
    cursor = connection.cursor()
    
    # Fetch PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL")
    traceback.print_exc()
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
