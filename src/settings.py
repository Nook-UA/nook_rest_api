from dotenv import load_dotenv
import os

class Settings:
    def __init__(self):
        load_dotenv(".env")

        # Configs for authentication using AWS Cognito
        self.aws_default_region = os.getenv("AWS_DEFAULT_REGION")
        self.cognito_user_pool_id = os.getenv("COGNITO_USER_POOL_ID")
        self.cognito_app_client_id = os.getenv("COGNITO_APP_CLIENT_ID")

        # Configs for database connection
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_name = os.getenv("DB_NAME")

settingObj = Settings()