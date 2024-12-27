import os

DATABASE_URI = os.getenv(
    'DATABASE_URI', 
    'sqlite:///reports.db'  # Default to SQLite for local testing
)
