# Configuración de base de datos 
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def init_app(app):
    """Initialize the database with the application."""
    db.init_app(app)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()