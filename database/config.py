import os

# Use SQLite for development (default to SQLite if no environment variable is set)
DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///reports.db')
