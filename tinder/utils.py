import os
import stat
import json
import datetime
import requests
from . import constants


def pull_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')


def get_facebook_user_id(fb_username):
    ''' Simple utility to pull the FB User ID for a given
        FB Username
    '''
    data = requests.get(
        'https://graph.facebook.com/{0}'.format(fb_username),
    ).json()
    return data['id']


def write_auth_to_file(auth, fname=constants.DEFAULT_AUTH_FILE_PATH):
    fname = os.path.expanduser(fname)
    json.dump({
        'fb_id': auth.fb_id,
        'fb_token': auth.fb_token,
        'tinder_token': auth.tinder_token,
    }, open(fname, 'w'))
    os.chmod(fname, stat.S_IMODE(0600))


def read_auth_from_file(fname=constants.DEFAULT_AUTH_FILE_PATH):
    fname = os.path.expanduser(fname)
    return json.load(open(fname))


def load_auth_from_file(fname=constants.DEFAULT_AUTH_FILE_PATH):
    from . import api  # Circular
    data = read_auth_from_file(fname)
    auth = api.APIAuth(data['fb_id'], data['fb_token'])
    auth.tinder_token = data['tinder_token']
    return auth


def load_api_from_file(fname=constants.DEFAULT_AUTH_FILE_PATH):
    from . import api  # Circular
    auth = load_auth_from_file(fname)
    return api.API(auth_handler=auth)
