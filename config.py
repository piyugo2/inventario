# Archivo de configuración 
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration class."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-pharmacy-inventory'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///pharmacy_inventory.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True
    
class ProductionConfig(Config):
    """Configuration for production environment."""
    DEBUG = False
    
# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}