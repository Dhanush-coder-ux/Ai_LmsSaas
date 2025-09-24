from google import genai
import os
from dotenv import load_dotenv


load_dotenv()

client = genai.Client(api_key=os.environ['GENAI_API_KEY'])




