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
        ],
        optional_keys = [ 'hosttags', 'host' ],
    ),
    title = _("Query Jenkins for Jobs"),
    help  = _(''),
    match = 'first'
)
