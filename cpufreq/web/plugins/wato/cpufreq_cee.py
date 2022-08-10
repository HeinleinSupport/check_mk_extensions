#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

try:
    from cmk.gui.i18n import _
    from cmk.gui.plugins.wato import (
        HostRulespec,
        rulespec_registry,
    )
    from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
    from cmk.gui.valuespec import DropdownChoice

    def _valuespec_agent_config_cpufreq():
        return DropdownChoice(
            title = _("CPU Frequencies (Linux)"),
            help = _("This will deploy the agent plugin <tt>cpufreq</tt> to collect CPU frequencies."),
            choices = [
                ( True, _("Deploy plugin for CPU Frequencies") ),
                ( None, _("Do not deploy plugin for CPU Frequencies") ),
            ]
        )

    rulespec_registry.register(
        HostRulespec(
            group=RulespecGroupMonitoringAgentsAgentPlugins,
            name="agent_config:cpufreq",
            valuespec=_valuespec_agent_config_cpufreq,
        ))

except ModuleNotFoundError:
    # RAW edition
    pass
