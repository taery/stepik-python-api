import configparser

import requests
from simple_rest_client.api import API
from simple_rest_client.models import Request
from simple_rest_client.request import make_request

from .resources import AbstractObjectResource, StepSourceResource


class StepikApi(API):
    def __init__(self, server_url=None):
        super().__init__(api_root_url='{}/api/'.format(server_url), headers={}, timeout=15,
                         append_slash=False, json_encode_body=True)

        self.token = None
        self.server_url = server_url

    def auth(self, client_id, client_secret):
        auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        session = requests.Session()
        request = Request(
            url='{}/oauth2/token/'.format(self.server_url),
            method='post',
            params={},
            body={'grant_type': 'client_credentials'},
            headers={},
            timeout=self.timeout,
            kwargs={'auth': auth}
        )
        response = make_request(session, request)
        try:
            if response.body:
                self.token = response.body['access_token']
                self.headers['Authorization'] = 'Bearer ' + self.token
                self.headers['Content-Type'] = 'application/json'

                return self.init_resources()
        except Exception as e:
            print('Failed to connect to Stepik: {}'.format(e))
            return False

    def init_resources(self):
        self.add_resource(resource_name='lessons', resource_class=AbstractObjectResource)
        self.add_resource(resource_name='step_sources', resource_class=StepSourceResource)
        return True

    def __getattribute__(self, name: str):
        return super().__getattribute__(name)


# WIP handle other exceptions
def init_api(setting_path='./resources/'):
    settings_file_path = setting_path + 'settings.properties'
    c = configparser.ConfigParser()
    c.read(settings_file_path)

    api_host = c['stepik']['api_host']
    api_client_id = c['stepik']['client_id']
    api_client_secret = c['stepik']['client_secret']

    # WIP: Raise an exception without auth
    api = StepikApi(api_host)
    api.auth(api_client_id, api_client_secret)
    return api
