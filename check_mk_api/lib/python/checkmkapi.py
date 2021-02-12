#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2021 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

# https://checkmk.com/cms_rest_api.html

from pprint import pprint
import requests
import warnings
import os
import json

class CMKRESTAPI():
    def __init__(self, site_url=None, api_user=None, api_secret=None):
        if not site_url:
            site_url = self._site_url()
        if not api_secret:
            api_user, api_secret = self._site_creds(api_user)
        self.api_url = '%sapi/v0' % self._check_mk_url(site_url)
        self.session = requests.session()
        self.session.headers['Authorization'] = f"Bearer {api_user} {api_secret}"
        self.session.headers['Accept'] = 'application/json'

    def _check_mk_url(self, url):
        if url[-1] == '/':
            if not url.endswith('check_mk/'):
                url += 'check_mk/'
        else:
            if not url.endswith('check_mk'):
                url += '/check_mk/'
        return url

    def _site_url(self):
        urldefault = None
        if 'OMD_ROOT' in os.environ and 'HOME' in os.environ and os.environ['HOME'] == os.environ['OMD_ROOT']:
            siteconfig = {}
            execfile(os.path.join(os.environ['OMD_ROOT'], 'etc', 'omd', 'site.conf'), siteconfig, siteconfig)
            urldefault = 'http://%s:%s/%s' % (siteconfig['CONFIG_APACHE_TCP_ADDR'],
                                              siteconfig['CONFIG_APACHE_TCP_PORT'],
                                              os.environ['OMD_SITE'])
        return urldefault

    def _site_creds(self, username=None):
        password = None
        if 'OMD_ROOT' in os.environ and 'HOME' in os.environ and os.environ['HOME'] == os.environ['OMD_ROOT']:
            if not username:
                username = 'automation'
            password = open(os.path.join(os.environ['OMD_ROOT'], 'var', 'check_mk', 'web', username, 'automation.secret')).read().strip()
        return username, password

    def _check_response(self, resp):
        pprint(resp.request.url)
        pprint(resp.request.headers)
        resp.raise_for_status()
        if resp.content:
            data = resp.json()
        else:
            data = {}
        etag = resp.headers.get('ETag', '').strip('"')
        return data, etag

    def _get_url(self, uri, data={}):
        pprint(uri)
        pprint(f"{self.api_url}/{uri}")
        return self._check_response(
            self.session.get(
                f"{self.api_url}/{uri}",
                params=data
            )
        )

    def _post_url(self, uri, data={}):
        return self._check_response(
            self.session.post(
                f"{self.api_url}/{uri}",
                json=data,
                headers={"Content-Type": 'application/json',}
            )
        )

    def _put_url(self, uri, etag, data={}):
        return self._check_response(
            self.session.put(
                f"{self.api_url}/{uri}",
                json=data,
                headers={
                    "Content-Type": 'application/json',
                    "If-Match": etag,
                }
            )
        )
    
    def _delete_url(self, uri, etag):
        return self._check_response(
            self.session.delete(
                f"{self.api_url}/{uri}",
                headers={"If-Match": etag}
            )
        )

    def add_host(self, hostname, folder, attributes={}):
        try:
            return self._post_url(
                f"domain-types/host_config/collections/all",
                data={
                    'host_name': hostname,
                    'folder': folder,
                    'attributes': attributes
                },
            )
        except requests.exceptions.HTTPError as er:
            if er.response.status_code == 400:
                return {}, None
            raise

    def get_host(self, hostname, effective_attr=False):
        return self._get_url(
            f"/objects/host_config/{hostname}",
            data={"effective_attributes": "true" if effective_attr else "false"}
        )

    def get_all_hosts(self, effective_attr=False):
        data, etag = self._get_url(
            f"/domain-types/host_config/collections/all",
            data={"effective_attributes": "true" if effective_attr else "false"}
        )
        hosts = {}
        for hinfo in data.get('value', []):
            if hinfo.get('domainType') == 'link':
                hostdata, etag = self._get_url(
                    hinfo['href'],
                    data={"effective_attributes": "true" if effective_attr else "false"}
                )
                if hostdata.get('domainType') == 'host_config':
                    hosts[hostdata['id']] = hostdata['extensions']
        return hosts

    def delete_host(self, hostname, etag=None):
        if not etag:
            hostdata, etag = self.get_host(hostname)
        return self._delete_url(f"/objects/host_config/{hostname}", etag)

    def edit_host(self, hostname, etag=None, set_attr={}, update_attr={}, unset_attr=[]):
        if not etag:
            hostdata, etag = self.get_host(hostname)
        return self._put_url(
            f"objects/host_config/{hostname}",
            etag,
            data={
                'attributes': set_attr,
                'update_attributes': update_attr,
                'remove_attributes': unset_attr,
            },
        )

    def disc_host(self, hostname):
        return self._post_url(f"/objects/host/{hostname}/actions/discover-services/mode/tabula-rasa")

    def activate(self, sites=[]):
        data, etag = self._post_url(
            "/domain-types/activation_run/actions/activate-changes/invoke",
            data={
                'redirect': False,
                'sites': sites
            },
        )
        pprint(data)
        if data.get('domainType') == 'activation_run':
            for link in data.get('links', []):
                if link.get('rel') == 'urn:com.checkmk:rels/wait-for-completion':
                    pprint(link.get('href'))
                    return self._get_url(link.get('href'))
        return data, etag

    # def bake_agents(self):
    #     api_bake_agents = { u'action': u'bake_agents' }
    #     api_bake_agents.update(self.api_creds)
    #     return self.api_request(params=api_bake_agents)

# class MultisiteAPI():
#     def __init__(self, site_url, api_user, api_secret):
#         if not site_url:
#             site_url = _site_url()
#         if not api_secret:
#             api_user, api_secret = _site_creds(api_user)
#         self.site_url = check_mk_url(site_url)
        
#         self.api_creds = {'_username': api_user, '_secret': api_secret, 'request_format': 'python', 'output_format': 'python', '_transid': '-1'}
#         self.down_from_now = {'_down_from_now': "from+for+now"}
#         self.do_actions = {'_do_actions': "yes"}
#         self.do_confirm = {'_do_confirm': "yes"}
#         self.down_remove ={'_down_remove': "Remove"}

#     def api_request(self, api_url, params, data=None, errmsg='Error', fail=True, command=False):
#         with warnings.catch_warnings():
#             warnings.simplefilter('ignore')
#             if data:
#                 resp = requests.post(api_url, verify=False, params=params, data='request=%s' % repr(data))
#             else:
#                 resp = requests.get(api_url, verify=False, params=params)
#             if resp.status_code == 200 and command:
#                 if("MESSAGE: " in resp.text):                   
#                     msg = resp.text[resp.text.find("\n")+1:]                   
#                     return eval(msg)
#                 else:   
#                     return eval(resp.text)
#             elif resp.status_code == 200:
#                 return eval(resp.text)
#             else:
#                 raise resp.text
#         return []

#     def view(self, view_name, **kwargs):
#         result = []
#         request = {'view_name': view_name}
#         request.update(self.api_creds)
#         request.update(kwargs)
#         resp = self.api_request(self.site_url + 'view.py', request, errmsg='Cannot get view data')
#         header = resp[0]
#         for data in resp[1:]:
#             item = {}
#             for i in xrange(len(header)):
#                 item[header[i]] = data[i]
#             result.append(item)
#         return result

#     def set_downtime(self, view_name, site, host, _down_comment, _down_minutes, **kwargs):
#         result = []
#         request = {'view_name': view_name, 'site': site, 'host': host, '_down_comment': _down_comment, '_down_minutes': _down_minutes}
#         request.update(self.api_creds)
#         request.update(self.down_from_now)
#         request.update(self.do_actions)
#         request.update(self.do_confirm)
#         request.update(kwargs)
#         resp = self.api_request(self.site_url + 'view.py', request, errmsg='Cannot get view data', command=True)
#         header = resp[0]
#         for data in resp[1:]:
#             item = {}
#             for i in range(len(header)):
#                 item[header[i]] = data[i]
#             result.append(item)
#         return result

#     def revoke_downtime(self, view_name, site, host, _down_comment, **kwargs):
#         result = []
#         request = {'view_name': view_name, 'site': site, 'host': host}
#         request.update(self.api_creds)
#         request.update(self.do_actions)
#         request.update(self.do_confirm)
#         request.update(self.down_remove)
#         request.update(kwargs)
#         resp = self.api_request(self.site_url + 'view.py', request, errmsg='Cannot get view data', command=True)
#         header = resp[0]
#         for data in resp[1:]:
#             item = {}
#             for i in range(len(header)):
#                 item[header[i]] = data[i]
#             result.append(item)
#         return result
