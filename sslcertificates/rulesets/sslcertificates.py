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
    migrate_to_lower_float_levels,
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

def _migrate_from_tuple(value):
    if isinstance(value, tuple):
        return {
            "after": value[0],
            "reason": value[1],
        }
    return value

def _default_values(param):
    if "warnalgo" not in param:
        param["warnalgo"] = ['md5WithRSAEncryption', 'sha1WithRSAEncryption']
    return param

def _parameter_valuespec_sslcertificates() -> Dictionary:
    return Dictionary(
        migrate = _default_values,
        elements = {
            'age': DictElement(
                parameter_form=SimpleLevels(
                    title = Title('Certificate Age'),
                    help_text = Help("Days until expiry of certificate"),
                    migrate = lambda model: migrate_to_lower_float_levels(model, scale=86400.0),
                    level_direction = LevelDirection.LOWER,
                    form_spec_template = TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR],
                    ),
                    prefill_fixed_levels = InputHint(
                        value=(90 * 86400.0, 60 * 86400.0),
                    )
                )),
            'warnalgo': DictElement(
                parameter_form=List(
                    title = Title('Signature Algorithms that generate WARNs'),
                    help_text = Help('The default value is <tt>md5WithRSAEncryption</tt> and <tt>sha1WithRSAEncryption</tt>.'),
                    element_template=String(),
                    editable_order=False,
                )),
            'ignore': DictElement(
                parameter_form=Dictionary(
                    title = Title('Ignore old Certificates'),
                    help_text = Help('Set number of days after which an expired certificate is ignored. A reason has to be given.'),
                    migrate = _migrate_from_tuple,
                    
                    elements = {
                        'after': DictElement(
                            required=True,
                            parameter_form=Integer(
                                title = Title('Ignore after'),
                                unit_symbol = ('days'),
                                prefill = DefaultValue(365),
                            )),
                        'reason': DictElement(
                            required=True,
                            parameter_form=String(
                                title = Title("Reason"),
                                custom_validate = [validators.LengthInRange(min_value=10)],
                                field_size = 72,
                            )),
                    }
                )),
        },
        ignored_elements=["use_subject"],
    )

rule_spec_sslcertificates = CheckParameters(
    name="sslcertificates",
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_valuespec_sslcertificates,
    title=Title("Parameters for SSL certificates"),
    condition=HostAndItemCondition(
        item_title=Title("Certificate File"),
        item_form=String(
            help_text=Help("The name of the certificate file"),
        )
    ),
)

def _valuespec_sslcertificates_inventory() -> Dictionary:
    return Dictionary(
        elements={
            'min_lifetime': DictElement(
                parameter_form=TimeSpan(
                    title=Title("Minimal lifetime of certificate"),
                    displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR],
                    prefill=InputHint(864000.0),
                    migrate=float,
                    help_text=Help("Certificates with a lifetime less than this value will not be discovered."),
            )),
            'use_subject': DictElement(
                parameter_form=BooleanChoice(
                    title=Title("Service Name from certificate subject"),
                    help_text=Help("Use certificate subject for the service name instead of thumbprint or filename."),
                    label=Label("Use certificate subject."),
            )),
        },
    )

rule_spec_sslcertificates_inventory = DiscoveryParameters(
    name="sslcertificates_inventory",
    topic=Topic.GENERAL,
    title=Title("SSL certificates discovery"),
    help_text=Help("This selects which certificates are discovered."),
    parameter_form=_valuespec_sslcertificates_inventory,
)

def _migrate_from_alternative_to_dict(param):
    if isinstance(param, dict) and param == {}:
        param = {"deploy": True}
    if isinstance(param, bool):
        param = {"deploy": param}
    if not param:
        param = {"deploy": False}
    if "deploy" not in param:
        param["deploy"] = True
    return param

def _valuespec_agent_config_sslcertificates():
    return Dictionary(
        migrate=_migrate_from_alternative_to_dict,
        elements = {
            "deploy": DictElement(
                required=True,
                parameter_form=BooleanChoice(
                    label=Label("Deploy the SSL certificates plugin"),
                    prefill=DefaultValue(True),
                ),
            ),
            "interval": DictElement(
                parameter_form = TimeSpan(
                    title = Title("Run asynchronously"),
                    label = Label("Interval for collecting data"),
                    migrate = float,
                    prefill = DefaultValue(3600.0),
                    displayed_magnitudes = [TimeMagnitude.HOUR, TimeMagnitude.MINUTE],
            )),
            "directories": DictElement(
                parameter_form = List(
                    title = Title("Directories or filename patterns to look into for SSL certificate files"),
                    help_text = Help("Enter path patterns that will be searched for certificate files. Only works on Linux. On Windows the agent plugin looks into the cert store."),
                    element_template = String(
                        field_size=80,
                        custom_validate=[
                            validators.MatchRegex(
                                regex = r"^/\S+$",
                                error_msg = "Directory paths must begin with <tt>/</tt> and must not contain spaces.",
                            ),
                        ],
                    ),
                    editable_order=False,
            )),
        },
    )

rule_spec_sslcertificates_bakery = AgentConfig(
    name="sslcertificates",
    title=Title("SSL Certificates"),
    help_text=Help("This will deploy the agent plugin <tt>sslcertificates</tt> for checking SSL certificate files. <b>Note:</b> If you want to configure several directories to look into for SSL certificate files, then simply create several rules."),
    topic=Topic.APPLICATIONS,
    parameter_form=_valuespec_agent_config_sslcertificates,
)
