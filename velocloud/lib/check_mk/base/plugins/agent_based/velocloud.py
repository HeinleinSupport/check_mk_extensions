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
    any_of,
    check_levels,
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

def _render_integer(value):
    return "%d" % value

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

def parse_velocloud_pathnum(string_table: StringTable):
    if string_table:
        return { 'pathnum': int(string_table[0][0]) }
    return None

register.snmp_section(
    name="velocloud_pathnum",
    detect=any_of(
        equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.45346.1.1"),
        all_of(
          contains(".1.3.6.1.2.1.1.1.0", "VeloCloud"),
          equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072.3.2.10"),
        ),
    ),
    parse_function=parse_velocloud_pathnum,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.45346.1.1.2.4.2",
        oids=["1.0"],
    ),
)

def discover_velocloud_pathnum(section) -> DiscoveryResult:
    yield Service()

def check_velocloud_pathnum(params, section) -> CheckResult:
    yield from check_levels(
        section.get('pathnum'),
        metric_name='active_vpn_tunnels',
        levels_upper=params.get('levels_upper'),
        render_func=_render_integer,
        label='Active Paths',
    )

register.check_plugin(
    name='velocloud_pathnum',
    service_name="VeloCloud Paths",
    discovery_function=discover_velocloud_pathnum,
    check_function=check_velocloud_pathnum,
    check_ruleset_name="velocloud_pathnum",
    check_default_parameters={
        'levels_upper': (23, 25),
    },
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

def parse_velocloud_hastate(string_table: StringTable):
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
            'wan_active': int(string_table[0][2]),
            'lan_active': int(string_table[0][3]),
            'wan_standby': int(string_table[0][4]),
            'lan_standby': int(string_table[0][5]),
        }
        return section
    return None

register.snmp_section(
    name="velocloud_hastate",
    detect=any_of(
        equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.45346.1.1"),
        all_of(
          contains(".1.3.6.1.2.1.1.1.0", "VeloCloud"),
          equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072.3.2.10"),
        ),
    ),
    parse_function=parse_velocloud_hastate,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.45346.1.1.2.1.2",
        oids=[
            "1.0", # vceHaAdminState
            "2.0", # vceHaPeerState
            "3.0", # vceHaActiveWanItfNum
            "4.0", # vceHaActiveLanItfNum
            "5.0", # vceHaStanbyWanItfNum
            "6.0", # vceHaStanbyLanItfNum
        ],
    ),
)

def discover_velocloud_hastate(section) -> DiscoveryResult:
    yield Service(parameters={
        'admin_text': section['admin_text'],
    })

def check_velocloud_hastate(params, section) -> CheckResult:
    if section['admin'] in [1, 2, 3, 4]:
        if section['admin_text'] != params.get('admin_text'):
            yield Result(state=State.WARN,
                         summary='Admin State changed from %s to %s' % (params.get('admin_text'), section['admin_text']))
        else:
            yield Result(state=State.OK,
                         summary='Admin State: %s' % section['admin_text'])
        if section['admin'] > 1:
            if section['peer'] != 3:
                yield Result(state=State.CRIT,
                             summary='Peer State: %s' % section['peer_text'])
            else:
                yield Result(state=State.OK,
                             summary='Peer State: %s' % section['peer_text'])
            if section['wan_active'] == section['wan_standby']:
                yield Result(state=State.OK,
                             summary='%d WAN links' % section['wan_active'])
            else:
                yield Result(state=State.CRIT,
                             summary='WAN: active node has %d links but standby node has %d links' % (section['wan_active'], section['wan_standby']))
            if section['lan_active'] == section['lan_standby']:
                yield Result(state=State.OK,
                             summary='%d LAN links' % section['lan_active'])
            else:
                yield Result(state=State.CRIT,
                             summary='LAN: active node has %d links but standby node has %d links' % (section['lan_active'], section['lan_standby']))


register.check_plugin(
    name='velocloud_hastate',
    service_name="VeloCloud HA",
    discovery_function=discover_velocloud_hastate,
    check_function=check_velocloud_hastate,
    check_default_parameters={
        'admin_text': 'None',
    },
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

_velocloud_map_vpn_state = {
    '1': (State.WARN, 'Initial'),
    '2': (State.CRIT, 'Dead'),
    '3': (State.CRIT, 'Unusable'),
    '4': (State.WARN, 'Quiet'),
    '5': (State.OK, 'Standby'),
    '6': (State.WARN, 'Unstable'),
    '7': (State.OK, 'Stable'),
    '8': (State.CRIT, 'Unknown'),
}

def parse_velocloud_link(string_table: StringTable):
    section = {}
    for name, intf, txjitter, rxjitter, txlatency, rxlatency, txlost, rxlost, vpnstate, txpackets, rxpackets, txbytes, rxbytes in string_table:
        if intf in section:
            raise '%s is duplicate' % intf
        section[intf] = {
            'name': name,
            'tx_jitter': float(txjitter) / 1000.0,
            'rx_jitter': float(rxjitter) / 1000.0,
            'tx_latency': float(txlatency) / 1000.0,
            'rx_latency': float(rxlatency) / 1000.0,
            'if_out_errors': int(txlost),
            'if_in_errors': int(rxlost),
            'raw_state': int(vpnstate),
            'state': _velocloud_map_vpn_state.get(vpnstate, (State.UNKNOWN, 'Unknown')),
            'if_out_unicast': int(txpackets),
            'if_in_unicast': int(rxpackets),
            'if_out_bps': int(txbytes),
            'if_in_bps': int(rxbytes),
        }
    return section

register.snmp_section(
    name="velocloud_link",
    detect=any_of(
        equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.45346.1.1"),
        all_of(
          contains(".1.3.6.1.2.1.1.1.0", "VeloCloud"),
          equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072.3.2.10"),
        ),
    ),
    parse_function=parse_velocloud_link,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.45346.1.1.2.3.2.2.1",
        oids=[
            "3",  # vceLinkName
            "33", # vceLinkItf
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
    for intf, data in section.items():
        yield Service(
            item=intf,
            parameters={'raw_state': data['raw_state']}
        )

def check_velocloud_link(item, params, section) -> CheckResult:
    if item in section:
        data = section[item]
        vs = get_value_store()
        now = time.time()
        yield Result(state=State.OK,
                     summary=data['name'])
        if data['raw_state'] != params.get('raw_state'):
            yield Result(state=State.WARN,
                         summary='State has changed from %s to %s' % (_velocloud_map_vpn_state.get(params.get('state'), (3, 'Unknown'))[1], data['state'][1]))
        else:
            yield Result(state=State.OK,
                         summary='State is %s' % data['state'][1])
        for key, value in data.items():
            if key in [ 'name', 'raw_state', 'state' ]:
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
    check_default_parameters={
        'raw_state': 0,
    },
)

#   .--arp-----------------------------------------------------------------.
#   |                                                                      |
#   |                           __ _ _ __ _ __                             |
#   |                          / _` | '__| '_ \                            |
#   |                         | (_| | |  | |_) |                           |
#   |                          \__,_|_|  | .__/                            |
#   |                                    |_|                               |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'

def parse_velocloud_arp(string_table: StringTable):
    if string_table:
        return { 'arp': int(string_table[0][0]) }
    return None

register.snmp_section(
    name="velocloud_arp",
    detect=any_of(
        equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.45346.1.1"),
        all_of(
          contains(".1.3.6.1.2.1.1.1.0", "VeloCloud"),
          equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072.3.2.10"),
        ),
    ),
    parse_function=parse_velocloud_arp,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.45346.1.1.2.5.2",
        oids=[
            "1.0",
        ],
    ),
)

def discover_velocloud_arp(section) -> DiscoveryResult:
    yield Service()

def check_velocloud_arp(section) -> CheckResult:
    yield Result(state=State.OK,
                 summary="%d ARP entries" % section['arp'])
    yield Metric( 'arp_entries', section['arp'] )

register.check_plugin(
    name='velocloud_arp',
    service_name="VeloCloud ARP",
    discovery_function=discover_velocloud_arp,
    check_function=check_velocloud_arp,
)

# #   .--path----------------------------------------------------------------.
# #   |                                    _   _                             |
# #   |                        _ __   __ _| |_| |__                          |
# #   |                       | '_ \ / _` | __| '_ \                         |
# #   |                       | |_) | (_| | |_| | | |                        |
# #   |                       | .__/ \__,_|\__|_| |_|                        |
# #   |                       |_|                                            |
# #   +----------------------------------------------------------------------+
# #   |                                                                      |
# #   '----------------------------------------------------------------------'

# def parse_velocloud_path(string_table: StringTable):
#     section = {}
#     map_path_state = {
#         '1': (State.WARN, 'Initial'),
#         '2': (State.CRIT, 'Dead'),
#         '3': (State.CRIT, 'Unusable'),
#         '4': (State.WARN, 'Quiet'),
#         '5': (State.WARN, 'Unstable'),
#         '6': (State.WARN, 'Bandwidth unmeasurable'),
#         '7': (State.OK, 'waiting for Link Bandwidth'),
#         '8': (State.OK, 'measuring Tx Bandwidth'), 
#         '9': (State.OK, 'measuring Rx Bandwwidth'),
#         '10': (State.OK, 'Stable'), 
#         '11': (State.OK, 'Active'),
#         '12': (State.OK, 'upHsby'),
#         '13': (State.OK, 'idleHsby'),
#         '14': (State.OK, 'Backup'),
#         '15': (State.CRIT, 'Unknown')
#     }
#     map_iptype = {
#         '1': ('.', str),
#         '2': (':', lambda x: format(x, 'x')),
#     }
#     for oidend, iptype, ip, name, pathstate, rxstate, txstate, txlatency, rxlatency, rxbytes, txbytes, rxlost, txlost, rxpackets, txpackets, rxjitter, txjitter in string_table:

#         ipstring = map_iptype[iptype][0].join(map(map_iptype[iptype][1], map(ord, ip)))
        
#         oidend_s = oidend.split('.')
#         gwaddrtype = oidend_s[16]
#         # gwaddrlen = oidend_s[17]
#         gwaddr = map_iptype[gwaddrtype][0].join(map(map_iptype[gwaddrtype][1], oidend_s[18:]))

#         item = "%s %s %s" % (name, ipstring, gwaddr)

#         if item in section:
#             raise '%s is duplicate' % item
        
#         section[item] = {
#             'state': map_path_state.get(pathstate, (State.UNKNOWN, 'Unknown')),
#             'rxstate': map_path_state.get(rxstate, (State.UNKNOWN, 'Unknown')),
#             'txstate': map_path_state.get(txstate, (State.UNKNOWN, 'Unknown')),
#             'tx_jitter': float(txjitter) / 1000.0,
#             'rx_jitter': float(rxjitter) / 1000.0,
#             'tx_latency': float(txlatency) / 1000.0,
#             'rx_latency': float(rxlatency) / 1000.0,
#             'if_out_errors': int(txlost),
#             'if_in_errors': int(rxlost),
#             'if_out_unicast': int(txpackets),
#             'if_in_unicast': int(rxpackets),
#             'if_out_bps': int(txbytes),
#             'if_in_bps': int(rxbytes),
#         }
#     return section

# register.snmp_section(
#     name="velocloud_path",
#     detect=any_of(
#         equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.45346.1.1"),
#         all_of(
#           contains(".1.3.6.1.2.1.1.1.0", "VeloCloud"),
#           equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.8072.3.2.10"),
#         ),
#     ),
#     parse_function=parse_velocloud_path,
#     fetch=SNMPTree(
#         base=".1.3.6.1.4.1.45346.1.1.2.4.2.2.1",
#         oids=[
#             OIDEnd(),
#             "2",  # vcePathIpType
#             "3",  # vcePathIp
#             "6",  # vcePathPeerName
#             "7",  # vcePathState
#             "10", # vcePathRxState
#             "11", # vcePathTxState
#             "13", # vcePathTxAveLatency
#             "14", # vcePathRxAveLatency
#             "15", # vcePathRxBytes
#             "16", # vcePathTxBytes
#             "17", # vcePathRxLostPkt
#             "18", # vcePathTxLostPkt
#             "19", # vcePathRxPkt
#             "20", # vcePathTxPkt
#             "21", # vcePathRxJitter
#             "22", # vcePathTxJitter
#         ],
#     ),
# )

# def discover_velocloud_path(section) -> DiscoveryResult:
#     for name in section:
#         yield Service(item=name)

# def check_velocloud_path(item, section) -> CheckResult:
#     if item in section:
#         data = section[item]
#         vs = get_value_store()
#         now = time.time()
#         yield Result(state=data['state'][0],
#                      summary='Path: %s' % data['state'][1])
#         yield Result(state=data['rxstate'][0],
#                      summary='RX: %s' % data['rxstate'][1])
#         yield Result(state=data['txstate'][0],
#                      summary='TX: %s' % data['txstate'][1])
        
#         for key, value in data.items():
#             if key.endswith('state'):
#                 continue
#             if key.endswith('jitter') or key.endswith('latency'):
#                 yield Metric(key, value)
#             else:
#                 rate = get_rate(vs, 'velocloud_path.%s.%s' % (item, key), now, value)
#                 yield Metric(key, rate)

# register.check_plugin(
#     name='velocloud_path',
#     service_name="VeloCloud Path %s",
#     discovery_function=discover_velocloud_path,
#     check_function=check_velocloud_path,
# )
