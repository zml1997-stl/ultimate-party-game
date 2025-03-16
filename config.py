import os

class Config:
    """Base configuration class with default settings."""
    # Secret key for session management and security (override in production via env var)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default-secret-key-for-dev-only')

    # Flask-SocketIO settings
    SOCKETIO_MESSAGE_QUEUE = os.environ.get('SOCKETIO_MESSAGE_QUEUE', None)  # Optional for scaling

    # Debug mode (disable in production)
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'

    # Environment variable to determine if running on Heroku
    IS_HEROKU = os.environ.get('IS_HEROKU', 'False') == 'True'

class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True

class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False

# Select configuration based on environment variable or default to Production
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

# Load the appropriate config based on FLASK_ENV, defaulting to production
env = os.environ.get('FLASK_ENV', 'production')
app_config = config_map.get(env, ProductionConfig)