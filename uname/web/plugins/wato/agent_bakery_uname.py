#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_rule("agents/" + _("Linux Agent"),
    "agent_config:uname",
    Alternative(
        title = _("Kernel Version Check"),
        help = _("This will deploy the agent plugin <tt>uname</tt> for monitoring the kernel version."),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the uname plugin"),
                elements = [
                   ( "interval", Age(title = _("Run asynchronously"), label = _("Interval for collecting data"), default_value = 300 )),
                   # Extendable for later use. defaults-extra-file currently empty,
                   # but this could be filled with options that are configured
                   # here (e.g. an alternative port number, etc.)
                ],
            ),
            FixedValue(None, title = _("Do not deploy the uname plugin"), totext = _("(disabled)") ),
        ]
    )
)

