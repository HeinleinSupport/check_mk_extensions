#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2025 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de
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

from cmk.agent_based.v2 import (
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_rate,
    get_value_store,
    Metric,
    render,
    Result,
    Service,
    SimpleSNMPSection,
    SNMPSection,
    SNMPTree,
    startswith,
    State,
    StringTable,
)

from cmk.plugins.lib import temperature

import time


#   .--State---------------------------------------------------------------.
#   |                       ____  _        _                               |
#   |                      / ___|| |_ __ _| |_ ___                         |
#   |                      \___ \| __/ _` | __/ _ \                        |
#   |                       ___) | || (_| | ||  __/                        |
#   |                      |____/ \__\__,_|\__\___|                        |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def parse_omnipcx_state(string_table: StringTable):
    map_state = {
        "0": ("indeterminate", State.UNKNOWN),
		"1": ("critical", State.CRIT),
		"2": ("major", State.CRIT),
		"3": ("minor", State.WARN),
		"4": ("warning", State.WARN),
		"5": ("normal", State.OK),
    }

    map_role = {
        "0": "INDETERMINATE",
		"1": "MAIN",
		"2": "STAND-BY",
		"3": "ACTIVE-PCS",
		"4": "INACTIVE-PCS",
    }
    
    section = {
        "mib_version": int(string_table[0][0]),
        "state": map_state.get(string_table[0][1], ("unknown (%s)" % string_table[0][1], State.UNKNOWN)),
        "role": map_role.get(string_table[0][2], "UNKNOWN (%s)" % string_table[0][2]),
        "reg_sets": int(string_table[0][3]),
        "unreg_sets": int(string_table[0][4]),
        "in_service": int(string_table[0][5]),
        "out_of_service": int(string_table[0][6]),
    }
    return section

snmp_section_omnipcx_state = SimpleSNMPSection(
    name="omnipcx_state",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.637.64.4400.1.1.10"), # A4400 pbcAgent on Linux
    parse_function=parse_omnipcx_state,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.637.64.4400.1",
        oids=[
            "0",    # A4400-CPU-MIB::pbxMibVersion
            "2",    # A4400-CPU-MIB::pbxState
            "4.0",  # A4400-RTM-MIB::pbxRole
            "5.0",  # A4400-RTM-MIB::sipRegSets
            "6.0",  # A4400-RTM-MIB::sipUnregSets
            "7.0",  # A4400-RTM-MIB::setsInService
            "8.0",  # A4400-RTM-MIB::setsOutOfService
        ],
    ),
)

def discover_omnipcx_state(section) -> DiscoveryResult:
    if 'state' in section:
        yield Service()

def check_omnipcx_state(section) -> CheckResult:
    if 'state' in section:
        yield Result(
            state=section['state'][1],
            summary="State is %s" % section["state"][0],
        )
    if "role" in section:
        yield Result(
            state=State.OK,
            summary="Role is %s" % section["role"],
        )
    map_metric = {
        "reg_sets": "sip_sets_registered",
        "unreg_sets": "sip_sets_unregistered",
        "in_service": "sip_sets_in_service",
        "out_of_service": "sip_sets_out_service",
    }
    for key, metric_name in map_metric.items():
        if key in section:
            yield Metric(
                name=metric_name,
                value=section[key],
            )

check_plugin_omnipcx_state = CheckPlugin(
    name="omnipcx_state",
    sections=['omnipcx_state'],
    service_name="OmniPCX state",
    discovery_function=discover_omnipcx_state,
    check_function=check_omnipcx_state,
)


#   .--IPDomain------------------------------------------------------------.
#   |            ___ ____  ____                        _                   |
#   |           |_ _|  _ \|  _ \  ___  _ __ ___   __ _(_)_ __              |
#   |            | || |_) | | | |/ _ \| '_ ` _ \ / _` | | '_ \             |
#   |            | ||  __/| |_| | (_) | | | | | | (_| | | | | |            |
#   |           |___|_|   |____/ \___/|_| |_| |_|\__,_|_|_| |_|            |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def parse_omnipcx_ipdomain(string_table: StringTable):
    section = {}
    for line in string_table:
        section[line[0]] = {
            "conf_avail": int(line[1]),
            "conf_busy": int(line[2]),
            "conf_ooo": int(line[3]),
            "dsp_avail": int(line[4]),
            "dsp_busy": int(line[5]),
            "dsp_ooo": int(line[6]),
            "dsp_overrun": int(line[7]),
            "cac_allowed": int(line[8]),
            "cac_used": int(line[9]),
            "cac_overrun": int(line[10]),
        }
    return section

snmp_section_omnipcx_ipdomain = SimpleSNMPSection(
    name="omnipcx_ipdomain",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.637.64.4400.1.1.10"), # A4400 pbcAgent on Linux
    parse_function=parse_omnipcx_ipdomain,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.637.64.4400.1.3.1",
        oids=[
            "1",   # A4400-RTM-MIB::ipDomain
            "2",   # A4400-RTM-MIB::confAvailable
            "3",   # A4400-RTM-MIB::confBusy
            "4",   # A4400-RTM-MIB::confOutOfOrder
            "5",   # A4400-RTM-MIB::dspRessAvailable
            "6",   # A4400-RTM-MIB::dspRessBusy
            "7",   # A4400-RTM-MIB::dspRessOutOfService
            "8",   # A4400-RTM-MIB::dspRessOverrun
            "9",   # A4400-RTM-MIB::cacAllowed
            "10",  # A4400-RTM-MIB::cacUsed
            "11",  # A4400-RTM-MIB::cacOverrun
        ],
    ),
)

def discover_omnipcx_ipdomain(section) -> DiscoveryResult:
    for ipdomain in section:
        yield Service(item=ipdomain)

def render_int(val):
    return "%d" % val

def render_freq(val):
    return "%.2f/s" % val

map_omnipcx_ipdomain_metrics = {
    "conf_avail": {
        "label": "Available conference circuits",
        "render": render_int,
        "name": "sip_conf_avail",
    },
    "conf_busy": {
        "label": "Busy conference circuits",
        "render": render_int,
        "name": "sip_conf_busy",
    },
    "conf_ooo": {
        "label": "Conference ciruits out of service",
        "render": render_int,
        "name": "sip_conf_ooo",
    },
    "dsp_avail": {
        "label": "Available DSP compressors",
        "render": render_int,
        "name": "sip_dsp_avail",
    },
    "dsp_busy": {
        "label": "Busy DSP compressors",
        "render": render_int,
        "name": "sip_dsp_busy",
    },
    "dsp_ooo": {
        "label": "DSP compressors out of service",
        "render": render_int,
        "name": "sip_dsp_ooo",
    },
    "dsp_overruns": {
        "label": "DSP compressors overruns",
        "render": render_freq,
        "name": "sip_dsp_overruns",
    },
    "cac_allowed": {
        "label": "Allowed external comms",
        "render": render_int,
        "name": "sip_cac_allowed",
    },
    "cac_used": {
        "label": "Used external comms",
        "render": render_int,
        "name": "sip_cac_used",
    },
    "cac_overruns": {
        "label": "CAC overruns",
        "render": render_freq,
        "name": "sip_cac_overruns",
    },
}

def check_omnipcx_ipdomain(item, params, section) -> CheckResult:
    if item in section:
        data = section[item]
        vs = get_value_store()
        now = time.time()
        data["dsp_overruns"] = get_rate(
            vs,
            f"dsp_overrun.%s" % item,
            now,
            data["dsp_overrun"],
        )
        data["cac_overruns"] = get_rate(
            vs,
            f"cac_overrun.%s" % item,
            now,
            data["cac_overrun"],
        )
        for key, info in map_omnipcx_ipdomain_metrics.items():
            if key in data:
                yield from check_levels(
                    value=data[key],
                    levels_lower=params.get(f"{key}_lower"),
                    levels_upper=params.get(f"{key}_upper"),
                    label=info["label"],
                    metric_name=info["name"],
                    render_func=info["render"],
                    notice_only=True,
                )

check_plugin_omnipcx_ipdomain = CheckPlugin(
    name="omnipcx_ipdomain",
    sections=['omnipcx_ipdomain'],
    service_name="OmniPCX IP domain %s",
    discovery_function=discover_omnipcx_ipdomain,
    check_function=check_omnipcx_ipdomain,
    check_default_parameters={},
)


#   .--Trunk---------------------------------------------------------------.
#   |                     _____                 _                          |
#   |                    |_   _| __ _   _ _ __ | | __                      |
#   |                      | || '__| | | | '_ \| |/ /                      |
#   |                      | || |  | |_| | | | |   <                       |
#   |                      |_||_|   \__,_|_| |_|_|\_\                      |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def parse_omnipcx_trunk(string_table: StringTable):
    map_type = {
        "0": "BCA",
        "1": "T2",
        "2": "T2COMP",
        "3": "T2IP",
        "4": "T2ATM",
        "5": "T2BBC2",
        "6": "T2SIP",
        "7": "T2IPPR",
        "8": "MIXTE",
        "9": "T0",
        "10": "DPNSS",
        "11": "DASS2",
        "12": "BCAADDON",
        "13": "T2HYBRID",
        "14": "LIALDE",
        "15": "T1",
    }

    map_status = {
        "0": "OOS",
        "1": "INS",
    }

    section = {}
    for line in string_table:
        section[line[0]] = {
            "name": line[1],
            "crystalno": int(line[2]),
            "couplerno": int(line[3]),
            "type": map_type.get(line[4]),
            "node": int(line[5]),
            "chan_free": int(line[6]),
            "chan_busy": int(line[7]),
            "chan_ooo": int(line[8]),
            "state": map_status.get(line[9]),
            "cumul_oos": int(line[10]),
            "cumul_overrun": int(line[11]),
        }

    return section

snmp_section_omnipcx_trunk = SimpleSNMPSection(
    name="omnipcx_trunk",
    detect=startswith(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.637.64.4400.1.1.10"), # A4400 pbcAgent on Linux
    parse_function=parse_omnipcx_trunk,
    fetch=SNMPTree(
        base=".1.3.6.1.4.1.637.64.4400.1.9.1",
        oids=[
            "1",   # A4400-RTM-MIB::trunkid
            "2",   # A4400-RTM-MIB::trunkname
            "3",   # A4400-RTM-MIB::crystalno
            "4",   # A4400-RTM-MIB::couplerno
            "5",   # A4400-RTM-MIB::trunktype
            "6",   # A4400-RTM-MIB::nodepbx
            "7",   # A4400-RTM-MIB::freechan
            "8",   # A4400-RTM-MIB::busychan
            "9",   # A4400-RTM-MIB::ooschan
            "10",  # A4400-RTM-MIB::trunkstatus
            "11",  # A4400-RTM-MIB::cumuloos
            "12",  # A4400-RTM-MIB::cumuloverrun
        ],
    ),
)

def discover_omnipcx_trunk(section) -> DiscoveryResult:
    for trunkid in section:
        yield Service(item=trunkid)

map_omnipcx_trunk_metrics = {
    "crystalno": {
        "label": "Crystal number",
        "render": render_int,
        "name": None,
    },
    "couplerno": {
        "label": "Coupler number",
        "render": render_int,
        "name": None,
    },
    "node": {
        "label": "PBX node number",
        "render": render_int,
        "name": None,
    },
    "chan_free": {
        "label": "Available channels",
        "render": render_int,
        "name": "sip_chan_free",
    },
    "chan_busy": {
        "label": "Busy channels",
        "render": render_int,
        "name": "sip_chan_busy",
    },
    "chan_oos": {
        "label": "Channels out of service",
        "render": render_int,
        "name": "sip_chan_oos",
    },
    "cumul_ooss": {
        "label": "OOS Channels",
        "render": render_freq,
        "name": "sip_cumul_ooss",
    },
    "cumul_overruns": {
        "label": "Failed outgoing calls",
        "render": render_freq,
        "name": "sip_cumul_overruns",
    },
}

map_omnipcx_trunk_strings = {
    "name": {
        "label": "Name",
    },
    "type": {
        "label": "Type",
    },
    "status": {
        "label": "State",
    }
}

def check_omnipcx_trunk(item, params, section) -> CheckResult:
    if item in section:
        data = section[item]
        vs = get_value_store()
        now = time.time()
        data["cumul_ooss"] = get_rate(
            vs,
            f"cumul_oos.%s" % item,
            now,
            data["cumul_oos"],
        )
        data["cumul_overruns"] = get_rate(
            vs,
            f"cumul_overrun.%s" % item,
            now,
            data["cumul_overrun"],
        )
        for key, info in map_omnipcx_trunk_strings.items():
            if key in data:
                yield Result(
                    state=State.OK,
                    summary="%s: %s" % (info["label"], data[key]),
                )
        for key, info in map_omnipcx_trunk_metrics.items():
            if key in data:
                yield from check_levels(
                    value=data[key],
                    levels_lower=params.get(f"{key}_lower"),
                    levels_upper=params.get(f"{key}_upper"),
                    label=info["label"],
                    metric_name=info["name"],
                    render_func=info["render"],
                    notice_only=True,
                )
        

check_plugin_omnipcx_trunk = CheckPlugin(
    name="omnipcx_trunk",
    sections=['omnipcx_trunk'],
    service_name="OmniPCX trunk %s",
    discovery_function=discover_omnipcx_trunk,
    check_function=check_omnipcx_trunk,
    check_default_parameters={},
)
