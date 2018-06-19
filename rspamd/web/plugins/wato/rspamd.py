#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_rule("agents/" + _("Agent Plugins"),
    "agent_config:rspamd",
    Alternative(
        title = _("Rspamd statistics"),
        help = _("This will deploy the agent plugin <tt>rspamd</tt> for Rspamd statistics."),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the rspamd plugin"),
                elements = [
                   ( "interval", Age(title = _("Run asynchronously"), label = _("Interval for collecting data"), default_value = 300 )),
                   # Extendable for later use. defaults-extra-file currently empty,
                   # but this could be filled with options that are configured
                   # here (e.g. an alternative port number, etc.)
                ],
            ),
            FixedValue(None, title = _("Do not deploy the rspamd plugin"), totext = _("(disabled)") ),
        ]
    )
)

