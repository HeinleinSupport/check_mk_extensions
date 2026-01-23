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

from decorator import decorator

import cachetclient.client as client
import cachetclient.exceptions as exceptions


@decorator
def api_token_required(f, *args, **kwargs):
    """
    Decorator helper function to ensure some methods aren't needlessly called
    without an api_token configured.
    """
    try:
        if args[0].api_token is None:
            raise AttributeError('Parameter api_token is required.')
    except AttributeError:
        raise AttributeError('Parameter api_token is required.')

    return f(*args, **kwargs)


def check_required_args(required_args, args):
    """
    Checks if all required_args have a value.
    :param required_args: list of required args
    :param args: kwargs
    :return: True (if an exception isn't raised)
    """
    for arg in required_args:
        if arg not in args:
            raise KeyError('Required argument: %s' % arg)
    return True


class Cachet(client.CachetClient):
    """
    Base class that extends CachetClient and defaults API methods to
    unimplemented.
    """
    def __init__(self, **kwargs):
        super(Cachet, self).__init__(**kwargs)

    # Default to unimplemented methods
    def delete(self, **kwargs):
        raise exceptions.UnimplementedException

    def get(self, **kwargs):
        raise exceptions.UnimplementedException

    def post(self, **kwargs):
        raise exceptions.UnimplementedException

    def put(self, **kwargs):
        raise exceptions.UnimplementedException


class Ping(Cachet):
    """
    /ping API endpoint
    """
    def __init__(self, **kwargs):
        super(Ping, self).__init__(**kwargs)

    def get(self, **kwargs):
        """
        https://docs.cachethq.io/docs/ping
        """
        return self._get('ping')


class Version(Cachet):
    """
    /version API endpoint
    """
    def __init__(self, **kwargs):
        super(Version, self).__init__(**kwargs)

    def get(self, **kwargs):
        """
        https://docs.cachethq.io/docs/version
        """
        return self._get('version')


class Components(Cachet):
    """
    /components API endpoint
    """
    def __init__(self, **kwargs):
        super(Components, self).__init__(**kwargs)

    @api_token_required
    def delete(self, id):
        """
        https://docs.cachethq.io/docs/delete-a-component
        """
        return self._delete('components/%s' % id)

    def get(self, id=None, **kwargs):
        """
        https://docs.cachethq.io/docs/get-components
        https://docs.cachethq.io/docs/get-a-component
        """
        if id is not None:
            return self._get('components/%s' % id, data=kwargs)
        elif 'params' in kwargs:
            data = dict(kwargs)
            params = data.pop('params')
            return self._get('components', data=data, params=params)
        else:
            return self._get('components', data=kwargs)

    @api_token_required
    def post(self, **kwargs):
        """
        https://docs.cachethq.io/docs/components
        """
        # default values
        kwargs.setdefault('enabled', kwargs.get('enabled', True))

        required_args = ['name', 'status', 'enabled']
        check_required_args(required_args, kwargs)

        return self._post('components', data=kwargs)

    @api_token_required
    def put(self, **kwargs):
        """
        https://docs.cachethq.io/docs/update-a-component
        """
        required_args = ['id']
        check_required_args(required_args, kwargs)

        return self._put('components/%s' % kwargs['id'], data=kwargs)


class Groups(Cachet):
    """
    /components/groups API endpoint
    """
    def __init__(self, **kwargs):
        super(Groups, self).__init__(**kwargs)

    @api_token_required
    def delete(self, id):
        """
        https://docs.cachethq.io/docs/delete-component-group
        """
        return self._delete('components/groups/%s' % id)

    def get(self, id=None, **kwargs):
        """
        https://docs.cachethq.io/docs/get-componentgroups
        https://docs.cachethq.io/docs/get-a-component-group
        """
        if id is not None:
            return self._get('components/groups/%s' % id, data=kwargs)
        elif 'params' in kwargs:
            data = dict(kwargs)
            params = data.pop('params')
            return self._get('components/groups', data=data, params=params)
        else:
            return self._get('components/groups', data=kwargs)

    @api_token_required
    def post(self, **kwargs):
        """
        https://docs.cachethq.io/docs/post-componentgroups
        """
        required_args = ['name']
        check_required_args(required_args, kwargs)

        return self._post('components/groups', data=kwargs)

    @api_token_required
    def put(self, **kwargs):
        """
        https://docs.cachethq.io/docs/put-component-group
        """
        required_args = ['id']
        check_required_args(required_args, kwargs)

        return self._put('components/groups/%s' % kwargs['id'], data=kwargs)


class Incidents(Cachet):
    """
    /incidents API endpoint
    """
    def __init__(self, **kwargs):
        super(Incidents, self).__init__(**kwargs)

    @api_token_required
    def delete(self, id):
        """
        https://docs.cachethq.io/docs/delete-an-incident
        """
        return self._delete('incidents/%s' % id)

    def get(self, id=None, **kwargs):
        """
        https://docs.cachethq.io/docs/get-incidents
        https://docs.cachethq.io/docs/get-an-incident
        """
        if id is not None:
            return self._get('incidents/%s' % id, data=kwargs)
        elif 'params' in kwargs:
            data = dict(kwargs)
            params = data.pop('params')
            return self._get('incidents', data=data, params=params)
        else:
            return self._get('incidents', data=kwargs)

    @api_token_required
    def post(self, **kwargs):
        """
        https://docs.cachethq.io/docs/incidents
        """
        # default values
        kwargs.setdefault('visible', kwargs.get('visible', True))
        kwargs.setdefault('notify', kwargs.get('notify', False))

        required_args = ['name', 'message', 'status', 'visible', 'notify']
        check_required_args(required_args, kwargs)

        return self._post('incidents', data=kwargs)

    @api_token_required
    def put(self, **kwargs):
        """
        https://docs.cachethq.io/docs/update-an-incident
        """
        required_args = ['id']
        check_required_args(required_args, kwargs)

        return self._put('incidents/%s' % kwargs['id'], data=kwargs)


class Metrics(Cachet):
    """
    /metrics API endpoint
    """
    def __init__(self, **kwargs):
        super(Metrics, self).__init__(**kwargs)

    @api_token_required
    def delete(self, id):
        """
        https://docs.cachethq.io/docs/delete-a-metric
        """
        return self._delete('metrics/%s' % id)

    def get(self, id=None, **kwargs):
        """
        https://docs.cachethq.io/docs/get-metrics
        https://docs.cachethq.io/docs/get-a-metric
        """
        if id is not None:
            return self._get('metrics/%s' % id, data=kwargs)
        else:
            return self._get('metrics', data=kwargs)

    @api_token_required
    def post(self, **kwargs):
        """
        https://docs.cachethq.io/docs/metrics
        """
        # default values
        kwargs.setdefault('default_value', kwargs.get('default_value', 0))

        required_args = ['name', 'suffix', 'description', 'default_value']
        check_required_args(required_args, kwargs)

        return self._post('metrics', data=kwargs)


class Points(Cachet):
    """
    /metrics/<metric>/points API endpoint
    """
    def __init__(self, **kwargs):
        super(Points, self).__init__(**kwargs)

    @api_token_required
    def delete(self, metric_id, point_id):
        """
        https://docs.cachethq.io/docs/delete-a-metric-point
        """
        return self._delete('metrics/%s/points/%s' % (metric_id, point_id))

    def get(self, metric_id=None, **kwargs):
        """
        https://docs.cachethq.io/docs/get-metric-points
        """
        if metric_id is None:
            raise AttributeError('metric_id is required to get metric points.')

        return self._get('metrics/%s/points' % metric_id, data=kwargs)

    @api_token_required
    def post(self, **kwargs):
        """
        https://docs.cachethq.io/docs/post-metric-points
        """
        required_args = ['id', 'value']
        check_required_args(required_args, kwargs)

        return self._post('metrics/%s/points' % kwargs['id'], data=kwargs)


class Subscribers(Cachet):
    """
    /subscribers API endpoint
    """
    def __init__(self, **kwargs):
        super(Subscribers, self).__init__(**kwargs)

    @api_token_required
    def delete(self, id):
        """
        https://docs.cachethq.io/docs/delete-subscriber
        """
        return self._delete('subscribers/%s' % id)

    def get(self, **kwargs):
        """
        https://docs.cachethq.io/docs/get-subscribers
        """
        return self._get('subscribers', data=kwargs)

    @api_token_required
    def post(self, **kwargs):
        """
        https://docs.cachethq.io/docs/subscribers
        """
        required_args = ['email']
        check_required_args(required_args, kwargs)

        return self._post('subscribers', data=kwargs)
