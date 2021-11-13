import requests
import hashlib
import hmac
import json
import os
import re
from copy import deepcopy
from threading import Thread
from datetime import datetime
from flask import Blueprint, request
from api.mongo import get_db
from base64 import b64encode


drone_events = Blueprint('drone-events', __name__, url_prefix='')
key = os.getenv('DRONE_WEBHOOK_SECRET') 


def _process_user_event(payload):
    if payload['action'] == 'created':
        print('Event: User created')
    if payload['action'] == 'updated':
        print('Event: User updated')
    if payload['action'] == 'deleted':
        print('Event: User deleted')
        

def _process_repo_event(payload):
    if payload['action'] == 'enabled':
        print('Event: Repo enabled')
    if payload['action'] == 'disabled':
        print('Event: Repo disabled')


def _process_build_event(payload):
    if payload['action'] == 'created':
        print('Event: Build created')
    if payload['action'] == 'updated':
        print('Event: Build updated')


DRONE_EVENT_HANDLERS = {
    'user': _process_user_event,
    'repo': _process_repo_event,
    'build': _process_build_event,
}

def _construct_signature_string():
    # https://tools.ietf.org/html/draft-cavage-http-signatures-10#section-2.3
    signature_headers = re.search(
        r'^.*headers=\"(.*?)\"', 
        request.headers['Signature']
    ).group(1).split(' ')

    signing_string = ''
    for header in signature_headers:
        signing_string += f'{ header }: { request.headers.get(header) }\n'
    signing_string = signing_string[:-1]

    print(signing_string)
    return signing_string


def _calculate_signature(key, signing_string):
    # drone signatures are calculated using hmac sha256
    return hmac.new(key, signing_string, hashlib.sha256).digest()


def _verify_signature(key):
    # https://datatracker.ietf.org/doc/html/draft-cavage-http-signatures-12#section-2.5
    expected = re.search(
        r'^.*signature=\"([a-zA-Z1-9\/\+\=].*?)\"', 
        request.headers['Signature']
    ).group(1)

    calculated = b64encode(
        _calculate_signature(
            key.encode(),
            _construct_signature_string().encode(),
        )
    ).decode()
    
    print(f'Signature: {expected}\nCalculated: {calculated}')

    # equal?
    return hmac.compare_digest(expected, calculated)


@drone_events.route('/', methods=['POST'])
def post_events():
    print(f'{ request.headers }')
    print(f'{ json.dumps(request.json, indent=2) }')
    
    response = { 'timestamp': datetime.utcnow()}
    event = request.headers.get('X-Drone-Event')

    if not _verify_signature(key):
        response['message'] = 'Invalid Signature'
        return response, 403

    if not event in DRONE_EVENT_HANDLERS.keys():
        response['message'] = 'Invalid payload'
        return response, 400

    Thread(
        target=DRONE_EVENT_HANDLERS[event], 
        kwargs={'payload': deepcopy(request.json) }
    ).start()
    response['message'] = 'Job queued'
    return response, 200
