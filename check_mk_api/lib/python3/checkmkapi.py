#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2021 Heinlein Support GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

# https://checkmk.com/cms_rest_api.html

"""API-Wrapper for the CheckMK 2.0 REST API and the Multisite API (Views)"""

import requests
import warnings
import os
import json
import time
import sys
import configparser
import json

def _check_mk_url(url):
    """ adds trailing check_mk path component to URL """
    if url[-1] != '/':
        url += '/'
    if not url.endswith('check_mk/'):
        url += 'check_mk/'
    return url

def _site_url():
    urldefault = None
    if os.environ.get('HOME', 'a') == os.environ.get('OMD_ROOT', 'b'):
        import cmk.utils.site
        siteconfig = cmk.utils.site.get_omd_config()
        urldefault = 'http://%s:%s/%s' % (siteconfig['CONFIG_APACHE_TCP_ADDR'],
                                          siteconfig['CONFIG_APACHE_TCP_PORT'],
                                          os.environ['OMD_SITE'])
    return urldefault

def _site_creds(username=None):
    password = None
    if os.environ.get('HOME', 'a') == os.environ.get('OMD_ROOT', 'b'):
        import cmk.utils.paths
        if not username:
            username = 'automation'
        password = open(
            os.path.join(
                cmk.utils.paths.var_dir,
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
        self._api_url = '%sapi/1.0' % _check_mk_url(site_url)
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
        # if resp.status_code >= 400:
        #     sys.stderr.write("%r\n" % data)
        return data, etag, resp

    def _get_url(self, uri, etag=None, data={}):
        return self._check_response(
            self._session.get(
                f"{self._api_url}/{uri}",
                params=data,
                allow_redirects=False,
            )
        )

    def _get_abolute_url(self, uri, etag=None, data={}):
        return self._check_response(
            self._session.get(
                f"{uri}",
                params=data,
                allow_redirects=False,
            )
        )

    def _post_url(self, uri, etag=None, data={}):
        headers={
            "Content-Type": 'application/json',
        }
        if etag:
            headers['If-Match'] = etag
        return self._check_response(
            self._session.post(
                f"{self._api_url}/{uri}",
                json=data,
                headers=headers,
                allow_redirects=False,
            )
        )

    def _put_url(self, uri, etag=None, data={}):
        headers={
            "Content-Type": 'application/json',
        }
        if etag:
            headers['If-Match'] = etag
        return self._check_response(
            self._session.put(
                f"{self._api_url}/{uri}",
                json=data,
                headers=headers,
                allow_redirects=False,
            )
        )

    def _delete_url(self, uri, etag=None, data=None):
        headers={
            "Content-Type": 'application/json',
        }
        if etag:
            headers['If-Match'] = etag
        return self._check_response(
            self._session.delete(
                f"{self._api_url}/{uri}",
                headers=headers,
                allow_redirects=False,
            )
        )

    def _request(self, method, uri, ok_code=200, etag=None, data=None):
        if isinstance(ok_code, int):
            ok_code=[ok_code]
        data, etag, resp = method(uri, etag, data)
        if resp.status_code in ok_code:
            return data, etag
        resp.raise_for_status()        

#   .--Folder--------------------------------------------------------------.
#   |                     _____     _     _                                |
#   |                    |  ___|__ | | __| | ___ _ __                      |
#   |                    | |_ / _ \| |/ _` |/ _ \ '__|                     |
#   |                    |  _| (_) | | (_| |  __/ |                        |
#   |                    |_|  \___/|_|\__,_|\___|_|                        |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def create_folder(self, title, parent, name=None, attributes={}):
        """Adds a folder to a parent folder.

        Args:
            title: The folder title as displayed in the user interface.
            parent: The folder in which the new folder shall be placed in. The root-folder is specified by '/'.
            name: The filesystem directory name (not path!) of the folder. No slashes are allowed. Will be deduced from the title if not specified.

        Returns:
            (data, etag)
            data: folder's data
            etag: current etag value
        """
        params={
                'title': title,
                'parent': parent,
                'attributes': attributes,
        }
        if name:
            params['name'] = name
        return self._request(
            self._post_url,
            "domain-types/folder_config/collections/all",
            data=params,
        )

    def get_folder(self, folder, show_hosts=False):
        """Gets a single folder

        Args:
            folder: The path of the folder being requested.
            show_hosts: When True, all hosts that are stored in this folder will also be shown.

        Returns:
            (data, etag)
            data: folder's data
            etag: current etag value
        """
        folder = folder.replace('/', '~')
        return self._request(
            self._get_url,
            f"objects/folder_config/{folder}",
            data={
                "show_hosts": show_hosts,
            }
        )

    def get_all_folders(self, parent='/', recursive=False, show_hosts=False):
        """Gets a folder subtree

        Args:
            parent: Show all sub-folders of this folder. The default is the root-folder.
            recursive: List the folder (default: root) and all its sub-folders recursively.
            show_hosts: When True, all hosts that are stored in this folder will also be shown.

        Returns:
            (data, etag)
            data: list of folders
            etag: current etag value
        """
        parent = parent.replace('/', '~')
        return self._request(
            self._get_url,
            f"domain-types/folder_config/collections/all",
            data={
                "parent": parent,
                "recursive": recursive,
                "show_hosts": show_hosts,
            }
        )

    def delete_folder(self, folder):
        """Delete a folder

        Args:
            folder: Folder path

        Returns:
            ({}, '')
        """
        folder = folder.replace('/', '~')
        return self._request(
            self._delete_url,
            f"objects/folder_config/{folder}",
            ok_code=204,
        )

    def edit_folder(self, folder, etag=None, title=None, attributes={}, update_attr={}, remove_attr=[]):
        """Edit a folder

        Args:
            folder: The path of the folder being requested.
            etag: (optional) etag value, if not provided the folder will be looked up first using get_folder().
            title: (optional) The title of the folder. Used in the GUI.
            set_attr: Replace all currently set attributes on the folder with these attributes. Any previously set attributes which are not given here will be removed.
            update_attr: Just update the folder's attributes with these attributes. The previously set attributes will not be touched.
            unset_attr: A list of attributes which should be removed.

            Only pass one of set_attr, update_attr or unset_attr.

        Returns:
            (data, etag)
            data: folder's data
            etag: current etag value
        """
        folder = folder.replace('/', '~')
        if not etag:
            folderdata, etag = self.get_folder(folder)
        changes = {}
        if title:
            changes['title'] = title
        if attributes:
            changes['attributes'] = attributes
        elif update_attr:
            changes['update_attributes'] = update_attr
        elif remove_attr:
            changes['remove_attributes'] = remove_attr
        if changes:
            return self._request(
                self._put_url,
                f"objects/folder_config/{folder}",
                etag=etag,
                data=changes,
            )
        return None, None

    def move_folder(self, folder, destination, etag="*"):
        """Moves a folder into a destination folder.

        Args:
            folder: The path of the folder being requested.
            destination: Where the folder has to be moved to.
            etag: (optional) etag value, if not provided the folder will be looked up first using get_folder().

        Returns:
            (data, etag)
            data: folder's data
            etag: current etag value
        """
        folder = folder.replace('/', '~')
        destination = destination.replace('/', '~')
        return self._request(
            self._post_url,
            f"objects/folder_config/{folder}/actions/move/invoke",
            etag=etag,
            data={
                "destination": destination,
            },
        )

#   .--Host----------------------------------------------------------------.
#   |                         _   _           _                            |
#   |                        | | | | ___  ___| |_                          |
#   |                        | |_| |/ _ \/ __| __|                         |
#   |                        |  _  | (_) \__ \ |_                          |
#   |                        |_| |_|\___/|___/\__|                         |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

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
        return self._request(
            self._post_url,
            f"domain-types/host_config/collections/all",
            data={
                'host_name': hostname,
                'folder': folder,
                'attributes': attributes,
            },
        )

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
        return self._request(
            self._get_url,
            f"objects/host_config/{hostname}",
            data={"effective_attributes": "true" if effective_attr else "false"}
        )

    def get_all_hosts(self, effective_attr=False, attributes=True):
        """Gets all hosts from the CheckMK configuration.

        Args:
            effective_attr: Show all effective attributes, which affect this host, not just the attributes which were set on this host specifically. This includes all attributes of all of this host's parent folders.
            attributes: If False do not fetch hosts' data

        Returns:
            hosts: Dictionary of host data or dict of hostname -> URL depending on aatributes parameter
        """
        data, etag = self._request(
            self._get_url,
            f"domain-types/host_config/collections/all",
            data={"effective_attributes": "true" if effective_attr else "false"}
        )
        hosts = {}
        etags = {}
        for hinfo in data.get('value', []):
            if hinfo.get('domainType') == 'link':
                if attributes:
                    hostdata, etag, resp = self._get_url(
                        hinfo['href'],
                        data={"effective_attributes": "true" if effective_attr else "false"}
                    )
                    if resp.status_code != 200:
                        resp.raise_for_status()
                    if hostdata.get('domainType') == 'host_config':
                        hosts[hostdata['id']] = hostdata['extensions']
                        etags[hostdata['id']] = etag
                else:
                    hosts[hinfo['title']] = hinfo['href']
            elif hinfo.get('domainType') == 'host_config':
                if attributes:
                    self_urls = [
                        link['href'] 
                        for link in hinfo.get("links", [])
                        if link["rel"] == "self"]
                    hostdata, etag, resp = self._get_abolute_url(
                        self_urls[0],
                        data={"effective_attributes": "true" if effective_attr else "false"}
                    )
                    if resp.status_code != 200:
                        resp.raise_for_status()
                    if hostdata.get('domainType') == 'host_config':
                        hosts[hostdata['id']] = hostdata['extensions']
                        etags[hostdata['id']] = etag
                else:
                    hosts[hinfo['title']] = hinfo['extensions']

        return hosts, etags

    def delete_host(self, hostname):
        """Deletes a host from the CheckMK configuration.

        Args:
            hostname: name of the host

        Returns:
            (data, etag)
            data: host's data
            etag: current etag value
        """
        return self._request(
            self._delete_url,
            f"objects/host_config/{hostname}",
            ok_code=204,
        )

    def edit_host(self, hostname, etag=None, set_attr={}, update_attr={}, unset_attr=[]):
        """Edit a host in the CheckMK configuration.

        Args:
            hostname: name of the host
            etag: (optional) etag value, if not provided the host will be looked up first using get_host().
            set_attr: Replace all currently set attributes on the host, with these attributes. Any previously set attributes which are not given here will be removed.
            update_attr: Just update the hosts attributes with these attributes. The previously set attributes will not be touched.
            unset_attr: A list of attributes which should be removed.

            Only pass one of set_attr, update_attr or unset_attr.

        Returns:
            (data, etag)
            data: host's data
            etag: current etag value
        """
        if not etag:
            hostdata, etag = self.get_host(hostname)
        changes = {}
        if set_attr:
            changes['attributes'] = set_attr
        elif update_attr:
            changes['update_attributes'] = update_attr
        elif unset_attr:
            changes['remove_attributes'] = unset_attr
        if changes:
            return self._request(
                self._put_url,
                f"objects/host_config/{hostname}",
                etag=etag,
                data=changes,
            )
        return None, None

    def disc_host(self, hostname, mode="new"):
        """Discovers services on a host.

        Args:
            hostname: name of the host

        Returns:
            (data, etag)
            data: discovery data
            etag: current etag value
        """
        return self._request(
            self._post_url,
            f"domain-types/service_discovery_run/actions/start/invoke",
            ok_code=[200, 204, 302],
            data={"host_name": hostname, "mode": mode},
        )

#   .--Activation----------------------------------------------------------.
#   |              _        _   _            _   _                         |
#   |             / \   ___| |_(_)_   ____ _| |_(_) ___  _ __              |
#   |            / _ \ / __| __| \ \ / / _` | __| |/ _ \| '_ \             |
#   |           / ___ \ (__| |_| |\ V / (_| | |_| | (_) | | | |            |
#   |          /_/   \_\___|\__|_| \_/ \__,_|\__|_|\___/|_| |_|            |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def _wait_for_activation(uri):
        code = 302
        while code == 302:
            time.sleep(1)
            data, etag, resp = self._get_url(uri)
            code = resp.status_code
        return data, etag, resp

    def activate(self, sites=[]):
        """Activates pending changes

        Args:
            sites: On which sites the configuration shall be activated. An empty list means all sites which have pending changes.

        Returns:
            (data, etag): usually both empty
        """
        # sleep for 2s to let API settle down
        time.sleep(2)
        postdata = { 'redirect': False, 'sites': sites, 'force_foreign_changes': False }
        data, etag, resp = self._post_url(
            "domain-types/activation_run/actions/activate-changes/invoke",
            etag='*',
            data=postdata,
        )
        if resp.status_code == 422:
            return data, etag
        if resp.status_code == 200:
            return data, etag
        if resp.status_code == 302:
            if data.get('domainType') == 'activation_run':
                for link in data.get('links', []):
                    if link.get('rel') == 'urn:com.checkmk:rels/wait-for-completion':
                        d, e, r = self._wait_for_activation(link.get('href'))
                        if r.status_code == 204:
                            return d, e
                        r.raise_for_status()
        resp.raise_for_status()

#   .--Agent---------------------------------------------------------------.
#   |                        _                    _                        |
#   |                       / \   __ _  ___ _ __ | |_                      |
#   |                      / _ \ / _` |/ _ \ '_ \| __|                     |
#   |                     / ___ \ (_| |  __/ | | | |_                      |
#   |                    /_/   \_\__, |\___|_| |_|\__|                     |
#   |                            |___/                                     |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def bake_agents(self):
        """Bakes agent packages

        Returns:
            (data, etag): usually both empty
        """
        return self._request(
            self._post_url,
            "domain-types/agent/actions/bake/invoke",
        )

    def download_agent(self, hostname, ostype):
        """Download agent package for a host

        Args:
            hostname: name of the host
            ostype: type of agent ("aix_tgz", "linux_deb", "linux_rpm", "linux_tgz", "solaris_pkg", "solaris_tgz" or "windows_msi")

        Returns:
            filename, filecontent
        """

        data, etag, resp = self._get_url(
            "domain-types/agent/actions/download_by_host/invoke",
            data={
                "agent_type": "host_name",
                "host_name": hostname,
                "os_type": ostype,
            })
        if resp.status_code == 200:
            filename = resp.headers["content-disposition"].split("filename=")[1].strip('"')
            resp.raw.decode_content = True
            return filename, resp.raw
        resp.raise_for_status()

#   .--Downtime------------------------------------------------------------.
#   |           ____                      _   _                            |
#   |          |  _ \  _____      ___ __ | |_(_)_ __ ___   ___             |
#   |          | | | |/ _ \ \ /\ / / '_ \| __| | '_ ` _ \ / _ \            |
#   |          | |_| | (_) \ V  V /| | | | |_| | | | | | |  __/            |
#   |          |____/ \___/ \_/\_/ |_| |_|\__|_|_| |_| |_|\___|            |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

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
        if services:
            if not isinstance(services, list):
                services = [ services ]
            return self._request(
                self._post_url,
                "domain-types/downtime/collections/service",
                ok_code=204,
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
            return self._request(
                self._post_url,
                "domain-types/downtime/collections/host",
                ok_code=204,
                data={
                    'downtime_type': 'host',
                    'start_time':    start_time, # 2017-07-21T17:32:28Z
                    'end_time':      end_time,   # 2017-07-21T17:42:28Z
                    'comment':       comment,
                    'host_name':     hostname,
                }
            )

    def revoke_downtime(self, hostname, services = None):
        """Revokes scheduled downtime

        Args:
            hostname: name of host
            services: list of service descriptions. If empty, all scheduled downtimes for the host will be removed.

        Returns:
            (data, etag): usually empty
        """
        params={
            'delete_type': 'params',
            'hostname':    hostname,
        }
        if services:
            if not isinstance(services, list):
                services = [ services ]
            params['services'] = services

        return self._request(
            self._post_url,
            "domain-types/downtime/actions/delete/invoke",
            ok_code=204,
            data=params,
        )

#   .--Acknowledge Problem-------------------------------------------------.
#   |       _        _                        _          _                 |
#   |      / \   ___| | ___ __   _____      _| | ___  __| | __ _  ___      |
#   |     / _ \ / __| |/ / '_ \ / _ \ \ /\ / / |/ _ \/ _` |/ _` |/ _ \     |
#   |    / ___ \ (__|   <| | | | (_) \ V  V /| |  __/ (_| | (_| |  __/     |
#   |   /_/   \_\___|_|\_\_| |_|\___/ \_/\_/ |_|\___|\__,_|\__, |\___|     |
#   |                                                      |___/           |
#   |               ____            _     _                                |
#   |              |  _ \ _ __ ___ | |__ | | ___ _ __ ___                  |
#   |              | |_) | '__/ _ \| '_ \| |/ _ \ '_ ` _ \                 |
#   |              |  __/| | | (_) | |_) | |  __/ | | | | |                |
#   |              |_|   |_|  \___/|_.__/|_|\___|_| |_| |_|                |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def acknowledge_host_problem(self, hostname, comment, sticky=True, persistent=False, notify=False):
        """Acknowledges host problem

        Args:
            hostname: name of host
            comment: ack comment
            sticky, persistent, notify: options for ack

        Returns:
            (data, etag): usually empty
        """
        params={
            'acknowledge_type': 'host',
            'host_name': hostname,
            'comment': comment,
            'sticky': sticky,
            'persistent': persistent,
            'notify': notify,
        }
        return self._request(
            self._post_url,
            "/domain-types/acknowledge/collections/host",
            ok_code=204,
            data=params,
        )

    def acknowledge_service_problem(self, hostname, service, comment, sticky=True, persistent=False, notify=False):
        """Acknowledges service problem

        Args:
            hostname: name of host
            service: service description
            comment: ack comment
            sticky, persistent, notify: options for ack

        Returns:
            (data, etag): usually empty
        """
        params={
            'acknowledge_type': 'service',
            'host_name': hostname,
            'service_description': service,
            'comment': comment,
            'sticky': sticky,
            'persistent': persistent,
            'notify': notify,
        }
        return self._request(
            self._post_url,
            "/domain-types/acknowledge/collections/service",
            ok_code=204,
            data=params,
        )

#   .--User----------------------------------------------------------------.
#   |                         _   _                                        |
#   |                        | | | |___  ___ _ __                          |
#   |                        | | | / __|/ _ \ '__|                         |
#   |                        | |_| \__ \  __/ |                            |
#   |                         \___/|___/\___|_|                            |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def create_user(self, username, fullname, args):
        """Creates a new user

        Args:
            username: A unique username for the user
            fullname: The alias or full name of the user
            args: additional options (see REST API documentation)

        Returns:
            (data, etag): new user object and eTag
        """
        params={
            'username': username,
            'fullname': fullname,
        }
        params.update(args)
        return self._request(
            self._post_url,
            "domain-types/user_config/collections/all",
            data=params,
        )

    def get_user(self, username):
        """Show a user

        Args:
            username: Username

        Returns:
            (data, etag): user object and eTag
        """
        return self._request(
            self._get_url,
            f"objects/user_config/{username}",
        )

    def edit_user(self, username, etag=None, args=None):
        """Edit a user

        Args:
            username: The name of the user to edit
            etag: The value of the, to be modified, object's ETag header.
            args: additional options (see REST API documentation)

        Returns:
            (data, etag): the user object and eTag
        """
        if not etag:
            userdata, etag = self.get_user(username)
        return self._request(
            self._put_url,
            f"objects/host_config/{username}",
            etag,
            data=args
        )

    def delete_user(self, username):
        """Delete a user

        Args:
            username: The name of the user to delete

        Returns:
            Nothing
        """
        return self._request(
            self._delete_url,
            f"objects/user_config/{username}",
            ok_code=204,
        )

#   .--Contact Group-------------------------------------------------------.
#   |   ____            _             _      ____                          |
#   |  / ___|___  _ __ | |_ __ _  ___| |_   / ___|_ __ ___  _   _ _ __     |
#   | | |   / _ \| '_ \| __/ _` |/ __| __| | |  _| '__/ _ \| | | | '_ \    |
#   | | |__| (_) | | | | || (_| | (__| |_  | |_| | | | (_) | |_| | |_) |   |
#   |  \____\___/|_| |_|\__\__,_|\___|\__|  \____|_|  \___/ \__,_| .__/    |
#   |                                                            |_|       |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def create_contactgroup(self, name, alias):
        """Create a contact group

        Args:
            name: A unique name for the contact group.
            alias: An alias for the contact group.

        Returns:
            (data, etag): contact group object and eTag    
        """
        return self._request(
            self._post_url,
            "domain-types/contact_group_config/collections/all",
            data={
                "name": name,
                "alias": alias,
            },
        )

    def get_contactgroup(self, name):
        """Get a contact group

        Args:
            name: The name of the contact group.

        Returns:
            (data, etag): contact group object and eTag    
        """
        return self._request(
            self._get_url,
            f"objects/contact_group_config/{name}"
        )

    def get_all_contactgroups(self):
        """Get all contact groups

        Returns:
            (data, etag): contact group objects and eTag    
        """
        return self._request(
            self._get_url,
            f"domain-types/contact_group_config/collections/all"
        )

    def edit_contactgroup(self, name, alias, etag="*"):
        """Change the contact group's alias

        Args:
            name: The name of the contact group.
            alias: The new alias.
            etag: The value of the, to be modified, object's ETag header.

        Returns:
            (data, etag): contact group object and eTag    
        """
        return self._request(
            self._put_url,
            f"objects/contact_group_config/{name}",
            etag=etag,
            data={
                "alias": alias,
            }
        )

    def delete_contactgroup(self, name):
        """Delete the contact group

        Args:
            name: The name of the contact group.
        """
        return self._request(
            self._delete_url,
            f"objects/contact_group_config/{name}",
            ok_code=204,
        )

#   .--Timeperiod----------------------------------------------------------.
#   |        _____ _                                _           _          |
#   |       |_   _(_)_ __ ___   ___ _ __   ___ _ __(_) ___   __| |         |
#   |         | | | | '_ ` _ \ / _ \ '_ \ / _ \ '__| |/ _ \ / _` |         |
#   |         | | | | | | | | |  __/ |_) |  __/ |  | | (_) | (_| |         |
#   |         |_| |_|_| |_| |_|\___| .__/ \___|_|  |_|\___/ \__,_|         |
#   |                              |_|                                     |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def create_timeperiod(self, name, alias, active_time_ranges, exceptions = [], exclude = []):
        """Create a time period

        Args:
            name: A unique name for the time period.
            alias: An alias for the time period.
            active_time_ranges: The list of active time ranges.
            exceptions: A list of additional time ranges to be added.
            exclude: A list of time period aliases whose periods are excluded.

        Returns:
            Nothing
        """
        params={
            'name': name,
            'alias': alias,
            'active_time_ranges': active_time_ranges,
        }
        if exceptions:
            params['exceptions'] = exceptions
        if exclude:
            params['exclude'] = exclude
        return self._request(
            self._post_url,
            "domain-types/time_period/collections/all",
            data=params,
        )

    def get_timeperiods(self):
        """Show all time periods

        Args:
            None

        Returns:
            list of timeperiods
            etag
        """
        return self._request(
            self._get_url,
            "domain-types/time_period/collections/all",
        )

    def delete_timeperiod(self, name, etag):
        """Delete a time period

        Args:
            name: name of the time period
            etag: The value of the, to be modified, object's ETag header.

        Returns:
            Nothing
        """
        return self._request(
            self._delete_url,
            f"objects/time_period/{name}",
            ok_code=204,
            etag=etag,
        )

    def get_timeperiod(self, name):
        """Show a time period

        Args:
            name: name of the time period

        Returns:
            timeperiod
            etag
        """
        return self._request(
            self._get_url,
            f"objects/time_period/{name}",
        )

    def edit_timeperiod(self, name, etag, alias=None, active_time_ranges=[], exceptions=[], exclude=[]):
        """Update a time period

        Args:
            name: name of the time period
            etag: The value of the, to be modified, object's ETag header.
            active_time_ranges: The list of active time ranges.
            exceptions: A list of additional time ranges to be added.
            exclude: A list of time period aliases whose periods are excluded.

        Returns:
            edited timeperiod
        """
        params={}
        if alias:
            params['alias'] = alias
        if active_time_ranges:
            params['active_time_ranges'] = active_time_ranges
        if exceptions:
            params['exceptions'] = exceptions
        if exclude:
            params['exclude'] = exclude
        if params:
            return self._request(
                self._put_url,
                f"objects/time_period/{name}",
                etag=etag,
                data=params,
            )
        return None, None

#   .--Ruleset-------------------------------------------------------------.
#   |                  ____        _                _                      |
#   |                 |  _ \ _   _| | ___  ___  ___| |_                    |
#   |                 | |_) | | | | |/ _ \/ __|/ _ \ __|                   |
#   |                 |  _ <| |_| | |  __/\__ \  __/ |_                    |
#   |                 |_| \_\\__,_|_|\___||___/\___|\__|                   |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def get_rulesets(self):
        """Show all rulesets

        Args:
            None

        Returns:
            list of rulesets
            etag
        """
        return self._request(
            self._get_url,
            "domain-types/ruleset/collections/all",
        )

#   .--Rule----------------------------------------------------------------.
#   |                         ____        _                                |
#   |                        |  _ \ _   _| | ___                           |
#   |                        | |_) | | | | |/ _ \                          |
#   |                        |  _ <| |_| | |  __/                          |
#   |                        |_| \_\\__,_|_|\___|                          |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def get_rules(self, ruleset_name):
        """Gets rules from ruleset by name

        Args:
            ruleset_name

        Returns:
            rules
            etag
        """
        return self._request(
            self._get_url,
            "domain-types/rule/collections/all",
            data={'ruleset_name': ruleset_name},
        )

#   .--Host Tag Groups-----------------------------------------------------.
#   |                _   _           _     _____                           |
#   |               | | | | ___  ___| |_  |_   _|_ _  __ _                 |
#   |               | |_| |/ _ \/ __| __|   | |/ _` |/ _` |                |
#   |               |  _  | (_) \__ \ |_    | | (_| | (_| |                |
#   |               |_| |_|\___/|___/\__|   |_|\__,_|\__, |                |
#   |                                                |___/                 |
#   |                    ____                                              |
#   |                   / ___|_ __ ___  _   _ _ __  ___                    |
#   |                  | |  _| '__/ _ \| | | | '_ \/ __|                   |
#   |                  | |_| | | | (_) | |_| | |_) \__ \                   |
#   |                   \____|_|  \___/ \__,_| .__/|___/                   |
#   |                                        |_|                           |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def create_host_tag_group(self, name, title, tags, topic = None, help = None):
        """Create a host tag group

        Args:
            name: A unique name for the host tag group.
            title: An alias for the host tag group.
            tags: A list of host tags belonging to the host tag group (list of dict)
            topic: Different tags can be grouped in a topic (string)
            help: A help description for the tag group (string)

        Returns:
            (taggroup, etag)
        """
        params={
            'ident': name,
            'title': title,
            'tags': tags,
        }
        if topic:
            params['topic'] = topic
        if help:
            params['help'] = help
        return self._request(
            self._post_url,
            "domain-types/host_tag_group/collections/all",
            data=params,
        )

    def get_host_tag_groups(self):
        """Show all host tag groups

        Args:
            None

        Returns:
            list of host tag groups
            etag
        """
        return self._request(
            self._get_url,
            "domain-types/host_tag_group/collections/all",
        )

    def get_host_tag_group(self, name):
        """Show a host tag group

        Args:
            name: name of the host tag group

        Returns:
            host tag group
            etag
        """
        return self._request(
            self._get_url,
            f"objects/host_tag_group/{name}",
        )

    def delete_host_tag_group(self, name):
        """Delete a host tag group

        Args:
            name: name of the host tag group

        Returns:
            Nothing
        """
        return self._request(
            self._delete_url,
            f"objects/host_tag_group/{name}",
            ok_code=204,
        )

    def edit_host_tag_group(self, name, etag, title = None, topic = None, help = None, tags = []):
        """Update a host tag group

        Args:
            name: name of the host tag group
            etag: The value of the, to be modified, object's ETag header.
            title: A title for the host tag
            topic: Different tags can be grouped in a topic
            help: A help description for the tag group
            tags: A list of host tags belonging to the host tag group

        Returns:
            host tag group
            etag
        """
        params = {}
        if title:
            params['title'] = title
        if topic:
            params['topic'] = topic
        if help:
            params['help'] = help
        if len(tags) > 0:
            params['tags'] = tags
        if params:
            return self._request(
                self._put_url,
                f"objects/host_tag_group/{name}",
                etag=etag,
                data=params,
            )
        return None, None

#   .--Auxiliary Tags------------------------------------------------------.
#   |      _              _ _ _                    _____                   |
#   |     / \  _   ___  _(_) (_) __ _ _ __ _   _  |_   _|_ _  __ _ ___     |
#   |    / _ \| | | \ \/ / | | |/ _` | '__| | | |   | |/ _` |/ _` / __|    |
#   |   / ___ \ |_| |>  <| | | | (_| | |  | |_| |   | | (_| | (_| \__ \    |
#   |  /_/   \_\__,_/_/\_\_|_|_|\__,_|_|   \__, |   |_|\__,_|\__, |___/    |
#   |                                      |___/             |___/         |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def create_aux_tag(self, name, title, topic, help = None):
        """Create an auxiliary tag

        Args:
            name: A unique name for the auxliary tag.
            title: An alias for the auxiliary tag.
            topic: Different tags can be grouped in a topic (string)
            help: A help description for the auxiliary tag (string)

        Returns:
            (auxtag, etag)
        """
        params={
            'aux_tag_id': name,
            'title': title,
            'topic': topic,
        }
        if help:
            params['help'] = help
        return self._request(
            self._post_url,
            "domain-types/aux_tag/collections/all",
            data=params,
        )

    def get_aux_tags(self):
        """Show all auxiliary tags

        Args:
            None

        Returns:
            list of auxiliary tags
            etag
        """
        return self._request(
            self._get_url,
            "domain-types/aux_tag/collections/all",
        )

    def get_aux_tag(self, name):
        """Show an auxiliary tag

        Args:
            name: name of the auxiliary tag

        Returns:
            auxiliary tag
            etag
        """
        return self._request(
            self._get_url,
            f"objects/aux_tag/{name}",
        )

    def delete_aux_tag(self, name):
        """Delete an auxiliary tag

        Args:
            name: name of the auxiliary tag

        Returns:
            Nothing
        """
        return self._request(
            self._post_url,
            f"objects/aux_tag/{name}/actions/delete/invoke",
            ok_code=204,
        )

    def edit_aux_tag(self, name, title = None, topic = None, help = None):
        """Update an auxiliary tag

        Args:
            name: name of the auxiliary tag
            title: A title for the host tag
            topic: Different tags can be grouped in a topic
            help: A help description for the tag group

        Returns:
            auxiliary tag
            etag
        """
        params = {}
        if title:
            params['title'] = title
        if topic:
            params['topic'] = topic
        if help:
            params['help'] = help
        if params:
            return self._request(
                self._put_url,
                f"objects/aux_tag/{name}",
                etag='*',
                data=params,
            )
        return None, None

#   .--Notifications-------------------------------------------------------.
#   |       _   _       _   _  __ _           _   _                        |
#   |      | \ | | ___ | |_(_)/ _(_) ___ __ _| |_(_) ___  _ __  ___        |
#   |      |  \| |/ _ \| __| | |_| |/ __/ _` | __| |/ _ \| '_ \/ __|       |
#   |      | |\  | (_) | |_| |  _| | (_| (_| | |_| | (_) | | | \__ \       |
#   |      |_| \_|\___/ \__|_|_| |_|\___\__,_|\__|_|\___/|_| |_|___/       |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def create_notification_rule(self, rule_config):
        """Create a notification rule

        Args:
            rule_config: the configuration of the rule as described in the API documentation

        Returns:
            (rule, etag)
        """
        return self._request(
            self._post_url,
            "domain-types/notification_rule/collections/all",
            data={
                "rule_config": rule_config,
            },
        )

    def get_all_notification_rules(self):
        """Show all notification rules

        Args:
            None

        Returns:
            list of notification rules
            etag
        """
        return self._request(
            self._get_url,
            "domain-types/notification_rule/collections/all",
        )

    def get_notification_rule(self, rule_id):
        """Show a notification rule

        Args:
            rule_id: UUID of the notification rule

        Returns:
            notification rule
            etag
        """
        return self._request(
            self._get_url,
            f"objects/notification_rule/{rule_id}",
        )

    def delete_notification_rule(self, rule_id):
        """Delete a notification rule

        Args:
            rule_id: UUID of the notification rule

        Returns:
            Nothing
        """
        return self._request(
            self._post_url,
            f"objects/notification_rule/{rule_id}/actions/delete/invoke",
            ok_code=204,
        )

    def edit_notification_rule(self, rule_id, rule_config):
        """Replace a notification rule

        Args:
            rule_id: UUID of the notification rule
            rule_config: the configuration of the rule as described in the API documentation

        Returns:
            notification rule
            etag
        """
        return self._request(
            self._put_url,
            f"objects/notification_rule/{rule_id}",
            data={
                "rule_config": rule_config,
            },
        )

#   .--Host Groups---------------------------------------------------------.
#   |        _   _           _      ____                                   |
#   |       | | | | ___  ___| |_   / ___|_ __ ___  _   _ _ __  ___         |
#   |       | |_| |/ _ \/ __| __| | |  _| '__/ _ \| | | | '_ \/ __|        |
#   |       |  _  | (_) \__ \ |_  | |_| | | | (_) | |_| | |_) \__ \        |
#   |       |_| |_|\___/|___/\__|  \____|_|  \___/ \__,_| .__/|___/        |
#   |                                                   |_|                |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

    def bulk_create_host_groups(self, entries = {}):
        """Bulk create host groups

        Args:
           entries: Mapping of host group name to alias (title)

        Returns:
          (list of host groups, etag)
        """
        list_of_host_groups = []
        for name, title in entries.items():
            list_of_host_groups.append({'name': name, 'alias': title})
        return self._request(
            self._post_url,
            "domain-types/host_group_config/actions/bulk-create/invoke",
            data={
                "entries": list_of_host_groups,
            })
        

    def bulk_delete_host_groups(self, entries = []):
        """Bulk delete host groups

        Args:
           entries: list of host group names

        Returns:
          None
        """
        return self._request(
            self._post_url,
            "domain-types/host_group_config/actions/bulk-delete/invoke",
            ok_code=204,
            data={
                "entries": entries,
            })

    def bulk_edit_host_groups(self, entries = {}):
        """Bulk update host groups (change alias)

        Args:
           entries: Mapping of host group name to alias (title)

        Returns:
          (list of host groups, etag)
        """
        list_of_host_groups = []
        for name, title in entries.items():
            list_of_host_groups.append({'name': name, 'attributes': {'alias': title}})
        return self._request(
            self._put_url,
            "domain-types/host_group_config/actions/bulk-update/invoke",
            etag='*',
            data={
                "entries": list_of_host_groups,
            })

    def create_host_group(self, name, title):
        """Create host group

        Args:
            name: internal name of host group
            title: human readable alias of host group

        Returns:
            (host group, etag)
        """
        return self._request(
            self._post_url,
            "domain-types/host_group_config/collections/all",
            data={
                "name": name,
                "alias": title,
            })

    def get_all_host_groups(self):
        """Show all host groups

        Args:
            None

        Returns:
            list of host groups
            etag
        """
        return self._request(
            self._get_url,
            "domain-types/host_group_config/collections/all",
        )

    def delete_host_group(self, name):
        """Delete a host group

        Args:
            name: internal name of host group

        Returns:
            None
        """
        return self._request(
            self._delete_url,
            f"objects/host_group_config/{name}",
            ok_code=204,
        )
        
    def get_host_group(self, name):
        """Show a host group

        Args:
            name: internal name of host group

        Returns:
            (host group, etag)
        """
        return self._request(
            self._get_url,
            f"objects/host_group_config/{name}"
        )

    def edit_host_group(self, name, title, etag="*"):
        """Update a host group

        Args:
            name: internal name of host group
            title: human readable alias of host group

        Returns:
            (host group, etag)
        """
        return self._request(
            self._put_url,
            f"objects/host_group_config/{name}",
            etag=etag,
            data={
                "alias": title,
            })
        

#
#   .--MULTISITE-----------------------------------------------------------.
#   |           __  __ _   _ _   _____ ___ ____ ___ _____ _____            |
#   |          |  \/  | | | | | |_   _|_ _/ ___|_ _|_   _| ____|           |
#   |          | |\/| | | | | |   | |  | |\___ \| |  | | |  _|             |
#   |          | |  | | |_| | |___| |  | | ___) | |  | | | |___            |
#   |          |_|  |_|\___/|_____|_| |___|____/___| |_| |_____|           |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.
    
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
                # sys.stderr.write("%s\n" % resp.text)
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

