#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

def parse_updater_hostname(info):
    parsed = {}

    for line in info:
        parsed[line[0]] = line[1]

    return parsed

def inventory_updater_hostname(parsed):
    if 'conf' in parsed:
        yield None, {}

def check_updater_hostname(item, params, parsed):
    import cmk.utils.debug
    if cmk.utils.debug.enabled():
        pprint.pprint(parsed)
        pprint.pprint(host_name())
    map = { 'fqdn': 'FQDN',
            'host': 'Hostname',
            'conf': 'Updater Configuration' }
    for key, value in parsed.items():
        state = 0
        if key == 'conf' and value != host_name():
            state = 1
        yield state, "%s: %s" % ( map[key], value )

check_info['updater_hostname'] = {
    'parse_function'            : parse_updater_hostname,
    'inventory_function'        : inventory_updater_hostname,
    'check_function'            : check_updater_hostname,
    'service_description'       : 'Check_MK Updater Hostname',
    'has_perfdata'              : False,
}
