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

COLORS = {
    'green': 0x38af28,
    'yellow': 0xddb231,
    'red': 0xb51c1c,
}

# TODO: 
#   - Deal with Emebed limits
#   - Deal with API rate limiting


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
    
    user = request.get('user')
    system = request.get('system')

    payload = {
        'embeds': [
            {
              "type": "rich",
              "title": 'User created',
              "description": 'A new user was created',
              "color": COLORS['green'],
              "fields": [
                {
                  "name": 'username',
                  "value": user.get('login'),
                  "inline": True
                },
                {
                  "name": 'active',
                  "value": 'yes' if user.get('active') else 'no',
                  "inline": True
                },
                {
                  "name": 'type',
                  "value": 'Machine' if user.get('machine') else 'User',
                  "inline": True
                },
                {
                  "name": 'role',
                  "value": 'Admin' if user.get('admin') else 'Member',
                  "inline": True
                },
                {
                  "name": 'created',
                  "value": user.get('created'),
                  "inline": True,
                },
                {
                  "name": 'last login',
                  "value": f"{user.get('last_login') } days ago",
                  "inline": True,
                }
              ],
              "thumbnail": {
                "url": user.get('avatar'),
                "height": 0,
                "width": 0
              },
              "footer": {
                "text": system.get('host'),
                "icon_url": f"{ system.get('link') }/favicon.png"
              },
              "url": f"{ system.get('link') }/settings/users"
            }
        ]
    }
    _create_message(payload)


def post_user_updated(request):
    user = request.get('user')
    system = request.get('system')

    payload = {
        'embeds': [
            {
              "type": "rich",
              "title": 'User updated',
              "description": 'A user was updated',
              "color": COLORS['yellow'],
              "fields": [
                {
                  "name": 'username',
                  "value": user.get('login'),
                  "inline": True
                },
                {
                  "name": 'active',
                  "value": 'yes' if user.get('active') else 'no',
                  "inline": True
                },
                {
                  "name": 'type',
                  "value": 'Machine' if user.get('machine') else 'User',
                  "inline": True
                },
                {
                  "name": 'role',
                  "value": 'Admin' if user.get('admin') else 'Member',
                  "inline": True
                },
                {
                  "name": 'created',
                  "value": user.get('created'),
                  "inline": True,
                },
                {
                  "name": 'last login',
                  "value": f"{user.get('last_login') } days ago",
                  "inline": True,
                }
              ],
              "thumbnail": {
                "url": user.get('avatar'),
                "height": 0,
                "width": 0
              },
              "footer": {
                "text": system.get('host'),
                "icon_url": f"{ system.get('link') }/favicon.png"
              },
              "url": f"{ system.get('link') }/settings/users"
            }
        ]
    }
    _create_message(payload)


def post_user_deleted(request):
    user = request.get('user')
    system = request.get('system')

    payload = {
        'embeds': [
            {
              "type": "rich",
              "title": 'User deleted',
              "description": 'A user was deleted',
              "color": COLORS['red'],
              "fields": [
                {
                  "name": 'username',
                  "value": user.get('login'),
                  "inline": True
                },
                {
                  "name": 'active',
                  "value": 'yes' if user.get('active') else 'no',
                  "inline": True
                },
                {
                  "name": 'type',
                  "value": 'Machine' if user.get('machine') else 'User',
                  "inline": True
                },
                {
                  "name": 'role',
                  "value": 'Admin' if user.get('admin') else 'Member',
                  "inline": True
                },
                {
                  "name": 'created',
                  "value": user.get('created'),
                  "inline": True,
                },
                {
                  "name": 'last login',
                  "value": f"{user.get('last_login') } days ago",
                  "inline": True,
                }
              ],
              "thumbnail": {
                "url": user.get('avatar'),
                "height": 0,
                "width": 0
              },
              "footer": {
                "text": system.get('host'),
                "icon_url": f"{ system.get('link') }/favicon.png"
              },
              "url": f"{ system.get('link') }/settings/users"
            }
        ]
    }
    _create_message(payload)


def post_repo_enabled(request):
    pass


def post_repo_disabled(request):
    pass


def post_build_created(request):
    pass


def post_build_updated(request):
    pass
