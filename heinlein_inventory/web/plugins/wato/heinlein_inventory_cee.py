#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

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

def _valuespec_agent_config_heinlein_inventory():
    return Alternative(
        title = _("Hardware/Software-Inventory (Heinlein)"),
        help = _("If you activate this option, the agent plugin <tt>heinlein_inventory</tt> will be deployed on "
                 "linux hosts. It gathers information about installed hardware and software and makes the "
                 "information available in Multisite and for exporting to third-party software. <b>Note:</b> "
                 "in order to actually use the inventory for a host you also need to enable it in "
                 "the ruleset <a href='wato.py?varname=active_checks%3Acmk_inv&folder=&mode=edit_ruleset'>"
                 "Hardware/Software-Inventory / Do hardware/software Inventory</a>.<br />It does not collect route info."),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the Heinlein HW/SW-Inventory plugin"),
                elements = [
                     ( "interval",
                        Age(
                            title = _("Interval for collecting data"),
                     )),
                ],
            ),
            FixedValue(None, title = _("Do not deploy the Heinlein HW/SW-Inventory plugin"), totext = _("(disabled)") ),
        ],
        default_value = {
            "interval" : 14400,
        }
    )

rulespec_registry.register(
     HostRulespec(
         group=RulespecGroupMonitoringAgentsAgentPlugins,
         name="agent_config:heinlein_inventory",
         valuespec=_valuespec_agent_config_heinlein_inventory,
     ))
