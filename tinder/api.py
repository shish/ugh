from . import models
from . import constants
from .binder import bind_api
from .exceptions import AuthorizationError


class APIAuth(object):
    fb_id = None
    fb_token = None
    tinder_token = None
    _data = None

    def __init__(self, fb_id, fb_token):
        self.fb_id = fb_id
        self.fb_token = fb_token

    @property
    def is_complete(self):
        return all([self.fb_id, self.fb_token, self.tinder_token])


class API(object):
    ''' Class used to map to all Tinder API endpoints
    '''
    def __init__(self, auth_handler=None, host='https://api.gotinder.com'):
        self.auth = auth_handler
        self.host = host

    def set_auth(self, fb_id, fb_token):
        self.auth = APIAuth(fb_id, fb_token)

    _authorize = bind_api(
        path='/auth',
        allowed_params=['facebook_token', 'facebook_id'],
        method='POST',
        require_auth=False,
    )

    def authorize(self):
        data = self._authorize(
            facebook_token=self.auth.fb_token,
            facebook_id=self.auth.fb_id,
        )
        if 'token' not in data:
            # Error authorizing.
            raise AuthorizationError(
                '{0}: {1}'.format(data['code'], data['error'])
            )
        self.auth.tinder_token = data['token']
        return models.Profile(data['user'], self)

    ping = bind_api(
        path='/user/ping',
        allowed_param=['lat', 'lon'],
        method='POST',
    )

    recs = bind_api(
        path='/user/recs',
    )

    like = bind_api(
        path='/like/{user_id}',
        allowed_param=['user_id'],
    )

    nope = bind_api(
        path='/pass/{user_id}',
        allowed_param=['user_id'],
    )

    updates = bind_api(
        path='/updates',
        allowed_param=['last_activity_date'],
        delete_param=['last_activity_date'],
        strict_delete_param=False,
        method='POST',
    )

    profile = bind_api(
        path='/profile',
        data_model=models.Profile,
    )

    update_profile = bind_api(
        path='/profile',
        allowed_param=constants.PROFILE_FIELDS,
        method='POST',
    )

    user_info = bind_api(
        path='/user/{user_id}',
        allowed_param=['user_id'],
    )

    report = bind_api(
        path='/report/{user_id}',
        allowed_param=['user_id', 'cause'],
        delete_param=['user_id'],
        method='POST',
    )

    match  = bind_api(
        path='/user/matches/{match_id}',
        allowed_param=['match_id'],
    )

    message = bind_api(
        path='/user/matches/{match_id}',
        allowed_param=['match_id', 'message'],
        delete_param=['match_id'],
        method='POST',
    )

    unmatch = bind_api(
        path='/user/matches/{match_id}',
        allowed_param=['match_id'],
        method='DELETE',
    )

    ## HELPERS ##

    def report_spam(self, user_id):
        return self.report(user_id=user_id, cause=constants.REPORT_CAUSE_SPAM)

    def report_inappropriate(self, user_id):
        return self.report(
            user_id=user_id,
            cause=constants.REPORT_CAUSE_INAPPROPRIATE,
        )

    def nearby(self):
        data = self.recs()
        if not 'results' in data:
            data['results'] = []
        for res in data['results']:
            yield models.User(res, self)

    def update_location(self, lat, lon):
        return self.ping(lat, lon)

    def get_user(self, user_id):
        data = self.user_info(user_id=user_id)
        return models.User(data['results'], self)

    def matches(self, since_date=None):
        ''' Since date should be a datetime.datetime instance
            representing the start date to get updated from.
            This is useful if you want matches from a long
            time ago.
        '''
        lad = since_date.isoformat() if since_date is not None else since_date
        mlist =  map(
            lambda x: models.Match(x, self),
            self.updates(last_activity_date=lad)['matches'],
        )
        return sorted(mlist, key=lambda x: x.last_activity_date, reverse=True)
