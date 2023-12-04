import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# AWS Credentials
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv('AWS_REGION')

# Cognito Config
USER_POOL_ID = os.getenv("USER_POOL_ID")
APP_CLIENT_ID = os.getenv("APP_CLIENT_ID")
APP_CLIENT_SECRET = os.getenv("APP_CLIENT_SECRET")

# Flask secret key(for signing cookies)
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")

# S3 Config
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")