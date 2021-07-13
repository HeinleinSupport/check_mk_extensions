#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Check_MK Redis Info Plugin
#
# Copyright 2016, Clemens Steinkogler <c.steinkogler[at]cashpoint.com>
#
# Extended 2017, Robert Sander <r.sander@heinlein-support.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path
from typing import Any, Dict

from .bakery_api.v1 import FileGenerator, OS, Plugin, PluginConfig, register

from cmk.utils import debug
from pprint import pprint

def get_redis_info_files(conf: Dict[str, Any]) -> FileGenerator:
    if debug.enabled():
        print("redis_info")
        pprint(conf)
    res = True
    if isinstance(conf, str) and conf == '_no_deploy':
        res = False
    elif isinstance(conf, tuple):
        lines = []
        if conf[0] == "static":
            lines.append("instances = %r" % conf[1][0])
            lines.append("password = %r" % conf[1][1])
        if conf[0] == "autodetect":
            if conf[1]:
                lines.append("password = %r" % conf[1])
        yield PluginConfig(base_os=OS.LINUX,
                           lines=lines,
                           target=Path("redis_info.cfg"),
                           include_header=True)
    if res:
        yield Plugin(base_os=OS.LINUX,
                     source=Path("redis_info.py"))

register.bakery_plugin(
    name="redis_info",
    files_function=get_redis_info_files,
)
