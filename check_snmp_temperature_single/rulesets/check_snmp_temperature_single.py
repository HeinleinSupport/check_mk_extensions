#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

#
# (c) 2013 Heinlein Support GmbH
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
    Dictionary,
    Integer,
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

def _valuespec_active_checks_snmp_temperature_single():
    return Dictionary(
        title = _("Check single Temperature via SNMP"),
        help = _("Checks a single Temperature on one SNMP OID."),
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
              )),
            ( "oid",
              TextAscii(
                  title = _("OID to query"),
              )),
            ( "levels_upper",
              Tuple(
                  title = _("Upper levels on Temperature"),
                  elements = [
                      Integer(title=_("Warning at"), unit='°C'),
                      Integer(title=_("Critical at"), unit='°C'),
                  ],
              )),
            ( "factor",
              Integer(
                  title = _("Factor"),
                  help = _("What factor is used by the SNMP agent to express the temperature. A factor of 10 means to agent shows 330 when the temperature is 33 °C."),
                  default_value = 10,
              )),
        ],
        optional_keys = [ 'hostname', 'port', 'timeout', 'creds', 'factor' ],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupIntegrateOtherServices,
        match_type="all",
        name="active_checks:snmp_temperature_single",
        valuespec=_valuespec_active_checks_snmp_temperature_single,
    ))

