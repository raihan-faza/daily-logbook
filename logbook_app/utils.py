import os

from dotenv import load_dotenv

api_key = os.getenv("API_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-very-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME = 3600
JWT_REFRESH_EXPIRATION = 7 * 3600
