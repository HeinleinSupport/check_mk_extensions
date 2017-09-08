#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2017 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

# https://mathias-kettner.de/checkmk_wato_webapi.html

from pprint import pprint
import requests
import json
import warnings

class WATOAPI():
    def __init__(self, site_url, api_user, api_secret):
        if site_url[-1] == '/':
            if not site_url.endswith('check_mk/'):
                site_url += 'check_mk/'
        else:
            if not site_url.endswith('check_mk'):
                site_url += '/check_mk/'
        self.api_url = '%s/webapi.py' % site_url
        self.api_creds = {'_username': api_user, '_secret': api_secret, 'output_format': 'json'}
        self.api_get_host = { 'action': 'get_host', 'effective_attributes': 1 }
        self.api_get_host.update(self.api_creds)
        self.api_get_all_hosts = { 'action': 'get_all_hosts', 'effective_attributes': 1 }
        self.api_get_all_hosts.update(self.api_creds)
        self.api_add_host = { 'action': 'add_host' }
        self.api_add_host.update(self.api_creds)
        self.api_edit_host = { 'action': 'edit_host' }
        self.api_edit_host.update(self.api_creds)
        self.api_del_host = { 'action': 'delete_host' }
        self.api_del_host.update(self.api_creds)
        self.api_disc_host = { 'action': 'discover_services' }
        self.api_disc_host.update(self.api_creds)
        self.api_activate = { 'action': 'activate_changes'}
        self.api_activate.update(self.api_creds)

    def api_request(self, params, data=None, errmsg='Error', fail=True):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            if data:
                resp = requests.post(self.api_url, verify=False, params=params, data='request=%s' % json.dumps(data))
            else:
                resp = requests.get(self.api_url, verify=False, params=params)
            try:
                resp1 = resp.json()
            except:
                raise
            resp = resp1
        if resp['result_code'] == 1:
            if fail:
                print params['action']
                pprint(data)
                import urllib
                print "curl '%s?%s' -d 'request=%s'" % (self.api_url, urllib.urlencode(params), json.dumps(data))
                raise RuntimeError('%s: %s' % ( errmsg, resp['result'] ))
            else:
                print '%s: %s' % ( errmsg, resp['result'] )
        return resp['result']

    def get_host(self, hostname, effective_attr=True):
        api_get_host = self.api_get_host.copy()
        if not effective_attr:
            api_get_host['effective_attributes'] = 0
        return self.api_request(params=api_get_host,
                                data={'hostname': hostname},
                                errmsg='Error getting hostinfo for %s' % hostname)

    def get_all_hosts(self, effective_attr=True):
        api_get_all_hosts = self.api_get_all_hosts.copy()
        if not effective_attr:
            api_get_all_hosts['effective_attributes'] = 0
        return self.api_request(params=api_get_all_hosts, errmsg='Error getting all hosts')

    def add_host(self, hostname, folder=None, set_attr = {}):
        return self.api_request(params=self.api_add_host,
                                data={'hostname': hostname,
                                      'folder': folder,
                                      'attributes': set_attr},
                                errmsg='Error adding host %s' % hostname)

    def edit_host(self, hostname, set_attr={}, unset_attr = [], nodes = []):
        data = {'hostname': hostname}
        if set_attr:
            data['attributes'] = set_attr
        if unset_attr:
            data['unset_attributes'] = unset_attr
        if nodes:
            data['nodes'] = nodes
        return self.api_request(params=self.api_edit_host,
                                data=data,
                                errmsg='Error updating host %s' % hostname)

    def delete_host(self, hostname):
        return self.api_request(params=self.api_del_host,
                                data={'hostname': hostname},
                                errmsg='Error deleting host %s' % hostname)
    
    def disc_host(self, hostname, fail=False):
        return self.api_request(params=self.api_disc_host,
                                data={"hostname": hostname},
                                errmsg='Error discovering host %s' % hostname,
                                fail=fail)

    def activate(self, sites=[]):
        if sites:
            params = {'mode': 'specific'}
            params.update(self.api_activate)
            return self.api_request(params=params, data={'sites': sites})
        else:
            return self.api_request(params=self.api_activate)

class MultisiteAPI():
    def __init__(self, site_url, api_user, api_secret):
        if site_url[-1] == '/':
            if not site_url.endswith('check_mk/'):
                site_url += 'check_mk/'
        else:
            if not site_url.endswith('check_mk'):
                site_url += '/check_mk/'
        self.site_url = site_url
        self.api_creds = {'_username': api_user, '_secret': api_secret, 'output_format': 'json', '_transid': '-1'}

    def api_request(self, api_url, params, data=None, errmsg='Error', fail=True):
        resp = []
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            if data:
                resp = requests.post(api_url, verify=False, params=params, data='request=%s' % json.dumps(data)).json()
            else:
                resp = requests.get(api_url, verify=False, params=params).json()
        return resp

    def view(self, view_name, **kwargs):
        result = []
        request = self.api_creds.copy()
        request['view_name'] = view_name
        request.update(kwargs)
        resp = self.api_request(self.site_url + 'view.py', request, errmsg='Cannot get view data')
        header = resp[0]
        for data in resp[1:]:
            item = {}
            for i in xrange(len(header)):
                item[header[i]] = data[i]
            result.append(item)
        return result
