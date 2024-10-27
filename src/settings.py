from dotenv import load_dotenv
import os

class Settings:
    def __init__(self):
        load_dotenv(".env")

        self.aws_default_region = os.getenv("AWS_DEFAULT_REGION")
        self.cognito_user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
        self.cognito_app_client_id = os.getenv("COGNITO_APP_CLIENT_ID")

settingObj = Settings()