"""Flask configuration variables."""

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    SECRET_KEY = 'secret_key'
    FLASK_APP = 'wsgi.py'
    FLASK_ENV = 'development'

    # Database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/medication_transfer_service'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False