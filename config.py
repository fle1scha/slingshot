import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ENVIRONMENT = os.getenv('FLASK_ENV', 'development')

    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_CHARSET = os.getenv('MYSQL_CHARSET', 'utf8mb4')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')

    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

    @classmethod
    def validate(cls):
        mandatory_envvars = ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'DB_NAME', 
                          'DB_USER', 'DB_PASSWORD', 'TWILIO_ACCOUNT_SID', 
                          'TWILIO_AUTH_TOKEN', 'TWILIO_PHONE_NUMBER']

        for var_name in mandatory_envvars:
            if not getattr(cls, var_name):
                raise RuntimeError(f"The environment variable '{var_name}' is missing.")