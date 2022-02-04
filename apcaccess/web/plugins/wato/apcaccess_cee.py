#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
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

    def _valuespec_agent_config_apcaccess():
        return DropdownChoice(
            title = _("APC UPS via apcaccess (Linux, Windows)"),
            help = _("This will deploy the agent plugin <tt>apcaccess</tt> to check various APC UPS stats."),
            choices = [
                ( True, _("Deploy plugin for APC UPS") ),
                ( None, _("Do not deploy plugin for APC UPS") ),
            ]
        )

    rulespec_registry.register(
         HostRulespec(
             group=RulespecGroupMonitoringAgentsAgentPlugins,
             name="agent_config:apcaccess",
             valuespec=_valuespec_agent_config_apcaccess,
         ))

except ModuleNotFoundError:
    # RAW edition
    pass
