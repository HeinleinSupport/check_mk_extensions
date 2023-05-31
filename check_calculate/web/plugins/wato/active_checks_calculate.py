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
    Dictionary,
    TextAscii,
    TextAreaUnicode,
    Tuple,
)

from cmk.gui.plugins.wato import (
    rulespec_registry,
    HostRulespec,
)

from cmk.gui.plugins.wato.active_checks.common import (
    RulespecGroupIntegrateOtherServices,
)

def _vs_levels(title):
    return Tuple(
        title=title,
        elements = [
            Float(title='Warning at'),
            Float(title='Critical at'),
        ])

def _valuespec_active_checks_calculate():
    return Dictionary(
        title = _("Calculate on Perfdata"),
        elements = [
            ('description',
             TextAscii(title=_('Service description'))),
            ('label',
             TextAscii(title=_('Label for check output'))),
            ('metric',
             TextAscii(title=_('Metric name for calculated value'))),
            ('levels_upper',
             _vs_levels(title=_('Upper levels'))),
            ('levels_lower',
             _vs_levels(title=_('Lower levels'))),
            ('expression',
             TextAreaUnicode(
                 title=_('Expression'),
                 help=_('The expression used here is compatible with the expression from custom graphs.'),
             )),
        ],
        optional_keys = [ 'levels_upper', 'levels_lower' ],
    )

rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupIntegrateOtherServices,
        match_type="all",
        name="active_checks:calculate",
        valuespec=_valuespec_active_checks_calculate,
    ))

