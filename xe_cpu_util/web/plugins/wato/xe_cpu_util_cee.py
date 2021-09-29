#!/usr/bin/env python3
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

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.valuespec import (
    DropdownChoice,
)
              
def _valuespec_agent_config_xe_cpu_util():
    return DropdownChoice(
        title = _("Xen CPU Utilization (Linux)"),
        help = _("This will deploy the agent plugin <tt>xe_cpu_util</tt> to check CPU utilisation on Xen hosts."),
        choices = [
            ( True, _("Deploy plugin xe_cpu_util") ),
            ( None, _("Do not deploy plugin xe_cpu_util") ),
        ]
    )

rulespec_registry.register(
     HostRulespec(
         group=RulespecGroupMonitoringAgentsAgentPlugins,
         name="agent_config:xe_cpu_util",
         valuespec=_valuespec_agent_config_xe_cpu_util,
     ))
