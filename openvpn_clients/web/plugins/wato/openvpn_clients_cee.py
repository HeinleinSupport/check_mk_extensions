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

    def _valuespec_agent_config_openvpn_clients():
        return DropdownChoice(
            title = _("CPU Frequencies (Linux)"),
            help = _("This will deploy the agent plugin <tt>openvpn_clients</tt> to collect statistics of OpenVPN instances."),
            choices = [
                ( True, _("Deploy plugin for OpenVPN clients") ),
                ( None, _("Do not deploy plugin for OpenVPN clients") ),
            ]
        )

    rulespec_registry.register(
        HostRulespec(
            group=RulespecGroupMonitoringAgentsAgentPlugins,
            name="agent_config:openvpn_clients",
            valuespec=_valuespec_agent_config_openvpn_clients,
        ))

except ModuleNotFoundError:
    # RAW edition
    pass
