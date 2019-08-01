#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_check_parameters(
    subgroup_applications,
    "jenkins",
    _("Jenkins Jobs"),
    ListOf(
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
    ),
    TextAscii(
        title = _("Service descriptions"),
        help = _('Specify service descriptions of the host that uses the special agent "jenkins".'),
        allow_empty = False
    ),
    match_type = "first",
)

register_rule('datasource_programs',
    "special_agents:jenkins",
    Dictionary(
        title = _("Jenkins"),
        elements = [
            ('url', HTTPUrl(title=_('Jenkins URL'))),
            ('auth', Tuple(title = _("Authentication"),
                elements = [
                    TextAscii(title=_("Username")),
                    Password(title=_("Password")),
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
