#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) Robert Sander <r.sander@heinlein-support.de>

# This is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2. This file is  distributed
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
    migrate_to_integer_simple_levels,
    SingleChoice,
    SingleChoiceElement,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import (
    AgentConfig,
    CheckParameters,
    DiscoveryParameters,
    HostAndItemCondition,
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
    print(f"Before (apcaccess): {param}")
    if "battery_capacity" in param:
        param["capacity"] = param["battery_capacity"]
        del(param["battery_capacity"])
    if "timeleft" in param:
        param["battime"] = param["timeleft"]
        del(param["timeleft"])
    for key in ["output_load", "voltage"]:
        if key in param:
            del(param[key])
    print(f"After (apcaccess): {param}")
    return param

def _parameter_valuespec_apcaccess():
    return Dictionary(
        migrate = _migrate_parameter,
        title = Title("Levels for battery parameters"),
        elements = {
            'capacity': DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    title=Title("Battery capacity"),
                    migrate=migrate_to_integer_simple_levels,
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Integer(unit_symbol="%"),
                    prefill_fixed_levels=InputHint(value=(90, 80)),
                )),
            'battime': DictElement(
                required=True,
                parameter_form=SimpleLevels(
                    title=Title("Time left on battery"),
                    migrate=migrate_to_integer_simple_levels,
                    level_direction=LevelDirection.LOWER,
                    form_spec_template=Integer(unit_symbol="minutes"),
                    prefill_fixed_levels=InputHint(value=(10, 5)),
                )),
        },
        ignored_elements = ["upsname", "model"],
    )

rule_spec_exchange_package = CheckParameters(
    name="apcaccess",
    topic=Topic.ENVIRONMENTAL,
    parameter_form=_parameter_valuespec_apcaccess,
    title=Title("APC Power Supplies (directly connected)"),
    condition=HostAndItemCondition(item_title=Title("UPS instance")),
)


#   .--Discovery-----------------------------------------------------------.
#   |              ____  _                                                 |
#   |             |  _ \(_)___  ___ _____   _____ _ __ _   _               |
#   |             | | | | / __|/ __/ _ \ \ / / _ \ '__| | | |              |
#   |             | |_| | \__ \ (_| (_) \ V /  __/ |  | |_| |              |
#   |             |____/|_|___/\___\___/ \_/ \___|_|   \__, |              |
#   |                                                  |___/               |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def _valuespec_apcaccess_inventory():
    return Dictionary(
        elements={
            'servicedesc': DictElement(
                required=True,
                parameter_form=SingleChoice(
                    title=Title('Service Name'),
                    prefill=DefaultValue("file"),
                    elements=[
                        SingleChoiceElement(name="file", title=Title('apcupsd configuration file name')),
                        SingleChoiceElement(name='upsname', title=Title('value of UPSNAME field')),
                        SingleChoiceElement(name='model', title=Title('value of MODEL field')),
                    ],
                )),
        },
    )

rule_spec_apcaccess_inventory = DiscoveryParameters(
    name="apcaccess_inventory",
    topic=Topic.GENERAL,
    title=Title("APC Access discovery"),
    help_text=Help("This selects which attribute is used for the service description."),
    parameter_form=_valuespec_apcaccess_inventory,
)


#   .--Bakery--------------------------------------------------------------.
#   |                   ____        _                                      |
#   |                  | __ )  __ _| | _____ _ __ _   _                    |
#   |                  |  _ \ / _` | |/ / _ \ '__| | | |                   |
#   |                  | |_) | (_| |   <  __/ |  | |_| |                   |
#   |                  |____/ \__,_|_|\_\___|_|   \__, |                   |
#   |                                             |___/                    |
#   +----------------------------------------------------------------------+
#   |                                                                      |
#   '----------------------------------------------------------------------'
#.

def _migrate_from_bool_to_dict(param):
    if isinstance(param, bool):
        param = {"deploy": param}
    if not param:
        param = {"deploy": False}
    return param

def _valuespec_agent_config_apcaccess():
    return Dictionary(
        elements={
            "deploy": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Deploy plugin for APC UPS"),
                    prefill=DefaultValue(True),
                ),
            )
        },
        migrate=_migrate_from_bool_to_dict,
    )

rule_spec_apcaccess_bakery = AgentConfig(
    name="apcaccess",
    title=Title("APC UPS via apcaccess (Linux, Windows)"),
    help_text=Help("This will deploy the agent plugin <tt>apcaccess</tt> to check various APC UPS stats."),
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_agent_config_apcaccess,
)