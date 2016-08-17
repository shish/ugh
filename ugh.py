#!/usr/bin/env python

import tinder.api
from time import sleep
from pprint import pprint
import threading
from Queue import Queue
import re
import os
import sys


class col:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    HEADER = '\033[95m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get(fn):
    if os.path.exists(fn):
        return open(fn).read().strip()
    else:
        print('You need to supply "%s"' % fn)
        sys.exit(1)


USER_ID = get('user_id.txt')
USER_TOKEN = get('user_token.txt')
WORDS_YAY = get('words_yay.txt').split()
WORDS_NAY = get('words_nay.txt').split()


_log = file('log.txt', 'a')


def req(decision, func, uid):
    def _todo():
        r = func(uid)
        if r.get('status') != 200:
            pprint(r)
        _log.write("%s %s\n" % (decision, uid))
        _log.flush()
    _todo()


def fetch(api):
    print 'Fetching new recommendations...'
    rs = api.recs()
    if 'results' not in rs:
        print "Empty results - you ran out of people?"
        sleep(5)
        return []

    non_blank = []
    for r in rs['results']:
        uid = r['_id']
        if r['bio'] and len(re.sub("[^a-zA-Z]", "", r['bio'])) > 5:
            non_blank.append(r)
        else:
            req("fail", api.nope, uid)
    print "%d were non-empty" % len(non_blank)
    return non_blank


api = tinder.api.API()
api.set_auth(USER_ID, USER_TOKEN)
api.authorize()


in_buf = []

while True:
    if len(in_buf) == 0:
        while len(in_buf) < 20:
            in_buf.extend(fetch(api))

    r = in_buf.pop(0)
    number = 0
    uid = r['_id']

    print col.YELLOW + '*' * 70 + col.ENDC
    b = r['bio']
    for w in WORDS_YAY:
        #number += len(re.findall(b, w))
        b = re.sub(w, col.GREEN + w + col.ENDC, b, flags=re.I)
    for w in WORDS_NAY:
        #number -= len(re.findall(b, w))
        b = re.sub(w, col.RED + w + col.ENDC, b, flags=re.I)
    print b

    if r['common_likes']:
        print 'Likes'
        for x in r['common_likes']:
            print "https://www.facebook.com/%s" % x
            number += 1

    if r['common_friends']:
        print 'Friends'
        for x in r['common_friends']:
            print "https://www.facebook.com/%s" % x
            number += 1

    if number > 5:
        print("auto-like (%d)" % number)
        req("auto", api.like, uid)
    elif raw_input('y/N? ') == 'y':
        req("like", api.like, uid)
    else:
        req("nope", api.nope, uid)
