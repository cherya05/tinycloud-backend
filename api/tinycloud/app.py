import os
from flask import Flask
from flask_restful import Api
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from .extensions import db
from .routes.url_mapping import url_bp

def create_app():
    app = Flask(__name__)
    
    user = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    hostname = os.getenv('POSTGRES_HOST')
    name = os.getenv('POSTGRES_DB')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{hostname}:5432/{name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    
    app.register_blueprint(url_bp)
    
    migrate = Migrate(app, db)
    
    api = Api(app)

    return app

app = create_app()
base = DeclarativeBase()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)