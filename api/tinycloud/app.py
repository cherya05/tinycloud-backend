import os
from flask import Flask
from flask_restful import Api
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from .extensions import db
from .routes.url_mapping import url_bp
from .services.elasticsearch_service import ElasticsearchService
from .services.metrics import init_metrics, metrics_bp

def create_app():
    app = Flask(__name__)
    
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    hostname = os.getenv('DB_HOST')
    name = os.getenv('DB_NAME')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{hostname}:5432/{name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    es_service = ElasticsearchService()
    app.config['ELASTICSEARCH_SERVICE'] = es_service

    db.init_app(app)
    app.register_blueprint(url_bp)
    app.register_blueprint(metrics_bp)
    init_metrics(app)
    
    migrate = Migrate(app, db, directory='api/tinycloud/migrations')
    
    api = Api(app)

    return app

app = create_app()
base = DeclarativeBase()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)