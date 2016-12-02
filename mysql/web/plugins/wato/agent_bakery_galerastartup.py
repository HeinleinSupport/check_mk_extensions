#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

group = "agents/" + _("Agent Plugins")

register_rule(group,
    "agent_config:galerastartup",
    DropdownChoice(
        title = _("MySQL Galera Cluster Address (Linux)"),
        help = _("This will deploy the agent plugin <tt>galerastartup</tt> that checks the setting of wsrep_cluster_address."),
        choices = [
            ( True, _("Deploy plugin for Galera Cluster Address") ),
            ( None, _("Do not deploy plugin for Galera Cluster Address") ),
        ]
    )
)

