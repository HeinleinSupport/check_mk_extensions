#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.


from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    HostLabelGenerator,
)

from .agent_based_api.v1 import (
    check_levels,
    register,
    render,
    Result,
    State,
    HostLabel,
    Service,
    )

from .utils import temperature

def parse_apcaccess(string_table):
    parsed = {}
    instance = False
    for line in string_table:
        if line[0].startswith("[["):
            instance = line[0][2:-2]
            parsed[instance] = {}
        elif instance:
            parsed[instance][line[0].strip()] = ":".join(line[1:]).strip()
    return parsed

register.agent_section(
    name="apcaccess",
    parse_function=parse_apcaccess,
)

def discovery_apcaccess(section) -> DiscoveryResult:
    for instance in section:
        yield Service(item=instance)

def check_apcaccess(item, params, section) -> CheckResult:
    if item in section:
        data = section[item]
        if 'UPSNAME' in data and 'MODEL' in data and 'SERIALNO' in data and 'FIRMWARE' in data:
            yield Result(state=State.OK,
                         summary=", ".join([data['UPSNAME'],
                                            data.get('MODEL'),
                                            data.get('SERIALNO'),
                                            data.get('FIRMWARE')]))
        else:
            yield Result(state=State.UNKNOWN, summary='Unkown UPS / no data')
        metrics = { 'voltage': ('OUTPUTV', 'Output Voltage'),
                    'output_load': ('LOADPCT', 'Output Load'),
                    'battery_capacity': ('BCHARGE', 'Battery Capacity'),
                    'timeleft': ('TIMELEFT', 'Time Left') }
        human_readable = {'voltage': lambda x: "%0.0fV" % x,
                          'output_load': render.percent,
                          'battery_capacity': render.percent,
                          'timeleft': render.timespan }
        factors = { 'timeleft': 60.0 }
        for metric, (key, text) in metrics.items():
            if key in data:
                value = float(data.get(key).split(' ')[0]) * factors.get(metric, 1.0)
                if metric in params:
                    if len(params[metric]) == 2:
                        warn, crit = map(lambda x: x * factors.get(metric, 1.0), params[metric])
                        if warn < crit:
                            yield from check_levels(value,
                                                    levels_upper=(warn, crit),
                                                    metric_name=metric,
                                                    render_func=human_readable[metric],
                                                    label=text)
                        else:
                            yield from check_levels(value,
                                                    levels_lower=(warn, crit),
                                                    metric_name=metric,
                                                    render_func=human_readable[metric],
                                                    label=text)
                    elif len(params[metric]) == 4:
                        low_warn, low_crit, warn, crit = map(lambda x: x * factors.get(metric, 1.0), params[metric])
                        yield from check_levels(value,
                                                levels_upper=(warn, crit),
                                                levels_lower=(low_warn, low_crit),
                                                metric_name=metric,
                                                render_func=human_readable[metric],
                                                label=text)
                else:
                    yield Result(state=State.OK,
                                 summary="%s: %s" % (text, human_readable[metric](value)))
                    yield Metric(metric, value)
        if data.get('STATUS') != 'ONLINE' and data.get('SELFTEST') == 'NO':
            yield Result(state=State.CRIT,
                         summary='Status is ' + data.get('STATUS'))

register.check_plugin(
    name="apcaccess",
    service_name="APC %s Status",
    sections=["apcaccess"],
    discovery_function=discovery_apcaccess,
    check_function=check_apcaccess,
    check_default_parameters={
        "voltage"         : (210, 190, 240, 260),
        "output_load"     : (80, 90),
        "battery_capacity": (90, 80),
        "timeleft"        : (10, 5),
    },
    check_ruleset_name="apcaccess",
)

def discovery_apcaccess_temp(section):
    for instance in section:
        if 'ITEMP' in section[instance]:
            yield Service(item=instance)

def check_apcaccess_temp(item, params, section):
    if item in section and 'ITEMP' in section[item]:
        itemp = section[item]['ITEMP'].split(' ')
        yield from temperature.check_temperature(float(itemp[0]),
                                                 params,
                                                 unique_name='apcaccess_temp.%s' % item,
                                                 dev_unit=itemp[1].lower())

register.check_plugin(
    name="apcaccess_temperature",
    service_name="APC %s Temperature",
    sections=["apcaccess"],
    discovery_function=discovery_apcaccess_temp,
    check_function=check_apcaccess_temp,
    check_default_parameters={
        "levels"    : (40, 50),
    },
    check_ruleset_name="temperature",
)
