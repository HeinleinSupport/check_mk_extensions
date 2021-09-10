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
    CascadingDropdown,
    Dictionary,
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

from cmk.gui.plugins.wato.active_checks import (
    RulespecGroupIntegrateOtherServices,
)

def _valuespec_active_checks_snmp():
    return Dictionary(
        title = _("Check SNMP OID"),
        help = _("Checks SNMP OIDs with the Nagios plugin <tt>check_snmp</tt>."),
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
            ( "query",
              ListOf(
                  Dictionary(
                      elements = [
                          ( "oid",
                            TextAscii(
                                title = _("OID to query"),
                            )),
                          ( "levels_upper",
                            Tuple(
                                title = _("Upper levels"),
                                elements = [
                                    Integer(title=_("Warning at"), unit='°C'),
                                    Integer(title=_("Critical at"), unit='°C'),
                                ],
                            )),
                      ],
                      optional_keys = [ 'levels_upper' ],
                  ),
                  title = _("OIDs to query"),
              )),
            ( "match",
              CascadingDropdown(
                  title = _("Match SNMP value"),
                  choices = [
                      ( "string",
                        _("String"),
                        TextAscii(
                            label = _("string to match"),
                        ),
                      ),
                      ( "ereg",
                        _("Regex"),
                        RegExp(
                            label = _("regular expression"),
                            help = _("Return OK state (for that OID) if extended regular expression matches"),
                            mode = RegExp.infix,
                        ),
                      ),
                      ( "eregi",
                        _("Regexi"),
                        RegExp(
                            label = _("case insensitive regular expression"),
                            help = _("Return OK state (for that OID) if case-insensitive extended regular expression matches"),
                            mode = RegExp.infix,
                            case_sensitive = False,
                        ),
                      ),
                  ],
              )),
            ( "invert",
              FixedValue(
                  'Invert search result',
                  title = _("Invert Match"),
                  help = _("Invert search result (CRITICAL if found)"),
              )),
            ( "rate",
              Integer(
                  title = _("Rate Calculation"),
                  help = _("Enable rate calculation. Converts rate per second. For example, set mulitplier to 60 to convert to per minute."),
                  default_value = 1,
                  label = _("Rate Multiplier"),
                  unit = "s",
              )),
            ( "offset",
              Integer(
                  title = _("Offset"),
                  help = _("Add/substract the specified offset to numeric sensor data"),
                  default_value = 0,
              )),
        ],
        optional_keys = [ 'hostname', 'port', 'timeout', 'creds', "match", 'invert', 'rate', 'offset' ],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupIntegrateOtherServices,
        match_type="all",
        name="active_checks:snmp",
        valuespec=_valuespec_active_checks_snmp,
    ))

