import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get Reddit API credentials
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Validate credentials
if not REDDIT_CLIENT_ID or not REDDIT_CLIENT_SECRET:
    print("Warning: Reddit API credentials not found in environment variables.")
    print("Please set REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET environment variables.")
    print("For testing, you can create a .env file in the project root with these variables.")
