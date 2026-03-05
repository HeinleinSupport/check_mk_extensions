#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-

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

"""
Check_MK WATO rule spec for USP SES checks

Authors:    Roger Ellenberger <roger.ellenberger@wagner.ch>

"""

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.rule_specs import (
    CheckParameters,
    HostAndItemCondition,
    Topic,
)
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    Float,
    TimeSpan,
    TimeMagnitude,
    LevelDirection,
    SimpleLevels,
    InputHint,
    migrate_to_float_simple_levels,
)


def _form_spec_usp_ses_levels():
    return Dictionary(
        help_text=Help(
            'To obtain the data required for this check, please configure the'
            ' SNMP datasource "USP SES"". By default there is no alerting.'
        ),
        elements={
            'client_connections' : DictElement(
                                    parameter_form=SimpleLevels(
                                        title=Title("Client connections"),
                                        form_spec_template=Float(),
                                        level_direction=LevelDirection.UPPER,
                                        migrate=migrate_to_float_simple_levels,
                                        prefill_fixed_levels=InputHint((50.0, 100.0)),
                                    ),
                                    required=False,
            ),
            'requests_per_second' : DictElement(
                                    parameter_form=SimpleLevels(
                                        title=Title("Requests per second"),
                                        form_spec_template=Float(unit_symbol="1/s"),
                                        level_direction=LevelDirection.UPPER,
                                        migrate=migrate_to_float_simple_levels,
                                        prefill_fixed_levels=InputHint((20.0, 50.0))
                                    ),
                                    required=False,

            ),
            'active_users' : DictElement(
                                    parameter_form=SimpleLevels(
                                        title=Title("Active users"),
                                        form_spec_template=Float(),
                                        level_direction=LevelDirection.UPPER,
                                        migrate=migrate_to_float_simple_levels,
                                        prefill_fixed_levels=InputHint((20.0, 50.0))
                                    ),
                                    required=False,
            ),
            'avg_request_time' : DictElement(
                                    parameter_form=SimpleLevels(
                                        title=Title("Average request time"),
                                        form_spec_template=TimeSpan(
                                            displayed_magnitudes=[TimeMagnitude.SECOND,
                                                                  TimeMagnitude.MILLISECOND],
                                        ),
                                        level_direction=LevelDirection.UPPER,
                                        migrate=migrate_to_float_simple_levels,
                                        prefill_fixed_levels=InputHint((0.02, 0.05))
                                    ),
                                    required=False,
            ),
        }
)


rule_spec_usp_ses_levels = CheckParameters(
    title=Title("USP SES thresholds"),
    topic=Topic.NETWORKING,
    name="usp_ses_levels",
    condition=HostAndItemCondition(item_title=Title("vhost name")),
    parameter_form=_form_spec_usp_ses_levels,
)
