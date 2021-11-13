import os
import requests


DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')

HEADERS = {
    'Authorization': f'Bot { DISCORD_TOKEN }'
}


def post_user_created(payload):
    pass


def post_user_updated(payload):
    pass


def post_user_deleted(payload):
    pass


def post_repo_enabled(payload):
    pass


def post_repo_disabled(payload):
    pass


def post_build_created(payload):
    pass


def post_build_updated(payload):
    pass
