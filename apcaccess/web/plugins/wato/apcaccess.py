#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
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
    DropdownChoice,
    Tuple,
    Integer,
    TextAscii,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    HostRulespec,
    RulespecGroupCheckParametersDiscovery,
    RulespecGroupCheckParametersEnvironment,
)

def _parameter_valuespec_apcaccess():
    return Dictionary(
        title = _('UPS Status Values'),
        elements = [
            ( 'voltage',
            Tuple(
                title = _('Output Voltage'),
                elements = [
                    Integer(title = _("Warning below"), unit = u"V", default_value=210),
                    Integer(title = _("Critical below"), unit = u"V", default_value=190),
                    Integer(title = _("Warning at or above"), unit = u"V", default_value=240),
                    Integer(title = _("Critical at or above"), unit = u"V", default_value=260),
                ],
            )),
            ( 'output_load',
            Tuple(
                title = _('Output Load Percentage'),
                elements = [
                    Integer(title = _("Warning at or above"), unit = u"%", default_value=80),
                    Integer(title = _("Critical at or above"), unit = u"%", default_value=90),
                ],
            )),
            ( 'battery_capacity',
            Tuple(
                title = _('Battery Loaded Capacity'),
                elements = [
                    Integer(title = _("Warning below"), unit = u"%", default_value=90),
                    Integer(title = _("Critical below"), unit = u"%", default_value=80),
                ],
            )),
            ( 'timeleft',
            Tuple(
                title = _('Time Left'),
                elements = [
                    Integer(title = _("Warning below"), unit = u"minutes", default_value=10),
                    Integer(title = _("Critical below"), unit = u"minutes", default_value=5),
                ],
            )),
        ],
        ignored_keys = ["upsname", "model"],
    )

def _item_spec_apcaccess():
    return TextAscii(
        title = _("UPS instance"),
        allow_empty = False,
    )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="apcaccess",
        group=RulespecGroupCheckParametersEnvironment,
        item_spec=_item_spec_apcaccess,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_apcaccess,
        title=lambda: _("APC Power Supplies (directly connected)"),
    ))

def _valuespec_apcaccess_inventory():
    return Dictionary(
        title=_("APC Access discovery"),
        help=_("This selects which attribute is used for the service description."),
        elements=[
            ('servicedesc',
             DropdownChoice(
                 title=_('Service Name'),
                 choices=[
                     (None, _('apcupsd configuration file name')),
                     ('upsname', _('value of UPSNAME field')),
                     ('model', _('value of MODEL field')),
                 ],
            )),
        ],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupCheckParametersDiscovery,
        name="apcaccess_inventory",
        valuespec=_valuespec_apcaccess_inventory,
    ))
