#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# (c) 2023 Heinlein Support GmbH
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

try:
    from cmk.gui.i18n import _
    from cmk.gui.plugins.wato import (
        HostRulespec,
        rulespec_registry,
    )
    from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
    from cmk.gui.valuespec import (
        DropdownChoice,
    )

    def _valuespec_agent_config_siproxd_stats():
        return Alternative(
            title = _("Siproxd stats (Linux)"),
            help = _("This will deploy the agent plugin <tt>siproxd_stats</tt>."),
            style = "dropdown",
            elements = [
                Dictionary(
                    title = _("Deploy the siproxd_stats plugin"),
                    elements = [
                       ( "interval", Age(title = _("Run asynchronously"), label = _("Interval for collecting data"), default_value = 300 )),
                    ],
                ),
                FixedValue(None, title = _("Do not deploy the siproxd_stats plugin"), totext = _("(disabled)") ),
            ]
        )

    rulespec_registry.register(
         HostRulespec(
             group=RulespecGroupMonitoringAgentsAgentPlugins,
             name="agent_config:siproxd_stats",
             valuespec=_valuespec_agent_config_siproxd_stats,
         ))

except ModuleNotFoundError:
    # RAW edition
    pass
