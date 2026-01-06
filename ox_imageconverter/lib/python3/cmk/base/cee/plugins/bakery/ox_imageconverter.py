#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2023 Heinlein Consulting GmbH
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
    password_store,
)

def _lookup_for_bakery(pw_id: str) -> str:
    return password_store.lookup(password_store.password_store_path(), pw_id)

def _get_password(v):
    if isinstance(v, tuple):
        if v[0] == "cmk_postprocessed":
            if v[1] == "explicit_password":
                return v[2][1]
            if v[1] == "stored_password":
                return _lookup_for_bakery(v[2][0])
    return None

def get_ox_imageconverter_files(conf: Dict[str, Any]) -> FileGenerator:
    if isinstance(conf, bool):
        conf = {"deploy": conf}
    if conf.get("deploy"):
        yield Plugin(
            base_os=OS.LINUX,
            source=Path("ox_imageconverter"),
            interval=int(conf.get("interval", 0)),
        )
        yield PluginConfig(
            base_os=OS.LINUX,
            lines=[
                'OX_USERNAME="%s"' % conf.get("username"),
                'OX_PASSWORD="%s"' % _get_password(conf.get("password")),
            ],
            target=Path("ox_imageconverter.cfg"),
            include_header=True,
        )

register.bakery_plugin(
    name="ox_imageconverter",
    files_function=get_ox_imageconverter_files,
)
