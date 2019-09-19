#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:mailman_queues",
    Alternative(
        title = _("Mailman queues (Linux)"),
        help = _("This will deploy the agent plugin <tt>mailman_queues</tt> "
                 "for checking Mailman queues.<br />The default "
                 "queues are <tt>bounces</tt>, <tt>in</tt>, <tt>out</tt> and <tt>shunt</tt>."),
        style = "dropdown",
        elements = [
            Dictionary(
                title = _("Deploy the Mailman queues plugin"),
                elements = [
                   ( "queues",
                     ListOfStrings(
                       title = _("Queues to look into for mail files"),
                       help = _("One queue name per line.<br />The default queues are <tt>bounces</tt>, <tt>in</tt>, <tt>out</tt> and <tt>shunt</tt>."),
                       valuespec = TextAscii(
                            size = 80,
                            regex = "^[^ \t*/]+$",
                            regex_error = _("Queues must not contain spaces, / and *."),
                       ),
                       allow_empty = False,
                     )
                   ),
                ],
                optional_keys = True,
            ),
            FixedValue(None, title = _("Do not deploy the Mailman queues plugin"), totext = _("(disabled)") ),
        ]
    ),
)

