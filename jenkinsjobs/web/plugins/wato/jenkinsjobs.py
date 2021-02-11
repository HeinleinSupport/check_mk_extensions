#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-


from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Tuple,
    Integer,
    ListOfStrings,
    MonitoringState,
    TextAscii,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    RulespecGroupCheckParametersApplications,
)

def _item_spec_jenkins():
    return TextAscii(
        title = _("Service descriptions"),
        help = _('Specify service descriptions of the host that uses the special agent "jenkins".'),
        allow_empty = False
    )

def _parameter_valuespec_jenkins():
    return ListOf(
        Dictionary(
            elements = [
                ('url',
                 TextAscii(title=_('Datasource Name'))
                 ),
                ('levels',
                 Levels(title=_('Levels'))
                 ),
            ],
            optional_keys = False,
        ),
        title = _('Levels for Datasources'),
        add_label = _('Add levels for datasource'),
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="jenkins",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_jenkins,
        match_type="first",
        parameter_valuespec=_parameter_valuespec_jenkins,
        title=lambda: _("Jenkins Jobs"),
    ))

register_rule('datasource_programs',
    "special_agents:jenkins",
    Dictionary(
        title = _("Jenkins"),
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
                        ('hostname', MonitoredHostname(title=_('Hostname'), from_active_config=True)),
                        ('jobs', ListOf(RegExp('prefix', label=_('RegExp for job name')),
                                        title=_('List of Regular Expressions'))),
                    ],
                    optional_keys = [],
                ),
                title = _('Jobs to query for monitored hosts.'),
                )),
        ],
        optional_keys = [ 'auth' ],
    ),
    title = _("Jenkins Jobs"),
    help  = _(''),
    match = 'first'
)
