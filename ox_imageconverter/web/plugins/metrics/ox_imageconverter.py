#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2023 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.gui.i18n import _

from cmk.gui.plugins.metrics import (
    metric_info,
    graph_info,
)

metric_info["cache_size"] = {
    "title" : _("Cache Size"),
    "unit"  : "bytes",
    "color" : "11/a",
}

metric_info["cache_key_count"] = {
    "title" : _("Cache Key Count"),
    "unit"  : "",
    "color" : "11/b",
}

metric_info["requests_cached_images"] = {
    "title" : _("Requests for cached Images"),
    "unit"  : "1/s",
    "color" : "12/a",
}

metric_info["requests_noncached_images"] = {
    "title" : _("Requests for non-cached Images"),
    "unit"  : "1/s",
    "color" : "12/b",
}

metric_info["peak_key_count_background"] = {
    "title" : _("Peak Key Count Background"),
    "unit"  : "",
    "color" : "13/a",
}

metric_info["peak_key_count_instant"] = {
    "title" : _("Peak Key Count Instant"),
    "unit"  : "",
    "color" : "14/a",
}

metric_info["peak_key_count_medium"] = {
    "title" : _("Peak Key Count Medium"),
    "unit"  : "",
    "color" : "15/a",
}

graph_info["ox_imageconverter_cache_requests"] = {
    "title"  : _("Cache Requests"),
    "metrics": [
        ("requests_per_sec", "line"),
        ("requests_noncached_images", "line"),
        ("requests_cached_images", "line"),
    ],
}
