#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

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
    
    def _valuespec_agent_config_amavis():
        return DropdownChoice(
            title = _("Amavis (Linux)"),
            help = _("This will deploy the agent plugin <tt>amavis</tt> to check various amavisd-new stats."),
            choices = [
                ( True, _("Deploy plugin for amavisd-new") ),
                ( None, _("Do not deploy plugin for amavisd-new") ),
            ]
        )
    
    rulespec_registry.register(
        HostRulespec(
            group=RulespecGroupMonitoringAgentsAgentPlugins,
            name="agent_config:amavis",
            valuespec=_valuespec_agent_config_amavis,
        ))
    
except ModuleNotFoundError:
    # RAW edition
    pass

