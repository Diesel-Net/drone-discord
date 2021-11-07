from flask import (
    Blueprint,
    current_app,
    request,
)
from api import logger
from api.database import get_db
import requests
import pendulum
import json
from datetime import datetime
import hashlib
import hmac
from base64 import b64encode

bp = Blueprint('log', __name__, url_prefix='')

class Color:
    QUEUED = '#dadee6'
    SUCCESS = '#04bd8a'
    FAILURE = '#eb1c23'
    RUNNING = '#08acee'

def send_message_to_slack(
    channel,
    token,
    attachments=None, 
    blocks=None, 
    text=None, 
    ts=None, 
    update=False
):
    args = {
        'token': token,
        'channel': channel,
        'text': text,
        'blocks': json.dumps(blocks) if blocks else None,
        'attachments': json.dumps(attachments) if attachments else None,
        # 'thread_ts': thread_ts,
        'ts': ts,
    }

    endpoint = 'chat.postMessage'
    if update:
        endpoint = 'chat.update'

    return requests.post('https://slack.com/api/' + endpoint, args).json()

def create_attachments(
    build_link,
    build_number,
    build_start,
    build_status,
    build_trigger,
    color,
    duration,
    repository,
    repository_link,
    version,
    version_link,
    author_avatar=None,
):
    attachment = {
        'mrkdwn_in': ['text'],
        'color': color,
        #'pretext': '',
        #'author_name': 'author_name',
        #'author_link': 'http://flickr.com/bobby/',
        #'author_icon': 'https://placeimg.com/16/16/people',
        #'title': 'title',
        #'title_link': 'https://api.slack.com/',
        #'text': 'Optional `text` that appears within the attachment',
        'fields': [
            {
                'title': 'REPOSITORY',
                'value': f'<{ repository_link }|{ repository }>',
                'short': True
            },
            {
                'title': 'VERSION',
                'value': f'<{ repository_link }/tree/{ version }|{ version }>',
                'short': True
            },
            {
                'title': 'STATUS',
                'value': build_status.capitalize(),
                'short': True
            },
            {
                'title': 'DURATION',
                'value': duration,
                'short': True
            }
        ],
        #'thumb_url': 'http://placekitten.com/g/200/200',
        'footer': f'<{ build_link }|Build #{ build_number }>, triggered by { build_trigger }',
        'footer_icon': author_avatar,
        'ts': build_start.timestamp(),
    }

    return [attachment]


def calculate_signature(key, signing_string):
    # drone signatures are calulcated using hmac sha256
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
    
    logger.info(f'Signature: {expected}\nCalculated: {calculated}')

    # equal?
    return hmac.compare_digest(expected, calculated)


@bp.route('/hook', methods=['POST'])
def log():
    logger.debug(request.headers)

    if not verify_signature(current_app.config['DRONE_WEBHOOK_SECRET']):
        logger.error('Unable to verify signature.')
        return {}, 500

    data = request.get_json()
    event = data['event']
    action = data['action']

    if event != 'build':
        logger.debug('Not a build event.')
        # return {}, 200

    build = data['build']
    repo = data['repo']
    
    build_status = build['status']
    build_event = build['event']

    build_trigger = build['trigger'].replace('@hook', 'GitHub Hook')
    build_ref = build['ref']
    author_avatar = build['author_avatar']
    drone_link = data['system']['link']
    
    started = pendulum.parse(datetime.utcfromtimestamp(build['started']).isoformat())
    finished = None
    duration_human_readable = f'Just started'
    if build['started'] and not build['finished']:
        duration_human_readable = f'{ (pendulum.now() - started).in_words() }...'
    if build['finished']:
        finished = pendulum.parse(datetime.utcfromtimestamp(build['finished']).isoformat())
        duration = finished - started
        duration_human_readable = duration.in_words()


    slug = repo['slug']
    repo_link = repo['link']

    version = build_ref.split('/').pop()
    version_link = f'{repo_link}/tree/{version}'

    build_number = build['number']
    build_link = f'{drone_link}/{slug}/{build_number}'

    token = current_app.config['SLACK_BOT_USER_OAUTH_ACCESS_TOKEN']
    channel = current_app.config['SLACK_BUILD_LOG_CHANNEL']

    if action == 'created':
        color = Color.QUEUED
    if build_status == 'running':
        color = Color.RUNNING
    if finished:
        if build_status == 'success':
            color = Color.SUCCESS
        else:
            color = Color.FAILURE

    try:
        db = get_db()
        result = db.builds.find_one(
            {
                'commit': build['after'],
                'build_number': build_number,
            }
        )

        ts = None
        if result:
            ts = result.get('ts')
            channel = result.get('channel')

        attachments = create_attachments(
            color=color,
            repository=slug,
            repository_link=repo_link,
            version=version,
            version_link=version_link,
            duration=duration_human_readable,
            build_link=build_link,
            build_number=build_number,
            build_start=started,
            build_status=build_status,
            author_avatar=author_avatar,
            build_trigger=build_trigger,
        )

        response = send_message_to_slack(
            channel=channel,
            token=token,
            ts=ts,
            attachments=attachments,
            update=action != 'created'
        )
        
        logger.debug(response)

        if 'ts' in response:
            ts = response['ts']
            channel = response['channel']
            result = db.builds.insert_one(
                {
                    'date' : datetime.utcnow(),
                    'ts': ts,
                    'channel': channel,
                    'commit': build['after'],
                    'build_number': build_number,
                }
            )

        if finished:
            db.builds.remove({
                'commit': build['after'],
                'build_number': build_number,
            })
    
    except Exception as e:
        logger.error(e)

    return {}, 200
