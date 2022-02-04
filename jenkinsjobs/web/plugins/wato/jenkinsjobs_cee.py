#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

try:
    from cmk.gui.i18n import _
    from cmk.gui.plugins.wato import (
        HostRulespec,
        rulespec_registry,
    )
    from cmk.gui.cee.plugins.wato.agent_bakery.rulespecs.utils import RulespecGroupMonitoringAgentsAgentPlugins
    from cmk.gui.valuespec import (
        Alternative,
        Dictionary,
        FixedValue,
        HTTPUrl,
        ListOf,
        MonitoredHostname,
        Password,
        RegExp,
        TextAscii,
        Tuple,
    )

    def _valuespec_agent_config_jenkinsjobs():
        return Alternative(
            title = _("Jenkins Jobs (Linux)"),
            help = _("This will deploy the agent plugin <tt>jenkinsjobs</tt> to check Jenkins Jobs."),
            style = 'dropdown',
            elements = [
                Dictionary(
                    title = _('Deploy the Jenkins Jobs plugin.'),
                    elements = [
                        ('url', HTTPUrl(title=_('Jenkins URL'))),
                        ('auth', Alternative(title = _("Authentication"),
                            style = 'dropdown',
                            elements = [
                                Password(title=_("OAuth Token")),
                                Tuple(title=_("Credentials"),
                                    elements = [
                                        TextAscii(title=_("Username")),
                                        Password(title=_("Password")),
                                    ])
                            ])),
                        ('hosts', ListOf(
                            Dictionary(
                                elements = [
                                    ('hostname', MonitoredHostname(title=_('Hostname'))),
                                    ('jobs', ListOf(RegExp('prefix', label=_('RegExp for job name')),
                                                    title=_('List of Jobs'))),
                                ],
                                optional_keys = [],
                            ),
                            title = _('Jobs to query for monitored hosts.'),
                            )),
                    ],
                    optional_keys = [ 'auth' ],
                    ),
                FixedValue( None, title = _("Do not deploy plugin for Jenkins Jobs"), totext = _("(disabled)") ),
            ]
        )

    rulespec_registry.register(
         HostRulespec(
             group=RulespecGroupMonitoringAgentsAgentPlugins,
             name="agent_config:jenkinsjobs",
             valuespec=_valuespec_agent_config_jenkinsjobs,
         ))

except ModuleNotFoundError:
    # RAW edition
    pass
