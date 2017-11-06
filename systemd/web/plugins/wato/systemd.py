#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# group = "checkparams"

register_rule("checkparams" + '/' + subgroup_inventory,
    varname = 'inventory_systemd_rules',
    title   = _('Linux Service Discovery (Systemd Units)'),
    help    = _('This ruleset defines criteria for automatically creating '
                'checks for systemd service units based upon what is running '
                'the the service discovery is done.'),
    valuespec = Dictionary(
        elements = [
            ('units', ListOfStrings(
                title = _("Systemd Units (Regular Expressions)"),
                help  = _('Regular expressions matching the begining of the internal name '
                          'of the systemd unit. '
                          'If no name is given then this rule will match all units. The '
                          'match is done on the <i>beginning</i> of the unit name. It '
                          'is done <i>case sensitive</i>. You can do a case insensitive match '
                          'by prefixing the regular expression with <tt>(?i)</tt>. Example: '
                          '<tt>(?i).*mssql</tt> matches all services which contain <tt>MSSQL</tt> '
                          'or <tt>MsSQL</tt> or <tt>mssql</tt> or...'),

                orientation = "horizontal",
            )),
            ('state', DropdownChoice(
                choices = [
                    ('active',     _('Active')),
                    ('inactive',   _('Inactive')),
                ],
                title = _("Create check if unit is active or not"),
            )),
        ],
        help = _('This rule can be used to configure the inventory of the windows services check. '
                 'You can configure specific windows services to be monitored by the windows check by '
                 'selecting them by name, current state during the inventory, or start mode.'),
    ),

    match = 'all',
)

register_rule("agents/" + _("Agent Plugins"),
    "agent_config:systemd",
    DropdownChoice(
        title = _("Systemd Units (Linux)"),
        help = _("This will deploy the agent plugin <tt>systemd</tt> to check state of systemd units (Linux services)."),
        choices = [
            ( True, _("Deploy plugin for Systemd Units") ),
            ( None, _("Do not deploy plugin for Systemd Units") ),
        ]
    )
)

