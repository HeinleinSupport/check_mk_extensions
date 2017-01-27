#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Check_MK Redis Info Plugin
#
# Copyright 2016, Clemens Steinkogler <c.steinkogler[at]cashpoint.com>
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

group = "checkparams"

subgroup_applications = _("Applications, Processes &amp; Services")

register_check_parameters(
    subgroup_applications,
    "redis_info",
    _("Redis info levels"),
    Dictionary(
        elements=[
            ("config",
             Tuple(
                 title=_("Config for Service"),
                 elements=[
                     Optional(
                         Tuple(
                             elements=[
                                 Float(
                                     title=_("Warning at"),
                                     default_value=5,
                                 ),
                                 Float(
                                     title=_("Critical at"),
                                     default_value=10,
                                 ),
                             ],
                         ),
                         label=_("Warn/Crit Levels"),
                         help=_("Put here the warn/crit-levels. For memory checks like used_memory, used_memory_peak and used_memory_rss should be given values in MB"),
                         none_label=_("No levels set"),
                         none_value=(None, None)
                     ),
                     DropdownChoice(
                         title=_("Create graph"),
                         help=_('default is No'),
                         choices=[
                             (False, _("No")),
                             (True, _("Yes")),
                         ],
                         default_value="no",
                     )
                 ]
             ),
             ),
        ]),
    TextAscii(
        title=_("Service description"),
        allow_empty=False,
    ),
    "dict"
)
