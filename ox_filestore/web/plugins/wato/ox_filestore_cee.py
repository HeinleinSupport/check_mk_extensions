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
        Alternative,
        Dictionary,
        FixedValue,
        Password,
        TextAscii,
    )

    def _valuespec_agent_config_ox_filestore():
        return Alternative(
            title = _("Open-Xchange Filestore Check"),
            help = _("This will deploy the agent plugin <tt>ox_filestore</tt> "
                     "for checking Open-Xchange file stores."),
            style = "dropdown",
            elements = [
                Dictionary(
                    title = _("Deploy the OX file stores plugin"),
                    elements = [
                        ( "username", TextAscii(title = _("Username for OX admin master"), allow_empty = False )),
                        ( "password", Password(title = _("Password for OX admin master"), allow_empty = False )),
                    ],
                    optional_keys = False,
                ),
                FixedValue(None, title = _("Do not deploy the OX filestores plugin"), totext = _("(disabled)") ),
            ]
        )

    rulespec_registry.register(
         HostRulespec(
             group=RulespecGroupMonitoringAgentsAgentPlugins,
             name="agent_config:ox_filestore",
             valuespec=_valuespec_agent_config_ox_filestore,
         ))

except ModuleNotFoundError:
    # RAW edition
    pass
