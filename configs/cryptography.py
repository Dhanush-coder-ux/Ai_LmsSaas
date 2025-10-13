import os
from dotenv import load_dotenv

load_dotenv()
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')
