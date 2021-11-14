import os
import requests
from datetime import datetime
from time import sleep
from api.mongo import get_db


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
DISCORD_API_BASE_URL = os.getenv('DISCORD_API_BASE_URL') or 'https://discord.com/api'
DISCORD_MESSAGES_API = f'{ DISCORD_API_BASE_URL }/channels/{ DISCORD_CHANNEL_ID }/messages'

HEADERS = {
    'Authorization': f'Bot { DISCORD_TOKEN }'
}

COLORS = {
    'green': 0x25c710,
    'yellow': 0xddb231,
    'red': 0xc51b1b,
    'blue': 0x21b7fd,
}


def _create_message(payload):
    try:
        response = requests.post(
            headers = HEADERS,
            url = DISCORD_MESSAGES_API,
            json = payload,
        )

        if response.status_code == 429:
            # rate limited
            retry_after = response.json()['retry_after']
            print(f"discord: rate limited, retrying after { retry_after } seconds")
            sleep(retry_after)
            _create_message(payload)
        
        assert response.status_code == 200     

    except Exception as ex:
        print(ex)
        print('discord: create_message() failure')

    return response


def _edit_message(payload, message_id):
    try:
        response = requests.patch(
            headers = HEADERS,
            url = f'{ DISCORD_MESSAGES_API }/{ message_id }',
            json = payload,
        )

        if response.status_code == 429:
            # rate limited
            retry_after = response.json()['retry_after']
            print(f"discord: rate limited, retrying after { retry_after } seconds")
            sleep(retry_after)
            _create_message(payload)

        assert response.status_code == 200      

    except Exception as ex:
        print(ex)
        print('discord: edit_message() failure')

    return response


def post_user_created(request):
    user = request.get('user')
    system = request.get('system')

    _create_message({
        'embeds': [{
            "type": "rich",
            "title": f"Hello, { user.get('login') }",
            "url": f"{ system.get('link') }/settings/users",
            "description": 'User created',
            "color": COLORS['blue'],
            "fields": [
                {
                  "name": 'username',
                  "value": user.get('login'),
                  "inline": True,
                },
                {
                  "name": 'active',
                  "value": 'yes' if user.get('active') else 'no',
                  "inline": True,
                },
                {
                  "name": 'type',
                  "value": 'Machine' if user.get('machine') else 'User',
                  "inline": True,
                },
                {
                  "name": 'role',
                  "value": 'Admin' if user.get('admin') else 'Member',
                  "inline": True,
                },
            ],
            "thumbnail": {
                "url": user.get('avatar'),
                "height": 0,
                "width": 0,
            },
            "footer": {
                "text": f"v{ system.get('version') }",
                "icon_url": f"{ system.get('link') }/favicon.png",
            },
        }]
    })


def post_user_deleted(request):
    user = request.get('user')
    system = request.get('system')

    _create_message({
        'embeds': [{
            "type": "rich",
            "title": f"Goodbye, { user.get('login') }",
            "url": f"{ system.get('link') }/settings/users",
            "description": 'User deleted',
            "color": COLORS['blue'],
            "fields": [
                {
                  "name": 'username',
                  "value": user.get('login'),
                  "inline": True,
                },
                {
                  "name": 'active',
                  "value": 'yes' if user.get('active') else 'no',
                  "inline": True,
                },
                {
                  "name": 'type',
                  "value": 'Machine' if user.get('machine') else 'User',
                  "inline": True,
                },
                {
                  "name": 'role',
                  "value": 'Admin' if user.get('admin') else 'Member',
                  "inline": True,
                },
            ],
            "thumbnail": {
                "url": user.get('avatar'),
                "height": 0,
                "width": 0,
            },
            "footer": {
                "text": f"v{ system.get('version') }",
                "icon_url": f"{ system.get('link') }/favicon.png",
            },
        }]
    })


def post_repo_enabled(request):
    user = request.get('user')
    repo = request.get('repo')
    system = request.get('system')

    _create_message({
        'embeds': [{
            "type": "rich",
            "title": repo.get('slug'),
            "url": f"{ system.get('link') }/{ repo.get('slug') }/settings",
            "description": 'Repository enabled\n',
            "color": COLORS['blue'],
            "fields": [
                {
                  "name": 'Config',
                  "value": repo.get('config_path'),
                  "inline": True,
                },
                {
                  "name": 'Protected',
                  "value": 'yes' if repo.get('protected') else 'no',
                  "inline": True,
                },
                {
                  "name": 'Trusted',
                  "value": 'yes' if repo.get('trusted') else 'no',
                  "inline": True,
                },
                {
                  "name": 'Ignore Forks',
                  "value": 'yes' if repo.get('ignore_forks') else 'no',
                  "inline": True,
                },
                {
                  "name": "Ignore PR's",
                  "value": 'yes' if repo.get('ignore_pull_requests') else 'no',
                  "inline": True,
                },
                {
                  "name": 'Repository',
                  "value": f"[Open in SCM]({ repo.get('link') })",
                  "inline": True,
                },
            ],
            "footer": {
                "text": f"v{ system.get('version') }",
                "icon_url": f"{ system.get('link') }/favicon.png",
            },
        }]
    })


def post_repo_disabled(request):
    repo = request.get('repo')
    system = request.get('system')

    _create_message({
        'embeds': [{
            "type": "rich",
            "title": repo.get('slug'),
            "url": f"{ system.get('link') }/{ repo.get('slug') }/settings",
            "description": 'Repository disabled\n',
            "color": COLORS['blue'],
            "fields": [
                {
                  "name": 'Config',
                  "value": repo.get('config_path'),
                  "inline": True,
                },
                {
                  "name": 'Protected',
                  "value": 'yes' if repo.get('protected') else 'no',
                  "inline": True,
                },
                {
                  "name": 'Trusted',
                  "value": 'yes' if repo.get('trusted') else 'no',
                  "inline": True,
                },
                {
                  "name": 'Ignore Forks',
                  "value": 'yes' if repo.get('ignore_forks') else 'no',
                  "inline": True,
                },
                {
                  "name": "Ignore PR's",
                  "value": 'yes' if repo.get('ignore_pull_requests') else 'no',
                  "inline": True,
                },
                {
                  "name": 'Repository',
                  "value": f"[Open in SCM]({ repo.get('link') })",
                  "inline": True,
                },
            ],
            "footer": {
                "text": f"v{ system.get('version') }",
                "icon_url": f"{ system.get('link') }/favicon.png",
            },
        }]
    })


def post_build_created(request):
    # TODO
    pass


def post_build_updated(request):
    # TODO
    pass
