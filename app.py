import os
import sqlite3
from flask import Flask
from app.routes.consumer_routes import consumer_bp
from app.routes.merchant_routes import merchant_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development_secret_key_here')
    
    # Ensure instance and uploads directories exist
    instance_path = os.path.join(os.path.dirname(__file__), 'instance')
    uploads_path = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    
    os.makedirs(instance_path, exist_ok=True)
    os.makedirs(uploads_path, exist_ok=True)
    
    app.register_blueprint(consumer_bp)
    app.register_blueprint(merchant_bp)
    
    return app

def init_db():
    app_dir = os.path.dirname(__file__)
    db_path = os.path.join(app_dir, 'instance', 'database.db')
    schema_path = os.path.join(app_dir, 'database', 'schema.sql')
    
    print(f"Initializing database at: {db_path}")
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
