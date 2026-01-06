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
    DataSize,
    DefaultValue,
    DictElement,
    Dictionary,
    IECMagnitude,
    Integer,
    InputHint,
    LevelDirection,
    migrate_to_password,
    migrate_to_upper_float_levels,
    Password,
    Percentage,
    SimpleLevels,
    String,
    TimeMagnitude,
    TimeSpan,
)
from cmk.rulesets.v1.rule_specs import (
    AgentConfig,
    CheckParameters,
    HostCondition,
    Topic,
)

# 'CacheHitRatio': { 'lower': ("fixed", (60, 40)) },
# 'CacheKeyCount': { 'upper': ("fixed", (90000, 100000)) },
# 'CacheSize': { 'lower': ("fixed", (10737418240, 0)), 'upper': ("fixed", (32212254720, 42949672960)) },
# 'MedianKeyProcessTimeMillis': { 'upper': ("fixed", (10, 1000000)) },

def _parameter_valuespec_ox_imageconverter_cache():
    return Dictionary(
        title = Title('OX ImageConverter Cache'),
        elements = {
            'CacheHitRatio': DictElement(
                parameter_form=Dictionary(
                    title = Title('Cache Hit Ratio'),
                    elements = {
                        'lower': DictElement(
                            required=True,
                            parameter_form=SimpleLevels(
                                form_spec_template=Percentage(),
                                title=Title("Lower Levels"),
                                level_direction=LevelDirection.LOWER,
                                prefill_fixed_levels=InputHint(value=(60.0, 40.0)),
                        )),
                    },
            )),
            'CacheKeyCount': DictElement(
                parameter_form=Dictionary(
                    title = Title('Cache Key Count'),
                    elements = {
                        'upper': DictElement(
                            required=True,
                            parameter_form=SimpleLevels(
                                form_spec_template=Integer(
                                    unit_symbol="keys",
                                ),
                                title=Title("Upper Levels"),
                                level_direction=LevelDirection.UPPER,
                                prefill_fixed_levels=InputHint(value=(90000, 100000)),
                            )),
                    },
            )),
            'CacheSize': DictElement(
                parameter_form=Dictionary(
                    title = Title('Cache Size'),
                    elements = {
                        'lower': DictElement(
                            required=True,
                            parameter_form=SimpleLevels(
                                form_spec_template=DataSize(
                                    displayed_magnitudes=[
                                        IECMagnitude.BYTE,
                                        IECMagnitude.KIBI,
                                        IECMagnitude.MEBI,
                                        IECMagnitude.GIBI,
                                    ],
                                ),
                                title=Title("Lower Levels"),
                                level_direction=LevelDirection.LOWER,
                                prefill_fixed_levels=InputHint(value=(10737418240, 0)),
                            )),
                        'upper': DictElement(
                            required=True,
                            parameter_form=SimpleLevels(
                                form_spec_template=DataSize(
                                    displayed_magnitudes=[
                                        IECMagnitude.BYTE,
                                        IECMagnitude.KIBI,
                                        IECMagnitude.MEBI,
                                        IECMagnitude.GIBI,
                                    ],
                                ),
                                title=Title("Upper Levels"),
                                level_direction=LevelDirection.UPPER,
                                prefill_fixed_levels=InputHint(value=(32212254720, 42949672960)),
                            )),
                    },
            )),
            'MedianKeyProcessTimeMillis': DictElement(
                parameter_form=Dictionary(
                    title = Title('Median Key Processing Time'),
                    elements = {
                        'upper': DictElement(
                            required=True,
                            parameter_form=SimpleLevels(
                                migrate=migrate_to_upper_float_levels,
                                form_spec_template=TimeSpan(
                                    displayed_magnitudes=[
                                        TimeMagnitude.SECOND,
                                        TimeMagnitude.MINUTE,
                                        TimeMagnitude.HOUR,
                                        TimeMagnitude.DAY,
                                    ],
                                ),
                                title=Title("Upper Levels"),
                                level_direction=LevelDirection.UPPER,
                                prefill_fixed_levels=InputHint(value=(10.0, 1000000.0)),
                            )),
                    },
            )),
        },
    )

rule_spec_ox_imageconverter_cache = CheckParameters(
    name="ox_imageconverter_cache",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_ox_imageconverter_cache,
    title=Title("Open-Xchange ImageConverter Cache"),
    condition=HostCondition(),
)

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
