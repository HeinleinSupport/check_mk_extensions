#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:otrs",
    Alternative(
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
                                  ( 'name', TextAscii(title=_("Queue name"), allow_empty=False, optional_key=False) ),
                                  ( 'id', Integer(title=_("Queue ID"), allow_empty=False) ),
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
)

