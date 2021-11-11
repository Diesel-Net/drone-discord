import requests
import hashlib
import hmac
from flask import Blueprint, request
from api.mongo import get_db
from base64 import b64encode

receive_events = Blueprint('receive-events', __name__, url_prefix='')

def calculate_signature(key, signing_string):
    # drone signatures are calculated using hmac sha256
    return hmac.new(key, signing_string, hashlib.sha256).digest()


def verify_signature(key):
    # grab the signature from the header
    for part in request.headers['Signature'].split(','):
        if part[:11] == 'signature="':
            # removes the trailing '"'
            expected = part[11:-1]

    # https://tools.ietf.org/html/draft-cavage-http-signatures-10#section-2.3
    signing_string = f'date: { request.headers["Date"] }\ndigest: { request.headers["Digest"] }'

    # calculate hmac sha256 hash with 'key' and the raw request 'body'
    calculated = b64encode(
        calculate_signature(
            key.encode(),
            signing_string.encode(),
        )
    ).decode()
    
    print(f'Signature: {expected}\nCalculated: {calculated}')

    # equal?
    return hmac.compare_digest(expected, calculated)


@receive_events.route('/', methods=['POST', 'GET'])
def receive():
    if request.method == 'GET':
        get_db().test.insert_one(
            {
                'hello': 'world',
            }
        )
        
        return 'Hello, World!', 200