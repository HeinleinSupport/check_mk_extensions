#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2017 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2. This file is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.


from cmk.plugins.lib import (
    elphase,
    temperature,
)

from collections.abc import Mapping # type: ignore
from typing import Any # type: ignore

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    RuleSetType,
    Service,
    State,
    StringTable,
)

from cmk.plugins.lib.ups import (
    Battery,
    check_ups_capacity,
)

Section = Mapping[str, Any]

def convert_value(time: str) -> int:
    factor = {
        "Minutes": 60.0,
        "Hours": 3600.0,
    }
    if time:
        value, unit = time.split(" ")
        return round(float(value) * factor.get(unit, 1.0))
    return None

def parse_apcaccess(string_table: StringTable) -> Section:
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
    for instance, data in parsed.items():
        tonbat = convert_value(data.get("TONBATT"))
        data["Battery"] = Battery(
            seconds_on_bat=tonbat,
            seconds_left=convert_value(data.get("TIMELEFT")),
            percent_charged=convert_value(data.get("BCHARGE")),
            on_battery=(tonbat > 0),
        )
        elphase = {}
        for key, metric in {"OUTPUTV": "voltage", "LOADPCT": "output_load"}.items():
            value = data.get(key, "").split(" ")[0]
            if value:
                elphase[metric] = float(value)
        if elphase:
            data["elphase"] = elphase
    return parsed

agent_section_apcaccess = AgentSection(
    name="apcaccess",
    parse_function=parse_apcaccess,
)

def discovery_apcaccess(params, section: Section) -> DiscoveryResult:
    for instance in section:
        if params.get('servicedesc') == 'upsname':
            yield Service(item=section[instance]['UPSNAME'], parameters={'upsname': instance})
        elif params.get('servicedesc') == 'model' and 'MODEL' in section[instance]:
            yield Service(item=section[instance]['MODEL'], parameters={'model': instance})
        else:
            yield Service(item=instance)

def check_apcaccess(item: str, params, section: Section) -> CheckResult:
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
        params_capacity = {
            "capacity": (0, 0),
            "battime": (0, 0),
        }
        for key in params_capacity.keys():
            if key in params:
                if params[key][0] == "fixed_levels":
                    params_capacity[key] = params[key]
        yield from check_ups_capacity(params_capacity, data["Battery"], None, None)
        if data.get('STATUS') != 'ONLINE' and data.get('STATUS') != 'ONLINE SLAVE':
            if 'SELFTEST' in data:
                if data['SELFTEST'] == 'NO':
                    yield Result(state=State.CRIT,
                                 summary='Status is ' + data.get('STATUS'))
            else:
                yield Result(state=State.CRIT,
                             summary='Status is ' + data.get('STATUS'))
        if 'SELFTEST' in data and data['SELFTEST'] not in ['OK', 'NO']:
            yield Result(state=State.WARN,
                         summary='Self-Test is ' + data['SELFTEST'])

check_plugin_apcaccess = CheckPlugin(
    name="apcaccess",
    service_name="APC %s Status",
    sections=["apcaccess"],
    discovery_ruleset_name="apcaccess_inventory",
    discovery_ruleset_type=RuleSetType.MERGED,
    discovery_default_parameters={'servicedesc': False},
    discovery_function=discovery_apcaccess,
    check_function=check_apcaccess,
    check_default_parameters={
        # "battery_capacity": (90, 80),
        # "timeleft"        : (10, 5),
    },
    check_ruleset_name="apcaccess",
)

def discovery_apcaccess_elphase(params, section: Section) -> DiscoveryResult:
    for instance in section:
        if "elphase" in section[instance]:
            if params.get('servicedesc') == 'upsname':
                yield Service(item=section[instance]['UPSNAME'], parameters={'upsname': instance})
            elif params.get('servicedesc') == 'model' and 'MODEL' in section[instance]:
                yield Service(item=section[instance]['MODEL'], parameters={'model': instance})
            else:
                yield Service(item=instance)

def check_apcaccess_elphase(item, params, section) -> CheckResult:
    if 'upsname' in params:
        item = params['upsname']
    elif 'model' in params:
        item = params['model']
    if item in section and "elphase" in section[item]:
        yield from elphase.check_elphase(item, params, {item: section[item]["elphase"]})

check_plugin_apcaccess_elphase = CheckPlugin(
    name="apcaccess_elphase",
    service_name="APC %s Output",
    sections=["apcaccess"],
    discovery_ruleset_name="apcaccess_inventory",
    discovery_ruleset_type=RuleSetType.MERGED,
    discovery_default_parameters={'servicedesc': False},
    discovery_function=discovery_apcaccess_elphase,
    check_function=check_apcaccess_elphase,
    check_default_parameters={},
    check_ruleset_name="ups_outphase",
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

check_plugin_apcaccess_temperature = CheckPlugin(
    name="apcaccess_temperature",
    service_name="APC %s Temperature",
    sections=["apcaccess"],
    discovery_ruleset_name="apcaccess_inventory",
    discovery_ruleset_type=RuleSetType.MERGED,
    discovery_default_parameters={'servicedesc': False},
    discovery_function=discovery_apcaccess_temp,
    check_function=check_apcaccess_temp,
    check_default_parameters={
        "levels"    : (40, 50),
    },
    check_ruleset_name="temperature",
)
