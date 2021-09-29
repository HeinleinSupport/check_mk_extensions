#!/usr/bin/env python3

import distutils.spawn
import os.path
import subprocess
import socket
import sys

xeninventory='/etc/xensource-inventory'
xe=distutils.spawn.find_executable('xe')

def execute(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return p.stdout.readlines()

if xe:
    hostuuid = None
    if os.path.isfile(xeninventory):
        for line in open(xeninventory).readlines():
            name, key = line.split('=')
            if name == 'INSTALLATION_UUID':
                hostuuid = key.split("'")[1]
    if not hostuuid:
        for line in execute([xe, 'host-list', 'hostname=%s' % socket.gethostname() ]):
            if line.startswith('uuid'):
                hostuuid = line.split()[4]
    if not hostuuid:
        sys.exit(1)
    cpuuuid = None
    cpus = {}
    for line in execute([xe, 'host-cpu-list', 'host-uuid=%s' % hostuuid, 'params=uuid,number']):
        words = line.split()
        if words:
            if words[0] == 'uuid':
                cpuuuid=words[4]
            if words[0] == 'number' and cpuuuid:
                cpus[int(words[3])] = cpuuuid
    if cpus:
        print('<<<xe_cpu_util>>>')
        for cpuid in sorted(cpus.keys()):
            for line in execute([xe, 'host-cpu-param-get', 'uuid=%s' % cpus[cpuid], 'param-name=utilisation']):
                print("%d %s %s" % (cpuid, cpus[cpuid], line.strip()))
