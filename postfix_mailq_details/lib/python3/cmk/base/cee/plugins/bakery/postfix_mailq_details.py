#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
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

from pathlib import Path # type: ignore
from typing import Any, Dict # type: ignore

from cmk.base.plugins.bakery.bakery_api.v1 import (
    FileGenerator,
    OS,
    Plugin,
    PluginConfig,
    register,
)

def get_postfix_mailq_details_files(conf: Dict[str, Any]) -> FileGenerator:
    if conf.get("deploy"):
        yield Plugin(
            base_os=OS.LINUX,
            source=Path("postfix_mailq_details")
        )

    groupmap = { "one": "1", "two": "2" }
    prefixes = { '1': '+', '2': '-' }
    lines = []

    for group, number in groupmap.items():
        if group in conf:
            lines.append('QUEUES%s=\"%s\"' % (number, conf[group]['QUEUES'] ))
            lines.append('AGE%s=%s%d' % (number, prefixes[number], conf[group]['AGE'] / 60 ))
    
    if lines:
        yield PluginConfig(base_os=OS.LINUX,
                           lines=lines,
                           target=Path("postfix_mailq_details"),
                           include_header=True)

register.bakery_plugin(
    name="postfix_mailq_details",
    files_function=get_postfix_mailq_details_files,
)
