#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from .agent_based_api.v1 import (
    all_of,
    contains,
    equals,
    get_rate,
    get_value_store,
    register,
    Metric,
    OIDEnd,
    Result,
    Service,
    SNMPTree,
    State,
)
from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    StringTable,
)
import time
import ipaddress
import struct

#   .--pathnum-------------------------------------------------------------.
#   |                         _   _                                        |
#   |             _ __   __ _| |_| |__  _ __  _   _ _ __ ___               |
#   |            | '_ \ / _` | __| '_ \| '_ \| | | | '_ ` _ \              |
#   |            | |_) | (_| | |_| | | | | | | |_| | | | | | |             |
#   |            | .__/ \__,_|\__|_| |_|_| |_|\__,_|_| |_| |_|             |
#   |            |_|                                                       |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def parse_velocloud_pathnum(string_table: StringTable) -> StringTable:
    if string_table:
        return { 'pathnum': int(string_table[0][0]) }
    return None

register.snmp_section(
    name="velocloud_pathnum",
    detect=all_of(
        contains(".1.3.6.1.2.1.1.1.0", "VeloCloud"),
        equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072.3.2.10"),
    ),
    parse_function=parse_velocloud_pathnum,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.45346.1.1.2.4.2",
        oids=["1.0"],
    ),
)

def discover_velocloud_pathnum(section) -> DiscoveryResult:
    yield Service()

def check_velocloud_pathnum(section) -> CheckResult:
    yield Result(state=State.OK,
                 summary="%d Paths active" % section['pathnum'])
    yield Metric('active_vpn_tunnels', section['pathnum'])

register.check_plugin(
    name='velocloud_pathnum',
    service_name="VeloCloud Paths",
    discovery_function=discover_velocloud_pathnum,
    check_function=check_velocloud_pathnum,
)

#   .--hastate-------------------------------------------------------------.
#   |                  _               _        _                          |
#   |                 | |__   __ _ ___| |_ __ _| |_ ___                    |
#   |                 | '_ \ / _` / __| __/ _` | __/ _ \                   |
#   |                 | | | | (_| \__ \ || (_| | ||  __/                   |
#   |                 |_| |_|\__,_|___/\__\__,_|\__\___|                   |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def parse_velocloud_hastate(string_table: StringTable) -> StringTable:
    map_admin_state = {
        '1': 'Single',
        '2': 'Active Standby Pair',
        '3': 'Cluster',
        '4': 'VRRP Pair',
    }
    map_peer_state = {
        '1': 'initializing',
        '2': 'active',
        '3': 'standby',
    }
    if string_table:
        section = {
            'admin': int(string_table[0][0]),
            'peer': int(string_table[0][1]),
            'admin_text': map_admin_state.get(string_table[0][0], 'Unkown'),
            'peer_text': map_peer_state.get(string_table[0][1], 'Unknown'),
        }
        return section
    return None

register.snmp_section(
    name="velocloud_hastate",
    detect=all_of(
        contains(".1.3.6.1.2.1.1.1.0", "VeloCloud"),
        equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072.3.2.10"),
    ),
    parse_function=parse_velocloud_hastate,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.45346.1.1.2.1.2",
        oids=[
            "1.0",
            "2.0",
        ],
    ),
)

def discover_velocloud_hastate(section) -> DiscoveryResult:
    yield Service()

def check_velocloud_hastate(section) -> CheckResult:
    if section['admin'] > 4:
        yield Result(state=State.CRIT,
                     summary=section['admin_text'])
    elif section['admin'] > 1:
        yield Result(state=State.OK,
                     summary=section['admin_text'])
        if section['peer'] > 3:
            yield Result(state=State.CRIT,
                         summary=section['peer_text'])
        elif section['peer'] == 1:
            yield Result(state=State.WARN,
                         summary=section['peer_text'])
        else:
            yield Result(state=State.OK,
                         summary=section['peer_text'])
    else:
        yield Result(state=State.OK,
                     summary=section['admin_text'])

register.check_plugin(
    name='velocloud_hastate',
    service_name="VeloCloud HA",
    discovery_function=discover_velocloud_hastate,
    check_function=check_velocloud_hastate,
)

#   .--link----------------------------------------------------------------.
#   |                           _ _       _                                |
#   |                          | (_)_ __ | | __                            |
#   |                          | | | '_ \| |/ /                            |
#   |                          | | | | | |   <                             |
#   |                          |_|_|_| |_|_|\_\                            |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def parse_velocloud_link(string_table: StringTable) -> StringTable:
    section = {}
    map_vpn_state = {
        '1': (State.WARN, 'Initial'),
        '2': (State.CRIT, 'Dead'),
        '3': (State.CRIT, 'Unusable'),
        '4': (State.WARN, 'Quiet'),
        '5': (State.OK, 'Standby'),
        '6': (State.WARN, 'Unstable'),
        '7': (State.OK, 'Stable'),
        '8': (State.CRIT, 'Unknown'),
    }
    for name, txjitter, rxjitter, txlatency, rxlatency, txlost, rxlost, vpnstate, txpackets, rxpackets, txbytes, rxbytes in string_table:
        if name in section:
            raise '%s is duplicate' % name
        section[name] = {
            'tx_jitter': float(txjitter) / 1000.0,
            'rx_jitter': float(rxjitter) / 1000.0,
            'tx_latency': float(txlatency) / 1000.0,
            'rx_latency': float(rxlatency) / 1000.0,
            'if_out_errors': int(txlost),
            'if_in_errors': int(rxlost),
            'state': map_vpn_state.get(vpnstate, (State.UNKNOWN, 'Unknown')),
            'if_out_unicast': int(txpackets),
            'if_in_unicast': int(rxpackets),
            'if_out_bps': int(txbytes),
            'if_in_bps': int(rxbytes),
        }
    return section

register.snmp_section(
    name="velocloud_link",
    detect=all_of(
        contains(".1.3.6.1.2.1.1.1.0", "VeloCloud"),
        equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072.3.2.10"),
    ),
    parse_function=parse_velocloud_link,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.45346.1.1.2.3.2.2.1",
        oids=[
            "3",  # vceLinkName
            "20", # vceLinkTxJitter
            "21", # vceLinkRxJitter
            "22", # vceLinkTxLatency
            "23", # vceLinkRxLatency
            "24", # vceLinkTxLostPkt
            "25", # vceLinkRxLostPkt
            "26", # vceLinkVpnState
            "36", # vceLinkTotTxPkts
            "37", # vceLinkTotRxPkts
            "38", # vceLinkTotTxbytes
            "39", # vceLinkTotRxBytes
        ],
    ),
)

def discover_velocloud_link(section) -> DiscoveryResult:
    for name in section:
        yield Service(item=name)

def check_velocloud_link(item, section) -> CheckResult:
    if item in section:
        data = section[item]
        vs = get_value_store()
        now = time.time()
        yield Result(state=data['state'][0],
                     summary=data['state'][1])
        for key, value in data.items():
            if key == 'state':
                continue
            if key.endswith('jitter') or key.endswith('latency'):
                yield Metric(key, value)
            else:
                rate = get_rate(vs, 'velocloud_link.%s.%s' % (item, key), now, value)
                yield Metric(key, rate)

register.check_plugin(
    name='velocloud_link',
    service_name="VeloCloud Link %s",
    discovery_function=discover_velocloud_link,
    check_function=check_velocloud_link,
)

#   .--path----------------------------------------------------------------.
#   |                                    _   _                             |
#   |                        _ __   __ _| |_| |__                          |
#   |                       | '_ \ / _` | __| '_ \                         |
#   |                       | |_) | (_| | |_| | | |                        |
#   |                       | .__/ \__,_|\__|_| |_|                        |
#   |                       |_|                                            |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def parse_velocloud_path(string_table: StringTable) -> StringTable:
    section = {}
    map_path_state = {
        '1': (State.WARN, 'Initial'),
        '2': (State.CRIT, 'Dead'),
        '3': (State.CRIT, 'Unusable'),
        '4': (State.WARN, 'Quiet'),
        '5': (State.WARN, 'Unstable'),
        '6': (State.WARN, 'Bandwidth unmeasurable'),
        '7': (State.OK, 'waiting for Link Bandwidth'),
        '8': (State.OK, 'measuring Tx Bandwidth'), 
        '9': (State.OK, 'measuring Rx Bandwwidth'),
        '10': (State.OK, 'Stable'), 
        '11': (State.OK, 'Active'),
        '12': (State.OK, 'upHsby'),
        '13': (State.OK, 'idleHsby'),
        '14': (State.OK, 'Backup'),
        '15': (State.CRIT, 'Unknown')
    }
    map_iptype = {
        '1': ('.', str),
        '2': (':', lambda x: format(x, 'x')),
    }
    for oidend, iptype, ip, name, pathstate, rxstate, txstate, txlatency, rxlatency, rxbytes, txbytes, rxlost, txlost, rxpackets, txpackets, rxjitter, txjitter in string_table:

        ipstring = map_iptype[iptype][0].join(map(map_iptype[iptype][1], map(ord, ip)))
        
        oidend_s = oidend.split('.')
        gwaddrtype = oidend_s[16]
        # gwaddrlen = oidend_s[17]
        gwaddr = map_iptype[gwaddrtype][0].join(map(map_iptype[gwaddrtype][1], oidend_s[18:]))

        item = "%s %s %s" % (name, ipstring, gwaddr)

        if item in section:
            raise '%s is duplicate' % item
        
        section[item] = {
            'state': map_path_state.get(pathstate, (State.UNKNOWN, 'Unknown')),
            'rxstate': map_path_state.get(rxstate, (State.UNKNOWN, 'Unknown')),
            'txstate': map_path_state.get(txstate, (State.UNKNOWN, 'Unknown')),
            'tx_jitter': float(txjitter) / 1000.0,
            'rx_jitter': float(rxjitter) / 1000.0,
            'tx_latency': float(txlatency) / 1000.0,
            'rx_latency': float(rxlatency) / 1000.0,
            'if_out_errors': int(txlost),
            'if_in_errors': int(rxlost),
            'if_out_unicast': int(txpackets),
            'if_in_unicast': int(rxpackets),
            'if_out_bps': int(txbytes),
            'if_in_bps': int(rxbytes),
        }
    return section

register.snmp_section(
    name="velocloud_path",
    detect=all_of(
        contains(".1.3.6.1.2.1.1.1.0", "VeloCloud"),
        equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072.3.2.10"),
    ),
    parse_function=parse_velocloud_path,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.45346.1.1.2.4.2.2.1",
        oids=[
            OIDEnd(),
            "2",  # vcePathIpType
            "3",  # vcePathIp
            "6",  # vcePathPeerName
            "7",  # vcePathState
            "10", # vcePathRxState
            "11", # vcePathTxState
            "13", # vcePathTxAveLatency
            "14", # vcePathRxAveLatency
            "15", # vcePathRxBytes
            "16", # vcePathTxBytes
            "17", # vcePathRxLostPkt
            "18", # vcePathTxLostPkt
            "19", # vcePathRxPkt
            "20", # vcePathTxPkt
            "21", # vcePathRxJitter
            "22", # vcePathTxJitter
        ],
    ),
)

def discover_velocloud_path(section) -> DiscoveryResult:
    for name in section:
        yield Service(item=name)

def check_velocloud_path(item, section) -> CheckResult:
    if item in section:
        data = section[item]
        vs = get_value_store()
        now = time.time()
        yield Result(state=data['state'][0],
                     summary='Path: %s' % data['state'][1])
        yield Result(state=data['rxstate'][0],
                     summary='RX: %s' % data['rxstate'][1])
        yield Result(state=data['txstate'][0],
                     summary='TX: %s' % data['txstate'][1])
        
        for key, value in data.items():
            if key.endswith('state'):
                continue
            if key.endswith('jitter') or key.endswith('latency'):
                yield Metric(key, value)
            else:
                rate = get_rate(vs, 'velocloud_path.%s.%s' % (item, key), now, value)
                yield Metric(key, rate)

register.check_plugin(
    name='velocloud_path',
    service_name="VeloCloud Path %s",
    discovery_function=discover_velocloud_path,
    check_function=check_velocloud_path,
)
