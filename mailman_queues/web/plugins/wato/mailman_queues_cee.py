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
    Alternative,
    Dictionary,
    FixedValue,
    ListOfStrings,
    TextAscii,
)

def _valuespec_agent_config_mailman_queues():
    return Alternative(
        title = _("Mailman queues (Linux)"),
        help = _("This will deploy the agent plugin <tt>mailman_queues</tt> "
                 "for checking Mailman queues.<br />The default "
                 "queues are <tt>bounces</tt>, <tt>in</tt>, <tt>out</tt> and <tt>shunt</tt>."),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the Mailman queues plugin"),
                elements = [
                   ( "queues",
                     ListOfStrings(
                       title = _("Queues to look into for mail files"),
                       help = _("One queue name per line.<br />The default queues are <tt>bounces</tt>, <tt>in</tt>, <tt>out</tt> and <tt>shunt</tt>."),
                       valuespec = TextAscii(
                            size = 80,
                            regex = "^[^ \t*/]+$",
                            regex_error = _("Queues must not contain spaces, / and *."),
                       ),
                       allow_empty = False,
                     )
                   ),
                ],
                optional_keys = True,
            ),
            FixedValue(None, title = _("Do not deploy the Mailman queues plugin"), totext = _("(disabled)") ),
        ]
    )

rulespec_registry.register(
     HostRulespec(
         group=RulespecGroupMonitoringAgentsAgentPlugins,
         name="agent_config:mailman_queues",
         valuespec=_valuespec_agent_config_mailman_queues,
     ))
