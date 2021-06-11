#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2021 Heinlein Consulting GmbH
#          Robert Sander <r.sander@heinlein-support.de>

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

from typing import Optional

from .agent_based_api.v1 import (
    check_levels,
    register,
    render,
    startswith,
    Metric,
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

from .utils.interfaces import (
    get_traffic_levels,
    get_specific_traffic_levels,
)

def parse_lancom_xdsl(string_table):
    section = {}
    for id, interface in enumerate(string_table, start=1):
        if interface == []:
            continue
        interface = interface[0]
        section[str(id)] = {
            'state': int(interface[0]),
            'line': interface[1],
            'rate_up': int(interface[2]) * 125,
            'rate_down': int(interface[3]) * 125,
            'snr_down': float(interface[4]),
            'snr_up': float(interface[5]),
            'att_down': float(interface[6]),
            'att_up': float(interface[7]),
            'sync_uptime': int(interface[8]),
            'chipset': interface[9],
            'linetype': interface[10],
        }
    return section

def discover_lancom_xdsl(section) -> DiscoveryResult:
    for item, data in section.items():
        if data['state'] == 5:
            yield Service(item=item, parameters={'discovered': data})

def _check_lancom_xdsl_metric(value, discovered, metric_name, params, direction, label, render_func):
    p = { 'traffic': params }
    levels = get_traffic_levels(p)
    
    both = levels.get((direction, 'both'), (None, (None, None)))
    lower = levels.get((direction, 'lower'), (None, (None, None)))
    upper = levels.get((direction, 'upper'), (None, (None, None)))

    if upper[0] is None:
        upper = both
    if lower[0] is None:
        lower = both

    upper_levels = None
    if upper[0] == 'perc':
        upper_levels = ( discovered * (100 + upper[1][0]) / 100.0,
                         discovered * (100 + upper[1][1]) / 100.0 )
    elif upper[0] == 'abs':
        upper_levels = ( discovered + upper[1][0] / 8,
                         discovered + upper[1][1] / 8 )
    lower_levels = None
    if lower[0] == 'perc':
        lower_levels = ( discovered * (100 - lower[1][0]) / 100.0,
                         discovered * (100 - lower[1][1]) / 100.0 )
    elif lower[0] == 'abs':
        lower_levels = ( discovered - lower[1][0] / 8,
                         discovered - lower[1][1] / 8 )

    yield from check_levels(
        value,
        levels_upper=upper_levels,
        levels_lower=lower_levels,
        metric_name=metric_name,
        render_func=render_func,
        label=label,
        notice_only=True,
    )

def _render_db(value: Optional[float]) -> str:
    if value is None:
        return "No value"
    return "%0.2f dB" % value

def check_lancom_xdsl(item, params, section) -> CheckResult:
    if item in section:
        data = section[item]
        discovered = params.get('discovered', {})
        yield Result(state=State.OK,
                     summary=data['linetype'])
        yield Result(state=State.OK,
                     summary=data['chipset'])
        yield Result(state=State.OK,
                     summary=data['line'])
        yield from _check_lancom_xdsl_metric(
            data['rate_down'],
            discovered['rate_down'],
            'if_in_octets',
            params.get('data_rate', []),
            'in',
            'Data Rate IN',
            render.nicspeed,
        )
        yield from _check_lancom_xdsl_metric(
            data['rate_up'],
            discovered['rate_up'],
            'if_out_octets',
            params.get('data_rate', []),
            'out',
            'Data Rate OUT',
            render.nicspeed,
        )
        yield from _check_lancom_xdsl_metric(
            data['snr_down'],
            discovered['snr_down'],
            'signal_noise_down',
            params.get('signal_noise', []),
            'in',
            'Signal/Noise Ratio IN',
            _render_db,
        )
        yield from _check_lancom_xdsl_metric(
            data['snr_up'],
            discovered['snr_up'],
            'signal_noise_up',
            params.get('signal_noise', []),
            'out',
            'Signal/Noise Ratio OUT',
            _render_db,
        )
        yield from _check_lancom_xdsl_metric(
            data['att_down'],
            discovered['att_down'],
            'attenuation_down',
            params.get('attenuation', []),
            'in',
            'Attenuation IN',
            _render_db,
        )
        yield from _check_lancom_xdsl_metric(
            data['att_up'],
            discovered['att_up'],
            'attenuation_up',
            params.get('attenuation', []),
            'out',
            'Attenuation OUT',
            _render_db,
        )
        yield from check_levels(
            data['sync_uptime'],
            levels_upper=params.get('uptime_max'),
            levels_lower=params.get('uptime_min'),
            metric_name='uptime',
            render_func=render.timespan,
            label='Uptime',
        )

register.snmp_section(
    name="lancom_xdsl",
    parse_function=parse_lancom_xdsl,
    fetch=[
        SNMPTree(
            base=".1.3.6.1.4.1.2356.11.1.99.1",
            oids=[ "1", "2", "4", "5", "6", "7", "8", "9", "54", "14", "23" ],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.2356.11.1.99.2",
            oids=[ "1", "2", "4", "5", "6", "7", "8", "9", "54", "14", "23" ],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.2356.11.1.99.3",
            oids=[ "1", "2", "4", "5", "6", "7", "8", "9", "54", "14", "23" ],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.2356.11.1.99.4",
            oids=[ "1", "2", "4", "5", "6", "7", "8", "9", "54", "14", "23" ],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.2356.11.1.99.5",
            oids=[ "1", "2", "4", "5", "6", "7", "8", "9", "54", "14", "23" ],
        ),
    ],
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.2356.11.8"),
)

register.check_plugin(
    name="lancom_xdsl",
    sections=["lancom_xdsl"],
    service_name="LANCOM xDSL %s",
    discovery_function=discover_lancom_xdsl,
    check_function=check_lancom_xdsl,
    check_default_parameters={},
    check_ruleset_name="lancom_xdsl",
)
