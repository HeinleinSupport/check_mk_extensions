#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2020 Heinlein Support GmbH
#          Robert Sander <r.sander@heinlein-support.de>

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

from cmk.rulesets.v1 import (
    Help,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    Integer,
    InputHint,
    LevelDirection,
    migrate_to_integer_simple_levels,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostCondition,
    Topic,
)

def _dovereplstat_parameters(title: str) -> DictElement:
    return DictElement(
        parameter_form=SimpleLevels(
            migrate=migrate_to_integer_simple_levels,
            title=Title(title),
            form_spec_template=Integer(),
            level_direction=LevelDirection.UPPER,
            prefill_fixed_levels=InputHint((0, 0)),
        )
    )

def _parameter_valuespec_dovereplstat():
    return Dictionary(
        elements={
            'sync_requests': _dovereplstat_parameters('Levels for queued sync requests'),
            'high_requests': _dovereplstat_parameters('Levels for queued high requests'),
            'low_requests': _dovereplstat_parameters('Levels for queued low requests'),
            'failed_requests': _dovereplstat_parameters('Levels for waiting failed requests'),
            'full_resync_requests': _dovereplstat_parameters('Levels for queued full resync requests'),
        },
    )

rule_spec_dovereplstat = CheckParameters(
    name="dovereplstat",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_dovereplstat,
    title=Title("Dovecot Replication Status"),
    help_text=Help("This check uses the output of `doveadm replicator status`."),
    condition=HostCondition(),
)
