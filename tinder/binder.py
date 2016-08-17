import json
import requests
from urlparse import urljoin
from .exceptions import RequestError
from .constants import GLOBAL_HEADERS


def convert_to_utf8(value):
    if isinstance(value, str):
        value = unicode(value)
    if isinstance(value, unicode):
        return value.decode('utf-8')
    return value


def bind_api(**config):

    class APIMethod(object):
        path = config['path']
        allowed_param = config.get('allowed_param', [])
        delete_param = config.get('delete_param', [])
        strict_delete_param = config.get('strict_delete_param', True)
        data_model = config.get('data_model', None)
        method = config.get('method', 'GET')
        require_auth = config.get('require_auth', True)
        success_status_code = config.get('success_status_code', 200)
        fail_silently = config.get('fail_silently', True)

        def __init__(self, api, args, kwargs):
            self.api = api
            self.headers = kwargs.pop('headers', {})
            self.post_data = kwargs.pop('post_data', None)
            self.build_parameters(args, kwargs)
            self.path = self.path.format(**self.parameters)  # Sub any URL vars
            self.host = api.host
            self.delete_parameters()

        def build_parameters(self, args, kwargs):
            self.parameters = {}
            for idx, arg in enumerate(args):
                if arg is None:
                    continue

                try:
                    self.parameters[self.allowed_param[idx]] = \
                                                    convert_to_utf8(arg)
                except IndexError:
                    raise ValueError('Too many parameters supplied!')

            for k, arg in kwargs.iteritems():
                if arg is None:
                    continue
                if k in self.parameters:
                    raise ValueError(
                        'Multiple values for parameter {0} supplied!'.format(k)
                    )

                self.parameters[k] = convert_to_utf8(arg)

        def delete_parameters(self):
            ''' Silly function to remove items from self.parameters so they
                aren't serialized upon request. Used for edge cases.
            '''
            for param in self.delete_param:
                try:
                    if self.strict_delete_param or \
                                self.parameters[param] is None:
                        del self.parameters[param]
                except KeyError:
                    pass

        def update_headers(self):
            self.headers.update(GLOBAL_HEADERS)
            if self.require_auth:
                self.headers.update(
                    {'X-Auth-Token': self.api.auth.tinder_token}
                )

        def execute(self):
            if self.require_auth and self.api.auth.tinder_token is None:
                # Need to get the Tinder auth_token
                self.api.authorize()

            self.update_headers()

            # Build the request URL
            url = urljoin(self.host, self.path)

            if self.method in ('POST', 'PUT') and self.parameters:
                self.headers.update({'content-type': 'application/json'})
                self.post_data = json.dumps(self.parameters)

            response = requests.request(
                self.method,
                url,
                headers=self.headers,
                data=self.post_data,
            )
            data = response.json()
            if 'status' in data:
                if data['status'] != self.success_status_code:
                    raise RequestError(data['status'])
            return self.data_model(data, self.api) \
                if self.data_model is not None else data


    def _call(api, *args, **kwargs):
        method = APIMethod(api, args, kwargs)
        return method.execute()

    return _call
