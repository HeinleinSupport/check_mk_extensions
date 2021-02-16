#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2021 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

# https://checkmk.com/cms_rest_api.html

"""API-Wrapper for the CheckMK 2.0 REST API and the Multisite API (Views)"""

from pprint import pprint
import requests
import warnings
import os
import json
import time
import sys
import configparser

def _check_mk_url(url):
    """ adds trailing check_mk path component to URL """
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
        siteconfig = configparser.ConfigParser()
        with open(os.path.join(os.environ['OMD_ROOT'], 'etc', 'omd', 'site.conf'), 'r') as f:
            config_string = '[GLOBAL]\n' + f.read()
            siteconfig.read_string(config_string)
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

class CMKRESTAPI():
    def __init__(self, site_url=None, api_user=None, api_secret=None):
        """Initialize a REST-API instance. URL, User and Secret can be automatically taken from local site if running as site user.

        Args:
            site_url: the site URL
            api_user: username of automation user account
            api_secret: automation secret

        Returns:
            instance of CMKRESTAPI
        """
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
        """Adds a host to a folder in the CheckMK configuration.

        Args:
            hostname: unique name for the new host
            folder: The folder-id of the folder under which this folder shall be created. May be 'root' for the root-folder.

        Returns:
            (data, etag)
            data: host's data
            etag: current etag value
        """
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
        """Gets host configuration including eTag value.

        Args:
            hostname:  A hostname
            effective_attr: Show all effective attributes, which affect this host, not just the attributes which were set on this host specifically. This includes all attributes of all of this host's parent folders.

        Returns:
            (data, etag)
            data: host's data
            etag: current etag value
        """
        print(f'Get Host {hostname}')
        data, etag, resp = self._get_url(
            f"objects/host_config/{hostname}",
            data={"effective_attributes": "true" if effective_attr else "false"}
        )
        if resp.status_code == 200:
            return data, etag
        resp.raise_for_status()

    def get_all_hosts(self, effective_attr=False):
        """Gets all hosts from the CheckMK configuration.

        Args:
            effective_attr: Show all effective attributes, which affect this host, not just the attributes which were set on this host specifically. This includes all attributes of all of this host's parent folders.

        Returns:
            hosts: Dictionary of host data
        """
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
        """Deletes a host from the CheckMK configuration.

        Args:
            hostname: name of the host
            etag: (optional) etag value, if not provided the host will be looked up first using get_host().

        Returns:
            (data, etag)
            data: host's data
            etag: current etag value
        """
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
        """Edit a host in the CheckMK configuration.

        Args:
            hostname: name of the host
            etag: (optional) etag value, if not provided the host will be looked up first using get_host().
            set_attr: Replace all currently set attributes on the host, with these attributes. Any previously set attributes which are not given here will be removed.
            update_attr: Just update the hosts attributes with these attributes. The previously set attributes will not be touched.
            unset_attr: A list of attributes which should be removed.

        Returns:
            (data, etag)
            data: host's data
            etag: current etag value
        """
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
        """Discovers services on a host.

        Args:
            hostname: name of the host

        Returns:
            (data, etag)
            data: discovery data
            etag: current etag value
        """
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
        """Activates pending changes

        Args:
            sites: On which sites the configuration shall be activated. An empty list means all sites which have pending changes.

        Returns:
            (data, etag): usually both empty
        """
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
        """Bakes agent packages

        Returns:
            (data, etag): usually both empty
        """
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
        """Sets a scheduled downtime on a host or a service

        Args:
            comment: string
            start_time: The start datetime of the new downtime. The format has to conform to the ISO 8601 profile 2017-07-21T17:32:28Z
            end_time: The end datetime of the new downtime. The format has to conform to the ISO 8601 profile 2017-07-21T17:42:28Z
            hostname: hostname
            services: if set a list of service descriptions

        Returns:
            (data, etag): usually empty
        """
        print('Setting Downtime')
        if services:
            if not isinstance(services, list):
                services = [ services ]
            data, etag, resp = self._post_url(
                "domain-types/downtime/collections/service",
                data={
                    'downtime_type': 'service',
                    'start_time':    start_time, # 2017-07-21T17:32:28Z
                    'end_time':      end_time,   # 2017-07-21T17:42:28Z
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
                    'end_time':      end_time,   # 2017-07-21T17:42:28Z
                    'comment':       comment,
                    'host_name':     hostname,
                }
            )
        if resp.status_code == 204:
            return data, etag
        resp.raise_for_status()

    def revoke_downtime(self, hostname, services = None):
        """Revokes scheduled downtime

        Args:
            hostname: name of host
            services: list of service descriptions. If empty, all scheduled downtimes for the host will be removed.

        Returns:
            (data, etag): usually empty
        """
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
        """Fetches data from a Multisite view

        Args:
            view_name: name of the view to query
            kwargs: more arguments for the view

        Returns:
            List of Dictionaries, every item is a Dict(TableHeader -> Value) for the row
        """
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

