from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///absconding.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes import employees, alerts, analytics, vector_db, n8n_webhooks
    app.register_blueprint(employees.bp)
    app.register_blueprint(alerts.bp)
    app.register_blueprint(analytics.bp)
    app.register_blueprint(vector_db.bp)
    app.register_blueprint(n8n_webhooks.bp)
    
    # Create tables
    with app.app_context():
        db.create_all()
        # Initialize Vector DB on startup
        try:
            from app.services.vector_store import get_vector_store
            vector_store = get_vector_store()
            stats = vector_store.get_collection_stats()
            print(f"✓ Vector DB initialized")
            print(f"  Collections: {stats}")
        except Exception as e:
            print(f"⚠️  Vector DB initialization warning: {e}")
    
    return app