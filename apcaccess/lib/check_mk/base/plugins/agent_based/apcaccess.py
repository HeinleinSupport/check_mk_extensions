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
    Metric,
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
            key = line[0].strip()
            value = ":".join(line[1:]).strip()
            parsed[instance][key] = value
    return parsed

register.agent_section(
    name="apcaccess",
    parse_function=parse_apcaccess,
)

def discovery_apcaccess(params, section) -> DiscoveryResult:
    for instance in section:
        if params.get('servicedesc') == 'upsname':
            yield Service(item=section[instance]['UPSNAME'], parameters={'upsname': instance})
        elif params.get('servicedesc') == 'model' and 'MODEL' in section[instance]:
            yield Service(item=section[instance]['MODEL'], parameters={'model': instance})
        else:
            yield Service(item=instance)

def check_apcaccess(item, params, section) -> CheckResult:
    attrs = ['SERIALNO', 'FIRMWARE', 'UPSMODE']
    if 'upsname' in params:
        item = params['upsname']
        attrs.insert(0, 'MODEL')
    elif 'model' in params:
        item = params['model']
        attrs.insert(0, 'UPSNAME')
    else:
        attrs.insert(0, 'MODEL')
        attrs.insert(0, 'UPSNAME')
    if item in section:
        data = section[item]
        found = False
        for attr in attrs:
            if attr in data:
                found = True
                yield Result(state=State.OK,
                             summary="%s: %s" % (attr, data[attr]))
        if not found:
            yield Result(state=State.UNKNOWN, summary='Unkown UPS / no data')
        human_readable = {'voltage': lambda x: "%0.0fV" % x,
                          'output_load': render.percent,
                          'battery_capacity': render.percent,
                          'timeleft': render.timespan }
        metrics = { 'voltage': ('OUTPUTV', 'Output Voltage'),
                    'output_load': ('LOADPCT', 'Output Load'),
                    'battery_capacity': ('BCHARGE', 'Battery Capacity'),
                    'timeleft': ('TIMELEFT', 'Time Left') }
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
        if data.get('STATUS') != 'ONLINE' and data.get('STATUS') != 'ONLINE SLAVE':
            if 'SELFTEST' in data:
                if data['SELFTEST'] == 'NO':
                    yield Result(state=State.CRIT,
                                 summary='Status is ' + data.get('STATUS'))
            else:
                yield Result(state=State.CRIT,
                             summary='Status is ' + data.get('STATUS'))

register.check_plugin(
    name="apcaccess",
    service_name="APC %s Status",
    sections=["apcaccess"],
    discovery_ruleset_name="apcaccess_inventory",
    discovery_ruleset_type=register.RuleSetType.MERGED,
    discovery_default_parameters={'servicedesc': False},
    discovery_function=discovery_apcaccess,
    check_function=check_apcaccess,
    check_default_parameters={
        # "voltage"         : (210, 190, 240, 260), # there are other voltages
        "output_load"     : (80, 90),
        "battery_capacity": (90, 80),
        "timeleft"        : (10, 5),
    },
    check_ruleset_name="apcaccess",
)

def discovery_apcaccess_temp(params, section):
    for instance in section:
        if 'ITEMP' in section[instance]:
            if params.get('servicedesc') == 'upsname':
                yield Service(item=section[instance]['UPSNAME'], parameters={'upsname': instance})
            elif params.get('servicedesc') == 'model' and 'MODEL' in section[instance]:
                yield Service(item=section[instance]['MODEL'], parameters={'model': instance})
            else:
                yield Service(item=instance)

def check_apcaccess_temp(item, params, section):
    if 'upsname' in params:
        item = params['upsname']
    elif 'model' in params:
        item = params['model']
    if item in section and 'ITEMP' in section[item]:
        itemp = section[item]['ITEMP'].split(' ')
        yield from temperature.check_temperature(float(itemp[0]),
                                                 params,
                                                 dev_unit=itemp[1].lower())

register.check_plugin(
    name="apcaccess_temperature",
    service_name="APC %s Temperature",
    sections=["apcaccess"],
    discovery_ruleset_name="apcaccess_inventory",
    discovery_ruleset_type=register.RuleSetType.MERGED,
    discovery_default_parameters={'servicedesc': False},
    discovery_function=discovery_apcaccess_temp,
    check_function=check_apcaccess_temp,
    check_default_parameters={
        "levels"    : (40, 50),
    },
    check_ruleset_name="temperature",
)
