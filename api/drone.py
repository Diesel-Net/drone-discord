import requests
import hashlib
import hmac
import json
import os
import re
from copy import deepcopy
from threading import Thread
from datetime import datetime
from base64 import b64encode
from flask import Blueprint, request, current_app
from api.mongo import get_database
from api import discord


drone_events = Blueprint('drone-events', __name__, url_prefix='')
KEY = os.getenv('DRONE_WEBHOOK_SECRET') 


DRONE_EVENT_HANDLERS = {
    'user': {
        'created': discord.post_user_created,
        'deleted': discord.post_user_deleted,
    },
    'repo': {
        'enabled': discord.post_repo_enabled,
        'disabled': discord.post_repo_disabled,
    },
    'build': {
        'created': discord.post_build_created,
        'updated': discord.post_build_updated,
    }
}

def _construct_signature_string(headers):
    # https://tools.ietf.org/html/draft-cavage-http-signatures-10#section-2.3
    match = re.search(
        r'^.*headers=\"(.*?)\"', 
        headers.get('Signature', '')
    )

    if not match:
        return False

    signature_headers = match.group(1).split(' ')

    signing_string = ''
    for header in signature_headers:
        signing_string += f'{ header }: { headers.get(header) }\n'
    signing_string = signing_string[:-1]

    print(signing_string)
    return signing_string


def _calculate_signature(key, signing_string):
    # drone signatures are calculated using hmac sha256
    return hmac.new(key, signing_string, hashlib.sha256).digest()


def _verify_signature(key, headers):
    # https://datatracker.ietf.org/doc/html/draft-cavage-http-signatures-12#section-2.5
    match = re.search(
        r'^.*signature=\"([a-zA-Z1-9\/\+\=].*?)\"', 
        headers.get('Signature', '')
    )

    if not match:
        return False

    expected = match.group(1)

    calculated = b64encode(
        _calculate_signature(
            key.encode(),
            _construct_signature_string(headers).encode(),
        )
    ).decode()
    
    print(f'Signature: {expected}\nCalculated: {calculated}')

    # equal?
    return hmac.compare_digest(expected, calculated)


@drone_events.route('/', methods=['POST'])
def post_events():
    #print(request.headers)
    #print(json.dumps(request.json, indent=2))
    
    response = { 'timestamp': datetime.utcnow() }
    event = request.headers.get('X-Drone-Event')
    action = DRONE_EVENT_HANDLERS.get(event).get(request.json['action'])

    if not _verify_signature(KEY, request.headers):
        response['message'] = 'Invalid signature'
        return response, 403

    if not callable(action) or event != request.json['event']:
        response['message'] = 'Invalid payload'
        return response, 400

    Thread(
        target=action, 
        kwargs={
            'current_app': current_app._get_current_object(),
            'payload': deepcopy(request.json),
        },
    ).start()

    response['message'] = 'Job queued'

    return response, 200
