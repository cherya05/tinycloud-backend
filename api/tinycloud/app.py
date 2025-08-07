import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_restful import Api
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from extensions import db
from routes.url_mapping import url_bp

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def wait_for_db():
    import time
    from sqlalchemy.exc import OperationalError
    
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            with app.app_context():
                db.engine.connect()
                print("Database connection successful!")
                return True
        except OperationalError:
            print(f"Database not ready, attempt {attempt + 1}/{max_attempts}")
            time.sleep(2)
    
    print("Failed to connect to database after all attempts")
    return False

# Wait for database to be ready
if wait_for_db():
    with app.app_context():
        db.create_all()

app.register_blueprint(url_bp)

@app.route('/')
def health_check():
    return jsonify({"status": "healthy"})

migrate = Migrate(app, db)
base = DeclarativeBase()

api = Api(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
