#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from pathlib import Path
from typing import Any, Dict

from .bakery_api.v0 import FileGenerator, OS, Plugin, register

def get_mk_filehandler_files(conf: Dict[str, Any]) -> FileGenerator:
    yield Plugin(base_os=OS.LINUX,
                 source=Path("mk_filehandler"))

register.bakery_plugin(
    name="mk_filehandler",
    files_function=get_mk_filehandler_files,
)
