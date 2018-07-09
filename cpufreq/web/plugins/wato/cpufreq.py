#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_rule("agents/" + _("Agent Plugins"),
    "agent_config:cpufreq",
    DropdownChoice(
        title = _("CPU Frequencies (Linux)"),
        help = _("This will deploy the agent plugin <tt>cpufreq</tt> to collect CPU frequencies."),
        choices = [
            ( True, _("Deploy plugin for CPU Frequencies") ),
            ( None, _("Do not deploy plugin for CPU Frequencies") ),
        ]
    )
)

