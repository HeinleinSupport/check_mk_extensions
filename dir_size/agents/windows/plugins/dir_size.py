#!/usr/bin/env python3
# -*- coding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2025 Heinlein Consulting GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

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

import os

conffilename = os.path.join(
    os.environ.get("MK_CONFDIR"),
    "dir_size.cfg",
)

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

print("<<<dir_size>>>")
with open(conffilename, "r") as conffile:
    for line in conffile.readlines():
        dir = line.strip()
        size = int(get_size(dir) / 1024)
        print(f"{size}\t{dir}") 