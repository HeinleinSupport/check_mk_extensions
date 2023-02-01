#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2017 Heinlein Support GmbH
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

#{u'df': {u'nodes': [{u'crush_weight': 0.097595,
#                     u'depth': 2,
#                     u'device_class': u'hdd',
#                     u'id': 5,
#                     u'kb': 104754156,
#                     u'kb_avail': 103598436,
#                     u'kb_used': 1155720,
#                     u'name': u'osd.0',
#                     u'pgs': 94,
#                     u'pool_weights': {},
#                     u'reweight': 1.0,
#                     u'type': u'osd',
#                     u'type_id': 0,
#                     u'utilization': 1.103269,
#                     u'var': 0.989588}],
#         u'stray': [{u'crush_weight': 0.0,
#                     u'depth': 0,
#                     u'id': 6,
#                     u'kb': 0,
#                     u'kb_avail': 0,
#                     u'kb_used': 0,
#                     u'name': u'osd.6',
#                     u'pgs': 0,
#                     u'reweight': 0.0,
#                     u'type': u'osd',
#                     u'type_id': 0,
#                     u'utilization': 0.0,
#                     u'var': 0.0}],
#         u'summary': {u'average_utilization': 1.114877,
#                      u'dev': 0.045563,
#                      u'max_var': 1.087023,
#                      u'min_var': 0.964106,
#                      u'total_kb': 628524936,
#                      u'total_kb_avail': 621517656,
#                      u'total_kb_used': 7007280}},
# u'perf': {u'osd_perf_infos': [{u'id': 5,
#                                u'perf_stats': {u'apply_latency_ms': 0,
#                                                u'commit_latency_ms': 0}}]},
# u'nodes': {"ceph01":[0,1,2,9,10,11,18,19],
#            "ceph02":[3,4,5,12,13,14,20,21],
#            "ceph03":[6,7,8,15,16,17,22,23]}}

from .agent_based_api.v1.type_defs import (
    CheckResult,
    DiscoveryResult,
    HostLabelGenerator,
)

from .agent_based_api.v1 import (
    get_value_store,
    register,
    HostLabel,
    Metric,
    Result,
    State,
    Service,
    ServiceLabel,
    )

from .utils import df

import json
import time

def parse_cephosd(string_table):
    import json
    section = {}
    for line in string_table:
        try:
            section.update(json.loads("".join([item for item in line])))
        except ValueError:
            pass
    return section

def host_label_cephosd(section) -> HostLabelGenerator:
    if 'df' in section and 'nodes' in section['df'] and len(section['df']['nodes']) > 0:
        yield HostLabel('ceph/osd', 'yes')

register.agent_section(
    name="cephosd",
    parse_function=parse_cephosd,
    host_label_function=host_label_cephosd,
)

def discovery_cephosd(section) -> DiscoveryResult:
    if 'df' in section and 'nodes' in section['df']:
        for osd in section['df']['nodes']:
            service_labels=[]
            if 'device_class' in osd:
                service_labels.append(ServiceLabel('cephosd/device_class', osd['device_class']))
            yield Service(item='OSD %d' % osd['id'],
                          labels=service_labels)

def check_cephosd(item, params, section) -> CheckResult:
    if 'df' in section and 'nodes' in section['df']:
        value_store = get_value_store()
        for osd in section['df']['nodes']:
            if 'OSD %d' % osd['id'] == item:
                size_mb = osd['kb'] / 1024.0
                avail_mb = osd['kb_avail'] / 1024.0
                yield from df.df_check_filesystem_single(value_store,
                                                         item,
                                                         size_mb,
                                                         avail_mb,
                                                         0,
                                                         None,
                                                         None,
                                                         params=params)
                if 'pgs' in osd:
                    yield Result(state=State.OK,
                                 summary="%d PGs" % osd['pgs'])
                    yield Metric('num_pgs', osd['pgs'])
                if 'status' in osd and osd['status'] != 'up':
                    yield Result(state=State.WARN,
                                 summary="Status is %s" % osd['status'])
    if 'perf' in section and 'osd_perf_infos' in section['perf']:
        for osd in section['perf']['osd_perf_infos']:
            if 'OSD %d' % osd['id'] == item:
                apply_latency = osd['perf_stats']['apply_latency_ms']
                commit_latency = osd['perf_stats']['commit_latency_ms']
                yield Result(state=State.OK,
                             summary='Apply Latency: %dms, Commit Latency: %dms' % ( apply_latency,
                                                                                     commit_latency))
                yield Metric('apply_latency', apply_latency / 1000.0)
                yield Metric('commit_latency', commit_latency / 1000.0)

register.check_plugin(
    name="cephosd",
    service_name="Ceph %s",
    sections=["cephosd"],
    discovery_function=discovery_cephosd,
    check_function=check_cephosd,
    check_default_parameters=df.FILESYSTEM_DEFAULT_PARAMS,
    check_ruleset_name="filesystem",
)
