import os
import requests
from datetime import datetime
from time import sleep
from api.mongo import get_database

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
DISCORD_API_BASE_URL = os.getenv('DISCORD_API_BASE_URL') or 'https://discord.com/api'
DISCORD_MESSAGES_API = f'{ DISCORD_API_BASE_URL }/channels/{ DISCORD_CHANNEL_ID }/messages'

HEADERS = {
    'Authorization': f'Bot { DISCORD_TOKEN }'
}

COLORS = {
    'green': 0x42c768,
    'yellow': 0xddb231,
    'red': 0xbb3030,
    'blue': 0x21b7fd,
}


def _create_message(payload):
    response = None
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
        response = response.json()     

    except Exception as ex:
        print(ex)
        print('discord: create_message() failure')

    return response


def _edit_message(message_id, payload):
    response = None
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
            _edit_message(payload, message_id)

        assert response.status_code == 200 
        response = response.json()     

    except Exception as ex:
        print(ex)
        print('discord: edit_message() failure')

    return response


def post_user_created(current_app, payload):
    user = payload.get('user')
    system = payload.get('system')

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


def post_user_deleted(current_app, payload):
    user = payload.get('user')
    system = payload.get('system')

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


def post_repo_enabled(current_app, payload):
    user = payload.get('user')
    repo = payload.get('repo')
    system = payload.get('system')

    _create_message({
        'embeds': [{
            "type": "rich",
            "title": repo.get('slug'),
            "url": f"{ system.get('link') }/{ repo.get('slug') }/settings",
            "description": 'Repository enabled\n',
            "color": COLORS['blue'],
            "fields": [
                {
                  "name": 'Repository',
                  "value": f"[GitHub]({ repo.get('link') })",
                  "inline": False,
                },
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
            ],
            "footer": {
                "text": f"v{ system.get('version') }",
                "icon_url": f"{ system.get('link') }/favicon.png",
            },
        }]
    })


def post_repo_disabled(current_app, payload):
    repo = payload.get('repo')
    system = payload.get('system')

    _create_message({
        'embeds': [{
            "type": "rich",
            "title": repo.get('slug'),
            "url": f"{ system.get('link') }/{ repo.get('slug') }/settings",
            "description": 'Repository disabled\n',
            "color": COLORS['blue'],
            "fields": [
                {
                  "name": 'Repository',
                  "value": f"[GitHub]({ repo.get('link') })",
                  "inline": False,
                },
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
            ],
            "footer": {
                "text": f"v{ system.get('version') }",
                "icon_url": f"{ system.get('link') }/favicon.png",
            },
        }]
    })

def post_build_created(current_app, payload):
    user = payload.get('user')
    repo = payload.get('repo')
    build = payload.get('build')
    system = payload.get('system')

    version = build.get('ref').split('/').pop()

    response = _create_message({
        'embeds': [{
            "type": "rich",
            "title": f"{ repo.get('slug') } #{ build.get('number') }",
            "url": f"{ system.get('link') }/{ repo.get('slug')}/{ build.get('number')}",
            "description": build.get('message'),
            "color": COLORS['blue'],
            "fields": [
                {
                  "name": 'Repository',
                  "value": f"[GitHub]({repo.get('link')})",
                  "inline": True,
                },
                {
                  "name": 'Build',
                  "value": build.get('number'),
                  "inline": True,
                },
                {
                  "name": 'Version',
                  "value": f"[{ version }]({repo.get('link')}/tree/{ version })",
                  "inline": True,
                },
                {
                  "name": 'Status',
                  "value": build.get('status'),
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

    with current_app.app_context():
        database = get_database()
        database.build.insert_one({
            'id': build.get('id'),
            'status': build.get('status'),
            'messageId': response.get('id'),
        })


def post_build_updated(current_app, payload):
    # TODO: Getting rate limited on failure jobs. look into that
    # TODO: duration calculation
    # TODO: healthcheck always returning 200 due to coming-soon page
    
    repo = payload.get('repo')
    build = payload.get('build')
    system = payload.get('system')
    status = build.get('status')
    build_id = build.get('id')

    with current_app.app_context():
        database = get_database()
        message = database.build.find_one({
            'id': build_id,
        })

        if message.get('status') == status:
            # no change
            return
        else:
            database.build.update_one(message,{
                '$set' : {
                    'status' : status,
                }
            })

    
    version = build.get('ref').split('/').pop()
    color = COLORS['yellow']
    started = build.get('started')
    finished = build.get('finished')

    payload = {
        'embeds': [{
            "type": "rich",
            "title": f"{ repo.get('slug') } #{ build.get('number') }",
            "url": f"{ system.get('link') }/{ repo.get('slug')}/{ build.get('number')}",
            "description": build.get('message'),
            "color": COLORS['yellow'],
            "fields": [
                {
                  "name": 'Repository',
                  "value": f"[GitHub]({repo.get('link')})",
                  "inline": True,
                },
                {
                  "name": 'Build',
                  "value": build.get('number'),
                  "inline": True,
                },
                {
                  "name": 'Version',
                  "value": f"[{ version }]({repo.get('link')}/tree/{ version })",
                  "inline": True,
                },
                {
                  "name": 'Status',
                  "value": build.get('status'),
                  "inline": True,
                },
            ],
            "thumbnail": {
                "url": build.get('author_avatar'),
                "height": 0,
                "width": 0,
            },
            "footer": {
                "text": f"v{ system.get('version') }",
                "icon_url": f"{ system.get('link') }/favicon.png",
            },
        }]
    }

    if finished:
        duration = finished - started

        payload['embeds'][0]['fields'].append({
            'name': 'Duration',
            'value': duration,
            'inline': True,
        })

        if status == 'failure':
            payload['embeds'][0]['color'] = COLORS['red']
        if status == 'success':
             payload['embeds'][0]['color'] = COLORS['green']

        with current_app.app_context():
            database = get_database()
            database.message.delete_one({
                'buildId': build.get('id'),
            })


    _edit_message(message['messageId'], payload)
