#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2013 Heinlein Support GmbH
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
    Label,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    Integer,
    InputHint,
    LevelDirection,
    List,
    migrate_to_integer_simple_levels,
    SimpleLevels,
    String,
)
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostCondition,
    Topic,
)

def _migrate_tuple_list(p):
    print(f"vorher: {p}")
    r = []
    for i in p:
        if isinstance(i, tuple):
            i = {
                "name": i[0],
                "version": i[1],
            }
        r.append(i)
    print(f"nachher: {r}")
    return r

def _parameter_valuespec_lsbrelease():
    return Dictionary(
        elements={
            "distributions": DictElement(
                required=True,
                parameter_form=List(
                    title=Title("List of Distributions"),
                    help_text=Help("The check <tt>lsbrelease</tt> monitors the distribution version. The start of the lsb_release <tt>Description</tt> field has to match against the 'Name of Distribution', then the versions will be compared."),
                    add_element_label=Label("Add Distribution"),
                    migrate=_migrate_tuple_list,
                    element_template=Dictionary(
                        elements={
                            "name": DictElement(
                                required=True,
                                parameter_form=String(
                                    title=Title("Name of Distribution"),
                                )
                            ),
                            "version": DictElement(
                                required=True,
                                parameter_form=String(
                                    title=Title("Expected Version"),
                                )
                            ),
                        },
                    ),
                ),
            ),
        },
    )

rule_spec_lsbrelease = CheckParameters(
    name="lsbrelease",
    topic=Topic.OPERATING_SYSTEM,
    parameter_form=_parameter_valuespec_lsbrelease,
    title=Title("Distribution Version Check"),
    condition=HostCondition(),
)
