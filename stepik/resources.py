from types import MethodType

from json_encoder import json
from simple_rest_client.models import Request
from simple_rest_client.request import make_request
from simple_rest_client.resource import Resource


class StepikObject(dict):
    def __getattr__(self, k):
        return self[k]

    def __setattr__(self, k, v):
        self[k] = v
        return None


class AbstractObjectResource(Resource):
    resource_name_alias = None

    def parsed_response(self, response):
        # WIP parse here smartly, maybe like here:
        # WIP https://github.com/stripe/stripe-python/blob/master/stripe/util.py#L162
        response_body = response.body.get(self.resource_name_alias or self.resource_name)
        items = [StepikObject(item) for item in response_body]
        return items[0] if len(items) == 1 else items

    def add_action(self, action_name):
        def action_method(self, *args, body=None, params=None, headers=None, action_name=action_name, **kwargs):
            url = self.get_action_full_url(action_name, *args)
            method = self.get_action_method(action_name)
            if self.json_encode_body and body:
                body = json.dumps(body)
            request = Request(
                url=url,
                method=method,
                params=params or {},
                body=body,
                headers=headers or {},
                timeout=self.timeout,
                kwargs=kwargs
            )

            request.params.update(self.params)
            request.headers.update(self.headers)
            return self.parsed_response(make_request(self.session, request))

        setattr(self, action_name, MethodType(action_method, self))


class StepSourceResource(AbstractObjectResource):
    resource_name_alias = 'step-sources'

    actions = {
        'list': {
            'method': 'GET',
            'url': resource_name_alias,
        },
        'retrieve': {
            'method': 'GET',
            'url': resource_name_alias + '/{}',
        },
        'update': {
            'method': 'PUT',
            'url': resource_name_alias + '/{}',
        },
        'partial_update': {
            'method': 'PATCH',
            'url': resource_name_alias + '/{}',
        },
        'create': {
            'method': 'POST',
            'url': resource_name_alias
        },
    }
