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

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.valuespec import (
    Age,
    Alternative,
    Dictionary,
    FixedValue,
)

def _valuespec_agent_config_hpsa():
    return Alternative(
        title = _("HP RAID Status (Linux)"),
        help = _("This will deploy the agent plugin <tt>hpsa</tt> for monitoring the status of HP Raid controllers via <tt>ssacli</tt>, <tt>hpssacli</tt>, or <tt>hpacucli</tt>."),
        style = 'dropdown',
        elements = [
            Dictionary(
                title = _("Deploy plugin for HP RAID controllers"),
                elements = [
                    ("interval", Age(
                        title = _("Run asynchronously"),
                        label = _("Interval for collecting data"),
                        default_value = 300
                    )),
                ],
            ),
            FixedValue(
                None,
                title = _("Do not deploy plugin for HP RAID controllers"),
                totext = _("(disabled)")
            ),
        ]
    )

rulespec_registry.register(
     HostRulespec(
         group=RulespecGroupMonitoringAgentsAgentPlugins,
         name="agent_config:hpsa",
         valuespec=_valuespec_agent_config_hpsa,
     ))
