#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

try:
    from cmk.gui.i18n import _
    from cmk.gui.plugins.wato import (
        HostRulespec,
        rulespec_registry,
    )
    from cmk.gui.valuespec import (
        DropdownChoice,
    )
    from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins

    def _valuespec_agent_config_msexch_database_size():
        return DropdownChoice(
            title = _("MS Exchange Database Size (Windows)"),
            help = _("This will deploy the agent plugin <tt>msexch_database_size.ps1</tt> for monitoring the size of MS Exchange databases."),
            choices = [
                ( True, _("Deploy plugin for MS Exchange database size") ),
                ( None, _("Do not deploy plugin for MS Exchange database size") ),
            ]
        )

    rulespec_registry.register(
        HostRulespec(
            group=RulespecGroupMonitoringAgentsAgentPlugins,
            name="agent_config:msexch_database_size",
            valuespec=_valuespec_agent_config_msexch_database_size,
        ))

except ModuleNotFoundError:
    # RAW edition
    pass
