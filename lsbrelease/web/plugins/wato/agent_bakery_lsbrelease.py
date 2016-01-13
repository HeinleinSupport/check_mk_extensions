#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Linux Agent")

register_rule(group,
    "agent_config:lsbrelease",
    Alternative(
        title = _("Distribution Version Check"),
        help = _("This will deploy the agent plugin <tt>lsbrelease</tt> for monitoring the distribution version."),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the LSB-Release plugin"),
                elements = [
                   ( "interval", Age(title = _("Run asynchronously"), label = _("Interval for collecting data"), default_value = 300 )),
                   # Extendable for later use. defaults-extra-file currently empty,
                   # but this could be filled with options that are configured
                   # here (e.g. an alternative port number, etc.)
                ],
            ),
            FixedValue(None, title = _("Do not deploy the LSB-Release plugin"), totext = _("(disabled)") ),
        ]
    )
)

