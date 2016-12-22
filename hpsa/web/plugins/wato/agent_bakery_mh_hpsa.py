#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:mh_hpsa",
    Alternative(
        title = _("HP RAID Controller Status (Linux)"),
        help = _("This will deploy the agent plugin <tt>mh_hpsa</tt> for monitoring the status of HP Raid controllers via hpacucli."),
        style = 'dropdown',
        elements = [
            Dictionary(
                title = _("Deploy plugin for HP RAID controllers"),
                elements = [
                    ("interval", Age(
                        title = _("Run asynchronously"),
                        label = _("Interval for collecting data"),
                        default_value = 300
                    )),
                ],
            ),
            FixedValue( None, title = _("Do not deploy plugin for HP RAID controllers") ),
        ]
    )
)

