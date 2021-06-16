#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2021 Heinlein Consulting GmbH
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

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Age,
    Dictionary,
    Float,
    Tuple,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersNetworking,
)

def _item_spec_lancom_xdsl():
    return TextAscii(
        title = _("Interface ID"),
        allow_empty = False,
    )

def _vs_lancom_xdsl(metric_name, unit_name):
    def _vs_abs_perc(metric_name, unit_name):
        return CascadingDropdown(orientation="horizontal",
                                 choices=[("perc",
                                           _("Percentual levels (in relation to %s)" % metric_name),
                                           Tuple(orientation="float",
                                                 show_titles=False,
                                                 elements=[
                                                     Percentage(label=_("Warning at")),
                                                     Percentage(label=_("Critical at")),
                                                 ])),
                                          ("abs", _("Absolute levels in %s" % unit_name),
                                           Tuple(orientation="float",
                                                 show_titles=False,
                                                 elements=[
                                                     Float(label=_("Warning at")),
                                                     Float(label=_("Critical at")),
                                                 ])),
                                 ])
    return CascadingDropdown(orientation="horizontal",
                             choices=[
                                 ("both", _("Both"), _vs_abs_perc(metric_name, unit_name)),
                                 ("upper", _("Upper"), _vs_abs_perc(metric_name, unit_name)),
                                 ("lower", _("Lower"), _vs_abs_perc(metric_name, unit_name)),
                             ])

def _parameter_valuespec_lancom_xdsl():
    return Dictionary(elements=[
        ("data_rate",
         ListOf(
             CascadingDropdown(title=_("Direction"),
                               orientation="horizontal",
                               choices=[
                                   ('both', _("In / Out"), _vs_lancom_xdsl('data rate', 'bits per second')),
                                   ('in', _("In"), _vs_lancom_xdsl('data rate', 'bits per second')),
                                   ('out', _("Out"), _vs_lancom_xdsl('data rate', 'bits per second')),
                               ]),
             title=_("Data Rate"),
             help=_("Define levels in relation to the intially discovered data rate. These will act as lower or upper thresholds. The last entry will define the specific levels."),
         )),
        ("signal_noise",
         ListOf(
             CascadingDropdown(title=_("Direction"),
                               orientation="horizontal",
                               choices=[
                                   ('both', _("In / Out"), _vs_lancom_xdsl('signal/noise ratio', 'deciBel')),
                                   ('in', _("In"), _vs_lancom_xdsl('signal/noise ratio', 'deciBel')),
                                   ('out', _("Out"), _vs_lancom_xdsl('signal/noise ratio', 'deciBel')),
                               ]),
             title=_("Signal/Noise Ratio"),
             help=_("Define levels in relation to the intially discovered signal/noise ratio. These will act as lower or upper thresholds. The last entry will define the specific levels."),
         )),
        ("attenuation",
         ListOf(
             CascadingDropdown(title=_("Direction"),
                               orientation="horizontal",
                               choices=[
                                   ('both', _("In / Out"), _vs_lancom_xdsl('attenuation', 'deciBel')),
                                   ('in', _("In"), _vs_lancom_xdsl('attenuation', 'deciBel')),
                                   ('out', _("Out"), _vs_lancom_xdsl('attenuation', 'deciBel')),
                               ]),
             title=_("Attenuation"),
             help=_("Define levels in relation to the intially discovered attenuation. These will act as lower or upper thresholds. The last entry will define the specific levels."),
         )),
        ("uptime_min",
         Tuple(
             title=_("Minimum required uptime"),
             elements=[
                 Age(title=_("Warning if below")),
                 Age(title=_("Critical if below")),
             ],
         )),
        ("uptime_max",
         Tuple(
             title=_("Maximum allowed uptime"),
             elements=[
                 Age(title=_("Warning at")),
                 Age(title=_("Critical at")),
             ],
         )),
    ],
    ignored_keys = [ 'discovered' ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="lancom_xdsl",
        group=RulespecGroupCheckParametersNetworking,
        item_spec=_item_spec_lancom_xdsl,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_lancom_xdsl,
        title=lambda: _("LANCOM xDSL interfaces"),
    ))
