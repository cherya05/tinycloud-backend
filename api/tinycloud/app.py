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

app.register_blueprint(url_bp)

@app.route('/')
def health_check():
    return jsonify({"status": "healthy"})

migrate = Migrate(app, db)
base = DeclarativeBase()

api = Api(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

