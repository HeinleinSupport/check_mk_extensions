#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2026 Heinlein Support GmbH
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


from collections.abc import Mapping # type: ignore
from typing import Any, List # type: ignore

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_value_store,
    get_rate,
    Metric,
    Result,
    RuleSetType,
    Service,
    State,
    StringTable,
)

import time

from dataclasses import dataclass # type: ignore

from prometheus_client.parser import text_string_to_metric_families

from cmk.ccc import debug
from pprint import pprint

@dataclass(frozen=True, kw_only=True)
class PrometheusMetric:
    name: str
    documentation: str
    type: str
    value: float
    labels: Mapping[str, str]

Section = Mapping[str, PrometheusMetric]

xspct_db_metrics = {
    "event_loop_lag_seconds": "Event Loop Lag",
    "xspct_db_foreground_overloaded": "Foreground Overloaded",
    "xspct_db_requests_timeout": "Requests Timeout",
    "xspct_db_background_rejected": "Background Rejected",
    "xspct_db_background_errors": "Background Errors",
    "xspct_db_prefilter_domain_count": "Prefilter Domain Count",
    "http_requests_in_flight": "HTTP Requests",
}
xspct_db_titles = dict((v,k) for k,v in xspct_db_metrics.items())

def parse_xspct_db(string_table: StringTable) -> Section:
    if debug.enabled():
        pprint(string_table)
    parsed = {}
    for family in text_string_to_metric_families("\n".join(x[0] for x in string_table)):
        if debug.enabled():
            print("\n\n# Family")
            print(family.name)
            print(len(family.samples))

        if len(family.samples) == 1 and family.name in xspct_db_metrics:
            parsed[family.name] = PrometheusMetric(
                name=family.samples[0].name,
                documentation=family.documentation,
                type=family.type,
                value=family.samples[0].value,
                labels=family.samples[0].labels,
            )

        # if debug.enabled():
        #     print("\n\n# Family")
        #     print(family.name)
        #     print(family.documentation)
        #     print(family.type)
        #     print(family.unit)
        
        # for sample in family.samples:
        #     if debug.enabled():
        #         print("## Sample")
        #         print(sample.name)
        #         print(sample.value)
        #         print(sample.exemplar)
        #         print(sample.labels)
        #         print(sample.timestamp)
    
    if debug.enabled():
        pprint(parsed)
    return parsed

agent_section_xspct_db = AgentSection(
    name="xspct_db",
    parse_function=parse_xspct_db,
)

def discovery_xspct_db(section: Section) -> DiscoveryResult:
    for metric, title in xspct_db_metrics.items():
        if metric in section:
            yield Service(item=title)

def check_xspct_db(item: str, section: Section) -> CheckResult:
    metric_name = str(xspct_db_titles.get(item))
    metric = section.get(metric_name)
    if metric:
        if metric.type == "counter":
            if debug.enabled:
                print(f"counter: {metric_name}")
            vs = get_value_store()
            value = get_rate(vs, metric_name, time.time(), metric.value)
        else:
            if debug.enabled:
                print(f"gauge: {metric_name}")
            value = metric.value
        yield Metric(
            metric.name,
            value,
        )
        yield Result(
            state=State.OK,
            summary=metric.documentation,
        )

check_plugin_xspct_db = CheckPlugin(
    name="xspct_db",
    service_name="XSPC DB %s",
    sections=["xspct_db"],
    discovery_function=discovery_xspct_db,
    check_function=check_xspct_db,
    # check_default_parameters={
    # },
    # check_ruleset_name="xspct_db",
)
