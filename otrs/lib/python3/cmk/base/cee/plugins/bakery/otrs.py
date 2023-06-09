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

from pathlib import Path
from typing import Any, Dict

from .bakery_api.v1 import FileGenerator, OS, Plugin, PluginConfig, register

def get_otrs_files(conf: Dict[str, Any]) -> FileGenerator:
    yield Plugin(base_os=OS.LINUX,
                 source=Path("check_otrs.py"))
    lines = []
    if 'defaults' in conf:
        lines.append('[DEFAULT]')
        for key, value in conf['defaults'].items():
            lines.append("%s = %s" % (key, value))
    
    for queue in conf.get('queues', []):
        lines.append('')
        lines.append("[%s]" % queue['name'])
        lines.append("id = %d" % queue['id'])
        lines.append("types = %s" % queue['types'])

    if lines:
        yield PluginConfig(base_os=OS.LINUX,
                           lines=lines,
                           target=Path("otrs.cfg"),
                           include_header=True)

register.bakery_plugin(
    name="otrs",
    files_function=get_otrs_files,
)
