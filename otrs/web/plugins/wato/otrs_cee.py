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
        Integer,
        Password,
        TextAscii,
    )

    def _valuespec_agent_config_otrs():
        return Alternative(
            title = _("OTRS (Linux)"),
            help = _("This ruleset will deploy the agent plugin <tt>check_otrs.py</tt>."),
            style = "dropdown",
            elements = [
                Dictionary(
                    title = _("Deploy the OTRS plugin"),
                    optional_keys = False,
                    elements = [
                        ( "defaults",
                          Dictionary(
                              title = _("DB connection and default types."),
                              optional_keys = False,
                              elements = [
                                  ( 'dbhost', TextAscii(title = _("Hostname"), default_value='localhost') ),
                                  ( 'dbname', TextAscii(title = _("DB-Name"), default_value='otrs') ),
                                  ( 'dbuser', TextAscii(title = _("DB-User"), default_value='otrs') ),
                                  ( 'dbpass', Password(title = _("Password")) ),
                              ]
                          )
                        ),
                        ( "queues",
                          ListOf(
                              Dictionary(
                                  optional_keys = False,
                                  elements = [
                                      ( 'name', TextAscii(title=_("Queue name"), allow_empty=False) ),
                                      ( 'id', Integer(title=_("Queue ID")) ),
                                      ( 'types', TextAscii(title=_('Ticket state for this queue'), default_value="1 4 6 13") ),
                                  ]
                              ),
                              title = _("Queues to monitor"),
                              add_label = _("Add queue"),
                          )
                        ),
                    ],
                ),
                FixedValue(None, title = _("Do not deploy the OTRS plugin"), totext = _("disabled")),
            ]
        )

    rulespec_registry.register(
         HostRulespec(
             group=RulespecGroupMonitoringAgentsAgentPlugins,
             name="agent_config:otrs",
             valuespec=_valuespec_agent_config_otrs,
         ))

except ModuleNotFoundError:
    # RAW edition
    pass
