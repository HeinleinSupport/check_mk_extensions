#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2018 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# tails. You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

register_rule('datasource_programs',
    "special_agents:dynamicscrm",
    Dictionary(
            title = _("Credentials for the pingdom API."),
            elements = [
                ( "username",
                  TextAscii(
                      title = _("Username"),
                      allow_empty = False,
                  )
                ),
                ( "password",
                  Password(
                      title = _("Password"),
                      allow_empty = False,
                  )
                ),
                ( "tenant",
                  TextAscii(
                      title = _("Tenant"),
                      allow_empty = False,
                  )
                ),
                ( "orgurl",
                  TextAscii(
                      title = _("API endpoint URL"),
                      allow_empty = False,
                  )
                ),
                ( "authurl",
                  TextAscii(
                      title = _("Authentication endpoint URL"),
                      default_value = 'https://login.microsoftonline.com',
                  )
                ),
            ],
            optional_keys = ['authurl']
    ),
    title = _("Check Microsoft Dynamics CRM via Rest-API"),
    help  = _('This rule set selects the <tt>dynamicscrm</tt> special agent instead of the normal Check_MK Agent '
              'and allows monitoring your Microsoft Dynamics CRM tenant.'
              'The agent itself is located in the site directory under <tt>~/local/share/check_mk/agents/special</tt>.'),
    match = 'first')

register_check_parameters(
    subgroup_applications,
    'dynamics_crm_waiting_jobs',
    _('MS Dynamics CRM Waiting Jobs'),
    Levels(
        title = _('Number of waiting Jobs'),
        default_value = (100, 500),
        ),
    None,
    'first',
)

register_check_parameters(
    subgroup_applications,
    'dynamics_crm_api_success_rate',
    _('MS Dynamics CRM API Success Rate'),
    Tuple(
        title = _('Percentage Levels'),
        elements = [
            Float(title=_('Warning below'), default_value=99.0, unit='%'),
            Float(title=_('Critical below'), default_value=98.0, unit='%'),
            ],
        ),
    None,
    'first',
)

register_check_parameters(
    subgroup_applications,
    'dynamics_crm_plugin_success_rate',
    _('MS Dynamics CRM Plugin Success Rate'),
    Tuple(
        title = _('Percentage Levels'),
        elements = [
            Float(title=_('Warning below'), default_value=99.0, unit='%'),
            Float(title=_('Critical below'), default_value=98.0, unit='%'),
            ],
        ),
    None,
    'first',
)

register_check_parameters(
    subgroup_applications,
    'dynamics_crm_orb_transferlog',
    _('MS Dynamics CRM ORB transferlog'),
    Dictionary(
        title = _('Levels for HTTP Response Codes'),
        elements = [
            ('ok', Levels(title = _('OK'), default_value = None)),
            ('closed', Levels(title = _('Connection closed'), default_value = None)),
            ('null', Levels(title = _('Null'), default_value = None)),
            ('unknown', Levels(title = _('Unknown Response Code'), default_value = None)),
        ],
        ),
    None,
    'dict',
)
