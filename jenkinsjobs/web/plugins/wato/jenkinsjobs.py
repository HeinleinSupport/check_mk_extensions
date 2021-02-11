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
    HostRulespec,
    RulespecGroupCheckParametersApplications,
)

from cmk.gui.plugins.wato.datasource_programs import RulespecGroupDatasourceProgramsApps

def _item_spec_jenkinsjobs():
    return TextAscii(
        title = _("Service descriptions"),
        help = _('Specify service descriptions of the host that uses the special agent "jenkinsjobs".'),
        allow_empty = False
    )

def _parameter_valuespec_jenkinsjobs():
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
        check_group_name="jenkinsjobs",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_jenkinsjobs,
        match_type="first",
        parameter_valuespec=_parameter_valuespec_jenkinsjobs,
        title=lambda: _("Jenkins Jobs"),
    ))

def _valuespec_special_agents_jenkinsjobs():
    return Dictionary(
        title = _("JenkinsJobs"),
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
                                        title=_('List of Regular Expressions'))),
                    ],
                    optional_keys = [],
                ),
                title = _('Jobs to query for monitored hosts.'),
                )),
        ],
        optional_keys = [ 'auth' ],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsApps,
        name="special_agents:jenkinsjobs",
        valuespec=_valuespec_special_agents_jenkinsjobs,
    ))
