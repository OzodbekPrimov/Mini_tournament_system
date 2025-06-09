from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
