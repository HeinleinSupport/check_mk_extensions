#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2018 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

def inventory_xe_cpu_util(info):
    if len(info) > 0:
        yield None, {}

def check_xe_cpu_util(_no_item, params, info):
    cpus = {}
    for line in info:
        cpus[saveint(line[0])] = round(savefloat(line[2]) * 100.0, 1)
    if cpus:
        average = sum(cpus.values()) / len(cpus)
        perfdata = [ ('cpu_util_guest', average) ]
        if 'util' in params:
            if type(params['util']) == tuple:
                perfdata = [ ('cpu_util_guest', average, params['util'][0], params['util'][1]) ]
            state, text, perflevel = check_levels(average, 'xe_cpu_util_average', params['util'], unit='%')
        else:
            state, text, perflevel = 0, '', []
        yield state, 'Average CPU utilisation: %s%s' % (get_percent_human_readable(average), text), perfdata + perflevel
        if 'levels_single' or 'core_util_graph' in params:
            for cpuid in sorted(cpus.keys()):
                if 'core_util_graph' in params:
                    perfdata = [ ('cpu_core_util_%s' % cpuid, cpus[cpuid]) ]
                else:
                    perfdata = []
                if 'levels_single' in params:
                    if type(params['levels_single']) == tuple:
                        perfdata = [ ('cpu_core_util_%s' % cpuid, cpus[cpuid], params['levels_single'][0], params['levels_single'][1]) ]
                    state, text, perflevel = check_levels(cpus[cpuid], 'xe_cpu_util_%s' % cpuid, params['levels_single'], unit='%')
                else:
                    state, text, perflevel = 0, '', []
                if text:
                    yield state, "Core %d: %s%s" % (cpuid + 1, get_percent_human_readable(cpus[cpuid]), text), perfdata + perflevel
                elif perfdata:
                    yield 0, None, perfdata

# check_info["xe_cpu_util"] = {
#     'check_function'        : check_xe_cpu_util,
#     'inventory_function'    : inventory_xe_cpu_util,
#     'service_description'   : 'Xen CPU Utilisation',
#     'has_perfdata'          : True,
#     'group'                 : 'xe_cpu_util',
# }
