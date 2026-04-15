import os
from flask import Flask, jsonify
from flask_restful import Api
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from .extensions import db
from .routes.url_mapping import url_bp
from .config import Config
from flask_cors import CORS
from .services.elasticsearch_service import ElasticsearchService
from .services.metrics import init_metrics, metrics_bp


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    if not app.config["TESTING"]:
        es_service = ElasticsearchService()
        app.config["ELASTICSEARCH_SERVICE"] = es_service

    db.init_app(app)
    app.register_blueprint(url_bp)
    app.register_blueprint(metrics_bp)
    CORS(app)
    init_metrics(app)

    @app.route('/')
    def index():
        return jsonify({}), 200

    migrate = Migrate(app, db, directory=os.path.join(os.path.dirname(__file__), 'migrations'))
    
    api = Api(app)

    return app

base = DeclarativeBase()

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)
