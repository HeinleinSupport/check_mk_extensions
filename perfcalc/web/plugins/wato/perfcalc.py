#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

register_check_parameters(
    subgroup_applications,
    "perfcalc",
    _("Calculated Performance Data Levels"),
    ListOf(
        Dictionary(
            elements = [
                ('dsname',
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
        help = _('Specify service descriptions of the host that uses the special agent "perfcalc".'),
        allow_empty = False
    ),
    match_type = "first",
)

def transform_perfcalc_ds(source):
    if 'hosttags' not in source:
        source['hosttags'] = []
    return source

register_rule('datasource_programs',
    "special_agents:perfcalc",
    ListOf(
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
        forth = transform_perfcalc_ds,
        ),
        title = _('Service Specifications'),
        add_label = _('Add new service specification'),
    ),
    title = _("Calculate on the performance data of other checks."),
    help  = _('This special agent uses performance data collected via livestatus and can calculate sums, minimums, maximums and averages of datasources. A service check is created for every service specification defined with this rule.'),
    match = 'first')
