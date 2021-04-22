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
import configparser
import os

def check_mk_url(url):
    if url[-1] == '/':
        if not url.endswith('check_mk/'):
            url += 'check_mk/'
    else:
        if not url.endswith('check_mk'):
            url += '/check_mk/'
    return url

def _site_url():
    urldefault = None
    if os.environ.get('HOME', 'a') == os.environ.get('OMD_ROOT', 'b'):
        siteconfig = configparser.ConfigParser()
        with open(os.path.join(os.environ['OMD_ROOT'], 'etc', 'omd', 'site.conf'), 'r') as f:
            config_string = '[GLOBAL]\n' + f.read()
            siteconfig.read_string(config_string.decode())
        urldefault = 'http://%s:%s/%s' % (siteconfig['GLOBAL']['CONFIG_APACHE_TCP_ADDR'].strip("'"),
                                          siteconfig['GLOBAL']['CONFIG_APACHE_TCP_PORT'].strip("'"),
                                          os.environ['OMD_SITE'])
    return urldefault

def _site_creds(username=None):
    password = None
    if os.environ.get('HOME', 'a') == os.environ.get('OMD_ROOT', 'b'):
        if not username:
            username = 'automation'
        password = open(
            os.path.join(
                os.environ['OMD_ROOT'],
                'var',
                'check_mk',
                'web',
                username,
                'automation.secret')).read().strip()
    return username, password

class WATOAPI():
    def __init__(self, site_url=None, api_user=None, api_secret=None):
        if not site_url:
            site_url = _site_url()
        if not api_secret:
            api_user, api_secret = _site_creds(api_user)
        self.api_url = '%s/webapi.py' % check_mk_url(site_url)
        self.api_creds = {'_username': api_user, '_secret': api_secret, 'request_format': 'python', 'output_format': 'python'}

    def api_request(self, params, data=None, errmsg='Error', fail=True):
        result = { 'result_code': 1,
                   'result': None }
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            if data:
                resp = requests.post(self.api_url, verify=False, params=params,
                                     headers={'content-type': 'application/x-www-form-urlencoded'}, data='request=%s' % repr(data))
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
                print resp.request.headers
                print resp.request.body
                import urllib
                print "curl -v '%s?%s' -d \"request=%s\"" % (self.api_url, urllib.urlencode(params), repr(data))
                raise RuntimeError('%s: %s' % ( errmsg, result['result'] ))
            else:
                print '%s: %s' % ( errmsg, result['result'] )
        return result['result']

    def get_host(self, hostname, effective_attr=True):
        api_get_host = { u'action': u'get_host', u'effective_attributes': 1 }
        api_get_host.update(self.api_creds)
        if not effective_attr:
            api_get_host[u'effective_attributes'] = 0
        return self.api_request(params=api_get_host,
                                data={u'hostname': hostname},
                                errmsg='Error getting hostinfo for %s' % hostname)

    def get_all_hosts(self, effective_attr=True):
        api_get_all_hosts = { u'action': u'get_all_hosts', u'effective_attributes': 1 }
        api_get_all_hosts.update(self.api_creds)
        if not effective_attr:
            api_get_all_hosts[u'effective_attributes'] = 0
        return self.api_request(params=api_get_all_hosts, errmsg='Error getting all hosts')

    def add_host(self, hostname, folder=None, set_attr = {}):
        api_add_host = { u'action': u'add_host' }
        api_add_host.update(self.api_creds)
        return self.api_request(params=api_add_host,
                                data={u'hostname': hostname,
                                      u'folder': folder,
                                      u'attributes': set_attr},
                                errmsg='Error adding host %s' % hostname)

    def edit_host(self, hostname, set_attr={}, unset_attr = [], nodes = []):
        api_edit_host = { u'action': u'edit_host' }
        api_edit_host.update(self.api_creds)
        data = {u'hostname': hostname}
        if set_attr:
            data[u'attributes'] = set_attr
        if unset_attr:
            data[u'unset_attributes'] = unset_attr
        if nodes:
            data[u'nodes'] = nodes
        return self.api_request(params=api_edit_host,
                                data=data,
                                errmsg='Error updating host %s' % hostname)

    def delete_host(self, hostname):
        api_del_host = { u'action': u'delete_host' }
        api_del_host.update(self.api_creds)
        return self.api_request(params=api_del_host,
                                data={u'hostname': hostname},
                                errmsg='Error deleting host %s' % hostname)
    
    def disc_host(self, hostname, fail=False):
        api_disc_host = { u'action': u'discover_services' }
        api_disc_host.update(self.api_creds)
        return self.api_request(params=api_disc_host,
                                data={u'hostname': hostname},
                                errmsg='Error discovering host %s' % hostname,
                                fail=fail)

    def activate(self, sites=[], allow_foreign_changes=False, comment=False):
        api_activate = { u'action': u'activate_changes'}
        api_activate.update(self.api_creds)
        data = {}
        if allow_foreign_changes:
            data[u'allow_foreign_changes'] = u'1'
        if comment:
            data[u'comment'] = comment
        if sites:
            data[u'mode'] = u'specific'
            data[u'sites'] = sites
        return self.api_request(params=api_activate, data=data)

    def bake_agents(self):
        api_bake_agents = { u'action': u'bake_agents' }
        api_bake_agents.update(self.api_creds)
        return self.api_request(params=api_bake_agents)

class MultisiteAPI():
    def __init__(self, site_url=None, api_user=None, api_secret=None):
        if not site_url:
            site_url = _site_url()
        if not api_secret:
            api_user, api_secret = _site_creds(api_user)
        self.site_url = check_mk_url(site_url)
        self.api_creds = {'_username': api_user, '_secret': api_secret, 'request_format': 'python', 'output_format': 'python', '_transid': '-1'}
        self.down_from_now = {'_down_from_now': "from+for+now"}
        self.do_actions = {'_do_actions': "yes"}
        self.do_confirm = {'_do_confirm': "yes"}
        self.down_remove ={'_down_remove': "Remove"}

    def api_request(self, api_url, params, data=None, errmsg='Error', fail=True, command=False):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            if data:
                resp = requests.post(api_url, verify=False, params=params, data='request=%s' % repr(data))
            else:
                resp = requests.get(api_url, verify=False, params=params)
            if resp.status_code == 200 and command:
                if("MESSAGE: " in resp.text):                   
                    msg = resp.text[resp.text.find("\n")+1:]                   
                    return eval(msg)
                else:   
                    return eval(resp.text)
            elif resp.status_code == 200:
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

    def set_downtime(self, view_name, site, host, _down_comment, _down_minutes, **kwargs):
        result = []
        request = {'view_name': view_name, 'site': site, 'host': host, '_down_comment': _down_comment, '_down_minutes': _down_minutes}
        request.update(self.api_creds)
        request.update(self.down_from_now)
        request.update(self.do_actions)
        request.update(self.do_confirm)
        request.update(kwargs)
        resp = self.api_request(self.site_url + 'view.py', request, errmsg='Cannot get view data', command=True)
        header = resp[0]
        for data in resp[1:]:
            item = {}
            for i in range(len(header)):
                item[header[i]] = data[i]
            result.append(item)
        return result

    def revoke_downtime(self, view_name, site, host, _down_comment, **kwargs):
        result = []
        request = {'view_name': view_name, 'site': site, 'host': host}
        request.update(self.api_creds)
        request.update(self.do_actions)
        request.update(self.do_confirm)
        request.update(self.down_remove)
        request.update(kwargs)
        resp = self.api_request(self.site_url + 'view.py', request, errmsg='Cannot get view data', command=True)
        header = resp[0]
        for data in resp[1:]:
            item = {}
            for i in range(len(header)):
                item[header[i]] = data[i]
            result.append(item)
        return result
