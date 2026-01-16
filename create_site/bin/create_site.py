#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (C) 2025 Heinlein Consulting GmbH
# Robert Sander <r.sander@heinlein-support.de>
#

import argparse # type: ignore
from pprint import pprint # type: ignore

import checkmkapi

import requests

import paramiko
import ipaddress # type: ignore
import json
import string
import secrets


def url_to_site(url):
    return url.split('/')[3]


def execute_ssh_command(sshclient, command):
    ssh_stdin, ssh_stdout, ssh_stderr = sshclient.exec_command(command)
    exit_code = ssh_stdout.channel.recv_exit_status()
    stdout = [line for line in ssh_stdout]
    error = [line for line in ssh_stderr]
    if exit_code > 0:
        raise RuntimeError("".join(error))
    if args.debug:
        pprint(exit_code)
        pprint(stdout)
        pprint(error)
    return stdout

def generate_password(length=32):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--url', help='URL to central Check_MK site')
parser.add_argument('-u', '--username', help='name of the automation user')
parser.add_argument('-p', '--password', help='secret of the automation user')
parser.add_argument('-v', '--verbose', action='store_true', required=False)
parser.add_argument('-D', '--debug', action='store_true', required=False)
parser.add_argument('-k', '--key', required=True)
parser.add_argument("MONSERVER")
parser.add_argument("MONIP")
parser.add_argument("SITENAME")
parser.add_argument("SITEALIAS")
parser.add_argument("CMKPASSWD")
parser.add_argument("FOLDER")     # "/monitoring_server"

args = parser.parse_args()

if args.debug:
    pprint(args)

monshort = args.MONSERVER.split(".")[0]

# Connection to local API
central_wato = checkmkapi.CMKRESTAPI(args.url, args.username, args.password)

# Connection to remote API
remote_url = f"https://{args.MONSERVER}/{args.SITENAME}/"
remote_wato = checkmkapi.CMKRESTAPI(remote_url, "cmkadmin", args.CMKPASSWD)

version_info, etag = central_wato.version()
this_site = version_info["site"]

# Create SSH connection
try:
    sshkey = paramiko.RSAKey.from_private_key_file(args.key)
except paramiko.ssh_exception.SSHException:
    sshkey = paramiko.Ed25519Key.from_private_key_file(args.key)

sshclient = paramiko.SSHClient()
sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sshclient.connect(hostname=args.MONIP, username="root", pkey=sshkey)

if args.verbose:
    print(f"Creating {args.SITENAME} on {args.MONSERVER}")
print("".join(execute_ssh_command(sshclient, f"omd create --admin-password {args.CMKPASSWD} {args.SITENAME}")))

if args.verbose:
    print(f"Enabling Livestatus via TCP on {args.SITENAME}")
print("".join(execute_ssh_command(sshclient, f"omd config {args.SITENAME} set LIVESTATUS_TCP on")))

if args.verbose:
    print(f"Getting Livestatus TCP-Port from {args.SITENAME}")
port = int(("".join(execute_ssh_command(sshclient, f"omd config {args.SITENAME} show LIVESTATUS_TCP_PORT"))).strip())
if args.debug:
    pprint(port)

automation_secret = generate_password()

config_files = {
    "LDAP connections": "etc/check_mk/multisite.d/wato/user_connections.mk",
    "Global multisite settings": "etc/check_mk/multisite.d/wato/global.mk",
}
for desc, filename in config_files.items():
    if args.verbose:
        print(f"Copying {desc} to {args.SITENAME}")
    sftp = sshclient.open_sftp()
    res = sftp.put(
        f"/omd/sites/{this_site}/{filename}",
        f"/omd/sites/{args.SITENAME}/{filename}",
    )
    if args.debug:
        pprint(res)
    res = execute_ssh_command(sshclient, f"chown {args.SITENAME}:{args.SITENAME} /omd/sites/{args.SITENAME}/{filename}")
    if args.debug:
        pprint(res)
    res = execute_ssh_command(sshclient, f"chmod 0660 /omd/sites/{args.SITENAME}/{filename}")
    if args.debug:
        pprint(res)

if args.verbose:
    print(f"Starting site {args.SITENAME} on {args.MONSERVER}")
print("".join(execute_ssh_command(sshclient, f"omd start {args.SITENAME}")))

monip = ipaddress.ip_address(args.MONIP)
socket_type = {4: "tcp", 6: "tcp6"}[monip.version]

if args.FOLDER[0] not in ["/", "~"]:
    args.FOLDER = "/" + args.FOLDER

try:
    central_wato.get_host(monshort)
    if args.debug:
        print(f"Host {monshort} already exists")
except requests.exceptions.HTTPError as er:
    if er.response.status_code == 404:
        if args.verbose:
            print(f"Creating host {args.MONSERVER} on {this_site}")
        central_wato.add_host(monshort, args.FOLDER, {"ipaddress": str(monip)})
        central_wato.activate()

if args.verbose:
    print(f"Creating config for distributed monitoring")
site_config = {
    "site_config": {
        "basic_settings": {
            "alias": args.SITEALIAS,
            "site_id": args.SITENAME,
        },
        "status_connection": {
            "connection": {
                "socket_type": socket_type,
                "port": port,
                "encrypted": True,
                "verify": True,
                "host": str(monip),
            },
            "proxy": {
                "use_livestatus_daemon": "direct",
            },
            "connect_timeout": 3,
            "persistent_connection": True,
            "url_prefix": remote_url,
            "status_host": {
                "status_host_set": "enabled",
                "site": this_site,
                "host": monshort,
            },
            "disable_in_status_gui": False,
        },
        "configuration_connection": {
            "enable_replication": False,
        },
    }
}
if args.debug:
    print(json.dumps(site_config))
central_wato.create_site_connection(site_config)

if args.verbose:
    print(f"Creating automation account on {args.SITENAME}")
remote_wato.create_user("automation", "Automation Account", {"auth_option": {"auth_type": "automation", "secret": automation_secret }, "roles": ["admin"],})
if args.debug:
    print("Activating changes on remote site")
remote_wato.activate()

if args.verbose:
    print(f"Creating password store entry for {args.SITENAME}")
central_wato.create_password(f"site_{args.SITENAME}", f"Site {args.SITEALIAS} API secret", automation_secret)
central_wato.activate()
