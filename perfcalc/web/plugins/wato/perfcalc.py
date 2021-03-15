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
    HostTagCondition,
    Levels,
    RulespecGroupCheckParametersApplications,
)

from cmk.gui.plugins.wato.datasource_programs import RulespecGroupDatasourceProgramsApps

def _transform_perfcalc_parameter(params):
    if isinstance(params, dict):
        return params
    return {'list': params}

def _parameter_valuespec_perfcalc():
    return Transform(Dictionary(
        title = _('Levels for Datasources'),
        optional_keys = None,
        elements = [
            ('list', ListOf(
                Dictionary(
                    elements = [
                        ('dsname',       TextAscii(title=_('Datasource Name'))),
                        ('levels',       Levels(title=_('Upper Levels'))),
                        ('levels_lower', Levels(title=_('Lower Levels'))),
                    ],
                    optional_keys = ['levels', 'levels_lower'],
                ),
                add_label = _('Add levels for datasource'),
            )),
        ],
    ),
    forth = _transform_perfcalc_parameter,
    )

def _item_spec_perfcalc():
    return TextAscii(
        title = _("Service descriptions"),
        help = _('Specify service descriptions of the host that uses the special agent "perfcalc".'),
        allow_empty = False
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="perfcalc",
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_perfcalc,
        match_type="first",
        parameter_valuespec=_parameter_valuespec_perfcalc,
        title=lambda: _("Calculated Performance Data Levels"),
    ))

def _transform_perfcalc_ds(source):
    if 'hosttags' not in source:
        source['hosttags'] = []
    return source

def _valuespec_special_agents_perfcalc():
    return ListOf(
        Transform(
        Dictionary(
            title = _("Service Check specification"),
            elements = [
                ( "hosttags",
                  HostTagCondition(
                      title = _('Hosttags'),
                      help = _('Select hosts by matching tags. Hosts will be searched on all connected sites. If you also enter host names below both will be combined with AND as usual.'),
                      allow_empty = True,
                  )
                ),
                ( "host",
                  ListOfStrings(
                      title = _('Hostname'),
                      help = _('Specify the hosts where you want to collect the service performance data from. Hosts will be searched on all connected sites. Multiple entries will be combined with OR.'),
                      allow_empty = True,
                  )
                ),
                ( "service",
                  TextAscii(
                      title = _("Service Description"),
                      help = _('Enter the exact service description.'),
                      allow_empty = False,
                  )
                ),
                ( "datasource",
                  ListOfStrings(
                      title = _("Data Source"),
                      help = _('The data source name(s) of the service check that should be used in the calculation. Use the name from "Service performance data (source code)" in the service status detail view.'),
                      allow_empty = False,
                  )
                ),
                ( "operator",
                  DropdownChoice(
                      title = _('Operator'),
                      choices = [ ('sum', _('Sum')), ('min', _('Minimum')), ('max', _('Maximum')), ('ave', _('Average')) ],
                      help = _('The operator that is used for the calculation.')
                  )
                ),
            ],
            optional_keys = [ 'hosttags', 'host' ],
        ),
        forth = _transform_perfcalc_ds,
        ),
        title = _('Service Specifications'),
        add_label = _('Add new service specification'),
    )
    
    # help  = _('This special agent uses performance data collected via livestatus and can calculate sums, minimums, maximums and averages of datasources. A service check is created for every service specification defined with this rule.'),
    # match = 'first')

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupDatasourceProgramsApps,
        name="special_agents:perfcalc",
        valuespec=_valuespec_special_agents_perfcalc,
        title = lambda: _("Calculate on the performance data of other checks."),
    ))
