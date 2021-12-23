import os
import requests
from datetime import datetime, timedelta
from time import sleep
from api.mongo import get_database

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
DISCORD_API_BASE_URL = os.getenv('DISCORD_API_BASE_URL') or 'https://discord.com/api'
DISCORD_MESSAGES_API = f'{ DISCORD_API_BASE_URL }/channels/{ DISCORD_CHANNEL_ID }/messages'

HEADERS = {
    'Authorization': f'Bot { DISCORD_TOKEN }'
}

COLOR = {
    'green': 0x42c768,
    'yellow': 0xddb231,
    'red': 0xbb3030,
    'blue': 0x21b7fd,
}

BUILD_STATUS_COLOR = {
    'pending': COLOR['blue'],
    'running': COLOR['yellow'],
    'success': COLOR['green'],
    'failure': COLOR['red'],
    'killed': COLOR['red'],
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
            return _create_message(payload)
        
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
            return _edit_message(message_id, payload)

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
            "color": COLOR['blue'],
            "fields": [
                {
                  "name": 'username',
                  "value": user.get('login'),
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
            "color": COLOR['blue'],
            "fields": [
                {
                  "name": 'username',
                  "value": user.get('login'),
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
            "color": COLOR['blue'],
            "fields": [
                {
                  "name": 'Repository',
                  "value": f"[GitHub]({ repo.get('link') })",
                  "inline": True,
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
            "color": COLOR['blue'],
            "fields": [
                {
                  "name": 'Repository',
                  "value": f"[GitHub]({ repo.get('link') })",
                  "inline": True,
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

    status = build.get('status')
    build_id = build.get('id')
    build_number = build.get('number')
    started = build.get('started')
    finished = build.get('finished')
    trigger = build.get('trigger')
    trigger = trigger.replace('@hook', 'webhook')
    trigger = trigger.replace('@cron', build.get('cron', ''))
    git_version = build.get('ref').split('/').pop()
    repo_name = repo.get('slug')
    repo_url = repo.get('link')
    drone_url = system.get('link')

    response = _create_message({
        'embeds': [{
            "type": "rich",
            "title": f"{ repo_name } #{ build_number }",
            "url": f"{ drone_url }/{ repo_name }/{ build_number }",
            "description": build.get('message'),
            "color": BUILD_STATUS_COLOR.get(status),
            "fields": [
                {
                  "name": 'Build',
                  "value": build_number,
                  "inline": True,
                },
                {
                  "name": 'Trigger',
                  "value": trigger,
                  "inline": True,
                },
                {
                  "name": 'Event',
                  "value": build.get('event'),
                  "inline": True,
                },
                {
                  "name": 'Repository',
                  "value": f"[GitHub]({ repo_url })",
                  "inline": True,
                },
                {
                  "name": 'Version',
                  "value": f"[{ git_version }]({ repo_url }/tree/{ git_version })",
                  "inline": True,
                },
                {
                  "name": 'Status',
                  "value": status,
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
                "icon_url": f"{ drone_url }/favicon.png",
            },
        }]
    })

    with current_app.app_context():
        database = get_database()
        database.build.insert_one({
            'id': build.get('id'),
            'status': build.get('status'),
            'data': payload,
            'messageId': response.get('id'),
        })


def post_build_updated(current_app, payload):
    repo = payload.get('repo')
    build = payload.get('build')
    system = payload.get('system')
    
    status = build.get('status')
    build_id = build.get('id')
    build_number = build.get('number')
    started = build.get('started')
    finished = build.get('finished')
    trigger = build.get('trigger')
    trigger = trigger.replace('@hook', 'webhook')
    trigger = trigger.replace('@cron', build.get('cron', ''))
    git_version = build.get('ref').split('/').pop()
    repo_name = repo.get('slug')
    repo_url = repo.get('link')
    drone_url = system.get('link')

    payload = {
        'embeds': [{
            "type": "rich",
            "title": f"{ repo_name } #{ build_number }",
            "url": f"{ drone_url }/{ repo_name }/{ build_number }",
            "description": build.get('message'),
            "color": BUILD_STATUS_COLOR.get(status),
            "fields": [
                {
                  "name": 'Build',
                  "value": build_number,
                  "inline": True,
                },
                {
                  "name": 'Trigger',
                  "value": trigger,
                  "inline": True,
                },
                {
                  "name": 'Event',
                  "value": build.get('event'),
                  "inline": True,
                },
                {
                  "name": 'Repository',
                  "value": f"[GitHub]({ repo_url })",
                  "inline": True,
                },
                {
                  "name": 'Version',
                  "value": f"[{ git_version }]({ repo_url }/tree/{ git_version })",
                  "inline": True,
                },
                {
                  "name": 'Status',
                  "value": status,
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
                "icon_url": f"{ drone_url }/favicon.png",
            },
        }]
    }

    with current_app.app_context():
        database = get_database()
        previous_post = database.build.find_one({'id': build_id })

        if not previous_post:
            print(f"discord: unable to find previous build for { build_id }")
            return

        if previous_post.get('status') == status:
            # no change, do nothing
            return
        
        database.build.update_one(
            previous_post, {
                '$set': {
                    'status': status,
                    'data': payload, 
                }
            }
        )

        if finished:
            duration = finished - started

            payload['embeds'][0]['fields'].append({
                'name': 'Duration',
                'value': str(timedelta(seconds=duration)),
                'inline': True,
            })
            
            # build finished, so remove entry from database
            #database.build.delete_one({'id': build_id })

    _edit_message(previous_post['messageId'], payload)
