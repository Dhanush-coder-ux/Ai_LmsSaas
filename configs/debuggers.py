from dotenv import load_dotenv
import os
load_dotenv()


api_key,client_secrets  = os.getenv('DE_BUGGERS_API_KEY'),os.getenv('DE_BUGGER_CLIENT_SECRET')
debuggers_baseurl = "https://auth-debuugers.com"