#!/usr/bin/env python3

import socket

print("<<<updater_hostname>>>")

print("fqdn %s" % socket.getfqdn())
print("host %s" % socket.gethostname())

config = eval(open('/etc/cmk-update-agent.state', 'r').read())

print("conf %s" % config['host_name'])
