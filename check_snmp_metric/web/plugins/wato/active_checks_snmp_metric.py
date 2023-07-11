#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2021 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>
#

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  This file is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    CascadingDropdown,
    Dictionary,
    Float,
    Integer,
    ListOf,
    ListOfStrings,
    RegExp,
    TextAscii,
    Tuple,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    HostRulespec,
    SNMPCredentials,
)

from cmk.gui.plugins.wato.active_checks.common import (
    RulespecGroupIntegrateOtherServices,
)

def _valuespec_active_checks_snmp_metric():
    return Dictionary(
        title = _("Check SNMP Metric"),
        help = _("Checks SNMP Metrics with the Nagios plugin <tt>check_snmp_metric</tt>."),
        elements = [
            ( "description",
              TextAscii(
                  title = _("Service Description"),
                  help = _("Must be unique for every host. Defaults to command that is executed."),
                  size = 30,
              )),
            ( "hostname",
              TextAscii(
                  title = _("DNS Hostname or IP address"),
                  default_value = "$HOSTADDRESS$",
                  allow_empty = False,
                  help = _("You can specify a hostname or IP address different from IP address "
                           "of the host as configured in your host properties."),
              )),
            ( 'port',
              Integer(
                  title = _("SNMP Port"),
                  help = _("Default is 161."),
                  minvalue = 1,
                  maxvalue = 65535,
                  default_value = 161,
              )),
            ( "timeout",
              Integer(
                  title = _("Seconds before connection times out"),
                  unit = _("sec"),
                  default_value = 10,
              )),
            ( "creds",
              SNMPCredentials(
                  help = _("If not set, the SNMP credentials of the host will be used"),
              )),
            ( "oid",
              TextAscii(
                  title = _("OID to query"),
              )),
            ( "levels_upper",
              Tuple(
                  title = _("Upper levels"),
                  elements = [
                      Integer(title=_("Warning above")),
                      Integer(title=_("Critical above")),
                  ],
              )),
            ( "levels_lower",
              Tuple(
                  title = _("Lower levels"),
                  elements = [
                      Integer(title=_("Warning below")),
                      Integer(title=_("Critical below")),
                  ],
              )),
            ( "factor",
              Float(
                  title = _("Value factor"),
                  help = _("A Factor of 10 means that the value reported is ten times the real value, e.g. the OID contains 245, but the real temperature is 24,5°C"),
                  default_value = 1.0,
              )),
            ( "metric",
              TextAscii(
                  title = _("Metric name"),
                  help = _("Name of the metric for performance data. If obmitted, no performance data will be generated."),
              )),
            ( "unit",
              TextAscii(
                  title = _("Unit"),
                  help = _("Unit of the value. Used for display."),
              )),
        ],
        optional_keys = [ 'hostname', 'port', 'timeout', 'creds', 'levels_upper', 'levels_lower', 'factor', 'metric', 'unit', ],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupIntegrateOtherServices,
        match_type="all",
        name="active_checks:snmp_metric",
        valuespec=_valuespec_active_checks_snmp_metric,
    ))

