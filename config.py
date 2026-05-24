import os
from dotenv import load_dotenv

load_dotenv()

CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
WORDPRESS_URL = os.getenv('WORDPRESS_URL')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD')
CANVA_API_KEY = os.getenv('CANVA_API_KEY')

# Validation
if not all([CLAUDE_API_KEY, NOTION_API_KEY, NOTION_DATABASE_ID, WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD, CANVA_API_KEY]):
    raise ValueError('Missing required environment variables. Check .env file.')
