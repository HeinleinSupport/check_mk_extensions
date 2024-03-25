#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2024 Heinlein Consulting GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

import argparse
import checkmkapi
import sys
import requests
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', help='URL to Check_MK site')
parser.add_argument('-u', '--username', help='name of the automation user')
parser.add_argument('-p', '--password', help='secret of the automation user')
parser.add_argument('-r', '--remove', action="store_true", help='remove hosts, otherwise just set them to "do not monitor"')
args = parser.parse_args()

cmk = checkmkapi.CMKRESTAPI(args.url, args.username, args.password)

changes = False

for hostname in sys.stdin.readlines():
    hostname = hostname.strip()
    if args.remove:
        print(f"removing {hostname}.")
        try:
            cmk.delete_host(hostname)
            changes = True
        except requests.exceptions.HTTPError as er:
            if er.response.status_code == 404:
                print(f"{hostname} not found.")
            else:
                raise(er)
    else:
        try:
            host, etag = cmk.get_host(hostname)
            extensions = host.get("extensions", {})
            attributes = extensions.get("attributes", {})
            tag_criticality = attributes.get("tag_criticality")
            if tag_criticality != "offline":
                print(f"setting {hostname} to offline.")
                cmk.edit_host(hostname, etag=etag, update_attr={"tag_criticality": "offline"})
                changes = True
        except requests.exceptions.HTTPError as er:
            if er.response.status_code == 404:
                print(f"{hostname} not found.")
            else:
                raise(er)

if changes:
    print("activating changes.")
    cmk.activate()
        
