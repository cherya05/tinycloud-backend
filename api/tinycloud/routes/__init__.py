from flask import Blueprint
from routes.url_mapping import url_bp

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(url_bp, url_prefix='/url')