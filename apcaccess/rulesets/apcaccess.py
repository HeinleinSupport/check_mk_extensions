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

from cmk.gui.plugins.wato import (
    rulespec_registry,
    CheckParameterRulespecWithItem,
    HostRulespec,
    RulespecGroupCheckParametersDiscovery,
    RulespecGroupCheckParametersEnvironment,
)

from cmk.rulesets.v1 import (
    Help,
    Label,
    Title,
)
from cmk.rulesets.v1.form_specs import (
    BooleanChoice,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    DefaultValue,
    DictElement,
    Dictionary,
    FixedValue,
    Integer,
    InputHint,
    LevelDirection,
    List,
    migrate_to_integer_simple_levels,
    migrate_to_lower_float_levels,
    SingleChoice,
    SingleChoiceElement,
    SimpleLevels,
    String,
    TimeMagnitude,
    TimeSpan,
    validators,
)
from cmk.rulesets.v1.rule_specs import (
    AgentConfig,
    CheckParameters,
    DiscoveryParameters,
    HostAndItemCondition,
    Topic,
)
from pprint import pprint # type: ignore

# def _parameter_valuespec_apcaccess():
#     return Dictionary(
#         title = _('UPS Status Values'),
#         elements = [
#             ( 'voltage',
#             Tuple(
#                 title = _('Output Voltage'),
#                 elements = [
#                     Integer(title = _("Warning below"), unit = u"V", default_value=210),
#                     Integer(title = _("Critical below"), unit = u"V", default_value=190),
#                     Integer(title = _("Warning at or above"), unit = u"V", default_value=240),
#                     Integer(title = _("Critical at or above"), unit = u"V", default_value=260),
#                 ],
#             )),
#             ( 'output_load',
#             Tuple(
#                 title = _('Output Load Percentage'),
#                 elements = [
#                     Integer(title = _("Warning at or above"), unit = u"%", default_value=80),
#                     Integer(title = _("Critical at or above"), unit = u"%", default_value=90),
#                 ],
#             )),
#             ( 'battery_capacity',
#             Tuple(
#                 title = _('Battery Loaded Capacity'),
#                 elements = [
#                     Integer(title = _("Warning below"), unit = u"%", default_value=90),
#                     Integer(title = _("Critical below"), unit = u"%", default_value=80),
#                 ],
#             )),
#             ( 'timeleft',
#             Tuple(
#                 title = _('Time Left'),
#                 elements = [
#                     Integer(title = _("Warning below"), unit = u"minutes", default_value=10),
#                     Integer(title = _("Critical below"), unit = u"minutes", default_value=5),
#                 ],
#             )),
#         ],
#         ignored_keys = ["upsname", "model"],
#     )

# def _item_spec_apcaccess():
#     return TextAscii(
#         title = _("UPS instance"),
#         allow_empty = False,
#     )

# rulespec_registry.register(
#     CheckParameterRulespecWithItem(
#         check_group_name="apcaccess",
#         group=RulespecGroupCheckParametersEnvironment,
#         item_spec=_item_spec_apcaccess,
#         match_type="dict",
#         parameter_valuespec=_parameter_valuespec_apcaccess,
#         title=lambda: _("APC Power Supplies (directly connected)"),
#     ))

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

def _migrate_from_bool_to_dict(param):
    print(f"Before: {param}")
    if isinstance(param, bool):
        param = {"deploy": param}
    if not param:
        param = {"deploy": False}
    print(f"After: {param}")
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

rule_spec_sslcertificates_bakery = AgentConfig(
    name="apcaccess",
    title=Title("APC UPS via apcaccess (Linux, Windows)"),
    help_text=Help("This will deploy the agent plugin <tt>apcaccess</tt> to check various APC UPS stats."),
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_agent_config_apcaccess,
)