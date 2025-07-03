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
        Age,
        Alternative,
        Dictionary,
        FixedValue,
        ListOfStrings,
        TextAscii,
    )

    def _valuespec_agent_config_postfix_mailq_details():
        return Alternative(
            title = _("Postfix Queue Details (Linux)"),
            help = _("This ruleset will deploy the agent plugin <tt>postfix_mailq_details</tt>."),
            style = "dropdown",
            elements = [
                Dictionary(
                    title = _("Deploy the Postfix queue details plugin"),
                    elements = [
                        ( "1",
                          Dictionary(
                            title=_("First group"),
                            optional_keys = [],
                            elements = [
                              ( 'QUEUES', TextAscii(title = _("Queues"), default_value='active incoming') ),
                              ( 'AGE', Age(title=_("Count emails older than:"), default_value=300 ) ),
                            ]
                          )
                        ),
                        ( "2",
                          Dictionary(
                            title=_("Second group"),
                            optional_keys = [],
                            elements = [
                              ( 'QUEUES', TextAscii(title = _("Queues"), default_value='deferred') ),
                              ( 'AGE', Age(title=_("Count emails younger than:"), default_value=300 ) ),
                            ]
                          )
                        ),
                    ],
                ),
                FixedValue(None, title = _("Do not deploy the Postfix queue details plugin"), totext = _("disabled")),
            ]
        )

    rulespec_registry.register(
         HostRulespec(
             group=RulespecGroupMonitoringAgentsAgentPlugins,
             name="agent_config:postfix_mailq_details",
             valuespec=_valuespec_agent_config_postfix_mailq_details,
         ))

except ModuleNotFoundError:
    # RAW edition
    pass
