#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from cmk.agent_based.v2 import (
    any_of,
    check_levels,
    CheckPlugin,
    CheckResult,
    equals,
    DiscoveryResult,
    render,
    Service,
    SNMPSection,
    SNMPTree,
    StringTable,
)

from cmk.plugins.lib.elphase import check_elphase
from cmk.plugins.lib.temperature import check_temperature

# 508, 512 and 604 have the same mib
janitza_umg_device_map = {
    ".1.3.6.1.4.1.34278.8.6": "96",
    ".1.3.6.1.4.1.34278.10.1": "604",
    ".1.3.6.1.4.1.34278.10.4": "508",
    ".1.3.6.1.4.1.34278.10.5": "512",
}


def parse_janitza_umg(string_table: StringTable):
    if not string_table[0] or not string_table[0][0]:
        return None

    def flatten(line):
        return [x[0] for x in line]

    dev_type = janitza_umg_device_map[string_table[0][0][0]]

    info_offsets = {
        "508": {
            "energy": 4,
            "sumenergy": 5,
            "misc": 8,
        },
        "512": {
            "energy": 4,
            "sumenergy": 5,
            "misc": 8,
        },
        "604": {
            "energy": 4,
            "sumenergy": 5,
            "misc": 8,
        },
        "96": {
            "energy": 3,
            "sumenergy": 4,
            "misc": 6,
        },
    }[dev_type]

    rmsphase = flatten(string_table[1])
    sumphase = flatten(string_table[2])
    energy = flatten(string_table[info_offsets["energy"]])
    sumenergy = flatten(string_table[info_offsets["sumenergy"]])

    if dev_type in ["508", "512", "604"]:
        num_phases = 4
        num_currents = 4
    elif dev_type == "96":
        num_phases = 3
        num_currents = 6

    # the number of elements in each "block" within the snmp. This differs between
    # devices
    counts = [
        num_phases,  # voltages
        3,  # L1-L2, L2-L3, L3-L1
        num_currents,  # umg96 reports voltage for 3 phases and current for 6
        num_phases,  # real power
        num_phases,  # reactive power
        num_phases,  # Power in VA
        num_phases,  # Cos(Phi)
    ]

    def offset(block_id, phase):
        return sum(counts[:block_id], phase)

    # voltages are in 100mv, currents in 1mA, power in Watts / VA
    result: dict[str, float | list | int | dict] = {}

    for phase in range(num_phases):
        result["Phase %d" % (phase + 1)] = {
            "voltage": int(rmsphase[offset(0, phase)]) / 10.0,
            "current": int(rmsphase[offset(2, phase)]) / 1000.0,
            "power": int(rmsphase[offset(3, phase)]),
            "appower": int(rmsphase[offset(5, phase)]),
            "energy": int(energy[phase]) / 10,
        }

    result["Total"] = {"power": int(sumphase[0]), "energy": int(sumenergy[0])}

    misc = flatten(string_table[info_offsets["misc"]])
    result["Frequency"] = int(misc[0])
    # temperature not present in UMG508, UMG512 and UMG604
    if len(misc) > 1:
        result["Temperature"] = list(map(int, misc[1:]))
    else:
        result["Temperature"] = []
    return result

snmp_section_janitza_umg = SNMPSection(
    name = "janitza_umg",
    parse_function = parse_janitza_umg,
    detect = any_of(
        equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.34278.8.6"),
        equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.34278.10.1"),
        equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.34278.10.4"),
        equals(".1.3.6.1.2.1.1.2.0", ".1.3.6.1.4.1.34278.10.5"),
    ),
    fetch = [
        SNMPTree(
            base=".1.3.6.1.2.1.1.2",
            oids=["0"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.34278",
            oids=["1"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.34278",
            oids=["2"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.34278",
            oids=["3"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.34278",
            oids=["4"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.34278",
            oids=["5"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.34278",
            oids=["6"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.34278",
            oids=["7"],
        ),
        SNMPTree(
            base=".1.3.6.1.4.1.34278",
            oids=["8"],
        ),
    ],
)


def inventory_janitza_umg_inphase(section) -> DiscoveryResult:
    for item in section:
        if item.startswith("Phase"):
            yield Service(item=item)
        if item == "Total":
            yield Service(item=item)

check_plugin_janitza_umg = CheckPlugin(
    name = "janitza_umg",
    sections = ["janitza_umg"],
    service_name = "Input %s",
    discovery_function = inventory_janitza_umg_inphase,
    check_function = check_elphase,
    check_default_parameters = {
    },
    check_ruleset_name = "el_inphase",
)


def inventory_janitza_umg_freq(section) -> DiscoveryResult:
    # info[0] is frequency, info[1] is first temperature reading, info[2] is second.
    if "Frequency" in section:
        yield Service(item="1")

def check_janitza_umg_freq(item, params, section) -> CheckResult:
    if "Frequency" in section:
        if "levels_lower" in params:
            params_levels_lower = params["levels_lower"]
            if isinstance(params["levels_lower"], tuple):
                if isinstance(params["levels_lower"][0], int):
                    params_levels_lower = ("fixed", params["levels_lower"])
        else:
            params_levels_lower = None
        yield from check_levels(
            value=float(section["Frequency"]) / 100.0,
            metric_name="in_freq",
            levels_lower=params_levels_lower,
            render_func=render.frequency,
            label="Frequency",
        )

check_plugin_janitza_umg_freq = CheckPlugin(
    name = "janitza_umg_freq",
    sections = ["janitza_umg"],
    service_name = "Freqency %s",
    discovery_function = inventory_janitza_umg_freq,
    check_function = check_janitza_umg_freq,
    check_default_parameters = {},
    check_ruleset_name = "efreq",
)


def inventory_janitza_umg_temp(section) -> DiscoveryResult:
    ctr = 1
    for temp in section["Temperature"]:
        if temp != -1000:
            yield Service(item=str(ctr))
        ctr += 1

def check_janitza_umg_temp(item, params, section) -> CheckResult:
    idx = int(item) - 1
    if len(section["Temperature"]) > idx:
        yield from check_temperature(
            reading=float(section["Temperature"][idx]) / 10.0,
            params=params,
            unique_name="janitza_umg_%s" % item,
        )

check_plugin_janitza_umg_temp = CheckPlugin(
    name = "janitza_umg_temp",
    sections = ["janitza_umg"],
    service_name = "Temperature External %s",
    discovery_function = inventory_janitza_umg_temp,
    check_function = check_janitza_umg_temp,
    check_default_parameters = {
    },
    check_ruleset_name = "temperature",
)
