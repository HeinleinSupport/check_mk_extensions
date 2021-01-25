#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.wato import (
    HostRulespec,
    rulespec_registry,
)
from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
from cmk.gui.valuespec import (
    DropdownChoice,
)

def _valuespec_agent_config_mk_filehandler():
    return DropdownChoice(
        title = _("Filehandler (Linux)"),
        help = _("This will deploy the agent plugin <tt>mk_filehandler</tt> to check used file handles."),
        choices = [
            ( True, _("Deploy plugin for file handles") ),
            ( None, _("Do not deploy plugin for file handles") ),
        ]
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupMonitoringAgentsAgentPlugins,
        name="agent_config:mk_filehandler",
        valuespec=_valuespec_agent_config_mk_filehandler,
    ))
