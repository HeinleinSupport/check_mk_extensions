#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:postfix_mailq_details",
    Alternative(
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
                        optional_keys = False,
                        elements = [
                          ( 'QUEUES', TextAscii(title = _("Queues"), default_value='active incoming') ),
                          ( 'AGE', Age(title=_("Count eails older than:"), default_value=300 ) ),
                        ]
                      )
                    ),
                    ( "2",
                      Dictionary(
                        title=_("Second group"),
                        optional_keys = False,
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
)

