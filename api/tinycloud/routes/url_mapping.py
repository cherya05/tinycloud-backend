from flask import Blueprint, request, jsonify
from models.url_mapping import UrlMapping
from schemas.url_mapping import UrlSchema
from extensions import db
import secrets
import string
from datetime import datetime

url_bp = Blueprint('url', __name__, url_prefix='/url-mapping')

@url_bp.route('/', methods=['GET'])
def get_urls():
    url_mappings = UrlMapping.query.all()

    schema = UrlSchema(many=True)
    return jsonify(schema.dump(url_mappings))

@url_bp.route('/<id>', methods=['GET'])
def get_url(id):
    url_mapping = UrlMapping.query.filter_by(id=id).first()
    if url_mapping:
        return jsonify(UrlSchema().dump(url_mapping))
    else:
        return jsonify({'error': 'URL not found'}), 404

@url_bp.route('/', methods=['POST'])
def create_short_code():
    data = request.get_json()
    
    alphabet = string.ascii_letters + string.digits
    short_url = ''.join(secrets.choice(alphabet) for i in range(8))
    
    url_mapping = UrlMapping()
    url_mapping.long_url = data['long_url']
    url_mapping.short_url = short_url
    url_mapping.created_at = datetime.now()
    
    db.session.add(url_mapping)
    db.session.commit()
    
    schema = UrlSchema()
    return jsonify(schema.dump(url_mapping)), 201

@url_bp.route('/<id>', methods=['PUT'])
def update_url(id):
    data = request.get_json()

    url_mapping = UrlMapping.query.filter_by(id=id).first()


    if url_mapping:
        url_mapping.long_url = data['long_url']
        db.session.commit()
        return jsonify(UrlSchema().dump(url_mapping))
    else:
        return jsonify({'error': 'URL not found'}), 404

@url_bp.route('/<id>', methods=['DELETE'])
def delete_url(id):
    url_mapping = UrlMapping.query.filter_by(id=id).first()
    if url_mapping:
        db.session.delete(url_mapping)
        db.session.commit()
        return jsonify({'message': 'URL deleted successfully'}), 200
    else:
        return jsonify({'error': 'URL not found'}), 404

