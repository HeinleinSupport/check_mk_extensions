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
import time
import sys

def _check_mk_url(url):
    if url[-1] == '/':
        if not url.endswith('check_mk/'):
            url += 'check_mk/'
    else:
        if not url.endswith('check_mk'):
            url += '/check_mk/'
    return url

def _site_url():
    urldefault = None
    if 'OMD_ROOT' in os.environ and 'HOME' in os.environ and os.environ['HOME'] == os.environ['OMD_ROOT']:
        siteconfig = {}
        execfile(os.path.join(os.environ['OMD_ROOT'], 'etc', 'omd', 'site.conf'), siteconfig, siteconfig)
        urldefault = 'http://%s:%s/%s' % (siteconfig['CONFIG_APACHE_TCP_ADDR'],
                                          siteconfig['CONFIG_APACHE_TCP_PORT'],
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

class CMKRESTAPI():
    def __init__(self, site_url=None, api_user=None, api_secret=None):
        if not site_url:
            site_url = _site_url()
        if not api_secret:
            api_user, api_secret = _site_creds(api_user)
        self._api_url = '%sapi/v0' % _check_mk_url(site_url)
        self._session = requests.session()
        self._session.headers['Authorization'] = f"Bearer {api_user} {api_secret}"
        self._session.headers['Accept'] = 'application/json'

    def _check_response(self, resp):
        if resp.content:
            try:
                data = resp.json()
            except json.decoder.JSONDecodeError:
                data = resp.content
        else:
            data = {}
        etag = resp.headers.get('ETag', '').strip('"')
        if resp.status_code >= 400:
            sys.stderr.write("%r\n" % data)
        return data, etag, resp

    def _get_url(self, uri, data={}):
        return self._check_response(
            self._session.get(
                f"{self._api_url}/{uri}",
                params=data,
                allow_redirects=False,
            )
        )

    def _post_url(self, uri, data={}):
        return self._check_response(
            self._session.post(
                f"{self._api_url}/{uri}",
                json=data,
                headers={
                    "Content-Type": 'application/json',
                },
                allow_redirects=False,
            )
        )

    def _put_url(self, uri, etag, data={}):
        return self._check_response(
            self._session.put(
                f"{self._api_url}/{uri}",
                json=data,
                headers={
                    "Content-Type": 'application/json',
                    "If-Match": etag,
                },
                allow_redirects=False,
            )
        )
    
    def _delete_url(self, uri, etag):
        return self._check_response(
            self._session.delete(
                f"{self._api_url}/{uri}",
                headers={"If-Match": etag},
                allow_redirects=False,
            )
        )

    def add_host(self, hostname, folder, attributes={}):
        print(f'Add Host {hostname}')
        data, etag, resp = self._post_url(
            f"domain-types/host_config/collections/all",
            data={
                'host_name': hostname,
                'folder': folder,
                'attributes': attributes,
            },
        )
        if resp.status_code == 200:
            return data, etag
        resp.raise_for_status()

    def get_host(self, hostname, effective_attr=False):
        print(f'Get Host {hostname}')
        data, etag, resp = self._get_url(
            f"objects/host_config/{hostname}",
            data={"effective_attributes": "true" if effective_attr else "false"}
        )
        if resp.status_code == 200:
            return data, etag
        resp.raise_for_status()

    def get_all_hosts(self, effective_attr=False):
        print('Get All Hosts')
        data, etag, resp = self._get_url(
            f"domain-types/host_config/collections/all",
            data={"effective_attributes": "true" if effective_attr else "false"}
        )
        if resp.status_code != 200:
            resp.raise_for_status()
        hosts = {}
        for hinfo in data.get('value', []):
            if hinfo.get('domainType') == 'link':
                hostdata, etag, resp = self._get_url(
                    hinfo['href'],
                    data={"effective_attributes": "true" if effective_attr else "false"}
                )
                if resp.status_code != 200:
                    resp.raise_for_status()
                if hostdata.get('domainType') == 'host_config':
                    hosts[hostdata['id']] = hostdata['extensions']
        return hosts

    def delete_host(self, hostname, etag=None):
        print(f'Delete Host {hostname}')
        if not etag:
            hostdata, etag = self.get_host(hostname)
        data, etag, resp = self._delete_url(
            f"objects/host_config/{hostname}",
            etag
        )
        if resp.status_code == 200:
            return data, etag
        resp.raise_for_status()

    def edit_host(self, hostname, etag=None, set_attr={}, update_attr={}, unset_attr=[]):
        print(f'Edit Host {hostname}')
        if not etag:
            hostdata, etag = self.get_host(hostname)
        data, etag, resp = self._put_url(
            f"objects/host_config/{hostname}",
            etag,
            data={
                'attributes': set_attr,
                'update_attributes': update_attr,
                'remove_attributes': unset_attr,
            },
        )
        if resp.status_code == 200:
            return data, etag
        resp.raise_for_status()

    def disc_host(self, hostname):
        print(f'Discover Host {hostname}')
        data, etag, resp = self._post_url(
            f"objects/host/{hostname}/actions/discover-services/mode/tabula-rasa"
        )
        if resp.status_code == 204:
            return data, etag
        resp.raise_for_status()

    def _wait_for_activation(uri):
        code = 302
        while code == 302:
            time.sleep(1)
            print("Calling link %s" % uri)
            data, etag, resp = self._get_url(uri)
            code = resp.status_code
        return resp

    def activate(self, sites=[]):
        print('Activate Changes')
        data, etag, resp = self._post_url(
            "domain-types/activation_run/actions/activate-changes/invoke",
            data={
                'redirect': False,
                'sites': sites
            },
        )
        if resp.status_code == 200:
            return data, etag
        if resp.status_code == 302:
            if data.get('domainType') == 'activation_run':
                for link in data.get('links', []):
                    if link.get('rel') == 'urn:com.checkmk:rels/wait-for-completion':
                        r = self._wait_for_activation(link.get('href'))
                        if r.status_code == 204:
                            return {}, None
                        r.raise_for_status()
        resp.raise_for_status()

    def bake_agents(self):
        print('Bake Agents')
        data, etag, resp = self._post_url(
            "domain-types/agent/actions/bake",
        )
        if resp.status_code == 200:
            return data, etag
        resp.raise_for_status()

    # def download_agent(self, hostname, ostype):
    #     print('Download Agent')
    #     data, etag, resp = self._get_url(
    #         "objects/agent/ed81f94eb95181ca",
    #         data={
    #             "os_type": ostype,
    #             # "host_name": hostname,
    #         },
    #     )
    #     if resp.status_code == 204:
    #         return data, etag
    #     resp.raise_for_status()

    def set_downtime(self, comment, start_time, end_time, hostname,
                     services = None):
        print('Setting Downtime')
        if services:
            if not isinstance(services, list):
                services = [ services ]
            data, etag, resp = self._post_url(
                "domain-types/downtime/collections/service",
                data={
                    'downtime_type': 'service',
                    'start_time':    start_time, # 2017-07-21T17:32:28Z
                    'end_time':      end_time,   # 2017-07-21T17:32:28Z
                    'comment':       comment,
                    'host_name':     hostname,
                    'service_descriptions': services,
                }
            )
        else:
            data, etag, resp = self._post_url(
                "domain-types/downtime/collections/host",
                data={
                    'downtime_type': 'host',
                    'start_time':    start_time, # 2017-07-21T17:32:28Z
                    'end_time':      end_time,   # 2017-07-21T17:32:28Z
                    'comment':       comment,
                    'host_name':     hostname,
                }
            )
        if resp.status_code == 204:
            return data, etag
        resp.raise_for_status()

    def revoke_downtime(self, hostname, services = None):
        print('Removing Downtime')
        params={
            'delete_type': 'params',
            'hostname':    hostname,
        }
        if services:
            if not isinstance(services, list):
                services = [ services ]
            params['services'] = services

        data, etag, resp = self._post_url(
            "domain-types/downtime/actions/delete/invoke",
            data=params,
        )
        if resp.status_code == 204:
            return data, etag
        resp.raise_for_status()

class MultisiteAPI():
    def __init__(self, site_url=None, api_user=None, api_secret=None):
        if not site_url:
            site_url = _site_url()
        if not api_secret:
            api_user, api_secret = _site_creds(api_user)
        self._site_url = _check_mk_url(site_url)

        self._api_creds = {
            '_username': api_user,
            '_secret': api_secret,
            'request_format': 'python',
            'output_format': 'python',
            '_transid': '-1',
        }

    def _api_request(self, api_url, params, data=None):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            params.update(self._api_creds)
            if data:
                resp = requests.post(
                    self._site_url + api_url,
                    verify=False,
                    params=params,
                    data='request=%s' % repr(data),
                    allow_redirects=False,
                )
            else:
                resp = requests.get(
                    self._site_url + api_url,
                    verify=False,
                    params=params,
                    allow_redirects=False,
                )
            if resp.status_code == 200:
                if "MESSAGE: " in resp.text:
                    msg = resp.text[resp.text.find("\n")+1:]
                    return eval(msg)
                if resp.text.startswith('ERROR: '):
                    raise ValueError(resp.text[7:])
                else:
                    return eval(resp.text)
            else:
                sys.stderr.write("%s\n" % resp.text)
                resp.raise_for_status()

    def view(self, view_name, **kwargs):
        result = []
        request = {'view_name': view_name}
        request.update(kwargs)
        resp = self._api_request('view.py', request)
        header = resp[0]
        for data in resp[1:]:
            item = {}
            for i in range(len(header)):
                item[header[i]] = data[i]
            result.append(item)
        return result

