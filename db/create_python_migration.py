import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the base directory for migration files from the environment variable
base_dir = os.getenv('DB_BASE_DIR')

# Check if DB_BASE_DIR is set
if not base_dir:
    print("Error: DB_BASE_DIR is not set. Please set it in your .env file.")
    exit(1)

# Prompt the user for the environment
env = input("Enter the environment (dev/staging/prod): ").strip()

# Validate the environment input
if env not in ['dev', 'staging', 'prod']:
    print("Invalid environment. Please enter one of 'dev', 'staging', or 'prod'.")
    exit(1)

# Directory to store migration files for the specified environment
migration_dir = os.path.join(base_dir, env, 'python_migrations')

# Ensure the migrations directory exists
if not os.path.exists(migration_dir):
    os.makedirs(migration_dir)

# Prompt the user for the migration name
migration_name = input("Enter the migration name: ").strip()

# Generate the timestamp in the format YYYY_MM_DD_HHMMSS
timestamp = datetime.now().strftime('%Y_%m_%d_%H%M%S')

# Create the migration filename
filename = f"{timestamp}_{migration_name}.py"

# Path to the new migration file
filepath = os.path.join(migration_dir, filename)

# Create an empty migration file
with open(filepath, 'w') as file:
    file.write("# Write your Python migration here\n")

print(f"Created migration file: {filepath}")
