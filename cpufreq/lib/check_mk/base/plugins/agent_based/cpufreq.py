#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

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


# Example Agent Output
#<<<cpufreq>>>
#cpu0 ondemand 800000 800000 3001000
#cpu1 ondemand 3001000 800000 3001000
#cpu2 ondemand 1000000 800000 3001000
#cpu3 ondemand 1000000 800000 3001000

epsilon = 5 # 5%

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
)

from .agent_based_api.v1 import (
    check_levels,
    register,
    render,
    Metric,
    Result,
    State,
    Service,
    )

def parse_cpufreq(string_table):
    return string_table

register.agent_section(
    name="cpufreq",
    parse_function=parse_cpufreq,
)

def discovery_cpufreq(section) -> DiscoveryResult:
    if len(section) > 0 and len(section[0]) > 0:
        yield Service()

def check_cpufreq(section) -> CheckResult:
    cpumsgs = []
    freqs = []
    perfdata = []
    errors = []
    for line in section:
        res = State.OK
        cpu = line[0]
        governor = line[1]
        cur_freq = int(line[2]) * 1000.0
        if line[3] != 'unknown':
            min_freq = int(line[3]) * 1000.0
        else:
            min_freq = 0
        if line[4] != 'unknown':
            max_freq = int(line[4]) * 1000.0
        else:
            max_freq = 0

        freqs.append(cur_freq)

        yield from check_levels(cur_freq,
                                levels_upper=(max_freq * (100 - epsilon) / 100.0, max_freq),
                                levels_lower=(min_freq * (100 + epsilon) / 100.0, min_freq),
                                metric_name='freq_%s' % cpu,
                                render_func=render.frequency,
                                label='%s has %s governor with' % (cpu, governor),
                                notice_only=True)
    avg_freq = float(sum(freqs)) / max(len(freqs), 1)
    yield Result(state=State.OK,
                 summary="%d CPUs, average %s" % (len(freqs), render.frequency(avg_freq)))
    yield Metric('freq_cpu_avg', avg_freq)

register.check_plugin(
    name="cpufreq",
    service_name="CPU Frequencies",
    sections=["cpufreq"],
    discovery_function=discovery_cpufreq,
    check_function=check_cpufreq,
)

