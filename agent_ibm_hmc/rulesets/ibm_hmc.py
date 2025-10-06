#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2024 Heinlein Consulting GmbH
#          Robert Sander <r.sander@heinlein-support.de>

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

from cmk.rulesets.v1 import (
    Help,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    String,
)
from cmk.rulesets.v1.rule_specs import (
    SpecialAgent,
    Topic,
)

def _valuespec_special_agents_ibm_hmc() -> Dictionary:
    return Dictionary(
        title = Title(u'IBM HMC'),
        help_text = Help('This rule selects the IBM HMC agent. You can configure your connection settings here.'),
        elements = {
            "username": DictElement(
                required=True,
                parameter_form=String(
                    title=Title("User name")
                )),
            "ssh_id": DictElement(
                parameter_form=String(
                    title = Title('SSH key file'),
                    help_text = Help('Enter the location of the SSH key file, usually ~/.ssh/id_rsa or similar'),
              )),
        },
    )

rule_spec_special_agent_ibm_hmc = SpecialAgent(
    name="ibm_hmc",
    title=Title("IBM HMC"),
    topic=Topic.SERVER_HARDWARE,
    parameter_form=_valuespec_special_agents_ibm_hmc,
)
