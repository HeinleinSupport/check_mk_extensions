#   Copyright Red Hat, Inc. All Rights Reserved.
#
#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import requests
import json


class CachetClient(object):
    def __init__(self, **kwargs):
        """
        Initialize the class, get the necessary parameters
        """
        try:
            self.endpoint = kwargs['endpoint']
        except KeyError:
            raise KeyError('Cachet API endpoint is required')

        self.user_agent = kwargs.get('user_agent', 'python-cachetclient')
        self.api_token = kwargs.get('api_token', None)
        self.timeout = kwargs.get('timeout', None)
        self.verify = kwargs.get('verify', None)
        self.pagination = kwargs.get('pagination', False)

        self.http = requests.Session()

    def _request(self, url, method, **kwargs):
        if self.timeout is not None:
            kwargs.setdefault('timeout', self.timeout)

        if self.verify is not None:
            kwargs.setdefault('verify', self.verify)

        kwargs.setdefault('headers', kwargs.get('headers', {}))
        kwargs['headers']['User-Agent'] = self.user_agent
        kwargs['headers']['Accept'] = 'application/json'
        kwargs['headers']['Content-Type'] = 'application/json'
        if self.api_token is not None:
            kwargs['headers']['X-Cachet-Token'] = self.api_token

        # If we're sending data, make sure it's json encoded
        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])

        resp = self.http.request(method, url, **kwargs)
        if not resp.ok:
            resp.raise_for_status()

        try:
            body = resp.json()
        except ValueError:
            body = None

        if not self.pagination:
            if body is not None and 'meta' in body and 'pagination' in body['meta']:
                page_info = body['meta']['pagination']
                if page_info['total'] > page_info['count']:
                    # There are items not displayed in our result
                    kwargs.setdefault('params', kwargs.get('params', {}))
                    kwargs['params']['per_page'] = page_info['total']
                    return self._request(url, method, **kwargs)

        return resp, body

    def _delete(self, path, **kwargs):
        url = "%s/%s" % (self.endpoint, path)
        response, data = self._request(url, 'DELETE', **kwargs)
        return True

    def _get(self, path, **kwargs):
        url = "%s/%s" % (self.endpoint, path)
        response, data = self._request(url, 'GET', **kwargs)
        return json.dumps(data, indent=2)

    def _post(self, path, **kwargs):
        url = "%s/%s" % (self.endpoint, path)
        response, data = self._request(url, 'POST', **kwargs)
        return json.dumps(data, indent=2)

    def _put(self, path, **kwargs):
        url = "%s/%s" % (self.endpoint, path)
        response, data = self._request(url, 'PUT', **kwargs)
        return json.dumps(data, indent=2)
