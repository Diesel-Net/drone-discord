import os
import requests
from api.mongo import get_db


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
DISCORD_API_BASE_URL = os.getenv('DISCORD_API_BASE_URL') or 'https://discord.com/api'
DISCORD_MESSAGES_API = f'{ DISCORD_API_BASE_URL }/channels/{ DISCORD_CHANNEL_ID }/messages'

HEADERS = {
    'Authorization': f'Bot { DISCORD_TOKEN }'
}

# TODO: Deal with API rate limiting


def _create_message(payload):
    try:
        response = requests.post(
            headers = HEADERS,
            url = DISCORD_MESSAGES_API,
            json = payload,
        )
        
        assert response.status_code == 200      

    except Exception as ex:
        print('discord: create_message() failure')
        print(ex)

    return response

def _edit_message(payload, message_id):
    try:
        response = requests.patch(
            headers = HEADERS,
            url = f'{ DISCORD_MESSAGES_API }/{ message_id }',
            json = payload,
        )
        
        assert response.status_code == 200      

    except Exception as ex:
        print('discord: edit_message() failure')
        print(ex)

    return response

def post_user_created(request):
    
    payload = {
        'content': 'hello, world!'
    }

    _create_message(payload)


def post_user_updated(request):
    pass


def post_user_deleted(request):
    pass


def post_repo_enabled(request):
    pass


def post_repo_disabled(request):
    pass


def post_build_created(request):
    pass


def post_build_updated(request):
    pass
