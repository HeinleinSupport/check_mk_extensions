#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2017 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

# https://mathias-kettner.de/checkmk_wato_webapi.html

from pprint import pprint
import requests
import warnings

def check_mk_url(url):
    if url[-1] == '/':
        if not url.endswith('check_mk/'):
            url += 'check_mk/'
    else:
        if not url.endswith('check_mk'):
            url += '/check_mk/'
    return url

class WATOAPI():
    def __init__(self, site_url, api_user, api_secret):
        self.api_url = '%s/webapi.py' % check_mk_url(site_url)
        self.api_creds = {'_username': api_user, '_secret': api_secret, 'request_format': 'python', 'output_format': 'python'}

    def api_request(self, params, data=None, errmsg='Error', fail=True):
        result = { 'result_code': 1,
                   'result': None }
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            if data:
                resp = requests.post(self.api_url, verify=False, params=params, data='request=%s' % repr(data))
            else:
                resp = requests.get(self.api_url, verify=False, params=params)
            if resp.status_code == 200:
                result = eval(resp.text)
            else:
                raise RuntimeError(resp.text)
        if result['result_code'] == 1:
            if fail:
                print params['action']
                pprint(data)
                import urllib
                print "curl '%s?%s' -d 'request=%s'" % (self.api_url, urllib.urlencode(params), repr(data))
                raise RuntimeError('%s: %s' % ( errmsg, result['result'] ))
            else:
                print '%s: %s' % ( errmsg, result['result'] )
        return result['result']

    def get_host(self, hostname, effective_attr=True):
        api_get_host = { 'action': 'get_host', 'effective_attributes': 1 }
        api_get_host.update(self.api_creds)
        if not effective_attr:
            api_get_host['effective_attributes'] = 0
        return self.api_request(params=api_get_host,
                                data={'hostname': hostname},
                                errmsg='Error getting hostinfo for %s' % hostname)

    def get_all_hosts(self, effective_attr=True):
        api_get_all_hosts = { 'action': 'get_all_hosts', 'effective_attributes': 1 }
        api_get_all_hosts.update(self.api_creds)
        if not effective_attr:
            api_get_all_hosts['effective_attributes'] = 0
        return self.api_request(params=api_get_all_hosts, errmsg='Error getting all hosts')

    def add_host(self, hostname, folder=None, set_attr = {}):
        api_add_host = { 'action': 'add_host' }
        api_add_host.update(self.api_creds)
        return self.api_request(params=api_add_host,
                                data={'hostname': hostname,
                                      'folder': folder,
                                      'attributes': set_attr},
                                errmsg='Error adding host %s' % hostname)

    def edit_host(self, hostname, set_attr={}, unset_attr = [], nodes = []):
        api_edit_host = { 'action': 'edit_host' }
        api_edit_host.update(self.api_creds)
        data = {'hostname': hostname}
        if set_attr:
            data['attributes'] = set_attr
        if unset_attr:
            data['unset_attributes'] = unset_attr
        if nodes:
            data['nodes'] = nodes
        return self.api_request(params=api_edit_host,
                                data=data,
                                errmsg='Error updating host %s' % hostname)

    def delete_host(self, hostname):
        api_del_host = { 'action': 'delete_host' }
        api_del_host.update(self.api_creds)
        return self.api_request(params=api_del_host,
                                data={'hostname': hostname},
                                errmsg='Error deleting host %s' % hostname)
    
    def disc_host(self, hostname, fail=False):
        api_disc_host = { 'action': 'discover_services' }
        api_disc_host.update(self.api_creds)
        return self.api_request(params=api_disc_host,
                                data={"hostname": hostname},
                                errmsg='Error discovering host %s' % hostname,
                                fail=fail)

    def activate(self, sites=[]):
        api_activate = { 'action': 'activate_changes'}
        api_activate.update(self.api_creds)
        if sites:
            api_activate['mode'] = 'specific'
            return self.api_request(params=api_activate, data={'sites': sites})
        else:
            return self.api_request(params=api_activate)

    def bake_agents(self):
        api_bake_agents = { 'action': 'bake_agents' }
        api_bake_agents.update(self.api_creds)
        return self.api_request(params=api_bake_agents)

class MultisiteAPI():
    def __init__(self, site_url, api_user, api_secret):
        self.site_url = check_mk_url(site_url)
        self.api_creds = {'_username': api_user, '_secret': api_secret, 'request_format': 'python', 'output_format': 'python', '_transid': '-1'}

    def api_request(self, api_url, params, data=None, errmsg='Error', fail=True):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            if data:
                resp = requests.post(api_url, verify=False, params=params, data='request=%s' % repr(data))
            else:
                resp = requests.get(api_url, verify=False, params=params)
            if resp.status_code == 200:
                return eval(resp.text)
            else:
                raise resp.text
        return []

    def view(self, view_name, **kwargs):
        result = []
        request = {'view_name': view_name}
        request.update(self.api_creds)
        request.update(kwargs)
        resp = self.api_request(self.site_url + 'view.py', request, errmsg='Cannot get view data')
        header = resp[0]
        for data in resp[1:]:
            item = {}
            for i in xrange(len(header)):
                item[header[i]] = data[i]
            result.append(item)
        return result
