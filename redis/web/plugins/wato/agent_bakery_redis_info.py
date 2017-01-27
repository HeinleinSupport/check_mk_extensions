#!/usr/bin/python
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

register_rule("agents/" + _("Agent Plugins"),
    "agent_config:redis_info",
    CascadingDropdown(
        title = _("REDIS instances (Linux)"),
        help = _("If you activate this option, then the agent plugin <tt>redis_info</tt> will be deployed. "
                 "For each configured or detected REDIS instance there will be one new service with detailed "
                 "statistics of the current number of clients and processes and their various states."),
        style = "dropdown",
        choices = [
            ( "autodetect", _("Autodetect instances")
             ),
            ( "static", _("Specific list of instances"),
                ListOf(
                    Tuple(
                        elements = [
                            IPv4Address(
                                title = _("IP Address"),
                                default_value = "127.0.0.1",
                            ),
                            Alternative(
                                style = "dropdown",
                                elements = [
                                    FixedValue(None,
                                        title = _("Don't use custom port"),
                                        totext = _("Use default port"),
                                    ),
                                    Integer(
                                        title = _("TCP Port Number"),
                                        minvalue = 1,
                                        maxvalue = 65535,
                                        default_value = 6379,
                                    ),
                                ]
                            ),
                        ]
                    ),
                ),
            ),
            ( '_no_deploy', _("Do not deploy the redis_info plugin") ),
        ]
    ),
)

