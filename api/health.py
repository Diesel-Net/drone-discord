from flask import Blueprint, request
from api.mongo import get_db
from datetime import datetime

health_check = Blueprint('health-check', __name__, url_prefix='')


@health_check.route('/health', methods=['GET'])
def get_health():
    user_agent = request.headers['User-Agent']
    timestamp = datetime.utcnow()
    record = {
        'timestamp': timestamp,
        'userAgent': user_agent,
    }
    database = get_db() 
    database.health.insert_one(record)
    database.health.delete_one({'timestamp': timestamp})
    return { 'message': 'Healthy',
             'timestamp': timestamp }, 200
