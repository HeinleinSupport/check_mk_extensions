#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# (c) 2018 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#
#
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

register_check_parameters(
    subgroup_os,
    "xe_cpu_util",
    _("CPU utilization on Xen hosts"),
    Dictionary(
        elements = [
            ( "util",
                Levels(
                    title = _("Levels on total CPU utilization"),
                    unit = '%',
                    default_value = (90.0, 95.0),
                    ),
            ),
            ( "levels_single",
                Levels(
                    title = _("Levels on single cores"),
                    unit = '%',
                    default_value = (90.0, 95.0),
                    help = _("Here you can set levels on the CPU utilization on single cores"),
                ),
            ),
            ( "core_util_graph",
                Checkbox(
                    title = _("Graphs for individual cores"),
                    label = _("Enable performance graph for utilization of individual cores"),
                    help  = _("This adds another graph to the performance CPU utilization "
                              "details page, showing utilization of individual cores. "
                              "Please note that this graph may be impractical on "
                              "device with very many cores.")
                ),
            ),

        ],
    ),
    None,
    "dict",
)

register_rule('agents/' + _('Agent Plugins'),
    "agent_config:xe_cpu_util",
    DropdownChoice(
        title = _("Xen CPU Utilization (Linux)"),
        help = _("This will deploy the agent plugin <tt>xe_cpu_util</tt> to check CPU utilisation on Xen hosts."),
        choices = [
            ( True, _("Deploy plugin xe_cpu_util") ),
            ( None, _("Do not deploy plugin xe_cpu_util") ),
        ]
    )
)
