#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# (c) 2023 Heinlein Consulting GmbH
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
    migrate_to_lower_float_levels,
    migrate_to_password,
    Password,
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
    HostCondition,
    Topic,
)

def _migrate_from_tuple(value):
    if isinstance(value, tuple):
        return {
            "after": value[0],
            "reason": value[1],
        }
    return value

# 'CacheHitRatio': { 'lower': (60, 40) },
# 'CacheKeyCount': { 'upper': (90000, 100000) },
# 'CacheSize': { 'lower': (10737418240, 0), 'upper': (32212254720, 42949672960) },
# 'MedianKeyProcessTimeMillis': { 'upper': (10, 100000) },

# def _parameter_valuespec_ox_imageconverter_cache():
#     return Dictionary(
#         title = _('TITLE'),
#         elements = [
#             ( 'CacheHitRatio',
#               Dictionary(
#                   title = _('Cache Hit Ratio'),
#                   elements = [
#                       ('lower',
#                        SimpleLevels(Float, title=_("Lower Levels"), default_levels = (60.0, 40.0), unit = "%")),
#                   ],
#                   optional_keys = [],
#             )),
#             ( 'CacheKeyCount',
#               Dictionary(
#                   title = _('Cache Key Count'),
#                   elements = [
#                       ('upper',
#                        SimpleLevels(Integer, title=_("Upper Levels"), default_levels = (90000, 100000), unit = "keys")),
#                   ],
#                   optional_keys = [],
#             )),
#             ( 'CacheSize',
#               Dictionary(
#                   title = _('Cache Size'),
#                   elements = [
#                       ('lower',
#                        SimpleLevels(Filesize, title=_("Lower Levels"), default_levels = (10737418240, 0) )),
#                       ('upper',
#                        SimpleLevels(Filesize, title=_("Upper Levels"), default_levels = (32212254720, 42949672960) )),
#                   ],
#                   optional_keys = [],
#             )),
#             ( 'MedianKeyProcessTimeMillis',
#               Dictionary(
#                   title = _('Median Key Processing Time'),
#                   elements = [
#                       ('upper',
#                        SimpleLevels(Integer, title=_("Upper Levels"), default_levels = (10, 1000000), unit = "s")),
#                   ],
#                   optional_keys = [],
#             )),
#         ],
#         ignored_keys = ["upsname", "model"],
#     )

# rulespec_registry.register(
#     CheckParameterRulespecWithoutItem(
#         check_group_name="ox_imageconverter_cache",
#         group=RulespecGroupCheckParametersApplications,
#         match_type="dict",
#         parameter_valuespec=_parameter_valuespec_ox_imageconverter_cache,
#         title=lambda: _("Open-Xchange ImageConverter Cache"),
#     ))

# rule_spec_ox_imageconverter_cache = CheckParameters(
#     name="ox_imageconverter_cache",
#     topic=Topic.APPLICATIONS,
#     parameter_form=_parameter_valuespec_ox_imageconverter_cache,
#     title=Title("Open-Xchange ImageConverter Cache"),
#     condition=HostCondition(),
# )

def _migrate_from_alternative_to_dict(param):
    print(f"vorher: {param}")
    if isinstance(param, dict) and param == {}:
        param = {"deploy": True}
    if isinstance(param, bool):
        param = {"deploy": param}
    if not param:
        param = {"deploy": False}
    if "deploy" not in param:
        param["deploy"] = True
    if "credentials" in param:
        param["username"] = param["credentials"][0]
        param["password"] = migrate_to_password(("password", param["credentials"][1]))
        del(param["credentials"])
    print(f"nachher: {param}")
    return param

def _valuespec_agent_config_ox_imageconverter():
    return Dictionary(
        migrate=_migrate_from_alternative_to_dict,
        elements = {
            "deploy": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Deploy the SSL certificates plugin"),
                    prefill=DefaultValue(True),
                )),
            "username": DictElement(
                required=True,
                parameter_form=String(
                    title = Title("User ID"),
                    prefill=InputHint('monitoring'),
                )),
            'password': DictElement(
                required=True,
                parameter_form=Password(
                    title = Title("Password"),
                )),
            "interval": DictElement(
                parameter_form = TimeSpan(
                    title = Title("Run asynchronously"),
                    label = Label("Interval for collecting data"),
                    migrate = float,
                    prefill = DefaultValue(300.0),
                    displayed_magnitudes = [TimeMagnitude.HOUR, TimeMagnitude.MINUTE],
            )),
        }
    )

rule_spec_sslcertificates_bakery = AgentConfig(
    name="ox_imageconverter",
    title=Title("Open-Xchange ImageConverter (Linux)"),
    help_text=Help("This will deploy the agent plugin <tt>ox_imageconverter</tt> to check various Open-Xchange ImageConverter stats."),
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_agent_config_ox_imageconverter,
)
