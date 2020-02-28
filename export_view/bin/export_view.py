#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# This tool reads a multisite view as CSV and writes its contents
# to a file

# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

import os
import argparse
import requests

def check_mk_url(url):
    if url[-1] == '/':
        if not url.endswith('check_mk/'):
            url += 'check_mk/'
    else:
        if not url.endswith('check_mk'):
            url += '/check_mk/'
    return url

omdsite = os.environ.get('OMD_SITE')
parser = argparse.ArgumentParser()

user = None
url = None

if omdsite:
    omdroot = os.environ.get('OMD_ROOT')
    omdconfig = {}
    execfile(os.path.join(omdroot, 'etc', 'omd', 'site.conf'), omdconfig, omdconfig)
    user = 'automation'
    url = 'http://%s:%s/%s/check_mk/view.py' % (omdconfig['CONFIG_APACHE_TCP_ADDR'], omdconfig['CONFIG_APACHE_TCP_PORT'], omdsite)

parser.add_argument('-a', '--automation', help='name of the Check_MK automation user', default=user)
parser.add_argument('-s', '--secret', help='secret of the Check_MK automation user')
parser.add_argument('-u', '--url', help='URL of monitoring site', default=url)
parser.add_argument('-v', '--view', help='view name', required=True)
parser.add_argument('-o', '--output', help='output file name', required=True)
parser.add_argument('-d', '--debug', action='store_true', help='Enable debug output', default=False)
args = parser.parse_args()

if args.automation:
    if not args.secret:
        args.secret = open(os.path.join(omdroot, 'var', 'check_mk', 'web', args.automation, 'automation.secret')).read().strip()
else:
    raise RuntimeError('No automation credentials given.')

if not args.url:
    raise RuntimeError('No URL given.')

if not args.url.endswith('/check_mk/view.py'):
    args.url = check_mk_url(args.url) + 'view.py'

resp = requests.get(args.url, params={'_username': args.automation,
                                      '_secret': args.secret,
                                      'output_format': 'csv',
                                      '_transid': '-1',
                                      'view_name': args.view})
if resp.status_code == 200:
    if args.debug:
        print resp.text.encode('utf-8')
    else:
        with open(args.output, 'w') as output:
            output.write(resp.text.encode('utf-8'))
            output.write("\n")
else:
    raise resp.text
