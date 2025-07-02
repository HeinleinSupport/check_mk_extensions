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
    BooleanChoice,
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    InputHint,
    LevelDirection,
    List,
    migrate_to_integer_simple_levels,
    SingleChoice,
    SingleChoiceElement,
    SimpleLevels,
    String,
)
from cmk.rulesets.v1.rule_specs import (
    AgentConfig,
    CheckParameters,
    DiscoveryParameters,
    HostAndItemCondition,
    HostCondition,
    Topic,
)


#   .--Parameter-----------------------------------------------------------.
#   |          ____                                _                       |
#   |         |  _ \ __ _ _ __ __ _ _ __ ___   ___| |_ ___ _ __            |
#   |         | |_) / _` | '__/ _` | '_ ` _ \ / _ \ __/ _ \ '__|           |
#   |         |  __/ (_| | | | (_| | | | | | |  __/ ||  __/ |              |
#   |         |_|   \__,_|_|  \__,_|_| |_| |_|\___|\__\___|_|              |
#   |                                                                      |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def _migrate_parameter(param):
    if isinstance(param, tuple):
        return {
            "name": param[0],
            "value": param[1],
        }
    return param

def _parameter_valuespec_postconf():
    return Dictionary(
        elements = {
            'config': DictElement(
                required=True,
                parameter_form=List(
                    add_element_label=Label("Add Variable"),
                    help_text=Help("The check <tt>postconf</tt> monitors the Postfix configuration. Every configuration variable can be checked against a specific value."),
                    element_template=Dictionary(
                        migrate=_migrate_parameter,
                        elements={
                            "name": DictElement(
                                required=True,
                                parameter_form=String(
                                    title=Title("Name of Configuration Variable")
                                )),
                            "value": DictElement(
                                required=True,
                                parameter_form=String(
                                    title=Title("Expected Value"),
                                )),
                        }
                    )
                )),
        },
    )

rule_spec_postconf = CheckParameters(
    name="postconf",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_postconf,
    title=Title("Postfix Configuration Settings"),
    condition=HostCondition(),
)
