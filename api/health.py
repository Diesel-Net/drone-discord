from flask import Blueprint, request
from api.mongo import get_db
from datetime import datetime

health_check = Blueprint('health-check', __name__, url_prefix='')


@health_check.route('/health', methods=['GET'])
def healthy():
    user_agent = request.headers['User-Agent']
    timestamp = datetime.utcnow()
    ping = {
        'timestamp': timestamp,
        'msg': 'healthcheck',
        'userAgent': user_agent,
    }
    print(ping)
    get_db().health.insert_one(ping)
    pong = get_db().health.find_one({'timestamp': timestamp})
    return { 'status': 'Healthy',
             'timestamp': timestamp }, 200
